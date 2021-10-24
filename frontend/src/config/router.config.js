// eslint-disable-next-line
import { UserLayout, BasicLayout, BlankLayout, PageView } from '@/layouts'
import { bxAnaalyse } from '@/core/icons'

const RouteView = {
	name: 'RouteView',
	render: (h) => h('router-view')
}

/**
 * 菜单级别路由
 * @type { *[] }
 */
export const asyncRouterMap = [{
	path: '/',
	name: 'index',
	component: BasicLayout,
	meta: { title: 'menu.home' },
	redirect: '/home',
	children: [
		//     {
		//     path: '/home',
		//     name: 'home',
		//     component: () => import('@/views/home'),
		//     meta: { title: '概览', keepAlive: false, icon: "home" }
		// }, 
	]
},

]

/**
 * 基础路由
 * @type { *[] }
 */
export const constantRouterMap = [
	{
		path: "/console/remoteLinux",
		meta: { title: "Linux远程访问" },
		component: () => import('@/views/console/remoteLinux'),
		name: "remoteLinux",
		hidden: true,
	},
	{
		path: "/console/webWindows",
		meta: { title: "Windows远程访问" },
		component: () => import('@/views/console/webWindows'),
		name: "webWindows",
		hidden: true,
	},
	{
		path: "/console/console",
		meta: { title: "控制台" },
		component: () => import('@/views/console/console'),
		name: "console",
		hidden: true,
	},
	{
		path: '/404',
		component: () => import( /* webpackChunkName: "fail" */ '@/views/exception/404')
	},
	{
		path: '/403',
		component: () => import('@/views/exception/403')
	},
	{
		path: '/error',
		component: () => import('@/views/exception/error')
	}
]


/**
 * 不在菜单栏的路由 例：详情页路由
 * @type { *[] }
 */
export const detailRouterMap = [
	{
		path: "/voucher/password/passwordDetails",
		meta: { title: "凭证详情", parentRouteName: 'password' },
		component: () => import('@/views/voucher/passwordDetails.vue'),
		name: "passwordDetails",
		hidden: true
	},
	{
		path: "/voucher/ssh/sshDetails",
		meta: { title: "ssh详情", parentRouteName: 'ssh' },
		component: () => import('@/views/voucher/sshDetails.vue'),
		name: "sshDetails",
		hidden: true
	},
	{
		path: "/voucher/group/groupDetails",
		meta: { title: "分组详情", parentRouteName: 'voucherGrouping' },
		component: () => import('@/views/voucher/groupDetails.vue'),
		name: "groupDetails",
		hidden: true
	},
	{
		path: "/resources/host/hostDetails",
		meta: { title: "主机详情", parentRouteName: 'host' },
		component: () => import('@/views/resources/hostDetails.vue'),
		name: "hostDetails",
		hidden: true
	},
	{
		path: "/accessPolicy/visitPolicy/visitPolicyInfo",
		meta: { title: "访问策略详情", parentRouteName: 'visitPolicy' },
		component: () => import('@/views/accessPolicy/visitPolicy/visitPolicyInfo'),
		name: "visitPolicyInfo",
		hidden: true
	},
	{
		path: "/accessPolicy/commandPolicy/policyListInfo",
		meta: { title: "命令策略详情", parentRouteName: 'commandPolicy' },
		component: () => import('@/views/accessPolicy/commandPolicy/components/PolicyList/policyListInfo'),
		name: "policyListInfo",
		hidden: true
	},
	{
		path: "/auditManagement/historical/historicalDetails",
		meta: { title: "历史会话详情", parentRouteName: 'historical' },
		component: () => import('@/views/auditManagement/historicalDetails'),
		name: "historicalDetails",
		hidden: true
	},
	{
		path: '/noAuth',
		meta: { title: "暂无权限", },
		component: () => import('@/views/exception/noAuth'),
		name: "noAuth",
		hidden: true
	}
]