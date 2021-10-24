import request from '@/utils/request'

// 从cmdb获取主机数据
export const getAgent = (data = {}) => {
    return request({
        url: "get-agent/",
        method: "get",
        params: data
    })
}