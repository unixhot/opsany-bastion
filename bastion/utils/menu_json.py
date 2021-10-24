admin = {
        "code": 200,
        "successcode": 20023,
        "message": "获得菜单列表成功",
        "data": {
            "priority": "10",
            "menu_code": "bastion",
            "menu_type": "platform",
            "children": [{
                "priority": "10.1",
                "menu_code": "home",
                "menu_type": "directory",
                "auth": [{
                    "button_code": "10.1",
                    "id": 1078,
                    "button_name": "查看页面"
                }],
                "children": [],
                "menu_name": "概览",
                "parent_id": 1074,
                "menu_address": "/",
                "id": 1075
            }, {
                "priority": "10.2",
                "menu_code": "RouteView",
                "menu_type": "directory",
                "auth": [],
                "children": [{
                    "priority": "10.2.1",
                    "menu_code": "host",
                    "menu_type": "menu",
                    "auth": [{
                        "menu": {
                            "menu_name": "主机资源",
                            "id": 1077,
                            "menu_code": "host"
                        },
                        "button_code": "bastion_host_group_delete",
                        "id": 1115,
                        "button_name": "删除主机分组"
                    }, {
                        "menu": {
                            "menu_name": "主机资源",
                            "id": 1077,
                            "menu_code": "host"
                        },
                        "button_code": "bastion_host_details",
                        "id": 1106,
                        "button_name": "查看主机详情"
                    }, {
                        "menu": {
                            "menu_name": "主机资源",
                            "id": 1077,
                            "menu_code": "host"
                        },
                        "button_code": "bastion_host_login",
                        "id": 1107,
                        "button_name": "登录主机"
                    }, {
                        "menu": {
                            "menu_name": "主机资源",
                            "id": 1077,
                            "menu_code": "host"
                        },
                        "button_code": "bastion_host_credential_delete",
                        "id": 1108,
                        "button_name": "移除主机凭证"
                    }, {
                        "menu": {
                            "menu_name": "主机资源",
                            "id": 1077,
                            "menu_code": "host"
                        },
                        "button_code": "bastion_host_import",
                        "id": 1109,
                        "button_name": "导入主机"
                    }, {
                        "menu": {
                            "menu_name": "主机资源",
                            "id": 1077,
                            "menu_code": "host"
                        },
                        "button_code": "bastion_host_create",
                        "id": 1110,
                        "button_name": "新建主机"
                    }, {
                        "menu": {
                            "menu_name": "主机资源",
                            "id": 1077,
                            "menu_code": "host"
                        },
                        "button_code": "10.2.1",
                        "id": 1079,
                        "button_name": "查看页面"
                    }, {
                        "menu": {
                            "menu_name": "主机资源",
                            "id": 1077,
                            "menu_code": "host"
                        },
                        "button_code": "bastion_host_update",
                        "id": 1111,
                        "button_name": "修改主机"
                    }, {
                        "menu": {
                            "menu_name": "主机资源",
                            "id": 1077,
                            "menu_code": "host"
                        },
                        "button_code": "bastion_host_group_create",
                        "id": 1113,
                        "button_name": "新建主机分组"
                    }, {
                        "menu": {
                            "menu_name": "主机资源",
                            "id": 1077,
                            "menu_code": "host"
                        },
                        "button_code": "bastion_host_group_update",
                        "id": 1114,
                        "button_name": "修改主机分组"
                    }, {
                        "menu": {
                            "menu_name": "主机资源",
                            "id": 1077,
                            "menu_code": "host"
                        },
                        "button_code": "bastion_host_delete",
                        "id": 1112,
                        "button_name": "删除主机"
                    }],
                    "children": [],
                    "menu_name": "主机资源",
                    "parent_id": 1076,
                    "menu_address": "/resourceManagement/host",
                    "id": 1077
                }],
                "menu_name": "资源管理",
                "parent_id": 1074,
                "menu_address": "/resourceManagement",
                "id": 1076
            }, {
                "priority": "10.3",
                "menu_code": "RouteView1",
                "menu_type": "directory",
                "auth": [],
                "children": [{
                    "priority": "10.3.1",
                    "menu_code": "password",
                    "menu_type": "menu",
                    "auth": [{
                        "menu": {
                            "menu_name": "密码凭证",
                            "id": 1079,
                            "menu_code": "password"
                        },
                        "button_code": "bastion_password_update",
                        "id": 1120,
                        "button_name": "修改密码凭证"
                    }, {
                        "menu": {
                            "menu_name": "密码凭证",
                            "id": 1079,
                            "menu_code": "password"
                        },
                        "button_code": "bastion_password_delete",
                        "id": 1121,
                        "button_name": "删除密码凭证"
                    }, {
                        "menu": {
                            "menu_name": "密码凭证",
                            "id": 1079,
                            "menu_code": "password"
                        },
                        "button_code": "10.3.1",
                        "id": 1080,
                        "button_name": "查看页面"
                    }, {
                        "menu": {
                            "menu_name": "密码凭证",
                            "id": 1079,
                            "menu_code": "password"
                        },
                        "button_code": "bastion_password_details",
                        "id": 1116,
                        "button_name": "查看凭证详情"
                    }, {
                        "menu": {
                            "menu_name": "密码凭证",
                            "id": 1079,
                            "menu_code": "password"
                        },
                        "button_code": "bastion_password_resource_create",
                        "id": 1117,
                        "button_name": "关联资源"
                    }, {
                        "menu": {
                            "menu_name": "密码凭证",
                            "id": 1079,
                            "menu_code": "password"
                        },
                        "button_code": "bastion_password_resource_delete",
                        "id": 1118,
                        "button_name": "移除关联资源"
                    }, {
                        "menu": {
                            "menu_name": "密码凭证",
                            "id": 1079,
                            "menu_code": "password"
                        },
                        "button_code": "bastion_password_create",
                        "id": 1119,
                        "button_name": "新建密码凭证"
                    }],
                    "children": [],
                    "menu_name": "密码凭证",
                    "parent_id": 1078,
                    "menu_address": "/voucherManagement/password",
                    "id": 1079
                }, {
                    "priority": "10.3.2",
                    "menu_code": "ssh",
                    "menu_type": "menu",
                    "auth": [{
                        "menu": {
                            "menu_name": "SSH凭证",
                            "id": 1080,
                            "menu_code": "ssh"
                        },
                        "button_code": "bastion_ssh_details",
                        "id": 1122,
                        "button_name": "查看凭证详情"
                    }, {
                        "menu": {
                            "menu_name": "SSH凭证",
                            "id": 1080,
                            "menu_code": "ssh"
                        },
                        "button_code": "bastion_ssh_resource_create",
                        "id": 1123,
                        "button_name": "关联资源"
                    }, {
                        "menu": {
                            "menu_name": "SSH凭证",
                            "id": 1080,
                            "menu_code": "ssh"
                        },
                        "button_code": "bastion_ssh_resource_delete",
                        "id": 1124,
                        "button_name": "移除关联资源"
                    }, {
                        "menu": {
                            "menu_name": "SSH凭证",
                            "id": 1080,
                            "menu_code": "ssh"
                        },
                        "button_code": "bastion_ssh_create",
                        "id": 1125,
                        "button_name": "新建SSH凭证"
                    }, {
                        "menu": {
                            "menu_name": "SSH凭证",
                            "id": 1080,
                            "menu_code": "ssh"
                        },
                        "button_code": "bastion_ssh_update",
                        "id": 1126,
                        "button_name": "修改SSH凭证"
                    }, {
                        "menu": {
                            "menu_name": "SSH凭证",
                            "id": 1080,
                            "menu_code": "ssh"
                        },
                        "button_code": "bastion_ssh_delete",
                        "id": 1127,
                        "button_name": "删除SSH凭证"
                    }, {
                        "menu": {
                            "menu_name": "SSH凭证",
                            "id": 1080,
                            "menu_code": "ssh"
                        },
                        "button_code": "10.3.2",
                        "id": 1081,
                        "button_name": "查看页面"
                    }],
                    "children": [],
                    "menu_name": "SSH凭证",
                    "parent_id": 1078,
                    "menu_address": "/voucherManagement/ssh",
                    "id": 1080
                }, {
                    "priority": "10.3.3",
                    "menu_code": "voucherGrouping",
                    "menu_type": "menu",
                    "auth": [{
                        "menu": {
                            "menu_name": "凭证分组",
                            "id": 1081,
                            "menu_code": "voucherGrouping"
                        },
                        "button_code": "bastion_credential_group_details",
                        "id": 1128,
                        "button_name": "查看凭证分组详情"
                    }, {
                        "menu": {
                            "menu_name": "凭证分组",
                            "id": 1081,
                            "menu_code": "voucherGrouping"
                        },
                        "button_code": "bastion_credential_group_credential_create",
                        "id": 1129,
                        "button_name": "添加凭证"
                    }, {
                        "menu": {
                            "menu_name": "凭证分组",
                            "id": 1081,
                            "menu_code": "voucherGrouping"
                        },
                        "button_code": "bastion_credential_group_credential_delete",
                        "id": 1130,
                        "button_name": "移除凭证"
                    }, {
                        "menu": {
                            "menu_name": "凭证分组",
                            "id": 1081,
                            "menu_code": "voucherGrouping"
                        },
                        "button_code": "bastion_credential_group_create",
                        "id": 1131,
                        "button_name": "新建凭证分组"
                    }, {
                        "menu": {
                            "menu_name": "凭证分组",
                            "id": 1081,
                            "menu_code": "voucherGrouping"
                        },
                        "button_code": "bastion_credential_group_update",
                        "id": 1132,
                        "button_name": "修改凭证分组"
                    }, {
                        "menu": {
                            "menu_name": "凭证分组",
                            "id": 1081,
                            "menu_code": "voucherGrouping"
                        },
                        "button_code": "bastion_credential_group_delete",
                        "id": 1133,
                        "button_name": "删除凭证分组"
                    }, {
                        "menu": {
                            "menu_name": "凭证分组",
                            "id": 1081,
                            "menu_code": "voucherGrouping"
                        },
                        "button_code": "10.3.3",
                        "id": 1082,
                        "button_name": "查看页面"
                    }],
                    "children": [],
                    "menu_name": "凭证分组",
                    "parent_id": 1078,
                    "menu_address": "/voucherManagement/voucherGrouping",
                    "id": 1081
                }],
                "menu_name": "凭证管理",
                "parent_id": 1074,
                "menu_address": "/voucherManagement",
                "id": 1078
            }, {
                "priority": "10.4",
                "menu_code": "RouteView2",
                "menu_type": "directory",
                "auth": [],
                "children": [{
                    "priority": "10.4.1",
                    "menu_code": "visitPolicy",
                    "menu_type": "menu",
                    "auth": [{
                        "menu": {
                            "menu_name": "访问策略",
                            "id": 1083,
                            "menu_code": "visitPolicy"
                        },
                        "button_code": "bastion_access_strategy_on_off",
                        "id": 1134,
                        "button_name": "访问策略开关"
                    }, {
                        "menu": {
                            "menu_name": "访问策略",
                            "id": 1083,
                            "menu_code": "visitPolicy"
                        },
                        "button_code": "bastion_access_strategy_create",
                        "id": 1135,
                        "button_name": "新建访问策略"
                    }, {
                        "menu": {
                            "menu_name": "访问策略",
                            "id": 1083,
                            "menu_code": "visitPolicy"
                        },
                        "button_code": "bastion_access_strategy_update",
                        "id": 1136,
                        "button_name": "修改访问策略"
                    }, {
                        "menu": {
                            "menu_name": "访问策略",
                            "id": 1083,
                            "menu_code": "visitPolicy"
                        },
                        "button_code": "bastion_access_strategy_delete",
                        "id": 1137,
                        "button_name": "删除访问策略"
                    }, {
                        "menu": {
                            "menu_name": "访问策略",
                            "id": 1083,
                            "menu_code": "visitPolicy"
                        },
                        "button_code": "10.4.1",
                        "id": 1083,
                        "button_name": "查看页面"
                    }],
                    "children": [],
                    "menu_name": "访问策略",
                    "parent_id": 1082,
                    "menu_address": "/accessPolicy/visitPolicy",
                    "id": 1083
                }, {
                    "priority": "10.4.2",
                    "menu_code": "commandPolicy",
                    "menu_type": "menu",
                    "auth": [{
                        "menu": {
                            "menu_name": "命令策略",
                            "id": 1084,
                            "menu_code": "commandPolicy"
                        },
                        "button_code": "bastion_command_strategy_on_off",
                        "id": 1138,
                        "button_name": "访问命令开关"
                    }, {
                        "menu": {
                            "menu_name": "命令策略",
                            "id": 1084,
                            "menu_code": "commandPolicy"
                        },
                        "button_code": "bastion_command_strategy_create",
                        "id": 1139,
                        "button_name": "新建命令策略"
                    }, {
                        "menu": {
                            "menu_name": "命令策略",
                            "id": 1084,
                            "menu_code": "commandPolicy"
                        },
                        "button_code": "bastion_command_strategy_update",
                        "id": 1140,
                        "button_name": "修改命令策略"
                    }, {
                        "menu": {
                            "menu_name": "命令策略",
                            "id": 1084,
                            "menu_code": "commandPolicy"
                        },
                        "button_code": "bastion_command_strategy_delete",
                        "id": 1141,
                        "button_name": "删除命令策略"
                    }, {
                        "menu": {
                            "menu_name": "命令策略",
                            "id": 1084,
                            "menu_code": "commandPolicy"
                        },
                        "button_code": "bastion_command_create",
                        "id": 1142,
                        "button_name": "新建命令"
                    }, {
                        "menu": {
                            "menu_name": "命令策略",
                            "id": 1084,
                            "menu_code": "commandPolicy"
                        },
                        "button_code": "bastion_command_update",
                        "id": 1143,
                        "button_name": "修改命令"
                    }, {
                        "menu": {
                            "menu_name": "命令策略",
                            "id": 1084,
                            "menu_code": "commandPolicy"
                        },
                        "button_code": "bastion_command_delete",
                        "id": 1144,
                        "button_name": "删除命令"
                    }, {
                        "menu": {
                            "menu_name": "命令策略",
                            "id": 1084,
                            "menu_code": "commandPolicy"
                        },
                        "button_code": "bastion_command_group_create",
                        "id": 1145,
                        "button_name": "新建命令分组"
                    }, {
                        "menu": {
                            "menu_name": "命令策略",
                            "id": 1084,
                            "menu_code": "commandPolicy"
                        },
                        "button_code": "bastion_command_group_update",
                        "id": 1146,
                        "button_name": "修改命令分组"
                    }, {
                        "menu": {
                            "menu_name": "命令策略",
                            "id": 1084,
                            "menu_code": "commandPolicy"
                        },
                        "button_code": "bastion_command_group_delete",
                        "id": 1147,
                        "button_name": "删除命令分组"
                    }, {
                        "menu": {
                            "menu_name": "命令策略",
                            "id": 1084,
                            "menu_code": "commandPolicy"
                        },
                        "button_code": "10.4.2",
                        "id": 1084,
                        "button_name": "查看页面"
                    }],
                    "children": [],
                    "menu_name": "命令策略",
                    "parent_id": 1082,
                    "menu_address": "/accessPolicy/commandPolicy",
                    "id": 1084
                }],
                "menu_name": "权限策略",
                "parent_id": 1074,
                "menu_address": "/accessPolicy",
                "id": 1082
            }, {
                "priority": "10.5",
                "menu_code": "RouteView3",
                "menu_type": "directory",
                "auth": [],
                "children": [{
                    "priority": "10.5.1",
                    "menu_code": "online",
                    "menu_type": "menu",
                    "auth": [{
                        "menu": {
                            "menu_name": "在线会话",
                            "id": 1086,
                            "menu_code": "online"
                        },
                        "button_code": "bastion_session_off_line",
                        "id": 1148,
                        "button_name": "强制下线"
                    }, {
                        "menu": {
                            "menu_name": "在线会话",
                            "id": 1086,
                            "menu_code": "online"
                        },
                        "button_code": "10.5.1",
                        "id": 1085,
                        "button_name": "查看页面"
                    }],
                    "children": [],
                    "menu_name": "在线会话",
                    "parent_id": 1085,
                    "menu_address": "/auditManagement/online",
                    "id": 1086
                }, {
                    "priority": "10.5.2",
                    "menu_code": "historical",
                    "menu_type": "menu",
                    "auth": [{
                        "menu": {
                            "menu_name": "历史会话",
                            "id": 1087,
                            "menu_code": "historical"
                        },
                        "button_code": "10.5.2",
                        "id": 1086,
                        "button_name": "查看页面"
                    }],
                    "children": [],
                    "menu_name": "历史会话",
                    "parent_id": 1085,
                    "menu_address": "/auditManagement/historical",
                    "id": 1087
                }, {
                    "priority": "10.5.3",
                    "menu_code": "auditHistory",
                    "menu_type": "menu",
                    "auth": [{
                        "menu": {
                            "menu_name": "审计历史",
                            "id": 1088,
                            "menu_code": "auditHistory"
                        },
                        "button_code": "10.5.3",
                        "id": 1087,
                        "button_name": "查看页面"
                    }],
                    "children": [],
                    "menu_name": "审计历史",
                    "parent_id": 1085,
                    "menu_address": "/auditManagement/auditHistory",
                    "id": 1088
                }, {
                    "priority": "10.5.4",
                    "menu_code": "operationLog",
                    "menu_type": "menu",
                    "auth": [{
                        "menu": {
                            "menu_name": "操作日志",
                            "id": 1089,
                            "menu_code": "operationLog"
                        },
                        "button_code": "10.5.4",
                        "id": 1088,
                        "button_name": "查看页面"
                    }],
                    "children": [],
                    "menu_name": "操作日志",
                    "parent_id": 1085,
                    "menu_address": "/auditManagement/operationLog",
                    "id": 1089
                }],
                "menu_name": "审计管理",
                "parent_id": 1074,
                "menu_address": "/auditManagement",
                "id": 1085
            }, {
                "priority": "10.7",
                "menu_code": "RouteView5",
                "menu_type": "directory",
                "auth": [],
                "children": [{
                    "priority": "10.7.1",
                    "menu_code": "userManage",
                    "menu_type": "menu",
                    "auth": [{
                        "menu": {
                            "menu_name": "用户管理",
                            "id": 1122,
                            "menu_code": "userManage"
                        },
                        "button_code": "10.7.1",
                        "id": 1176,
                        "button_name": "查看页面"
                    }, {
                        "menu": {
                            "menu_name": "用户管理",
                            "id": 1122,
                            "menu_code": "userManage"
                        },
                        "button_code": "bastion_user_group_import",
                        "id": 1178,
                        "button_name": "用户组导入"
                    }, {
                        "menu": {
                            "menu_name": "用户管理",
                            "id": 1122,
                            "menu_code": "userManage"
                        },
                        "button_code": "bastion_user_group_remove",
                        "id": 1179,
                        "button_name": "用户组移除"
                    }, {
                        "menu": {
                            "menu_name": "用户管理",
                            "id": 1122,
                            "menu_code": "userManage"
                        },
                        "button_code": "bastion_user_import",
                        "id": 1180,
                        "button_name": "用户导入"
                    }, {
                        "menu": {
                            "menu_name": "用户管理",
                            "id": 1122,
                            "menu_code": "userManage"
                        },
                        "button_code": "bastion_user_remove",
                        "id": 1181,
                        "button_name": "用户移除"
                    }, {
                        "menu": {
                            "menu_name": "用户管理",
                            "id": 1122,
                            "menu_code": "userManage"
                        },
                        "button_code": "bastion_group_user_detail",
                        "id": 1182,
                        "button_name": "用户组成员查看"
                    }],
                    "children": [],
                    "menu_name": "用户管理",
                    "parent_id": 1121,
                    "menu_address": "/setting/userManage",
                    "id": 1122
                }],
                "menu_name": "平台设置",
                "parent_id": 1074,
                "menu_address": "/setting",
                "id": 1121
            }],
            "menu_name": "堡垒机",
            "parent_id": None,
            "menu_address": "/o/bastion/",
            "id": 1074
        }
    }

