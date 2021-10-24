import request from '@/utils/request'
// 获取会话
export const getSessionLog = (data = {}) => {
    return request({
        url: "session-log/",
        method: "get",
        params: data
    })
}


//强制下线
export const delSessionLog = (data = {}) => {
    return request({
        url: 'session-log/',
        method: 'delete',
        data
    })
}
export const baseUrl = process.env.NODE_ENV === "development" ?
    // 'https://dev.opsany.cn/t/control/api/bastion/v0_1/' 
    "http://192.168.0.10:8000/api/bastion/v0_1/"

    : window.location.origin + window.API_ROOT + "api/bastion/v0_1/"

//获取windows录像文件
export const getWindowsReplay = (id = "",) => {
    return baseUrl + 'session-log/guacamole/' + `${id}/`
}


// 获取审计历史
export const getCommandHistory = (data = {}) => {
    return request({
        url: "command-log/",
        method: "get",
        params: data
    })
}

// 获取操作日志
export const getOperationLog = (data = {}) => {
    return request({
        url: "operation-log/",
        method: "get",
        params: data
    })
}

// 获取操作命令记录
export const getSessionHistory = (data = {}) => {
    return request({
        url: "session-command-history/",
        method: "get",
        params: data
    })
}
