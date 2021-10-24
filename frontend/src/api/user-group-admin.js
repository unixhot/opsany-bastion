import request from '@/utils/request';
const url = 'bk-user-group-admin/'

//获取用户组列表
export const getUserGroupAdmin = (data = {}) => {
	return request({
		url,
		method: "get",
		params: data
	})
}

//删除某个用户组
export const delUserGroupAdmin = (data = {}) => {
	return request({
		url,
		method: "delete",
		data
	})
}

//新增用户组
export const addUserGroupAdmin = (data = {}) => {
	return request({
		url,
		method: "post",
		data
	})
}

//编辑用户组
export const editUserGroupAdmin = (data = {}) => {
	return request({
		url,
		method: "put",
		data
	})
}

