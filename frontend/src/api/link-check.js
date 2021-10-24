import request from '@/utils/request'

// 获取凭证数据
export const linkCheck = (data = {}) => {
	return request({
		url: "link-check-v2/",
		method: "post",
		data
	})
}

// 获取凭证数据
export const getLinkCheck = (data = {}) => {
	return request({
		url: "link-check-v2/",
		method: "get",
		params: data
	})
}
