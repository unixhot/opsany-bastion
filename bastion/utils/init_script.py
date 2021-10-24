import os
import sys


def init_default_group():
    dic = {
        "id": 1,
        "name": "默认分组",
        "description": "默认分组",
        "create_time": "2008-08-08 10:10:10.888888",
        "update_time": "2008-08-08 10:10:10.888888"
    }

    obj = HostGroupModel.fetch_all(id=1)
    if obj:
        obj.update(**dic)
    else:
        HostGroupModel.create(**dic)
    print("res", obj)
    print(" [Success] {} init_default_group Running".format(str(datetime.datetime.now()).rsplit(".", 1)[0]))


if __name__ == '__main__':
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
    import datetime

    print(" [Success] {} init_script Running".format(str(datetime.datetime.now()).rsplit(".", 1)[0]))
    # os.environ["BK_ENV"] = os.getenv("BK_ENV", "production")
    # os.environ.setdefault("BK_ENV", "production")     # 生产环境解注改行
    # os.environ.setdefault("BK_ENV", "testing")        # 开发环境解注改行
    sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
    import django

    django.setup()

    from bastion.models import HostGroupModel

    init_default_group()
    print(" [Success] {} init_script Execution Complete".format(str(datetime.datetime.now()).rsplit(".", 1)[0]))
