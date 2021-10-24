import request from '@/utils/request'
// 获取凭证数据 --新版
// GET获取资源凭证
// ?data_type=ssh
// ?data_type=password
// ?data_type=group
// ?data_type=host&host_id=
export const getResourceCredential = (data = {}) => {
	return request({
		url: "resource-credential/",
		method: "get",
		params: data
	})
}
