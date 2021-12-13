from bastion.models import HostGroupModel


def init_default_group():
    host_dic = {
        "name": "默认分组",
        "description": "默认分组",
        "create_time": "2008-08-08 10:10:10.888888",
        "update_time": "2008-08-08 10:10:10.888888",
        "group_type": "host"
    }
    database_dic = {
        "name": "默认分组",
        "description": "默认分组",
        "create_time": "2008-08-08 10:10:10.888889",
        "update_time": "2008-08-08 10:10:10.888889",
        "group_type": "database"
    }

    host_obj = HostGroupModel.fetch_one(name="默认分组", group_type="host")
    if host_obj:
        host_obj.update(**host_dic)
    else:
        HostGroupModel.create(**host_dic).update(**host_dic)
    database_obj = HostGroupModel.fetch_one(name="默认分组", group_type="database")
    if database_obj:
        database_obj.update(**database_dic)
    else:
        HostGroupModel.create(**database_dic).update(**database_dic)

