import request from '@/utils/request'
import config from '@/config/defaultSettings'
import { stringifyUrl } from '@/utils/util'
const url = 'windows-file/'
export const getWinFileInfo = (data = {}) => {
	return request({
		url,
		method: "get",
		params: data
	})
}
export const downLoadWinFile = (data = {}) => {
	return config.baseUrl + url + stringifyUrl(data)
}
export const uploadWinFile = (data = {}) => {
	return request({
		url,
		method: "post",
		data
	})
}
export const delWinFile = (data = {}) => {
	return request({
		url,
		method: "delete",
		data
	})
}
