(window["webpackJsonp"]=window["webpackJsonp"]||[]).push([["chunk-2b185ec5"],{"0c00":function(t,e,n){"use strict";e["a"]=[{width:800,height:600,key:1},{width:1024,height:768,key:2},{width:1280,height:720,key:3},{width:1280,height:800,key:4},{width:1280,height:1024,key:5},{width:1366,height:768,key:6},{width:1440,height:900,key:7},{width:1920,height:1080,key:8},{width:1920,height:1200,key:9},{width:2160,height:1440,key:10},{width:2560,height:1600,key:11},{width:2880,height:1800,key:12}]},"1da1":function(t,e,n){"use strict";n.d(e,"a",(function(){return o}));n("d3b7");function i(t,e,n,i,o,r,a){try{var c=t[r](a),s=c.value}catch(l){return void n(l)}c.done?e(s):Promise.resolve(s).then(i,o)}function o(t){return function(){var e=this,n=arguments;return new Promise((function(o,r){var a=t.apply(e,n);function c(t){i(a,o,r,c,s,"next",t)}function s(t){i(a,o,r,c,s,"throw",t)}c(void 0)}))}}},"8a60":function(t,e,n){var i;(function(o,r,a){if(o){for(var c,s={8:"backspace",9:"tab",13:"enter",16:"shift",17:"ctrl",18:"alt",20:"capslock",27:"esc",32:"space",33:"pageup",34:"pagedown",35:"end",36:"home",37:"left",38:"up",39:"right",40:"down",45:"ins",46:"del",91:"meta",93:"meta",224:"meta"},l={106:"*",107:"+",109:"-",110:".",111:"/",186:";",187:"=",188:",",189:"-",190:".",191:"/",192:"`",219:"[",220:"\\",221:"]",222:"'"},u={"~":"`","!":"1","@":"2","#":"3",$:"4","%":"5","^":"6","&":"7","*":"8","(":"9",")":"0",_:"-","+":"=",":":";",'"':"'","<":",",">":".","?":"/","|":"\\"},f={option:"alt",command:"meta",return:"enter",escape:"esc",plus:"+",mod:/Mac|iPod|iPhone|iPad/.test(navigator.platform)?"meta":"ctrl"},d=1;d<20;++d)s[111+d]="f"+d;for(d=0;d<=9;++d)s[d+96]=d.toString();C.prototype.bind=function(t,e,n){var i=this;return t=t instanceof Array?t:[t],i._bindMultiple.call(i,t,e,n),i},C.prototype.unbind=function(t,e){var n=this;return n.bind.call(n,t,(function(){}),e)},C.prototype.trigger=function(t,e){var n=this;return n._directMap[t+":"+e]&&n._directMap[t+":"+e]({},t),n},C.prototype.reset=function(){var t=this;return t._callbacks={},t._directMap={},t},C.prototype.stopCallback=function(t,e){var n=this;if((" "+e.className+" ").indexOf(" mousetrap ")>-1)return!1;if(E(e,n.target))return!1;if("composedPath"in t&&"function"===typeof t.composedPath){var i=t.composedPath()[0];i!==t.target&&(e=i)}return"INPUT"==e.tagName||"SELECT"==e.tagName||"TEXTAREA"==e.tagName||e.isContentEditable},C.prototype.handleKey=function(){var t=this;return t._handleKey.apply(t,arguments)},C.addKeycodes=function(t){for(var e in t)t.hasOwnProperty(e)&&(s[e]=t[e]);c=null},C.init=function(){var t=C(r);for(var e in t)"_"!==e.charAt(0)&&(C[e]=function(e){return function(){return t[e].apply(t,arguments)}}(e))},C.init(),o.Mousetrap=C,t.exports&&(t.exports=C),i=function(){return C}.call(e,n,e,t),i===a||(t.exports=i)}function h(t,e,n){t.addEventListener?t.addEventListener(e,n,!1):t.attachEvent("on"+e,n)}function p(t){if("keypress"==t.type){var e=String.fromCharCode(t.which);return t.shiftKey||(e=e.toLowerCase()),e}return s[t.which]?s[t.which]:l[t.which]?l[t.which]:String.fromCharCode(t.which).toLowerCase()}function y(t,e){return t.sort().join(",")===e.sort().join(",")}function m(t){var e=[];return t.shiftKey&&e.push("shift"),t.altKey&&e.push("alt"),t.ctrlKey&&e.push("ctrl"),t.metaKey&&e.push("meta"),e}function v(t){t.preventDefault?t.preventDefault():t.returnValue=!1}function b(t){t.stopPropagation?t.stopPropagation():t.cancelBubble=!0}function g(t){return"shift"==t||"ctrl"==t||"alt"==t||"meta"==t}function k(){if(!c)for(var t in c={},s)t>95&&t<112||s.hasOwnProperty(t)&&(c[s[t]]=t);return c}function w(t,e,n){return n||(n=k()[t]?"keydown":"keypress"),"keypress"==n&&e.length&&(n="keydown"),n}function _(t){return"+"===t?["+"]:(t=t.replace(/\+{2}/g,"+plus"),t.split("+"))}function x(t,e){var n,i,o,r=[];for(n=_(t),o=0;o<n.length;++o)i=n[o],f[i]&&(i=f[i]),e&&"keypress"!=e&&u[i]&&(i=u[i],r.push("shift")),g(i)&&r.push(i);return e=w(i,r,e),{key:i,modifiers:r,action:e}}function E(t,e){return null!==t&&t!==r&&(t===e||E(t.parentNode,e))}function C(t){var e=this;if(t=t||r,!(e instanceof C))return new C(t);e.target=t,e._callbacks={},e._directMap={};var n,i={},o=!1,a=!1,c=!1;function s(t){t=t||{};var e,n=!1;for(e in i)t[e]?n=!0:i[e]=0;n||(c=!1)}function l(t,n,o,r,a,c){var s,l,u=[],f=o.type;if(!e._callbacks[t])return[];for("keyup"==f&&g(t)&&(n=[t]),s=0;s<e._callbacks[t].length;++s)if(l=e._callbacks[t][s],(r||!l.seq||i[l.seq]==l.level)&&f==l.action&&("keypress"==f&&!o.metaKey&&!o.ctrlKey||y(n,l.modifiers))){var d=!r&&l.combo==a,h=r&&l.seq==r&&l.level==c;(d||h)&&e._callbacks[t].splice(s,1),u.push(l)}return u}function u(t,n,i,o){e.stopCallback(n,n.target||n.srcElement,i,o)||!1===t(n,i)&&(v(n),b(n))}function f(t){"number"!==typeof t.which&&(t.which=t.keyCode);var n=p(t);n&&("keyup"!=t.type||o!==n?e.handleKey(n,m(t),t):o=!1)}function d(){clearTimeout(n),n=setTimeout(s,1e3)}function k(t,e,n,r){function a(e){return function(){c=e,++i[t],d()}}function l(e){u(n,e,t),"keyup"!==r&&(o=p(e)),setTimeout(s,10)}i[t]=0;for(var f=0;f<e.length;++f){var h=f+1===e.length,y=h?l:a(r||x(e[f+1]).action);w(e[f],y,r,t,f)}}function w(t,n,i,o,r){e._directMap[t+":"+i]=n,t=t.replace(/\s+/g," ");var a,c=t.split(" ");c.length>1?k(t,c,n,i):(a=x(t,i),e._callbacks[a.key]=e._callbacks[a.key]||[],l(a.key,a.modifiers,{type:a.action},o,t,r),e._callbacks[a.key][o?"unshift":"push"]({callback:n,modifiers:a.modifiers,action:a.action,seq:o,level:r,combo:t}))}e._handleKey=function(t,e,n){var i,o=l(t,e,n),r={},f=0,d=!1;for(i=0;i<o.length;++i)o[i].seq&&(f=Math.max(f,o[i].level));for(i=0;i<o.length;++i)if(o[i].seq){if(o[i].level!=f)continue;d=!0,r[o[i].seq]=1,u(o[i].callback,n,o[i].combo,o[i].seq)}else d||u(o[i].callback,n,o[i].combo);var h="keypress"==n.type&&a;n.type!=c||g(t)||h||s(r),a=d&&"keydown"==n.type},e._bindMultiple=function(t,e,n){for(var i=0;i<t.length;++i)w(t[i],e,n)},h(t,"keypress",f),h(t,"keydown",f),h(t,"keyup",f)}})("undefined"!==typeof window?window:null,"undefined"!==typeof window?document:null)},b311:function(t,e,n){
/*!
 * clipboard.js v2.0.8
 * https://clipboardjs.com/
 *
 * Licensed MIT © Zeno Rocha
 */
(function(e,n){t.exports=n()})(0,(function(){return function(){var t={134:function(t,e,n){"use strict";n.d(e,{default:function(){return L}});var i=n(279),o=n.n(i),r=n(370),a=n.n(r),c=n(817),s=n.n(c);function l(t){return l="function"===typeof Symbol&&"symbol"===typeof Symbol.iterator?function(t){return typeof t}:function(t){return t&&"function"===typeof Symbol&&t.constructor===Symbol&&t!==Symbol.prototype?"symbol":typeof t},l(t)}function u(t,e){if(!(t instanceof e))throw new TypeError("Cannot call a class as a function")}function f(t,e){for(var n=0;n<e.length;n++){var i=e[n];i.enumerable=i.enumerable||!1,i.configurable=!0,"value"in i&&(i.writable=!0),Object.defineProperty(t,i.key,i)}}function d(t,e,n){return e&&f(t.prototype,e),n&&f(t,n),t}var h=function(){function t(e){u(this,t),this.resolveOptions(e),this.initSelection()}return d(t,[{key:"resolveOptions",value:function(){var t=arguments.length>0&&void 0!==arguments[0]?arguments[0]:{};this.action=t.action,this.container=t.container,this.emitter=t.emitter,this.target=t.target,this.text=t.text,this.trigger=t.trigger,this.selectedText=""}},{key:"initSelection",value:function(){this.text?this.selectFake():this.target&&this.selectTarget()}},{key:"createFakeElement",value:function(){var t="rtl"===document.documentElement.getAttribute("dir");this.fakeElem=document.createElement("textarea"),this.fakeElem.style.fontSize="12pt",this.fakeElem.style.border="0",this.fakeElem.style.padding="0",this.fakeElem.style.margin="0",this.fakeElem.style.position="absolute",this.fakeElem.style[t?"right":"left"]="-9999px";var e=window.pageYOffset||document.documentElement.scrollTop;return this.fakeElem.style.top="".concat(e,"px"),this.fakeElem.setAttribute("readonly",""),this.fakeElem.value=this.text,this.fakeElem}},{key:"selectFake",value:function(){var t=this,e=this.createFakeElement();this.fakeHandlerCallback=function(){return t.removeFake()},this.fakeHandler=this.container.addEventListener("click",this.fakeHandlerCallback)||!0,this.container.appendChild(e),this.selectedText=s()(e),this.copyText(),this.removeFake()}},{key:"removeFake",value:function(){this.fakeHandler&&(this.container.removeEventListener("click",this.fakeHandlerCallback),this.fakeHandler=null,this.fakeHandlerCallback=null),this.fakeElem&&(this.container.removeChild(this.fakeElem),this.fakeElem=null)}},{key:"selectTarget",value:function(){this.selectedText=s()(this.target),this.copyText()}},{key:"copyText",value:function(){var t;try{t=document.execCommand(this.action)}catch(e){t=!1}this.handleResult(t)}},{key:"handleResult",value:function(t){this.emitter.emit(t?"success":"error",{action:this.action,text:this.selectedText,trigger:this.trigger,clearSelection:this.clearSelection.bind(this)})}},{key:"clearSelection",value:function(){this.trigger&&this.trigger.focus(),document.activeElement.blur(),window.getSelection().removeAllRanges()}},{key:"destroy",value:function(){this.removeFake()}},{key:"action",set:function(){var t=arguments.length>0&&void 0!==arguments[0]?arguments[0]:"copy";if(this._action=t,"copy"!==this._action&&"cut"!==this._action)throw new Error('Invalid "action" value, use either "copy" or "cut"')},get:function(){return this._action}},{key:"target",set:function(t){if(void 0!==t){if(!t||"object"!==l(t)||1!==t.nodeType)throw new Error('Invalid "target" value, use a valid Element');if("copy"===this.action&&t.hasAttribute("disabled"))throw new Error('Invalid "target" attribute. Please use "readonly" instead of "disabled" attribute');if("cut"===this.action&&(t.hasAttribute("readonly")||t.hasAttribute("disabled")))throw new Error('Invalid "target" attribute. You can\'t cut text from elements with "readonly" or "disabled" attributes');this._target=t}},get:function(){return this._target}}]),t}(),p=h;function y(t){return y="function"===typeof Symbol&&"symbol"===typeof Symbol.iterator?function(t){return typeof t}:function(t){return t&&"function"===typeof Symbol&&t.constructor===Symbol&&t!==Symbol.prototype?"symbol":typeof t},y(t)}function m(t,e){if(!(t instanceof e))throw new TypeError("Cannot call a class as a function")}function v(t,e){for(var n=0;n<e.length;n++){var i=e[n];i.enumerable=i.enumerable||!1,i.configurable=!0,"value"in i&&(i.writable=!0),Object.defineProperty(t,i.key,i)}}function b(t,e,n){return e&&v(t.prototype,e),n&&v(t,n),t}function g(t,e){if("function"!==typeof e&&null!==e)throw new TypeError("Super expression must either be null or a function");t.prototype=Object.create(e&&e.prototype,{constructor:{value:t,writable:!0,configurable:!0}}),e&&k(t,e)}function k(t,e){return k=Object.setPrototypeOf||function(t,e){return t.__proto__=e,t},k(t,e)}function w(t){var e=E();return function(){var n,i=C(t);if(e){var o=C(this).constructor;n=Reflect.construct(i,arguments,o)}else n=i.apply(this,arguments);return _(this,n)}}function _(t,e){return!e||"object"!==y(e)&&"function"!==typeof e?x(t):e}function x(t){if(void 0===t)throw new ReferenceError("this hasn't been initialised - super() hasn't been called");return t}function E(){if("undefined"===typeof Reflect||!Reflect.construct)return!1;if(Reflect.construct.sham)return!1;if("function"===typeof Proxy)return!0;try{return Date.prototype.toString.call(Reflect.construct(Date,[],(function(){}))),!0}catch(t){return!1}}function C(t){return C=Object.setPrototypeOf?Object.getPrototypeOf:function(t){return t.__proto__||Object.getPrototypeOf(t)},C(t)}function S(t,e){var n="data-clipboard-".concat(t);if(e.hasAttribute(n))return e.getAttribute(n)}var T=function(t){g(n,t);var e=w(n);function n(t,i){var o;return m(this,n),o=e.call(this),o.resolveOptions(i),o.listenClick(t),o}return b(n,[{key:"resolveOptions",value:function(){var t=arguments.length>0&&void 0!==arguments[0]?arguments[0]:{};this.action="function"===typeof t.action?t.action:this.defaultAction,this.target="function"===typeof t.target?t.target:this.defaultTarget,this.text="function"===typeof t.text?t.text:this.defaultText,this.container="object"===y(t.container)?t.container:document.body}},{key:"listenClick",value:function(t){var e=this;this.listener=a()(t,"click",(function(t){return e.onClick(t)}))}},{key:"onClick",value:function(t){var e=t.delegateTarget||t.currentTarget;this.clipboardAction&&(this.clipboardAction=null),this.clipboardAction=new p({action:this.action(e),target:this.target(e),text:this.text(e),container:this.container,trigger:e,emitter:this})}},{key:"defaultAction",value:function(t){return S("action",t)}},{key:"defaultTarget",value:function(t){var e=S("target",t);if(e)return document.querySelector(e)}},{key:"defaultText",value:function(t){return S("text",t)}},{key:"destroy",value:function(){this.listener.destroy(),this.clipboardAction&&(this.clipboardAction.destroy(),this.clipboardAction=null)}}],[{key:"isSupported",value:function(){var t=arguments.length>0&&void 0!==arguments[0]?arguments[0]:["copy","cut"],e="string"===typeof t?[t]:t,n=!!document.queryCommandSupported;return e.forEach((function(t){n=n&&!!document.queryCommandSupported(t)})),n}}]),n}(o()),L=T},828:function(t){var e=9;if("undefined"!==typeof Element&&!Element.prototype.matches){var n=Element.prototype;n.matches=n.matchesSelector||n.mozMatchesSelector||n.msMatchesSelector||n.oMatchesSelector||n.webkitMatchesSelector}function i(t,n){while(t&&t.nodeType!==e){if("function"===typeof t.matches&&t.matches(n))return t;t=t.parentNode}}t.exports=i},438:function(t,e,n){var i=n(828);function o(t,e,n,i,o){var r=a.apply(this,arguments);return t.addEventListener(n,r,o),{destroy:function(){t.removeEventListener(n,r,o)}}}function r(t,e,n,i,r){return"function"===typeof t.addEventListener?o.apply(null,arguments):"function"===typeof n?o.bind(null,document).apply(null,arguments):("string"===typeof t&&(t=document.querySelectorAll(t)),Array.prototype.map.call(t,(function(t){return o(t,e,n,i,r)})))}function a(t,e,n,o){return function(n){n.delegateTarget=i(n.target,e),n.delegateTarget&&o.call(t,n)}}t.exports=r},879:function(t,e){e.node=function(t){return void 0!==t&&t instanceof HTMLElement&&1===t.nodeType},e.nodeList=function(t){var n=Object.prototype.toString.call(t);return void 0!==t&&("[object NodeList]"===n||"[object HTMLCollection]"===n)&&"length"in t&&(0===t.length||e.node(t[0]))},e.string=function(t){return"string"===typeof t||t instanceof String},e.fn=function(t){var e=Object.prototype.toString.call(t);return"[object Function]"===e}},370:function(t,e,n){var i=n(879),o=n(438);function r(t,e,n){if(!t&&!e&&!n)throw new Error("Missing required arguments");if(!i.string(e))throw new TypeError("Second argument must be a String");if(!i.fn(n))throw new TypeError("Third argument must be a Function");if(i.node(t))return a(t,e,n);if(i.nodeList(t))return c(t,e,n);if(i.string(t))return s(t,e,n);throw new TypeError("First argument must be a String, HTMLElement, HTMLCollection, or NodeList")}function a(t,e,n){return t.addEventListener(e,n),{destroy:function(){t.removeEventListener(e,n)}}}function c(t,e,n){return Array.prototype.forEach.call(t,(function(t){t.addEventListener(e,n)})),{destroy:function(){Array.prototype.forEach.call(t,(function(t){t.removeEventListener(e,n)}))}}}function s(t,e,n){return o(document.body,t,e,n)}t.exports=r},817:function(t){function e(t){var e;if("SELECT"===t.nodeName)t.focus(),e=t.value;else if("INPUT"===t.nodeName||"TEXTAREA"===t.nodeName){var n=t.hasAttribute("readonly");n||t.setAttribute("readonly",""),t.select(),t.setSelectionRange(0,t.value.length),n||t.removeAttribute("readonly"),e=t.value}else{t.hasAttribute("contenteditable")&&t.focus();var i=window.getSelection(),o=document.createRange();o.selectNodeContents(t),i.removeAllRanges(),i.addRange(o),e=i.toString()}return e}t.exports=e},279:function(t){function e(){}e.prototype={on:function(t,e,n){var i=this.e||(this.e={});return(i[t]||(i[t]=[])).push({fn:e,ctx:n}),this},once:function(t,e,n){var i=this;function o(){i.off(t,o),e.apply(n,arguments)}return o._=e,this.on(t,o,n)},emit:function(t){var e=[].slice.call(arguments,1),n=((this.e||(this.e={}))[t]||[]).slice(),i=0,o=n.length;for(i;i<o;i++)n[i].fn.apply(n[i].ctx,e);return this},off:function(t,e){var n=this.e||(this.e={}),i=n[t],o=[];if(i&&e)for(var r=0,a=i.length;r<a;r++)i[r].fn!==e&&i[r].fn._!==e&&o.push(i[r]);return o.length?n[t]=o:delete n[t],this}},t.exports=e,t.exports.TinyEmitter=e}},e={};function n(i){if(e[i])return e[i].exports;var o=e[i]={exports:{}};return t[i](o,o.exports,n),o.exports}return function(){n.n=function(t){var e=t&&t.__esModule?function(){return t["default"]}:function(){return t};return n.d(e,{a:e}),e}}(),function(){n.d=function(t,e){for(var i in e)n.o(e,i)&&!n.o(t,i)&&Object.defineProperty(t,i,{enumerable:!0,get:e[i]})}}(),function(){n.o=function(t,e){return Object.prototype.hasOwnProperty.call(t,e)}}(),n(134)}().default}))},b360:function(t,e,n){"use strict";n.r(e);var i=function(){var t=this,e=t.$createElement,n=t._self._c||e;return n("div",{staticClass:"container",staticStyle:{height:"100%"}},[n("div",{ref:"guacamole_box",staticClass:"guacamole_box"},[t._m(0)]),n("button",{attrs:{id:"clipboard",hidden:"","data-clipboard-text":""}}),n("a-input",{ref:"input",attrs:{"auto-focus":t.autofocus,hidden:""}}),t.showRight?n("div",{staticClass:"info"},[n("div",{staticClass:"rightbox"},[n("a-tabs",{on:{change:t.changeTabs},model:{value:t.tabs_key,callback:function(e){t.tabs_key=e},expression:"tabs_key"}},[n("a-tab-pane",{key:"1",staticClass:"session_info",attrs:{tab:"会话详情"}},[n("a-spin",{attrs:{spinning:t.sessionLoading}},[n("div",{staticStyle:{height:"100%"}},[n("div",[n("div",{staticClass:"term_info_box"},[n("div",{staticClass:"term_title"},[t._v("主机信息")]),n("div",{staticClass:"term_info"},[t._v("主机名称："+t._s(t.nodeInfo.host_name||"-"))]),n("div",{staticClass:"term_info"},[t._v("IP地址："+t._s(t.nodeInfo.host_address||"-"))])])])])])],1),n("a-tab-pane",{key:"2",staticClass:"file_trans",attrs:{tab:"文件传输",disabled:!t.file_manager}},[n("a-spin",{attrs:{spinning:t.fileLoading}},[n("div",{staticStyle:{height:"100%",overflow:"hidden"}},[n("div",{staticClass:"top_btns"},t._l(t.btnList,(function(e){return n("a-tooltip",{key:e.key,attrs:{placement:"top"}},[n("template",{slot:"title"},[n("span",[t._v(t._s(e.disabled?e.disabledHelp:e.text))])]),"upload"!=e.icon?n("a-button",{attrs:{icon:e.icon,type:"link",disabled:e.disabled},on:{click:function(n){return t.clickBtnChild(e)}}}):n("a-upload",{attrs:{name:"file",multiple:!1,showUploadList:!1,withCredentials:!0,customRequest:t.handleUpload,disabled:t.uploadLoading}},[n("a-button",{attrs:{icon:e.icon,type:"link",disabled:e.disabled},on:{click:function(n){return t.clickBtnChild(e)}}})],1)],2)})),1),n("div",{staticClass:"bread_box"},[n("a-breadcrumb",{staticClass:"breadcrumb_box"},t._l(t.breadCrumbList,(function(e,i){return n("a-breadcrumb-item",{key:i,staticClass:"breadcrumb",style:t.breadcrumbStyle,attrs:{title:e.name},nativeOn:{click:function(n){return t.clickBread(e,i)}}},[t._v(" "+t._s(e.name)+" ")])})),1)],1),t.tableData.length?n("div",{staticClass:"file_box"},t._l(t.tableData,(function(e,i){return n("div",{key:i,class:{isCheck:e.isCheck}},[n("span",{attrs:{title:e.name},on:{click:function(n){return t.clickFileName(e)}}},[n("a-icon",{staticStyle:{"padding-right":"2px"},attrs:{type:e.type}}),n("a-tooltip",{attrs:{placement:"topLeft",mouseLeaveDelay:.05}},[n("template",{slot:"title"},[n("span",[t._v(t._s(e.name))])]),n("span",[t._v(t._s(e.name))])],2)],1),n("a-tooltip",{attrs:{placement:"top"}},[n("template",{slot:"title"},[n("span",[t._v("删除")])]),n("a-icon",{staticClass:"del_icon",attrs:{type:"delete"},on:{click:function(n){return t.rightDelFile(e)}}})],2)],1)})),0):n("a-empty",{staticStyle:{"margin-top":"200px"}})],1)])],1)],1),1==t.tabs_key?n("a-button",{staticClass:"term_info_button",attrs:{type:"primary"},on:{click:t.closeRemote}},[t._v("关闭/结束会话")]):t._e()],1)]):t._e()],1)},o=[function(){var t=this,e=t.$createElement,n=t._self._c||e;return n("div",{staticClass:"guacamole_box_visible"},[n("div",{attrs:{id:"guacamole_box"}})])}],r=(n("99af"),n("7db0"),n("4160"),n("a15b"),n("fb6a"),n("a434"),n("b0c0"),n("d3b7"),n("ac1f"),n("5319"),n("1276"),n("159b"),n("96cf"),n("1da1")),a=n("a9c6"),c=n.n(a),s=n("ca00"),l=n("e6c6"),u=n("b775"),f=n("e819"),d="windows-file/",h=function(){var t=arguments.length>0&&void 0!==arguments[0]?arguments[0]:{};return Object(u["b"])({url:d,method:"get",params:t})},p=function(){var t=arguments.length>0&&void 0!==arguments[0]?arguments[0]:{};return f["a"].baseUrl+d+Object(s["b"])(t)},y=function(){var t=arguments.length>0&&void 0!==arguments[0]?arguments[0]:{};return Object(u["b"])({url:d,method:"post",data:t})},m=function(){var t=arguments.length>0&&void 0!==arguments[0]?arguments[0]:{};return Object(u["b"])({url:d,method:"delete",data:t})},v=n("b311"),b=n.n(v),g=n("8a60"),k=n.n(g),w=n("0c00"),_={data:function(){return{wsurl:"",guac:null,host_token:"",urlParams:{},nodeInfo:{},sessionLoading:!1,fileLoading:!1,uploadLoading:!1,tabs_key:"1",tableData:[],breadCrumbList:[],current_path:"",autofocus:!1,showRight:!0,copy_tool:!1,file_download:!1,file_upload:!1,file_manager:!1,timer:null,scale:1,dpi:96,screenArr:w["a"],activeScreen:{},winSizeKey:void 0}},methods:{initContent:function(){var t=this;return Object(r["a"])(regeneratorRuntime.mark((function e(){var n,i,o;return regeneratorRuntime.wrap((function(e){while(1)switch(e.prev=e.next){case 0:n=t.$createElement,i="http:"==window.location.protocol?"ws":"wss",t.wsurl="".concat(i,"://").concat(window.location.host,"/ws/bastion/"),o="".concat(t.wsurl,"guacamole/"),t.guac=new c.a.Client(new c.a.WebSocketTunnel(o)),t.getNodeInfo().then((function(e){t.handleMousetrap()})),t.$nextTick((function(){var e=document.getElementById("guacamole_box");t.resizeCanvas(),e.appendChild(t.guac.getDisplay().getElement());var i={token:t.host_token,width:t.activeScreen.width,height:t.activeScreen.height,dpi:t.dpi};t.guac.connect(Object(s["b"])(i).replace("?","")),t.guac.onerror=function(e){var i="Disconnected by other connection."==e.message?"另一用户已连接到此远程计算机，因此您的连接已失效。":"Windows堡垒机连接失败，请检查机器状态或联系管理员处理。";t.$notification.open({message:"提示",description:i,icon:n("a-icon",{attrs:{type:"frown"},style:"color: #FF4D4F"})})},t.guac.onclipboard=function(t,e){if(/^text\//.test(e)){var n=new c.a.StringReader(t),i="";n.ontext=function(t){i+=t},n.onend=function(){if(i.length<=65535){var t=document.getElementById("clipboard");t.setAttribute("data-clipboard-text",i);var e=new b.a("#clipboard");t.click(),e.destroy()}}}};var o=new c.a.Mouse(t.guac.getDisplay().getElement()),r=function(e){t.guac.sendMouseState(e)};o.onmousedown=o.onmouseup=r,o.onmousemove=function(t){a(t)};var a=function(e){e.y=e.y/t.scale,e.x=e.x/t.scale,t.guac.sendMouseState(e)},l=new c.a.Keyboard(document);l.onkeydown=function(e){t.guac.sendKeyEvent(1,e)},l.onkeyup=function(e){t.guac.sendKeyEvent(0,e)}}));case 7:case"end":return e.stop()}}),e)})))()},handleMousetrap:function(){var t=this,e=arguments.length>0&&void 0!==arguments[0]?arguments[0]:["ctrl+v","command+v"];this.copy_tool&&k.a.bind(e,(function(e){var n;t.$refs.input.focus(),null===(n=navigator.clipboard)||void 0===n||n.readText().then((function(e){for(var n=t.guac.createClipboardStream("text/plain"),i=new c.a.StringWriter(n),o=0;o<e.length;o+=4096)i.sendText(e.substring(o,o+4096));i.onack=function(t){},i.sendEnd()}))}))},getNodeInfo:function(){var t=this;return this.sessionLoading=!0,Object(l["a"])({token:this.host_token,data_type:"host"}).then((function(e){t.nodeInfo=e.data})).finally((function(){t.sessionLoading=!1})),new Promise((function(e,n){Object(l["a"])({token:t.host_token,data_type:"file_admin"}).then((function(e){t.copy_tool=e.data.copy_tool,t.file_download=e.data.file_download,t.file_manager=e.data.file_manager,t.file_upload=e.data.file_upload})).finally((function(){return e()}))}))},changeTabs:function(t){2==t&&this.getWinFileInfo()},clickBtnChild:function(t){this[t.key]&&this[t.key]()},refresh:function(){this.getWinFileInfo()},getWinFileInfo:function(){var t=this,e=arguments.length>0&&void 0!==arguments[0]?arguments[0]:this.current_path;this.fileLoading=!0;var n={data_type:"file_list",token:this.host_token,url:e};h(n).then((function(e){t.current_path=e.data.current_path,t.handleBreadCrumb();var n=[],i=[];e.data.data.file.forEach((function(t){n.push({name:t,type:"file",isCheck:!1})})),e.data.data.path.forEach((function(t){i.push({name:t,type:"folder",isCheck:!1})})),t.tableData=i.concat(n)})).finally((function(){t.fileLoading=!1}))},handleBreadCrumb:function(){var t=this.current_path&&this.current_path.split("/")||[],e=[];t.forEach((function(n,i){var o={name:n,path:t.slice(0,i+1).join("/")};e.push(o)})),e.length>3&&e.splice(1,e.length-3,{name:"...",path:null}),this.breadCrumbList=e},clickBread:function(t,e){t.path&&e!=this.breadCrumbList.length-1&&this.getWinFileInfo(t.path)},clickFileName:function(t){var e=this.current_path+"/"+t.name;"folder"==t.type?this.getWinFileInfo(e):(this.tableData.forEach((function(t){t.isCheck=!1})),t.isCheck=!0)},rightdownLoadFile:function(){var t=this.tableData.find((function(t){return t.isCheck}));if(!t)return this.$message.warning("请选择一个文件后下载");var e=this.current_path+"/"+t.name,n={token:this.host_token,url:e,data_type:"file"};window.open(p(n))},handleUpload:function(t){var e=this;this.uploadLoading=!0;var n=this.$message.loading("文件上传中...",0),i=new FormData;i.append(t.filename,t.file),i.append("token",this.host_token),i.append("url",this.current_path),y(i).then((function(t){e.$message.success(t.message),e.getWinFileInfo()})).finally((function(){n(),e.uploadLoading=!1}))},rightDelFile:function(t){var e=this,n=this.current_path+"/"+t.name,i={token:this.host_token,url:n};this.$confirm({title:"删除确认",content:"请确认是否删除【".concat(t.name,"】").concat("file"==t.type?"文件":"folder"==t.type?"文件夹":"","?"),okType:"danger",onOk:function(){return m(i).then((function(t){e.$message.success("删除成功"),e.getWinFileInfo()}))}})},closeRemote:function(){window.close()},debounce:function(t){var e=this,n=arguments.length>1&&void 0!==arguments[1]?arguments[1]:50;return this.timer=null,function(){e.timer&&clearTimeout(e.timer),e.timer=setTimeout(t,n)}},resizeCanvas:function(){var t=this;this.activeScreen=this.screenArr.find((function(e){return e.key==t.winSizeKey}))||{width:window.screen.width*window.devicePixelRatio,height:window.screen.height*window.devicePixelRatio};var e=this.$refs.guacamole_box,n=Math.floor(e.getBoundingClientRect().width),i=window.innerHeight,o=this.guac.getDisplay(),r=this.activeScreen.width,a=this.activeScreen.height,c=n/r,s=i/a;this.scale=Math.min(c,s),o.scale(this.scale)}},mounted:function(){var t,e=this;this.host_token=this.$route.query.host_token,this.winSizeKey=this.$route.query.winSize,this.initContent();var n=this.debounce(this.resizeCanvas);window.addEventListener("resize",n),this.$once("hook:beforeDestroy",(function(){window.removeEventListener("resize",n),e.timer&&clearTimeout(e.timer)})),null===(t=navigator.clipboard)||void 0===t||t.readText().then((function(){})).catch((function(t){"Read permission denied."==t.message&&e.$message.info("剪贴板读取权限被禁止,为了您的正常使用,请重新打开剪贴板权限。")}))},beforeDestroy:function(){this.guac&&this.guac.disconnect()},computed:{btnList:function(){return[{icon:"upload",key:"upload",text:"上传",disabled:!this.file_upload,disabledHelp:"因权限策略问题，暂时无法上传文件"},{icon:"download",key:"rightdownLoadFile",text:"下载",disabledHelp:"因权限策略问题或未选中文件，暂时无法下载文件",disabled:!this.tableData.find((function(t){return t.isCheck}))||!this.file_download},{icon:"reload",key:"refresh",text:"刷新",disabled:!this.file_manager,disabledHelp:"因权限策略问题，暂时无法查看文件"}]},breadcrumbStyle:function(){var t=this.breadCrumbList.length;return{maxWidth:1==t?"100%":2==t?"50%":3==t?"33%":"28%"}}}},x=_,E=(n("b38b"),n("2877")),C=Object(E["a"])(x,i,o,!1,null,"97fa68b0",null);e["default"]=C.exports},b38b:function(t,e,n){"use strict";var i=n("b5c3"),o=n.n(i);o.a},b5c3:function(t,e,n){},e6c6:function(t,e,n){"use strict";n.d(e,"b",(function(){return o})),n.d(e,"a",(function(){return r}));var i=n("b775"),o=function(){var t=arguments.length>0&&void 0!==arguments[0]?arguments[0]:{};return Object(i["b"])({url:"link-check-v2/",method:"post",data:t})},r=function(){var t=arguments.length>0&&void 0!==arguments[0]?arguments[0]:{};return Object(i["b"])({url:"link-check-v2/",method:"get",params:t})}}}]);