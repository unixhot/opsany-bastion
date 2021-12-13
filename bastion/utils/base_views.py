# -*- coding: utf-8 -*-
"""
Copyright © 2012-2020 OpsAny. All Rights Reserved.
"""  # noqa
from django.http import JsonResponse
from django.views import View
import json

from bastion.models import HostModel, SessionLogModel, StrategyAccessModel, StrategyCommandModel, CredentialModel, \
    UserInfo, UserGroupModel, UserGroupRelationshipModel
from bastion.component.common import GetUserInfo
from bastion.utils.esb_api import EsbApi
from bastion.utils.status_code import success, error, SuccessStatusCode, ErrorStatusCode
from bastion.utils.menu_json import admin, user


class BaseMenuStrategyCtrl(View):

    def get(self, request):
        """
        获取当前平台使用者的菜单列表
        """
        token = request.COOKIES.get("bk_token")
        esb_obj = EsbApi(token)
        res_data = esb_obj.get_user_info()
        self.create_or_update_current_user(res_data)
        if res_data.get("role") == 1:
            return JsonResponse(admin)
        return JsonResponse(user)
        # if res_data:
        # 创建/更新当前用户信息
        # self.create_or_update_current_user(esb_obj)
        # 更新已经导入的用户信息/关联组
        # self.update_all_import_user_group_info(esb_obj)

    def create_or_update_current_user(self, res_data):
        if res_data:
            username = res_data.pop("username", "")
            current_user = UserInfo.fetch_one(username=username)
            if current_user:
                current_user.update(**{
                    "phone": res_data.get("phone"),
                    "email": res_data.get("email"),
                    "ch_name": res_data.get("ch_name"),
                    "role": res_data.get("role")
                })
            else:
                UserInfo.create(**{
                    "username": username,
                    "phone": res_data.get("phone"),
                    "email": res_data.get("email"),
                    "ch_name": res_data.get("ch_name"),
                    "role": res_data.get("role")
                })

    # def update_all_import_user_group_info(self, esb_obj):
    #     res = esb_obj.get_user_group_sync()
    #     user_query_set = UserInfo.fetch_all()
    #     # 更新用户信息
    #     user_list = res.get("user_list")
    #     group_list = res.get("group_list")
    #     username_list = [user.get("username") for user in user_list]
    #     for user_query in user_query_set:
    #         # 处理已经从RBAC中删除的用户
    #         if user_query.username not in username_list:
    #             user_query.delete()
    #         # 更新已有用户的用户信息
    #         for user in user_list:
    #             if user_query.username == user.get("username"):
    #                 user_query.update(**{
    #                     "role": user.get("bk_role"),
    #                     "email": user.get("email"),
    #                     "ch_name": user.get("chname"),
    #                     "phone": user.get("phone")
    #                 })
    #         # 更新用户所在组关系
    #         current_user_rel = UserGroupRelationshipModel.fetch_all(user=user_query)
    #         user_group_rel_id = []
    #         for group in group_list:
    #             for group_user in group.get("user_list", []):
    #                 if group_user.get("username") == user_query.username:
    #                     group_query, _ = UserGroupModel.objects.update_or_create(
    #                         rbac_group_id=group.get("id"),
    #                         defaults={"name": group.get("group_name"), "description": group.get("description")}
    #                     )
    #                     rel, _ = UserGroupRelationshipModel.objects.update_or_create(
    #                         user=user_query,
    #                         user_group=group_query
    #                     )
    #                     user_group_rel_id.append(rel.id)
    #         # 删除无用的关系
    #         for user_group_rel in current_user_rel:
    #             if user_group_rel.id not in user_group_rel_id:
    #                 user_group_rel.delete()
    #     # 删除已删除的用户组
    #     group_query_set = UserGroupModel.fetch_all()
    #     for group_query in group_query_set:
    #         delete_flag = True
    #         for group in group_list:
    #             if group.get("id") == group_query.rbac_group_id:
    #                 delete_flag = False
    #         if delete_flag:
    #             group_query.delete()
    #     # 删除无关联的用户组
    #     # for group_query in group_query_set:
    #     #     if not group_query.group_user.get_queryset():
    #     #         group_query.delete()


