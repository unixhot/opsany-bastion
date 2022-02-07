import request from '@/utils/request'
// 获取网络代理数据
export const getNetworkProxy = (data = {}) => {
    return request({
        url: "network-proxy/",
        method: "get",
        params: data
    })
}

// 添加网络代理
export const addNetworkProxy = (data = {}) => {
    return request({
        url: "network-proxy/",
        method: "post",
        data
    })
}

// 修改网络代理
export const editNetworkProxy = (data = {}) => {
    return request({
        url: "network-proxy/",
        method: "put",
        data
    })
}

// 删除网络代理
export const delNetworkProxy = (data = {}) => {
    return request({
        url: "network-proxy/",
        method: "delete",
        data
    })
}

// 获取网络代理关联的主机或数据库
export const getNetworkProxyRelationHost = (data = {}) => {
    return request({
        url: "network-proxy-resource/",
        method: "get",
        params: data
    })
}

// 移除网络代理关联的主机或数据库
export const delNetworkProxyRelationHost = (data = {}) => {
    return request({
        url: "network-proxy-resource/",
        method: "delete",
        data
    })
}

// 添加网络代理关联的主机或数据库
export const addNetworkProxyRelationHost = (data = {}) => {
    return request({
        url: "network-proxy-resource/",
        method: "post",
        data
    })
}