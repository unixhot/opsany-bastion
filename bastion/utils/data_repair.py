import os
import sys


def data_repair():
    esb = EsbApi(access_token="opsany-esb-auth-token-9e8083137204")
    res = esb.get_user_group_sync()
    group_list = res.get("group_list")
    for group in group_list:
        group_query = UserGroupModel.fetch_one(name=group.get("group_name"))
        if group_query:
            group_query.update(**{"rbac_group_id": group.get("id")})


if __name__ == '__main__':
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
    import datetime
    print(" [Success] {} data_repair Running".format(str(datetime.datetime.now()).rsplit(".", 1)[0]))
    sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
    import django
    django.setup()
    from bastion.models import UserGroupModel
    from bastion.utils.esb_api import EsbApi
    data_repair()
    print(" [Success] {} data_repair Execution Complete".format(str(datetime.datetime.now()).rsplit(".", 1)[0]))
