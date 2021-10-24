import axios from 'axios'
import store from '@/store'
import storage from 'store'
import notification from 'ant-design-vue/es/notification'
import message from 'ant-design-vue/es/message'
import { VueAxios } from './axios'
import { ACCESS_TOKEN } from '@/store/mutation-types'
import config from '@/config/defaultSettings'
import qs from 'qs'

axios.defaults.withCredentials = true; //让ajax携带cookie

const isProd = process.env.NODE_ENV === 'production'

const loginOut = (c_url) => {
    const baseurl = window.API_ROOT.split('/')[0]
    window.location.href = baseurl + `/login/?c_url=${c_url}`
}

// 创建 axios 实例
const request = axios.create({
    // API 请求的默认前缀
    baseURL: config.baseUrl,
    // timeout: 15000 // 请求超时时间
})

// 异常拦截处理器
const errorHandler = (error) => {
    if (error.response) {
        const data = error.response.data
        // 从 localstorage 获取 token
        const token = storage.get(ACCESS_TOKEN);
        notification.error({
            message: '错误',
            description: error.response.statusText
        })
    }
    return Promise.reject(error)
}

// request interceptor
request.interceptors.request.use(config => {
    if (config.method.toLowerCase() == 'get') {
        config.paramsSerializer = (params) => {
            return qs.stringify(params, { arrayFormat: 'repeat' })
        }
    }
    return config
}, errorHandler)

// response interceptor
request.interceptors.response.use((response) => {
    const { code, successcode, errcode, errors, status_code, status_info } = response.data;
    if (code == '200' || status_code == 0) {
        return response.data
    } else {
        if (errcode == '40100') {
            isProd && loginOut(errors);
        } else {
            message.warning({
                content: response.data.message || response.data.errors || status_info
            })
        }
        return Promise.reject('expectations error')
    }
}, errorHandler)

const installer = {
    vm: {},
    install(Vue) {
        Vue.use(VueAxios, request)
    }
}

export default request

export {
    installer as VueAxios,
    request as axios
}