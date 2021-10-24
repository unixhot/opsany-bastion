import request from '@/utils/request'
// 获取主机数据
export const getHost = (data = {}) => {
    return request({
        url: "host/",
        method: "get",
        params: data
    })
}

// 新建主机
export const addHost = (data = {}) => {
    return request({
        url: "host/",
        method: "post",
        data
    })
}

// 编辑主机
export const editHost = (data = {}) => {
    return request({
        url: "host/",
        method: "put",
        data
    })
}
// 删除主机
export const delHost = (data = {}) => {
    return request({
        url: "host/",
        method: "delete",
        data
    })
}


// 获取主机分组数据
export const getHostGroup = (data = {}) => {
    return request({
        url: "host-group/",
        method: "get",
        params: data
    })
}

// 获取主机分组数据
export const addHostGroup = (data = {}) => {
    return request({
        url: "host-group/",
        method: "post",
        data
    })
}

// 修改主机分组
export const editHostGroup = (data = {}) => {
    return request({
        url: "host-group/",
        method: "put",
        data
    })
}
// 删除主机分组
export const delHostGroup = (data = {}) => {
    return request({
        url: "host-group/",
        method: "delete",
        data
    })
}

// 移除主机上的凭证
export const removeCredentialFromHost = (data = {}) => {
    return request({
        url: "host-credential/",
        method: "delete",
        data
    })
}


// 获取用户主机数据
export const getUserHost = (data = {}) => {
    return request({
        url: "auth-host/",
        method: "get",
        params: data
    })
}