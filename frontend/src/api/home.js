import request from '@/utils/request'
// 获取凭证数据
export const getHome = (data = {}) => {
    return request({
        url: "home-page/",
        method: "get",
        params: data
    })
}