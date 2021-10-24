import request from '@/utils/request'
const url = 'command-group/' //命令组
export const getCommandGroup = (data = {}) => {
	return request({
		url,
		method: "get",
		params: data
	})
}
export const addCommandGroup = (data = {}) => {
	return request({
		url,
		method: "post",
		data
	})
}
export const editCommandGroup = (data = {}) => {
	return request({
		url,
		method: "put",
		data
	})
}
export const delCommandGroup = (data = {}) => {
	return request({
		url,
		method: "delete",
		data
	})
}
