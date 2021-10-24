try:
    from iam import IAM, Request, Subject, Action, Resource

    from config import APP_CODE, SECRET_KEY, BK_IAM_HOST, BK_URL
except:
    pass


class Permission(object):
    def __init__(self):
        self._iam = IAM(APP_CODE, SECRET_KEY, BK_IAM_HOST, BK_URL)

    def _make_request_without_resources(self, username, action_id):
        request = Request(
            APP_CODE,
            Subject("user", username),
            Action(action_id),
            None,
            None,
        )
        return request

    def allowed_visit_host_resources(self, username):
        request = self._make_request_without_resources(username, "visit-host-resources")
        return self._iam.is_allowed(request)

    def allowed_action(self, username, action_id):
        request = self._make_request_without_resources(username, action_id)
        return self._iam.is_allowed(request)


if __name__ == '__main__':
    import os
    import sys
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
    import datetime

    sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
    import django
    django.setup()
    from iam import IAM, Request, Subject, Action, Resource

    from config import APP_CODE, SECRET_KEY, BK_IAM_HOST, BK_URL
    res = Permission().allowed_visit_host_resources("admin")
    print(res)