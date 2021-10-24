import request from '@/utils/request';

export const getPageAuth = (data = {}) => {
    return request({
        url: "authentication/",
        method: "get",
        params: data
    })
}
