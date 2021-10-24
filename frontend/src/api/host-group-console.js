import request from '@/utils/request'

// 获取主机列表（树类型）
export const getHostGroupList = (data = {}) => {
	return request({
		url: "host-group-console/",
		method: "get",
		params: data
	})
}

