import router from '@/router'
import { getPageAuth as getPageAuthApi } from '@/api/page-auth'

const replaceRouter = () => {
	router.push({ name: 'noAuth' })
}

export const getPageAuth = (vm, action_id = "") => {
	return new Promise((resolve, reject) => {
		setTimeout(() => {
			vm.$loading.show()
		}, 0);
		getPageAuthApi({ action_id }).then(res => {
			if (!res.data) replaceRouter()
			return resolve(res.data)
		}).catch(() => {
			replaceRouter()
			return resolve(false)
		}).finally(() => {
			setTimeout(() => {
				vm.$loading.hide()
			}, 0);
		})
	})
}