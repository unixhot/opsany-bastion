from bastion.models import UserInfo
from bastion.utils.esb_api import EsbApi


class GetUserInfo:
    def get_user_info(self, request=None, bk_token=None):
        if not bk_token:
            bk_token = request.COOKIES.get("bk_token")
        esb_obj = EsbApi(bk_token)
        user_info = esb_obj.get_user_info()
        return UserInfo.fetch_one(username=user_info.get("username"))

    def get_user_role(self, request=None, bk_token=None):
        if not bk_token:
            bk_token = request.COOKIES.get("bk_token")
        esb_obj = EsbApi(bk_token)
        user_info = esb_obj.get_user_info()
        return user_info.get("role")


class GetModelData:
    def __init__(self, model):
        self.model = model

    def get_one_data(self, id):
        query = self.model.fetch_one(id=id)
        if not query:
            return False, "数据不存在"
        end_data = query.to_dict()
        return True, end_data

    def get_all_data(self, kwargs):
        search_type, search_data, _ = kwargs.pop("search_type", None), kwargs.pop("search_data", None), kwargs.pop(
            "total", None)
        if search_type and search_data:
            kwargs[search_type + "__contains"] = search_data
        credential_group_queryset = self.model.fetch_all(**kwargs)
        end_data = []
        if credential_group_queryset:
            for i in credential_group_queryset:
                end_data.append(i.to_dict())
        return True, end_data

    def get_paging_data(self, kwargs):
        search_type, search_data, _ = kwargs.pop("search_type", None), kwargs.pop("search_data", None), kwargs.pop(
            "total", None)
        if search_type and search_data:
            kwargs[search_type + "__contains"] = search_data
        try:
            current, pageSize = int(kwargs.pop("current")), int(kwargs.pop("pageSize"))
        except Exception:
            current, pageSize = 1, 10
        current_page, total = self.model.pagination(current, pageSize, **kwargs)
        end_data = [i.to_dict() for i in current_page]
        res_data = {
            "current": current,
            "pageSize": pageSize,
            "total": total,
            "data": end_data
        }
        return True, res_data
