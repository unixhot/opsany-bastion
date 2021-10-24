import request from '@/utils/request'
const url = 'command-strategy-v2/' //访问策略
export const getCommandStrategy = (data = {}) => {
	return request({
		url,
		method: "get",
		params: data
	})
}
export const addCommandStrategy = (data = {}) => {
	return request({
		url,
		method: "post",
		data
	})
}
export const editCommandStrategy = (data = {}) => {
	return request({
		url,
		method: "put",
		data
	})
}
export const delCommandStrategy = (data = {}) => {
	return request({
		url,
		method: "delete",
		data
	})
}
