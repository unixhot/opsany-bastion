import { getMenuList } from '@/api/menu'
import { BasicLayout, BlankLayout, PageView, RouteView } from '@/layouts'
import { detailRouterMap } from '@/config/router.config'
import config from '@/config/defaultSettings'
const { expandMenu } = config
import Router from './index'
import store from '../store'
import { cloneDeep } from 'lodash'
// 前端路由表
const constantRouterComponents = {
	// 基础页面 layout 必须引入
	BasicLayout: BasicLayout,
	BlankLayout: BlankLayout,
	RouteView: RouteView,
	PageView: PageView,
	'403': () => import( /* webpackChunkName: "error" */ '@/views/exception/403'),
	'404': () => import( /* webpackChunkName: "error" */ '@/views/exception/404'),
	'500': () => import( /* webpackChunkName: "error" */ '@/views/exception/500'),

	'home': () => import('@/views/home/home.vue'), //概览
	'host': () => import('@/views/resources/host.vue'),//主机

	'password': () => import('@/views/voucher/password.vue'),//密码凭证
	'ssh': () => import('@/views/voucher/ssh.vue'),//密码凭证
	'voucherGrouping': () => import('@/views/voucher/group.vue'),//分组

	'visitPolicy': () => import('@/views/accessPolicy/visitPolicy'), //访问策略
	'commandPolicy': () => import('@/views/accessPolicy/commandPolicy'),//命令策略

	'online': () => import('@/views/auditManagement/online'),//在线会话
	'historical': () => import('@/views/auditManagement/historical'),//历史会话
	'auditHistory': () => import('@/views/auditManagement/auditHistory'),//审计历史
	'operationLog': () => import('@/views/auditManagement/operationLog'),//系统日志

	'authorizationHost': () => import('@/views/safe/authorizationHost.vue'),//主机

	'userManage': () => import('@/views/setting/userManage'), //用户管理
}


//对应的图标
const constRouterIcon = {
	'home': "home", //主页

	'host': "laptop",//主机资源
	'application': "hdd",//应用资源

	'password': "lock",//密码凭证
	'ssh': "key",//SSH凭证
	'voucherGrouping': "apartment",//凭证分组

	'visitPolicy': "select",//访问策略
	'commandPolicy': "code",//命令策略

	'online': "hourglass",//命令策略
	'historical': "history",//命令策略
	'auditHistory': "read",//命令策略
	'operationLog': "file-search",//命令策略

	'authorizationHost': "laptop",//主机资源
	'userManage': 'user',//用户管理
}

// 前端未找到页面路由（固定不用改）
const notFoundRouter = {
	path: '*',
	redirect: '/404',
	hidden: true
}

// 根级菜单
const rootRouter = {
	path: '/',
	name: "index",
	component: 'BasicLayout',
	meta: {
		title: '我买云',
	},
	redirect: '/',
	children: []
}

/**
 * 动态生成菜单
 * @param token
 * @returns {Promise<Router>}
 */

const cleaning = (data, auth) => {
	if (data.children?.length) {
		data.children.map(item => {
			cleaning(item, auth)
		})
	} else {
		if (data.auth?.length) {
			data.auth.map(btn => {
				auth[btn.button_code] = true
			})
		}
	}
}
let authObj = {}

export const generatorDynamicRouter = (token) => {
	return new Promise((resolve, reject) => {
		getMenuList().then(res => {
			store.commit('setMenuList', res.data?.children || [])

			const asyncData = cloneDeep(res.data)
			if (asyncData && asyncData.licence_status) {
				Router.push({ path: "error", query: { state: asyncData.licence_status } })
			}
			if (asyncData && (JSON.stringify(asyncData) == '{}' || JSON.stringify(asyncData) == '[]')) {
				Router.push({ path: '403' })
			}
			const menuNav = []
			const resRouter = asyncData && asyncData.children || [];
			if (expandMenu) {
				if (asyncData && asyncData.children) {
					cleaning(asyncData, authObj)
				}
				store.dispatch('GenerateBtnAuth', authObj)
				rootRouter.children = expendMenu(resRouter)
				rootRouter.component = BasicLayout
				menuNav.push(...[rootRouter, notFoundRouter])
				setDetailRouter(menuNav)
				resolve(menuNav)
			} else {
				rootRouter.children = resRouter
				menuNav.push(rootRouter)
				const routers = generator(menuNav)
				routers.push(notFoundRouter)
				setDetailRouter(routers)
				resolve(routers)
			}
		}).catch(err => {
			reject(err)
		})
	})
}

/**
 * 将详情等页面加入到路由里
 *
 * @param routers
 * @returns {*}
 */
export const setDetailRouter = (routers) => {
	for (let item of routers) {
		if (item.path === '/' && item.name === 'index') {
			item.children = item.children && item.children.concat(detailRouterMap) || []
		}
	}
}

/**
 * 格式化树形结构数据 生成 vue-router 层级路由表
 *
 * @param routerMap
 * @param parent
 * @returns {*}
 */
export const generator = (routerMap, parent) => {
	return routerMap.map(item => {
		const { menu_address, menu_code, menu_name } = item
		const currentRouter = {
			path: menu_address,
			name: menu_code,
			component: constantRouterComponents[menu_code],
			meta: {
				title: menu_name,
				icon: constRouterIcon[menu_code] || undefined,
				target: menu_code == 'link' ? '_blank' : null
			}
		}

		if (item.menu_code && item.menu_code.indexOf("RouteView") != -1) {
			currentRouter.component = RouteView
		}

		//根路由
		if (item.component == 'BasicLayout') {
			currentRouter.component = BasicLayout
			currentRouter.redirect = '/home'
			currentRouter.path = '/'
			currentRouter.name = 'index'
			currentRouter.meta.title = '我买云'
		}

		if (item.children && item.children.length > 0) {
			currentRouter.children = generator(item.children, currentRouter)
		}
		return currentRouter
	})
}

/**
 * 格式化树形结构数据 当菜单不折叠时候的路由表
 * 
 * @param {Array} router 后端返回的路由表
 */
const expendMenu = (router) => {
	const routeMap = [];
	const mapRouter = (router) => {
		router.forEach(item => {
			const { menu_address, menu_code, menu_name } = item
			const isRouteView = item.menu_code && item.menu_code.indexOf("RouteView") != -1; //是否为父级菜单
			const currentRouter = {
				path: menu_address,
				name: menu_code,
				component: constantRouterComponents[menu_code],
				meta: {
					title: menu_name,
					icon: isRouteView ? undefined : constRouterIcon[menu_code] || undefined,
					target: menu_code == 'link' ? '_blank' : null
				}
			}
			if (item.menu_code && item.menu_code.indexOf("RouteView") != -1) {
				currentRouter.name = undefined
			}

			routeMap.push(currentRouter)
			if (item.children && item.children.length) {
				mapRouter(item.children)
				item.children = []
			}
		})
	}
	mapRouter(router)
	return routeMap
}