class GetUserInfoCtrl(View):

    def get(self, request):
        """
        获取当前用户信息
        """
        token = request.COOKIES.get("bk_token")
        bk_user = EsbApi(token).get_user_info_from_workbench_or_login()
        data = {
            "phone": bk_user.get("phone"),
            "username": bk_user.get("username"),
            "email": bk_user.get("email"),
            "ch_name": bk_user.get("ch_name"),
            "role": bk_user.get("role")
        }
        return JsonResponse(success(SuccessStatusCode.MESSAGE_GET_SUCCESS, data))


class ReadAllMessageView(View):
    """
    全部已读
    """

    def get(self, request):
        bk_token = request.COOKIES.get("bk_token")
        EsbApi(bk_token).read_all_message()
        return JsonResponse(success(SuccessStatusCode.OPERATION_SUCCESS))


class GetNavCollectionView(View):
    """
    获取用户搜藏信息
    """

    def get(self, request):
        token = request.COOKIES.get("bk_token")
        end_data = EsbApi(token).get_nav_and_collection()
        return JsonResponse(success(SuccessStatusCode.MESSAGE_GET_SUCCESS, end_data))


class CollectionNavView(View):
    """
    用户搜藏
    """

    def post(self, request):
        token = request.COOKIES.get("bk_token")
        data = json.loads(request.body)
        nav_id = data.get("nav_id")
        end_data = EsbApi(token).collection_nav(nav_id)
        if isinstance(end_data, dict):
            successcode = end_data.pop("api_code")
            return JsonResponse({"code": 200, "successcode": successcode, "message": end_data.get("message"),
                                 "data": end_data.get("data")
                                 })
        else:
            return JsonResponse(error(ErrorStatusCode.INVALID_TOKEN))


class GetUserMessageView(View):
    """
    获取用户站内信
    """

    def get(self, request):
        kwargs = request.GET.dict()
        page = int(kwargs.pop("current", 1))
        per_page = int(kwargs.pop("pageSize", 10))
        token = request.COOKIES.get("bk_token")
        data = EsbApi(token).get_user_message_info(page, per_page)
        # sync_user_and_group(request)
        return JsonResponse(success(SuccessStatusCode.MESSAGE_GET_SUCCESS, data))


class HomePageView(View):
    def get(self, request):
        user_query = GetUserInfo().get_user_info(request)
        if not user_query:
            return JsonResponse(error(ErrorStatusCode.INPUT_ERROR, custom_message="用户不存在"))
        if user_query.role != 1:
            host_count = len(user_query.get_user_host_queryset_v2())
            session_finished_count = SessionLogModel.fetch_all(is_finished=True, user=user_query.username).count()
            session_unfinished_count = SessionLogModel.fetch_all(is_finished=False, user=user_query.username).count()
            strategy_access_count = len(user_query.get_user_strategy_access_queryset())
            strategy_command_count = len(user_query.get_strategy_command_queryset())
            credential_password_count, credential_ssh_count = 0, 0
            for host_credential in user_query.get_auth_host_credential_queryset():
                if host_credential.credential.credential_type == "ssh_key":
                    credential_ssh_count += 1
                else:
                    credential_password_count += 1
            host_id_list = [host.id for host in user_query.get_user_host_queryset_v2()]
            protocol_type = HostModel.PROTOCOL_TYPE[:2]
            host = dict()
            for type in protocol_type:
                host[type[0]] = HostModel.fetch_all(protocol_type=type[0], id__in=host_id_list).count()
        else:
            host_count = HostModel.fetch_all().count()
            session_finished_count = SessionLogModel.fetch_all(is_finished=True).count()
            session_unfinished_count = SessionLogModel.fetch_all(is_finished=False).count()
            strategy_access_count = StrategyAccessModel.fetch_all().count()
            strategy_command_count = StrategyCommandModel.fetch_all().count()
            credential_password_count = CredentialModel.fetch_all(
                credential_type=CredentialModel.CREDENTIAL_PASSWORD).count()
            credential_ssh_count = CredentialModel.fetch_all(credential_type=CredentialModel.CREDENTIAL_SSH_KEY).count()

            protocol_type = HostModel.PROTOCOL_TYPE[:2]
            host = dict()
            for type in protocol_type:
                host[type[0]] = HostModel.fetch_all(protocol_type=type[0]).count()

        dic = {
            "host_count": host_count,
            "session_count": session_finished_count + session_unfinished_count,
            "session_finished_count": session_finished_count,
            "session_unfinished_count": session_unfinished_count,
            "strategy_access_count": strategy_access_count,
            "strategy_command_count": strategy_command_count,
            "credential_password_count": credential_password_count,
            "credential_ssh_count": credential_ssh_count,
            "resource": {
                "host": host,
                # "sql":{
                #     "mysql": 1,
                #     "mongo": 3,
                #     "redis": 4
                # }
            },
            "role": user_query.role
        }
        return JsonResponse(success(SuccessStatusCode.MESSAGE_GET_SUCCESS, dic))


