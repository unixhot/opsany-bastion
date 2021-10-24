from django.views import View

from bastion.component.strategy import AccessStrategyComponent, CommandStrategyComponent


class AccessStrategyView(View):
    def get(self, request):
        return AccessStrategyComponent().get_access_strategy(request)

    def post(self, request):
        return AccessStrategyComponent().create_access_strategy(request)

    def put(self, request):
        return AccessStrategyComponent().update_access_strategy(request)

    def delete(self, request):
        return AccessStrategyComponent().delete_access_strategy(request)


class StrategyStatusView(View):
    def put(self, request):
        return AccessStrategyComponent().update_strategy_status(request)


class CommandStrategyView(View):
    def get(self, request):
        return CommandStrategyComponent().get_command_strategy(request)

    def post(self, request):
        return CommandStrategyComponent().create_command_strategy(request)

    def put(self, request):
        return CommandStrategyComponent().update_command_strategy(request)

    def delete(self, request):
        return CommandStrategyComponent().delete_command_strategy(request)
