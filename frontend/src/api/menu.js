import request from '@/utils/request'

/**
 * @deprecated  获取菜单列表
 * @param {data} Object
 * @returns Promise
 */

export const getMenuList = (data = {}) => {
    return request({
        url: "get-menu/",
        method: "get",
        params: data
    })
}