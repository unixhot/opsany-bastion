import request from '@/utils/request'
const url = 'command/' //命令
export const getCommand = (data = {}) => {
	return request({
		url,
		method: "get",
		params: data
	})
}
export const addCommand = (data = {}) => {
	return request({
		url,
		method: "post",
		data
	})
}
export const editCommand = (data = {}) => {
	return request({
		url,
		method: "put",
		data
	})
}
export const delCommand = (data = {}) => {
	return request({
		url,
		method: "delete",
		data
	})
}
