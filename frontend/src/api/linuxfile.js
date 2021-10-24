import request from '@/utils/request'
import config from '@/config/defaultSettings'
import { stringifyUrl } from '@/utils/util'
const url = 'linux-file/'
export const getLinuxFileInfo = (data = {}) => {
	return request({
		url,
		method: "get",
		params: data
	})
}
export const downLoadFile = (data = {}) => {
	return config.baseUrl + url + stringifyUrl(data)
}
export const uploadLinuxFile = (data = {}) => {
	return request({
		url,
		method: "post",
		data
	})
}
export const delLinuxFile = (data = {}) => {
	return request({
		url,
		method: "delete",
		data
	})
}