class GetAgentView(View):
    def get(self, request):
        """
        从资源平台获取节点
        """
        bk_token = request.COOKIES.get("bk_token")
        search_type = request.GET.get("search_type")
        search_data = request.GET.get("search_data")
        end_data = self.cache_cmdb_host(bk_token, search_type, search_data)
        return JsonResponse(success(SuccessStatusCode.MESSAGE_GET_SUCCESS, end_data))

    def cache_cmdb_host(self, bk_token, search_type, search_data):
        cmdb_data = EsbApi(bk_token).get_all_host(search_type=search_type, search_data=search_data) or []
        new_data = []
        for i in cmdb_data:
            model_code = i.get("model_code")
            name = model_code + "_name"
            public_ip = model_code + "_PUBLIC_IP"
            internal_ip = model_code + "_INTERNAL_IP"
            system_type = model_code + "_OS"
            show_name = model_code + "_VISIBLE_NAME"
            dic = {
                "opt_os": i.get("data").get(system_type),
                "show_name": i.get("data").get(show_name),
                "name": i.get("data").get(name),
                "ip1": i.get("data").get(public_ip),
                "ip2": i.get("data").get(internal_ip),
                "host_type": model_code,
                "ip1_type": "外",
                "ip2_type": "内",
                "add_type": "从资源平台导入"
            }
            if not HostModel.fetch_one(host_name_code=i.get("data").get(name)):
                new_data.append(dic)
        return new_data


