import request from '@/utils/request'
// 获取凭证数据
export const getGroup = (data = {}) => {
    return request({
        url: "credential-group/",
        method: "get",
        params: data
    })
}

// 获取凭证数据
export const addGroup = (data = {}) => {
    return request({
        url: "credential-group/",
        method: "post",
        data
    })
}

// 编辑凭证数据
export const editGroup = (data = {}) => {
    return request({
        url: "credential-group/",
        method: "put",
        data
    })
}
// 删除凭证数据
export const delGroup = (data = {}) => {
    return request({
        url: "credential-group/",
        method: "delete",
        data
    })
}

// 移除凭证分组与凭证的关联
export const removeCredential = (data = {}) => {
    return request({
        url: "group-credential/",
        method: "delete",
        data
    })
}