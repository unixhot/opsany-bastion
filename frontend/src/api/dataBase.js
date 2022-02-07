import request from '@/utils/request'
// 获取数据库数据
export const getDataBase = (data = {}) => {
    return request({
        url: "resource/database/",
        method: "get",
        params: data
    })
}

// 新建数据库
export const addDataBase = (data = {}) => {
    return request({
        url: "resource/database/",
        method: "post",
        data
    })
}

// 编辑数据库
export const editDataBase = (data = {}) => {
    return request({
        url: "resource/database/",
        method: "put",
        data
    })
}
// 删除数据库
export const delDataBase = (data = {}) => {
    return request({
        url: "resource/database/",
        method: "delete",
        data
    })
}

// 获取数据库分组数据
export const getDataBaseGroup = (data = {}) => {
    return request({
        url: "group/database/",
        method: "get",
        params: data
    })
}

// 获取数据库分组数据
export const addDataBaseGroup = (data = {}) => {
    return request({
        url: "group/database/",
        method: "post",
        data
    })
}

// 修改数据库分组
export const editDataBaseGroup = (data = {}) => {
    return request({
        url: "group/database/",
        method: "put",
        data
    })
}
// 获取用户数据库数据
export const getUserDataBase = (data = {}) => {
    return request({
        url: "auth/database/",
        method: "get",
        params: data
    })
}
// 删除数据库分组
export const delDataBaseGroup = (data = {}) => {
    return request({
        url: "group/database/",
        method: "delete",
        data
    })
}