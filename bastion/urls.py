# -*- coding: utf-8 -*-
"""
Copyright © 2012-2020 OpsAny. All Rights Reserved.
""" # noqa
from django.urls import path

from bastion.audit import audit_views
from bastion.utils import base_views
from bastion.credential import credential_views
from bastion.resource import resource_views, batch_views, network_proxy_views
from bastion.strategy import views as strategy_views
from bastion.strategy import views_v2 as strategy_views_v2
from bastion.core import views as core_views
from bastion import views

urlpatterns = [
    # 各平台基础API
    path("get-menu/", base_views.BaseMenuStrategyCtrl.as_view()),                           # 从同一权限拉取用户菜单
    path('user-info/', base_views.GetUserInfoCtrl.as_view()),                               # 获取用户信息
    path("get-nav-and-collection/", base_views.GetNavCollectionView.as_view()),             # 获取导航和搜藏
    path("collection/", base_views.CollectionNavView.as_view()),                            # 获取搜藏信息
    path("get-user-message/", base_views.GetUserMessageView.as_view()),                     # 获取用户站内信
    path("read-all-message/", base_views.ReadAllMessageView.as_view()),                     # 全部已读
    path("home-page/", base_views.HomePageView.as_view()),                                  # 概览页
    path("get-agent/", base_views.GetAgentView.as_view()),                                  # 资源平台导入
    path("user-admin/", base_views.UserAdminView.as_view()),                                # 用户管理
    path("bk-user-admin/", base_views.BkUserAdminView.as_view()),                           # 用户管理By Blue King
    path("user-group-admin/", base_views.UserGroupAdminView.as_view()),                     # 用户组管理
    path("bk-user-group-admin/", base_views.BkUserGroupAdminView.as_view()),                # 用户组管理By Blue King

    path("credential-group/", credential_views.CredentialGroupView.as_view()),              # 凭据分组
    path("credential/", credential_views.CredentialView.as_view()),                         # 密码凭据，SSH凭据
    path("host-group/", resource_views.HostGroupView.as_view()),                            # 主机分组
    path("host-group-console/", resource_views.HostGroupConsoleView.as_view()),             # 主机分组

    # resource_type or group_type：host database
    path("resource/<str:resource_type>/", resource_views.HostView.as_view()),  # 资源（主机，数据库）
    path("group/<str:group_type>/", resource_views.HostGroupView.as_view()),  # 资源分组（主机，数据库）
    path("auth/<str:resource_type>/", resource_views.AuthResourceView.as_view()),  # 资源（主机,数据库。经过授权校验的主机）
    path("network-proxy/", network_proxy_views.NetworkProxyView.as_view()),  # 网络代理
    path("network-proxy-resource/", network_proxy_views.NetworkProxyResourceView.as_view()),

    path("host/", resource_views.HostView.as_view()),                                       # 主机
    path("auth-host/", resource_views.AuthHostView.as_view()),                              # 主机

    path("group-credential/", credential_views.GroupCredentialView.as_view()),              # 凭据绑定分组 # 主机关联分组
    path("host-credential/", resource_views.HostCredentialView.as_view()),                  # 主机关联凭据
    path("sync_user_group/", credential_views.SyncUserGroupView.as_view()),
    # 策略
    path("access-strategy/", strategy_views.AccessStrategyView.as_view()),                  # 访问策略
    path("access-strategy-v2/", strategy_views_v2.AccessStrategyV2View.as_view()),          # 访问策略v2
    path("strategy-status/", strategy_views.StrategyStatusView.as_view()),                  # 访问策略状态
    path("command-strategy/", strategy_views.CommandStrategyView.as_view()),                # 访问策略
    path("command-strategy-v2/", strategy_views_v2.CommandStrategyV2View.as_view()),        # 访问策略v2
    # 资源凭证
    path("resource-credential/", strategy_views_v2.ResourceCredentialView.as_view()),       # 资源凭证

    path("command-group/", credential_views.CommandGroupView.as_view()),                    # 命令分组
    path("command/", credential_views.CommandView.as_view()),                               # 命令
    path("group-command/", credential_views.GroupCommandView.as_view()),                    # 命令分组关联
    # 连接验证
    path("link-check/", core_views.LinkCheckView.as_view()),                                # 连接前的验证
    path("link-check-v2/", core_views.LinkCheckV2View.as_view()),                           # 连接前的验证v2
    path("get-cache-token/", core_views.GetCacheTokenView.as_view()),                       # 其他平台获取token
    path("linux-file/", core_views.LinuxFileView.as_view()),                                # Linux上传下载
    path("windows-file/", core_views.WindowsFileView.as_view()),                            # Windows上传下载
    path("user/", resource_views.UserInfoView.as_view()),                                   # 用户数据
    path("group/", resource_views.GroupView.as_view()),                                     # 用户组
    # 审计
    path("operation-log/", audit_views.OperationLogView.as_view()),                         # 操作日志
    path("session-log/", audit_views.SessionLogView.as_view()),                             # 会话日志
    path("session-log/<str:type>/<str:log_name>/", audit_views.SessionLogView.as_view()),   # 会话详情
    path("session-command-history/", audit_views.SessionCommandHistoryView.as_view()),      # 会话命令详情
    path("command-log/", audit_views.CommandLogView.as_view()),                             # 命令日志
    # ESB
    path("get-info-for-workbench/", views.GetInfoForWorkbenchView.as_view()),
    # 鉴权
    path("authentication/", views.AuthenticationView.as_view()),

    # 批量下载
    path("check-import/", batch_views.BatchView.as_view()),
]