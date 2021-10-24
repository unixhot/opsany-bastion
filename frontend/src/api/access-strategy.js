import request from '@/utils/request'
const url = 'access-strategy-v2/' //访问策略
export const getAccessStrategy = (data = {}) => {
	return request({
		url,
		method: "get",
		params: data
	})
}
export const addAccessStrategy = (data = {}) => {
	return request({
		url,
		method: "post",
		data
	})
}
export const editAccessStrategy = (data = {}) => {
	return request({
		url,
		method: "put",
		data
	})
}
export const delAccessStrategy = (data = {}) => {
	return request({
		url,
		method: "delete",
		data
	})
}

export const editAccessStrategyStatus = (data = {}) => {
	return request({
		url: 'strategy-status/',
		method: "put",
		data
	})
}