from django.views import View

from bastion.component.strategy_v2 import AccessStrategyV2Component, CommandStrategyV2Component, BaseComponent


class AccessStrategyV2View(View):
    """
    访问策略
    """
    def get(self, request):
        return AccessStrategyV2Component().get_access_strategy(request)

    def post(self, request):
        return AccessStrategyV2Component().create_access_strategy(request)

    def put(self, request):
        return AccessStrategyV2Component().update_access_strategy(request)

    def delete(self, request):
        return AccessStrategyV2Component().delete_access_strategy(request)


class CommandStrategyV2View(View):
    """
    命令策略
    """
    def get(self, request):
        return CommandStrategyV2Component().get_command_strategy(request)

    def post(self, request):
        return CommandStrategyV2Component().create_command_strategy(request)

    def put(self, request):
        return CommandStrategyV2Component().update_command_strategy(request)

    def delete(self, request):
        return CommandStrategyV2Component().delete_command_strategy(request)


class ResourceCredentialView(View):
    """
    获取资源凭证
    """
    def get(self, request):
        return BaseComponent().get_resource_credential(request)
