import request from '@/utils/request';

/**
 * @deprecated  用户信息相关
 * @param {data} Object
 * @returns Promise
 */
//获取用户信息
export const getUserInfo = (data = {}) => {
	return request({
		url: "user-info/",
		method: "get",
		params: data
	})
}


/**
 * @deprecated  上传头像
 * @param {data} Object
 * @returns Promise
 */
//上传图标
export const uploadHeadImg = (data = {}) => {
	return request({
		url: "user-icon/",
		method: "post",
		data
	})
}

//获取所有用户列表
export const getUserList = (data = {}) => {
	return request({
		url: "user/",
		method: "get",
		params: data
	})
}

//获取所有用户组列表
export const getUserGroupList = (data = {}) => {
	return request({
		url: "group/",
		method: "get",
		params: data
	})
}
