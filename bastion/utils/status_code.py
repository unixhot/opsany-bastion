# -*- coding: utf-8 -*-
"""
Copyright © 2012-2020 OpsAny. All Rights Reserved.
""" # noqa

from enum import Enum


class ErrorStatusCode(Enum):
    # code = 400
    INVALID_REQUEST = (400, 40000, '不合法的请求')

    # code = 401
    INVALID_TOKEN = (401, 40100, '无效的token')
    USER_NOT_EXISTED_OR_WRONG_PASSWORD = (401, 40101, '用户名/密码错误')
    NOT_HAVE_USER_INFO = (401, 40102, '没有相应用户信息')

    # code = 404
    DATA_NOT_EXISTED = (404, 40400, '数据不存在')
    CREDENTIAL_GROUP_NOT_EXISTED = (404, 40401, '凭据分组不存在')
    CREDENTIAL_NOT_EXISTED = (404, 40402, '凭据不存在')
    HOST_GROUP_NOT_EXISTED = (404, 40403, '分组不存在')
    PARENT_HOST_GROUP_NOT_EXISTED = (404, 40404, '上级分组不存在')
    HOST_NOT_EXISTED = (404, 40405, '资源不存在')

    # code = 422
    CUSTOM_ERROR = (422, 42200, '')

    RECORD_HAS_EXISTED = (422, 42200, '记录已经存在')
    INPUT_ERROR = (422, 42201, '输入的内容有误')
    MUST_INPUT_MESSAGE = (422, 42202, '必须输入相关信息')
    KWARGS_ERROR = (422, 42203, '参数错误')
    CREDENTIAL_GROUP_DELETE_ERROR = (422, 42204, '当前分组下有关联凭据无法删除')
    HOST_GROUP_DELETE_ERROR = (422, 42205, '当前分组下有关联分组无法删除')
    HOST_GROUP_HAS_HOST_ERROR = (422, 42206, '当前分组下有关联资源无法删除')
    UNKNOWN_KWARGS_ERROR = (422, 42207, '出现未知的参数')
    DELETE_ERROR = (422, 42208, '删除失败')
    HANDLE_ERROR = (422, 42209, '操作失败')
    UPLOAD_ERROR = (422, 42210, '上传失败')
    PARAMS_ERROR = (422, 42233, '参数不合法')

    SERVER_ERROR = (422, 42222, '服务器开小差了，请您稍后再试或联系开发人员')


def error(error_info=ErrorStatusCode.INVALID_REQUEST, errors=None, custom_message=None):
    http_code, error_code, error_msg = error_info.value
    params = {
        'code': http_code,
        'message': error_msg,
        'errcode': error_code,
    }
    if errors:
        params['errors'] = errors
    if custom_message:
        params['message'] = custom_message
    return params


class SuccessStatusCode(Enum):
    # code = 200
    # 测试使用
    TEST_SUCCESS = (200, 20000, '服务器连接成功')
    OPERATION_SUCCESS = (200, 20001, '操作成功')
    # 模型组部分 04 - 07
    MESSAGE_CREATE_SUCCESS = (200, 20004, '相关信息创建成功')
    MESSAGE_GET_SUCCESS = (200, 20005, '相关信息信息获取成功')
    MESSAGE_DELETE_SUCCESS = (200, 20006, '相关信息删除成功')
    MESSAGE_UPDATE_SUCCESS = (200, 20007, '相关信息更新成功')
    MENU_GET_SUCCESS = (200, 20023, '获得菜单列表成功')
    UPLOAD_SUCCESS = (200, 20024, '文件上传成功')


def success(success_info=SuccessStatusCode.TEST_SUCCESS, data=None, custom_message=None):
    http_code, success_code, success_msg = success_info.value
    params = {
        'code': http_code,
        'successcode': success_code,
        'message': success_msg,
        'data': data,
    }
    if custom_message:
        params['message'] = custom_message
    return params