user = {
        "code": 200,
        "successcode": 20023,
        "message": "获得菜单列表成功",
        "data": {
            "priority": "10",
            "menu_code": "bastion",
            "menu_type": "platform",
            "children": [{
                "priority": "10.1",
                "menu_code": "home",
                "menu_type": "directory",
                "auth": [{
                    "button_code": "10.1",
                    "id": 1078,
                    "button_name": "查看页面"
                }],
                "children": [],
                "menu_name": "概览",
                "parent_id": 1074,
                "menu_address": "/",
                "id": 1075
            }, {
                "priority": "10.6",
                "menu_code": "RouteView4",
                "menu_type": "directory",
                "auth": [],
                "children": [{
                    "priority": "10.6.1",
                    "menu_code": "authorizationHost",
                    "menu_type": "menu",
                    "auth": [{
                        "menu": {
                            "menu_name": "授权主机",
                            "id": 1116,
                            "menu_code": "authorizationHost"
                        },
                        "button_code": "bastion_ops_host_login",
                        "id": 1177,
                        "button_name": "登录"
                    }, {
                        "menu": {
                            "menu_name": "授权主机",
                            "id": 1116,
                            "menu_code": "authorizationHost"
                        },
                        "button_code": "10.6.1",
                        "id": 1171,
                        "button_name": "查看页面"
                    }],
                    "children": [],
                    "menu_name": "授权主机",
                    "parent_id": 1115,
                    "menu_address": "/safe/authorizationHost",
                    "id": 1116
                }],
                "menu_name": "安全运维",
                "parent_id": 1074,
                "menu_address": "/safe",
                "id": 1115
            }],
            "menu_name": "堡垒机",
            "parent_id": None,
            "menu_address": "/o/bastion/",
            "id": 1074
        }
    }