class UserAdminView(View):
    def get(self, request):
        data = request.GET.dict()
        esb = EsbApi(request.COOKIES.get("bk_token"))
        self.update_all_import_user_group_info(esb)
        if data.get("data_type", "") == "list":         # 获取列表
            return self.get_list(request)
        if data.get("data_type", "") == "import":       # 获取导入列表
            return self.get_import_list(request)
        return JsonResponse(error(ErrorStatusCode.INPUT_ERROR, custom_message="请输入正确的内容"))

    def get_list(self, request):
        data = request.GET.dict()
        page = int(data.get("current", 1))
        per_page = int(data.get("pageSize", 10))
        search_type = data.get("search_type", "")
        search_data = data.get("search_data", None)
        filter_dict = {}
        if search_data and search_type:
            filter_dict[search_type + "__contains"] = search_data
        query_set, total = UserInfo.pagination(page, per_page, "-create_time", **filter_dict)
        end_data = {
            "current": page,
            "pageSize": per_page,
            "total": total,
            "data": [query.to_dict() for query in query_set]
        }
        return JsonResponse(success(SuccessStatusCode.MESSAGE_GET_SUCCESS, end_data))

    def handle_department_data(self, data):
        """
        处理数据结构，过滤用户信息
        """
        end_data = {}
        return end_data

    def get_import_list(self, request):
        token = request.COOKIES.get("bk_token")
        esb = EsbApi(token)
        rbac_data = esb.get_department_user_tree()
        bk_data = esb.get_all_users()
        # 用于处理层次问题，上层中可访问到下层内容
        self.handle_rbac_user_list(rbac_data)
        # 用于填充最外层用户不全问题
        self.handle_bk_user_list(rbac_data, bk_data)
        return JsonResponse(success(SuccessStatusCode.MESSAGE_GET_SUCCESS, rbac_data))

    def handle_import_user(self, user_list):
        end_data = []
        for user in user_list:
            if not UserInfo.fetch_one(username=user.get("username")):
                end_data.append(user)
        return end_data

    def handle_rbac_user_list(self, rbac_data):
        user_list = rbac_data.get("user_list")
        children = rbac_data.get("children")
        if children:
            for _children in children:
                _user_list = self.handle_rbac_user_list(_children)
                user_list.extend(_user_list)
            user_list = self.handle_import_user(user_list)
            rbac_data["user_list"] = user_list
            return user_list
        else:
            return self.handle_import_user(user_list)

    def handle_bk_user_list(self, rbac_data, bk_data):
        user_list = rbac_data.get("user_list")
        cache_user_list = [user.get("username") for user in user_list]
        for user in bk_data:
            if user.get("bk_username") not in cache_user_list:
                user_list.append({
                    'username': user.get("bk_username"),
                    'description': None,
                    'email': user.get("email"),
                    'phone': user.get("phone"),
                    'bk_role': user.get("bk_role"),
                    'chname': user.get("chname")
                })
        rbac_data["user_list"] = self.handle_import_user(user_list)

    def post(self, request):
        """
        {
            "user_list": [username1, username2, username3]
        }
        """
        data = json.loads(request.body)
        user_list = data.get("user_list")
        token = request.COOKIES.get("bk_token")
        esb = EsbApi(token)
        rbac_data = esb.get_user_group_sync()
        rbac_user_list = rbac_data.get("user_list")
        group_list = rbac_data.get("group_list")
        for username in user_list:
            self.create_user_info(username, rbac_user_list, group_list)
        return JsonResponse(success(SuccessStatusCode.OPERATION_SUCCESS))

    def create_user_info(self, username, rbac_user_list, group_list):
        user_object = None
        # 创建该用户
        for user in rbac_user_list:
            if user.get("username", "") == username:
                current_user = UserInfo.fetch_one(username=username)
                if current_user:
                    current_user.update(**{
                        "phone": user.get("phone"),
                        "email": user.get("email"),
                        "ch_name": user.get("chname"),
                        "role": user.get("bk_role")
                    })
                else:
                    UserInfo.create(**{
                        "username": username,
                        "phone": user.get("phone"),
                        "email": user.get("email"),
                        "ch_name": user.get("chname"),
                        "role": user.get("bk_role")
                    })
                break
        if user_object:
            # 获取该用户所在组
            for group in group_list:
                for group_user in group.get("user_list", []):
                    if group_user.get("username") == username:
                        group_query, _ = UserGroupModel.objects.update_or_create(
                            rbac_group_id=group.get("id"),
                            defaults={"name": group.get("group_name"), "description": group.get("description")}
                        )
                        UserGroupRelationshipModel.objects.get_or_create(
                            user=user_object,
                            user_group=group_query
                        )
            return True
        return False

    def delete(self, request):
        """
        {
            "user_list": [username1, username2, username3]
        }
        """
        data = json.loads(request.body)
        user_list = data.get("user_list")
        for username in user_list:
            user = UserInfo.fetch_one(username=username)
            if user:
                user.delete()
        return JsonResponse(success(SuccessStatusCode.MESSAGE_DELETE_SUCCESS))

    def update_all_import_user_group_info(self, esb_obj):
        res = esb_obj.get_user_group_sync()
        user_query_set = UserInfo.fetch_all()
        # 更新用户信息
        user_list = res.get("user_list")
        group_list = res.get("group_list")
        username_list = [user.get("username") for user in user_list]
        for user_query in user_query_set:
            # 处理已经从RBAC中删除的用户
            if user_query.username not in username_list:
                user_query.delete()
            # 更新已有用户的用户信息
            for user in user_list:
                if user_query.username == user.get("username"):
                    user_query.update(**{
                        "role": user.get("bk_role"),
                        "email": user.get("email"),
                        "ch_name": user.get("chname"),
                        "phone": user.get("phone")
                    })
            # 更新用户所在组关系
            current_user_rel = UserGroupRelationshipModel.fetch_all(user=user_query)
            user_group_rel_id = []
            for group in group_list:
                for group_user in group.get("user_list", []):
                    if group_user.get("username") == user_query.username:
                        group_query, _ = UserGroupModel.objects.update_or_create(
                            rbac_group_id=group.get("id"),
                            defaults={"name": group.get("group_name"), "description": group.get("description")}
                        )
                        rel, _ = UserGroupRelationshipModel.objects.update_or_create(
                            user=user_query,
                            user_group=group_query
                        )
                        user_group_rel_id.append(rel.id)
            # 删除无用的关系
            for user_group_rel in current_user_rel:
                if user_group_rel.id not in user_group_rel_id:
                    user_group_rel.delete()
        # 删除已删除的用户组
        group_query_set = UserGroupModel.fetch_all()
        for group_query in group_query_set:
            delete_flag = True
            for group in group_list:
                if group.get("id") == group_query.rbac_group_id:
                    delete_flag = False
            if delete_flag:
                group_query.delete()
        for group_query in group_query_set:
            if not group_query.group_user.get_queryset():
                group_query.delete()


