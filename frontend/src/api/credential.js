import request from '@/utils/request'
// 获取凭证数据
export const getCredential = (data = {}) => {
    return request({
        url: "credential/",
        method: "get",
        params: data
    })
}
// 新建凭证
export const addCredential = (data = {}) => {
    return request({
        url: "credential/",
        method: "post",
        data
    })
}
// 修改凭证
export const editCredential = (data = {}) => {
    return request({
        url: "credential/",
        method: "put",
        data
    })
}
// 删除凭证
export const delCredential = (data = {}) => {
    return request({
        url: "credential/",
        method: "delete",
        data
    })
}