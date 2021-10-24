import request from '@/utils/request';
const url = 'bk-user-admin/'

//获取用户列表
export const getUserAdmin = (data = {}) => {
	return request({
		url,
		method: "get",
		params: data
	})
}

//删除某个用户
export const delUserAdmin = (data = {}) => {
	return request({
		url,
		method: "delete",
		data
	})
}

//导入用户
export const addUserAdmin = (data = {}) => {
	return request({
		url,
		method: "post",
		data
	})
}