class UserGroupAdminView(View):
    def get(self, request):
        data = request.GET.dict()
        esb = EsbApi(request.COOKIES.get("bk_token"))
        self.update_all_import_user_group_info(esb)
        if data.get("data_type", "") == "list":         # 获取列表
            return self.get_list(request)
        if data.get("data_type", "") == "import":       # 获取导入列表
            return self.get_import_list(request)
        return JsonResponse(error(ErrorStatusCode.INPUT_ERROR, custom_message="请输入正确的内容"))

    def get_list(self, request):
        data = request.GET.dict()
        page = int(data.get("current", 1))
        per_page = int(data.get("pageSize", 10))
        search_type = data.get("search_type", "")
        search_data = data.get("search_data", None)
        filter_dict = {}
        if search_data and search_type:
            filter_dict[search_type + "__contains"] = search_data
        query_set, total = UserGroupModel.pagination(page, per_page, **filter_dict)
        end_data = {
            "current": page,
            "pageSize": per_page,
            "total": total,
            "data": [query.to_list_dict() for query in query_set]
        }
        return JsonResponse(success(SuccessStatusCode.MESSAGE_GET_SUCCESS, end_data))

    def get_import_list(self, request):
        token = request.COOKIES.get("bk_token")
        esb = EsbApi(token)
        rbac_data = esb.get_user_group_sync()
        res = self.handle_import_user_and_group(rbac_data)
        return JsonResponse(success(SuccessStatusCode.MESSAGE_GET_SUCCESS, res))

    def handle_import_user_and_group(self, rbac_data):
        user_list = rbac_data.get("user_list")
        user_dict = {}
        for user in user_list:
            user_dict[user.get("username")] = user
        group_list = rbac_data.get("group_list")
        group_data_list = []
        # 处理已经导入的用户
        for group in group_list:
            not_have_user_list = []
            for user in group.get("user_list", []):
                if user.get("username") and not UserInfo.fetch_one(username=user.get("username")):
                    not_have_user_list.append(user_dict.get(user.get("username")))
            if not_have_user_list:
                group["user_list"] = not_have_user_list
                group_data_list.append(group)
        return group_data_list

    def post(self, request):
        """
        {
            "group_id_list": []
        }
        """
        token = request.COOKIES.get("bk_token")
        esb = EsbApi(token)
        rbac_data = esb.get_user_group_sync()
        data = json.loads(request.body)
        group_id_list = data.get("group_id_list")
        if group_id_list:
            self.create_user_group(group_id_list, rbac_data)
        return JsonResponse(success(SuccessStatusCode.OPERATION_SUCCESS))

    def create_user_group(self, group_id_list, rbac_data):
        user_list = rbac_data.get("user_list")
        user_dict = {}
        for user in user_list:
            user_dict[user.get("username")] = user
        group_list = rbac_data.get("group_list")
        for group_id in group_id_list:
            for _group in group_list:
                if str(_group.get("id")) == str(group_id):
                    group_query, _ = UserGroupModel.objects.update_or_create(
                        rbac_group_id=group_id,
                        defaults={
                            "name": _group.get("group_name"),
                            "description": _group.get("description")
                        }
                    )
                    this_group_user_list = [_user.get("username") for _user in _group.get("user_list", [])]
                    # 创建对应用户
                    for username in this_group_user_list:
                        user_data = user_dict.get(username)
                        user_data.pop("username", "")
                        current_user = UserInfo.fetch_one(username=username)
                        if current_user:
                            current_user.update(**{
                                "phone": user_data.get("phone"),
                                "email": user_data.get("email"),
                                "ch_name": user_data.get("ch_name"),
                                "role": user_data.get("bk_role")
                            })
                        else:
                            current_user = UserInfo.create(**{
                                "username": username,
                                "phone": user_data.get("phone"),
                                "email": user_data.get("email"),
                                "ch_name": user_data.get("ch_name"),
                                "role": user_data.get("bk_role")
                            })
                        UserGroupRelationshipModel.objects.get_or_create(user=current_user, user_group=group_query)

    def delete(self, request):
        """
        {
            "group_id_list": []
        }
        """
        data = json.loads(request.body)
        group_id_list = data.get("group_id_list")
        for rbac_group_id in group_id_list:
            group = UserGroupModel.fetch_one(rbac_group_id=rbac_group_id)
            if group:
                group.delete()
        return JsonResponse(success(SuccessStatusCode.MESSAGE_DELETE_SUCCESS))

    def update_all_import_user_group_info(self, esb_obj):
        res = esb_obj.get_user_group_sync()
        user_query_set = UserInfo.fetch_all()
        # 更新用户信息
        user_list = res.get("user_list")
        group_list = res.get("group_list")
        username_list = [user.get("username") for user in user_list]
        for user_query in user_query_set:
            # 处理已经从RBAC中删除的用户
            if user_query.username not in username_list:
                user_query.delete()
            # 更新已有用户的用户信息
            for user in user_list:
                if user_query.username == user.get("username"):
                    user_query.update(**{
                        "role": user.get("bk_role"),
                        "email": user.get("email"),
                        "ch_name": user.get("chname"),
                        "phone": user.get("phone")
                    })
            # 更新用户所在组关系
            current_user_rel = UserGroupRelationshipModel.fetch_all(user=user_query)
            user_group_rel_id = []
            for group in group_list:
                for group_user in group.get("user_list", []):
                    if group_user.get("username") == user_query.username:
                        group_query, _ = UserGroupModel.objects.update_or_create(
                            rbac_group_id=group.get("id"),
                            defaults={"name": group.get("group_name"), "description": group.get("description")}
                        )
                        rel, _ = UserGroupRelationshipModel.objects.update_or_create(
                            user=user_query,
                            user_group=group_query
                        )
                        user_group_rel_id.append(rel.id)
            # 删除无用的关系
            for user_group_rel in current_user_rel:
                if user_group_rel.id not in user_group_rel_id:
                    user_group_rel.delete()
        # 删除已删除的用户组
        group_query_set = UserGroupModel.fetch_all()
        for group_query in group_query_set:
            delete_flag = True
            for group in group_list:
                if group.get("id") == group_query.rbac_group_id:
                    delete_flag = False
            if delete_flag:
                group_query.delete()
        # 删除无关联的用户组
        # for group_query in group_query_set:
        #     if not group_query.group_user.get_queryset():
        #         group_query.delete()


