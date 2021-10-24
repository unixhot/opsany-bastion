function _check_aborted(session) {
    if (session.aborted()) {
        throw new Zmodem.Error("aborted");
    }
}

export default function send_files(session, files, options) {
    if (!options) options = {};

    //Populate the batch in reverse order to simplify sending
    //the remaining files/bytes components.
    var batch = [];
    var total_size = 0;
    for (var f = files.length - 1; f >= 0; f--) {
        var fobj = files[f];
        total_size += fobj.size;
        batch[f] = {
            obj: fobj,
            name: fobj.name,
            size: fobj.size,
            mtime: new Date(fobj.lastModified),
            files_remaining: files.length - f,
            bytes_remaining: total_size,
        };
    }

    var file_idx = 0;

    function promise_callback() {
        var cur_b = batch[file_idx];

        if (!cur_b) {
            return Promise.resolve(); //batch done!
        }

        file_idx++;

        return session.send_offer(cur_b).then(function after_send_offer(xfer) {
            if (options.on_offer_response) {
                options.on_offer_response(cur_b.obj, xfer);
            }

            if (xfer === undefined) {
                return promise_callback(); //skipped
            }

            return new Promise(function(res) {
                var block = 1 * 1024 * 1024;
                var fileSize = cur_b.size;
                var fileLoaded = 0;
                var reader = new FileReader();
                reader.onerror = function reader_onerror(e) {
                    console.error('file read error', e);
                    throw ('File read error: ' + e);
                }

                function readBlob() {
                    var blob;
                    if (cur_b.obj.webkitSlice) {
                        blob = cur_b.obj.webkitSlice(fileLoaded, fileLoaded + block + 1);
                    } else if (cur_b.obj.mozSlice) {
                        blob = cur_b.obj.mozSlice(fileLoaded, fileLoaded + block + 1);
                    } else if (cur_b.obj.slice) {
                        blob = cur_b.obj.slice(fileLoaded, fileLoaded + block + 1);
                    } else {
                        blob = cur_b.obj;
                    }
                    reader.readAsArrayBuffer(blob);
                }
                var piece;
                reader.onload = function reader_onload(e) {
                    fileLoaded += e.total;
                    if (fileLoaded < fileSize) {
                        if (e.target.result) {
                            piece = new Uint8Array(e.target.result);
                            _check_aborted(session);
                            xfer.send(piece);
                            if (options.on_progress) {
                                options.on_progress(cur_b.obj, xfer, piece);
                            }
                        }
                        readBlob();
                    } else {
                        //
                        if (e.target.result) {
                            piece = new Uint8Array(e.target.result);
                            _check_aborted(session);
                            xfer.end(piece).then(function() {
                                if (options.on_progress && piece.length) {
                                    options.on_progress(cur_b.obj, xfer, piece);
                                }
                                if (options.on_file_complete) {
                                    options.on_file_complete(cur_b.obj, xfer);
                                }
                                res(promise_callback());
                            })
                        }
                    }
                }
                readBlob();
            });
        });
    }

    return promise_callback();
}