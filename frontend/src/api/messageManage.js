import request from '@/utils/request';


/**
 * @deprecated  消息管理
 * @param {data} Object
 * @returns Promise
 */

//获取消息列表 --头部导航
export const getUserMessageList = (data = {}) => {
    return request({
        url: "get-user-message/",
        method: "get",
        params: data
    })
}

//全部已读
export const readAllMessage = (data = {}) => {
    return request({
        url: "read-all-message/",
        method: "get",
        params: data
    })
}
