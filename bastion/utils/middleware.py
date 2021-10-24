from django.utils.deprecation import MiddlewareMixin


ENV = {"dev": "", "prod": "o", "stag": "t"}


class LocalLoginDebugMiddleware(MiddlewareMixin):
    def process_view(self, request, view, arg, kwarg):

        import platform
        # print("platform.system()", platform.system())
        if (not request.COOKIES.get("bk_token")) and (platform.system() == "Windows"):
            request.COOKIES.update(**{"bk_token": "7g42UwSWOJdx-Rxp9N3Vv9zA1BbL6gnu2lmGn1iWX18"})
        return None
