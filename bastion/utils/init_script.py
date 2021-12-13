from bastion.models import HostGroupModel


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

