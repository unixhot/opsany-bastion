# -*- coding: utf-8 -*-
import logging

from django.conf import settings
from django.contrib import auth
import json
try:
    from django.utils.deprecation import MiddlewareMixin
except Exception:
    MiddlewareMixin = object
from config import BK_URL, APP_CODE
import settings as env_config
from blueapps.account.conf import ConfFixture
from blueapps.account.handlers.response import ResponseHandler, JsonResponse
from blueapps.account.components.bk_token.forms import AuthenticationForm
from bastion.utils.status_code import error, ErrorStatusCode
ENV = {"dev": "", "prod": "o", "stag": "t"}
logger = logging.getLogger('component')


class LoginRequiredMiddleware(MiddlewareMixin):
    def process_view(self, request, view, args, kwargs):
        """
        Login paas by two ways
        1. views decorated with 'login_exempt' keyword
        2. User has logged in calling auth.login
        """
        # request.COOKIES["bk_token"] = "LilyG11EWaKBPTOF1ntULcXrkpK4IIu4v_K2eHOlcYg"
        if hasattr(request, 'is_wechat') and request.is_wechat():
            return None

        if hasattr(request, 'is_bk_jwt') and request.is_bk_jwt():
            return None

        if getattr(view, 'login_exempt', False):
            return None
        form = AuthenticationForm(request.COOKIES)
        login_out_url = "https%3A//" + BK_URL.split("https://")[-1] + "/" + ENV.get(getattr(env_config, "run_env", "dev")) +"/{}/&is_from_logout=1".format(APP_CODE)
        if form.is_valid():
            bk_token = form.cleaned_data['bk_token']
            user = None
            if bk_token != "None":
                user = auth.authenticate(request=request, bk_token=bk_token)
            if not user:
                try:
                    data = json.loads(request.body)
                except:
                    data = {}
                if request.GET.get("operator") or request.POST.get("operator") or data.get("operator"):
                    return None
                return JsonResponse(error(ErrorStatusCode.INVALID_TOKEN, login_out_url))
            if user.username and user.is_active:
                return None
            return JsonResponse(error(ErrorStatusCode.INVALID_TOKEN, login_out_url))

        if request.path_info == "/":
            handler = ResponseHandler(ConfFixture, settings)
            return handler.build_401_response(request)
        else:
            return JsonResponse(error(ErrorStatusCode.INVALID_TOKEN, login_out_url))

    def process_response(self, request, response):
        return response
