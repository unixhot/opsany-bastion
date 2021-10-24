const path = require('path')

export function timeFix() {
    const time = new Date()
    const hour = time.getHours()
    return hour < 9 ? '早上好' : hour <= 11 ? '上午好' : hour <= 13 ? '中午好' : hour < 20 ? '下午好' : '晚上好'
}

export function welcome() {
    const arr = ['休息一会儿吧', '准备吃什么呢?', '要不要打一把 DOTA', '我猜你可能累了']
    const index = Math.floor(Math.random() * arr.length)
    return arr[index]
}

/**
 * 触发 window.resize
 */
export function triggerWindowResizeEvent() {
    const event = document.createEvent('HTMLEvents')
    event.initEvent('resize', true, true)
    event.eventType = 'message'
    window.dispatchEvent(event)
}

export function handleScrollHeader(callback) {
    let timer = 0

    let beforeScrollTop = window.pageYOffset
    callback = callback || function() {}
    window.addEventListener(
        'scroll',
        event => {
            clearTimeout(timer)
            timer = setTimeout(() => {
                let direction = 'up'
                const afterScrollTop = window.pageYOffset
                const delta = afterScrollTop - beforeScrollTop
                if (delta === 0) {
                    return false
                }
                direction = delta > 0 ? 'down' : 'up'
                callback(direction)
                beforeScrollTop = afterScrollTop
            }, 50)
        },
        false
    )
}

export function isIE() {
    const bw = window.navigator.userAgent
    const compare = (s) => bw.indexOf(s) >= 0
    const ie11 = (() => 'ActiveXObject' in window)()
    return compare('MSIE') || ie11
}

/**
 * Remove loading animate
 * @param id parent element id or class
 * @param timeout
 */
export function removeLoadingAnimate(id = '', timeout = 1500) {
    if (id === '') {
        return
    }
    setTimeout(() => {
        document.body.removeChild(document.getElementById(id))
    }, timeout)
}


/**
 *
 * 搭配webpack内置的 require.context() 函数加载多个模块
 *
 * @param { Object } files 文件对象
 *
 * @return { Object } components 组件集合
 *
 * @Author 王伟伟
 */
export const readDirfiles = files => {
    const modules = {}
    files.keys().forEach(key => {
        const name = path.basename(key, '.vue')
        modules[name] = files(key).default || files(key)
    })
    return modules
}

/**
 * @description url参数序列化
 * @param {Object} search 需要序列化的对象
 * @param { Boolean } enCodeUrl 是否需要对url参数进行编码
 */
 export function stringifyUrl(search = {}, enCodeUrl = true) {
    return Object.entries(search).reduce(
        (t, v) => `${t}${v[0]}=${enCodeUrl?encodeURIComponent(v[1]):v[1]}&`,
        Object.keys(search).length ? "?" : ""
    ).replace(/&$/, "");
}