class BkUserAdminView(View):
    def get(self, request):
        data = request.GET.dict()
        if data.get("data_type", "") == "list":         # 获取列表
            return self.get_list(request)
        if data.get("data_type", "") == "import":       # 获取导入列表
            return self.get_import_list(request)
        return JsonResponse(error(ErrorStatusCode.INPUT_ERROR, custom_message="请输入正确的内容"))

    def get_list(self, request):
        data = request.GET.dict()
        page = int(data.get("current", 1))
        per_page = int(data.get("pageSize", 10))
        search_type = data.get("search_type", "")
        search_data = data.get("search_data", None)
        filter_dict = {}
        if search_data and search_type:
            filter_dict[search_type + "__contains"] = search_data
        query_set, total = UserInfo.pagination(page, per_page, "-create_time", **filter_dict)
        end_data = {
            "current": page,
            "pageSize": per_page,
            "total": total,
            "data": [query.to_dict() for query in query_set]
        }
        return JsonResponse(success(SuccessStatusCode.MESSAGE_GET_SUCCESS, end_data))

    def get_import_list(self, request):
        data = request.GET.dict()
        esb = EsbApi(request.COOKIES.get("bk_token"))
        page = int(data.get("current", 1))
        per_page = int(data.get("pageSize", 10))
        search_type = data.get("search_type", "")
        search_data = data.get("search_data", None)
        if search_data and search_type:
            res = esb.list_users(page, per_page, search_type, search_data)
        else:
            res = esb.list_users(page, per_page, search_type, search_data)
        end_data = {
            "current": page,
            "pageSize": per_page,
            "total": res.get("count", 0),
            "data": self.handle_results(res.get("results", []))
        }
        return JsonResponse(success(SuccessStatusCode.MESSAGE_GET_SUCCESS, end_data))

    def handle_results(self, results):
        end_data = []
        for result in results:
            user = UserInfo.fetch_one(username=result.get("username"))
            if user:
                is_import = True
            else:
                is_import = False
            end_data.append({
                "username": result.get("username"),
                "ch_name": result.get("display_name"),
                "email": result.get("email"),
                "is_import": is_import,
                "role": result.get("role")
            })
        return end_data

    def post(self, request):
        data = json.loads(request.body)
        username = data.get("username")
        token = request.COOKIES.get("bk_token")
        esb = EsbApi(token)
        res = esb.retrieve_user(username)
        if res:
            user = UserInfo.fetch_one(username=res.get("username"))
            if not user:
                UserInfo.create(**{
                    "username": res.get("username"),
                    "ch_name": res.get("display_name"),
                    "email": res.get("email"),
                    "phone": res.get("telephone"),
                    "role": res.get("role")
                })
                return JsonResponse(success(SuccessStatusCode.OPERATION_SUCCESS))
        return JsonResponse(error(ErrorStatusCode.INPUT_ERROR))

    def delete(self, request):
        data = json.loads(request.body)
        user_list = data.get("user_list")
        for username in user_list:
            user = UserInfo.fetch_one(username=username)
            if user:
                user.delete()
        return JsonResponse(success(SuccessStatusCode.MESSAGE_DELETE_SUCCESS))


