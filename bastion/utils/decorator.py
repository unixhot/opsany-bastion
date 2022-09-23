# -*- coding: utf-8 -*-
import requests
import json
from django.db import transaction
from bastion.models import UserInfo, UserGroupModel, UserGroupRelationshipModel
from bastion.utils.esb_api import EsbApi
from config import APP_CODE, BK_COMPONENT_API_URL, SECRET_KEY


def user_sync(func):
    def wrapped_function(obj, request, **kwargs):
        all_user_list = get_all_users(request)

        """
        phone username email ch_name role
        """
        temp_user_list = []
        for each_user in all_user_list:

            used_field = {}
            used_field["phone"] = each_user.get("phone")
            used_field["username"] = each_user.get("bk_username")
            used_field["email"] = each_user.get("email")
            used_field["ch_name"] = each_user.get("chname")
            used_field["role"] = each_user.get("bk_role")

            if not UserInfo.objects.filter(username=each_user["bk_username"]).count():
                obj_user = UserInfo.objects.create(**used_field)
            else:
                obj_user = UserInfo.objects.select_for_update().filter(username=each_user["bk_username"])
                with transaction.atomic():
                    obj_user.update(**used_field)
            temp_user_list.append(used_field["username"])

        local_all_users = UserInfo.objects.all()
        deleted_user_list = []
        for each in local_all_users:
            if each.username not in temp_user_list:
                deleted_user_list.append(each.username)
        UserInfo.objects.filter(username__in=deleted_user_list).delete()
        return func(obj, request, **kwargs)

    return wrapped_function


def user_group_sync(func):
    def wrapped_function(obj, request, **kwargs):
        sync_user_and_group(request)
        return func(obj, request, **kwargs)

    return wrapped_function


def get_all_users(request):
    host = BK_COMPONENT_API_URL
    bk_token = request.COOKIES.get('bk_token')
    # self.bk_token = "9lDBNOxzXjqJ5BH3QpfxcA2HG7eAjfDkmVivxaHtWpA"
    headers = {"Accept": "application/json"}
    params = {
        "bk_app_code": APP_CODE,
        "bk_app_secret": SECRET_KEY,
        "bk_token": bk_token,
    }
    url = "/api/c/compapi/v2/bk_login/get_all_users/"
    res = requests.get(host + url, params=params, headers=headers, verify=False)
    user_list = json.loads(res.content)["data"]
    return user_list


def sync_user_and_group(request):
    bk_token = request.COOKIES.get('bk_token')
    data = EsbApi(bk_token).get_user_group_sync()
    user_list = data.get("user_list", [])
    if user_list:
        sync_user(user_list)
    group_list = data.get("group_list", [])
    if group_list:
        sync_user_group(group_list)
    return True


def sync_user(user_list):
    temp_user_list = list()
    for user_dict in user_list:
        username = user_dict.get("username")
        used_field = {
            "phone": user_dict.get("phone"),
            "username": username,
            "email": user_dict.get("email"),
            "ch_name": user_dict.get("chname"),
            "role": user_dict.get("bk_role"),
        }
        if not UserInfo.objects.filter(username=username).count():
            obj_user = UserInfo.objects.create(**used_field)
        else:
            obj_user = UserInfo.objects.select_for_update().filter(username=username)
            obj_user.update(**used_field)
        temp_user_list.append(username)

    local_all_users = UserInfo.objects.all()
    deleted_user_list = []
    for each in local_all_users:
        if each.username not in temp_user_list:
            deleted_user_list.append(each.username)
    UserInfo.objects.filter(username__in=deleted_user_list).delete()


def sync_user_group(group_list):
    new_group_list = list()
    new_user_group_relationship_list = list()
    for group in group_list:
        group_name = group.get("group_name")
        group_dic = {"name": group_name, "description": group.get("description")}
        user_group_query = UserGroupModel.fetch_one(name=group_name)
        if user_group_query:
            user_group_query.update(**group_dic)
        else:
            user_group_query = UserGroupModel.create(**group_dic)
        new_group_list.append(group_name)
        group_user_list = group.get("user_list", [])
        if group_user_list:
            for user_info in group_user_list:
                username = user_info.get("username")
                user_info_query = UserInfo.fetch_one(username=username)
                if user_info_query:
                    user_dic = {"user": user_info_query, "user_group": user_group_query}
                    relationship = UserGroupRelationshipModel.fetch_one(**user_dic)

                    if not relationship:
                        relationship = UserGroupRelationshipModel.create(**user_dic)
                        print("relationship", relationship)
                    new_user_group_relationship_list.append(relationship.id)
    local_user_group_queryset = UserGroupModel.fetch_all()
    local_user_group_rel_queryset = UserGroupRelationshipModel.fetch_all()
    for local_user_group in local_user_group_queryset:
        if local_user_group.name not in new_group_list:
            local_user_group.delete()
    for local_user_group_rel in local_user_group_rel_queryset:
        if local_user_group_rel.id not in new_user_group_relationship_list:
            local_user_group_rel.delete()