class BkUserGroupAdminView(View):
    def get(self, request):
        data = request.GET.dict()
        page = int(data.get("current", 1))
        per_page = int(data.get("pageSize", 10))
        search_type = data.get("search_type", "")
        search_data = data.get("search_data", None)
        filter_dict = {}
        if search_data and search_type:
            filter_dict[search_type + "__contains"] = search_data
        query_set, total = UserGroupModel.pagination(page, per_page, "-create_time", **filter_dict)
        end_data = {
            "current": page,
            "pageSize": per_page,
            "total": total,
            "data": [query.to_list_dict() for query in query_set]
        }
        return JsonResponse(success(SuccessStatusCode.MESSAGE_GET_SUCCESS, end_data))

    def post(self, request):
        data = json.loads(request.body)
        name = data.get("name")
        description = data.get("description")
        username_list = data.get("username_list", [])
        if UserGroupModel.fetch_one(name=name):
            return JsonResponse(error(ErrorStatusCode.INPUT_ERROR, custom_message="用户组名不能重复"))
        group = UserGroupModel.create(**{
            "name": name,
            "description": description,
        })
        for username in username_list:
            user = UserInfo.fetch_one(username=username)
            if user:
                UserGroupRelationshipModel.create(user=user, user_group=group)
        return JsonResponse(success(SuccessStatusCode.MESSAGE_CREATE_SUCCESS))

    def put(self, request):
        data = json.loads(request.body)
        id = data.get("id")
        name = data.get("name")
        description = data.get("description")
        username_list = data.get("username_list", [])
        group = UserGroupModel.fetch_one(id=id)
        other_group = UserGroupModel.objects.filter(name=name).exclude(id=id)
        if other_group:
            return JsonResponse(error(ErrorStatusCode.INPUT_ERROR, custom_message="用户组名不能重复"))
        if group:
            group = group.update(**{
                "name": name,
                "description": description,
            })
            rels = UserGroupRelationshipModel.fetch_all(user_group=group)
            for rel in rels:
                rel.delete()
            for username in username_list:
                user = UserInfo.fetch_one(username=username)
                if user:
                    UserGroupRelationshipModel.create(user=user, user_group=group)
            return JsonResponse(success(SuccessStatusCode.MESSAGE_UPDATE_SUCCESS))
        return JsonResponse(error(ErrorStatusCode.DATA_NOT_EXISTED))

    def delete(self, request):
        data = json.loads(request.body)
        id = data.get("id")
        group = UserGroupModel.fetch_one(id=id)
        if group:
            group.delete()
            return JsonResponse(success(SuccessStatusCode.MESSAGE_DELETE_SUCCESS))
        return JsonResponse(error(ErrorStatusCode.DATA_NOT_EXISTED))