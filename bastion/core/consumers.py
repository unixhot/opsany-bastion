import paramiko
import time
import json
import logging
import uuid
import datetime
import settings
import threading
import os
import io
import socket
from django.utils import timezone
from channels.generic.websocket import WebsocketConsumer
from django_redis import get_redis_connection
try:
    from django.utils.encoding import smart_unicode
except ImportError:
    from django.utils.encoding import smart_text as smart_unicode

from bastion.core.terminal.component import SSHBaseComponent
from bastion.core.status_code import WebSocketStatusCode
from bastion.component.core import CheckUserHostComponent
from bastion.component.common import GetUserInfo
from bastion.models import HostModel, CredentialModel, SessionLogModel, HostCredentialRelationshipModel
from bastion.core.terminal.component import SshTerminalThread, InterActiveShellThread
from bastion.utils.encryption import PasswordEncryption
from bastion.core.guacamole.component import GuacamoleThread, GuacamoleThreadWrite
from bastion.core.guacamole.client import GuacamoleClient

app_logging = logging.getLogger("app")


class WebSSH(WebsocketConsumer):
    # def __init__(self):
    #     super(WebSSH, self).__init__()
    #     self.ssh = paramiko.SSHClient()
    #     self.http_user = True
    #     self.channel_session = True
    #     self.channel_session_user = True
    #     self.first_flag = True
    #     self.wait_time = time.time()
    #     self.user = self.get_user()
    #     self.cache = get_redis_connection("cache")
    #     self.token = ""
    #     self.host = None
    #     self.session_log = None
    ssh = paramiko.SSHClient()
    http_user = True
    channel_session = False
    channel_session_user = False
    first_flag = True
    wait_time = time.time()
    user = None
    cache = get_redis_connection("cache")
    token = ""
    link_config = {}
    host = None
    session_log = None

    def get_user(self):
        user = GetUserInfo().get_user_info(bk_token=self.scope.get("cookies").get("bk_token"))
        return user

    def get_cookie(self):
        cookies = None
        cookie = {}
        for header in self.scope['headers']:
            if header[0] == b'cookie':
                cookies = header[1].decode()
                break
        if cookies:
            cookie = dict([cookie.split('=', 1) for cookie in cookies.split('&')])
        return cookie

    def get_request_param_dict(self):
        query_string = self.scope.get("query_string").decode()
        request_param = dict([x.split('=', 1) for x in query_string.split('&')])
        return request_param

    def check_link_user(self, user_id):
        self.user = self.get_user()
        if self.user:
            try:
                if self.user.id == user_id:
                    return True
                return False
            except Exception as e:
                app_logging.error("[ERROR] SSH web socket, check_link_user error: {}, param: {}".format(
                        str(e), str(user_id))
                )
                return False
        return False

    def get_link_config(self, token):
        try:
            if not self.link_config:
                data = self.cache.get(token).decode("utf-8")
                self.link_config = eval(data)
            else:
                pass
            return True, self.link_config
        except Exception as e:
            app_logging.error("[ERROR] SSH web socket, get_link_config error: {}, param: {}".format(
                    str(e), str(token))
            )
            return False, {}

    def check_link_time(self, data):
        """
        使用Token从缓存中读取验证数据
        """
        access_data = data.get("access_data")
        try:
            access_ip = self.scope.get("client")[0]
        except Exception as e:
            app_logging.error("[ERROR] SSH web socket, check_link_time error: {}, param: {}".format(
                str(e), str(self.scope)
            ))
            access_ip = ""
        status, _ = CheckUserHostComponent().check_access_strategy(access_data, access_ip)
        return status

    def check_token(self, check_user=False):
        request_param = self.get_request_param_dict()
        if not self.token:
            if request_param.get("token"):
                self.token = request_param.get("token")
            else:
                self.token = self.get_cookie().get("link_token")
        status, data = self.get_link_config(self.token)
        if status:
            if not check_user:
                status = self.check_link_user(data.get("user_id"))
            else:
                status = True
            if status:
                if data.get("admin") or data.get("cache"):
                    return None, "", data
                status = self.check_link_time(data)
                if status:
                    return True, "", data
                return False, WebSocketStatusCode.ACCESS_ERROR, {}
            return False, WebSocketStatusCode.USER_ERROR, {}
        return False, WebSocketStatusCode.PARAM_ERROR, {}

    def close_connect(self, text):
        self.send(text_data=str(text))
        self.close()
        return

    def create_session_log(self, data):
        try:
            query_string = self.scope['query_string'].decode()
            query_dict = dict([x.split('=', 1) for x in query_string.split('&')])
            width = int(float(query_dict["width"]))
            height = int(float(query_dict["height"]))
        except:
            width = 175
            height = 55
        """
        根据Token获取的缓存数据记录登陆日志
        """
        log_name = str(uuid.uuid4())
        if not data.get("cache"):
            try:
                login_name = HostCredentialRelationshipModel.fetch_one(id=data.get("credential_host_id")).credential.login_name
            except Exception as e:
                app_logging.error("[ERROR] Ws api error, get credential error: {} param: {}".format(
                        str(e), str(data.get("credential_host_id"))
                ))
                login_name = "root"
            session_log = SessionLogModel.create(**{
                "host_id": data.get("host_id"),
                "channel": self.channel_name,
                "host_name": self.host.host_name,
                "system_type": self.host.system_type,
                "host_address": self.host.host_address,
                "protocol_type": self.host.protocol_type,
                "login_type": 1,
                "port": self.host.port,
                "login_name": login_name,
                "log_name": log_name,
                "user": self.user.username,
                "width": width,
                "height": height
            })
        else:
            session_log = SessionLogModel.create(**{
                "channel": self.channel_name,
                "host_name": data.get("host_info").get("host_name"),
                "system_type": data.get("host_info").get("system_type"),
                "host_address": data.get("host_info").get("ip"),
                "protocol_type": "ssh",
                "login_type": 1,
                "port": data.get("host_info").get("port"),
                "login_name": data.get("host_info").get("username", ""),
                "log_name": log_name,
                "user": self.user.username,
                "width": width,
                "height": height
            })
        return session_log

    def client_ssh_by_password(self, ip, port, username, password, sock=None):
        try:
            self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.ssh.connect(hostname=ip, port=port, username=username, password=password, sock=sock, timeout=3)
            return True, ""
        except socket.timeout:
            return False, WebSocketStatusCode.TIME_OUT
        except Exception as e:
            app_logging.error("[ERROR] SSH web socket, client_ssh_by_password error: {}, param: {}".format(
                    str(e), str([ip, port, username, password])
            ))
            return False, WebSocketStatusCode.SSH_CHECK_ERROR

    def client_ssh_by_ssh_key(self, ip, port, login_name, ssh_key, passphrase, sock=None):
        """
        创建秘钥登陆SSH连接
        """
        try:
            self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            io_pri_key = io.StringIO(ssh_key)
            pri_key = paramiko.RSAKey.from_private_key(io_pri_key, password=passphrase)
            self.ssh.connect(hostname=ip, port=port, username=login_name, pkey=pri_key, timeout=3, sock=sock)
            return True, ""
        except socket.timeout:
            return False, WebSocketStatusCode.TIME_OUT
        except Exception as e:
            app_logging.error("[ERROR] SSH web socket, client_ssh_by_ssh_key error: {}, param: {}".format(
                    str(e), str([ip, port, ssh_key, passphrase])
            ))
            return False, WebSocketStatusCode.SSH_CHECK_ERROR

    def get_password(self, password):
        """
        密码解密
        """
        try:
            password = PasswordEncryption().decrypt(password)
        except Exception as e:
            app_logging.error("[ERROR] SSH web socket, get_password error: {}, param: {}".format(
                    str(e), str(password)
            ))
            password = ""
        return password

    def create_proxy_sock_by_password(self, ip, port, username, password, host_ip, host_port):
        """
        通过密码创建代理连接
        """
        try:
            proxy = paramiko.SSHClient()
            proxy.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            proxy.connect(hostname=ip, port=port, username=username, password=self.get_password(password))
            sock = proxy.get_transport().open_channel(
                'direct-tcpip', (host_ip, host_port), (ip, 0)
                        )
            return True, sock
        except Exception as e:
            app_logging.error("[ERROR] SSH web socket, create_proxy_sock_by_password error: {}, param: {}".format(
                    str(e), str(ip)
            ))
            return False, None

    def create_proxy_sock_by_ssh_key(self, ip, port, username, ssh_key, passphrase, host_ip, host_port):
        """
        通过密码创建代理连接
        """
        try:
            proxy = paramiko.SSHClient()
            proxy.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            io_pri_key = io.StringIO(ssh_key)
            pri_key = paramiko.RSAKey.from_private_key(io_pri_key, password=self.get_password(passphrase))
            proxy.connect(hostname=ip, port=port, username=username, pkey=pri_key)
            sock = proxy.get_transport().open_channel(
                'direct-tcpip', (host_ip, host_port), (ip, 0)
                        )
            return True, sock
        except Exception as e:
            app_logging.error("[ERROR] SSH web socket, create_proxy_sock_by_ssh_key error: {}, param: {}".format(
                    str(e), str(ip)
            ))
            return False, None

    def _create_ssh_link(self, credential, host, password):
        """
        创建SSH连接
        """
        network_proxy = host.network_proxy
        sock = None
        if network_proxy:
            if network_proxy.credential_type == network_proxy.CREDENTIAL_PASSWORD:
                status, sock = self.create_proxy_sock_by_password(
                        network_proxy.linux_ip,
                        network_proxy.linux_port,
                        network_proxy.linux_login_name,
                        network_proxy.linux_login_password,
                        self.host.host_address,
                        self.host.port
                    )
            else:
                status, sock = self.create_proxy_sock_by_ssh_key(
                        network_proxy.linux_ip,
                        network_proxy.linux_port,
                        network_proxy.linux_login_name,
                        network_proxy.ssh_key,
                        network_proxy.passphrase,
                        self.host.host_address,
                        self.host.port
                    )
            if not status:
                self.close_connect(WebSocketStatusCode.PROXY_LINK_ERROR)
                return
        if credential.login_type == CredentialModel.LOGIN_AUTO:
            if credential.credential_type == CredentialModel.CREDENTIAL_PASSWORD:
                password = self.get_password(credential.login_password)
                login_name = credential.login_name
                status, code = self.client_ssh_by_password(host.host_address, host.port, login_name, password, sock)
            else:
                password = credential.passphrase
                ssh_key = credential.ssh_key
                login_name = credential.login_name
                status, code = self.client_ssh_by_ssh_key(host.host_address, host.port, login_name, ssh_key, password, sock)
        else:
            if credential.credential_type == CredentialModel.CREDENTIAL_PASSWORD:
                login_name = credential.login_name
                status, code = self.client_ssh_by_password(host.host_address, host.port, login_name, password, sock)
            else:
                ssh_key = credential.ssh_key
                login_name = credential.login_name
                status, code = self.client_ssh_by_ssh_key(host.host_address, host.port, login_name, ssh_key, password, sock)
        if not status:
            self.close_connect(code)

    def _create_cache_ssh_link(self, token_data):
        """
        创建SSH连接
        """
        host_info = token_data.get("host_info")
        if token_data.get("login_type") == "password":
            status, code = self.client_ssh_by_password(
                    host_info.get("ip"),
                    host_info.get("port"),
                    host_info.get("username"),
                    host_info.get("password")
            )
        else:
            status, code = self.client_ssh_by_ssh_key(
                    host_info.get("ip"),
                    host_info.get("port"),
                    host_info.get("username", "root"),
                    host_info.get("ssh_key"),
                    host_info.get("password")
            )
        if not status:
            self.close_connect(code)

    def create_ssh_link(self, data):
        """
        校验数据以及创建SSH连接
        """
        if not data.get("cache"):
            host_id = data.get("host_id")
            credential_host_id = data.get("credential_host_id")
            password = data.get("password")
            credential_host = HostCredentialRelationshipModel.fetch_one(id=credential_host_id)
            self.host = HostModel.fetch_one(id=host_id)
            if not self.host or not credential_host:
                self.close_connect(WebSocketStatusCode.PARAM_ERROR)
            if self.host.system_type != HostModel.SYSTEM_LINUX:
                self.close_connect(WebSocketStatusCode.HOST_TYPE_ERROR)
            self._create_ssh_link(credential_host.credential, self.host, password)
        else:
            self._create_cache_ssh_link(data)

    def connect(self):
        self.wait_time = time.time()
        self.accept()
        # 验证token
        status, code, data = self.check_token()
        if not status and status is not None:
            self.close_connect(code)
        try:
            self.create_ssh_link(data)
        except Exception as e:
            app_logging.error("[ERROR] Create ssh link error: {}".format(str(e)))
            self.close_connect(WebSocketStatusCode.SSH_CHECK_ERROR)
        self.session_log = self.create_session_log(data)
        self.start_ssh()

    def start_ssh(self):
        chan = self.ssh.invoke_shell(width=self.session_log.width, height=self.session_log.height, term='xterm')
        sshterminal = SshTerminalThread(self, chan, self.user.username, self.token)
        sshterminal.setDaemon = True
        sshterminal.start()
        log_name = self.session_log.log_name + '.log'
        interactivessh = InterActiveShellThread(chan, self, log_name=log_name, width=self.session_log.width,
                                                    height=self.session_log.height)
        interactivessh.setDaemon = True
        interactivessh.start()

    def disconnect(self, close_code):
        self.close_ssh()
        time.sleep(0.5)
        try:
            self.session_log.update(**{
                "is_finished": True,
                "end_time": datetime.datetime.now()
            })
        except Exception as e:
            app_logging.error("[ERROR] Update Session Log error: {}, param: {}".format(str(e), str(self.session_log)))
        try:
            self.close()
        except:
            pass

    def close_ssh(self):
        self.queue.publish(self.channel_name, json.dumps(['close']))

    @property
    def queue(self):
        queue = SSHBaseComponent().get_redis_instance()
        queue.pubsub()
        return queue

    def receive(self, text_data=None, bytes_data=None, **kwargs):
        status, code, data = self.check_token(check_user=True)
        if not status and status is not None:
            self.close_connect(code)
        try:
            if text_data is not None:           # 普通命令执行
                self.queue.publish(self.channel_name, text_data)
            if bytes_data:                       # RZ SZ
                self.queue.publish(self.channel_name, bytes_data)
        except socket.error:
            self.disconnect(1000)
            return
        except ValueError:
            if self.first_flag:
                self.first_flag = False
            self.queue.publish(self.channel_name, smart_unicode(text_data))
        except Exception as e:
            self.disconnect(1000)
            return


class GuacamoleWebsocket(WebsocketConsumer):
    GUACD_CLIENT = None
    width = 1920
    height = 1080
    dpi = 900
    wait_time = time.time()
    token = ""
    cache = get_redis_connection("cache")
    user = None
    recording_path = os.path.join(settings.GUACD_PATH, "logfile")
    recording_name = str(uuid.uuid4())

    # def __init__(self):
    #     super(GuacamoleWebsocket, self).__init__()
    #     self.wait_time = time.time()
    #     self.token = ""
    #     self.cache = get_redis_connection("cache")
    #     self.user = self.get_user()
    #     self.recording_path = os.path.join(settings.GUACD_PATH, "logfile")
    #     self.recording_name = str(uuid.uuid4())

    def get_request_param_dict(self):
        query_string = self.scope.get("query_string").decode()
        request_param = dict([x.split('=', 1) for x in query_string.split('&')])
        return request_param

    def get_user(self):
        user = GetUserInfo().get_user_info(bk_token=self.scope.get("cookies").get("bk_token"))
        return user

    def get_cookie(self):
        cookies = None
        cookie = {}
        for header in self.scope['headers']:
            if header[0] == b'cookie':
                cookies = header[1].decode()
                break
        if cookies:
            cookie = dict([cookie.split('=', 1) for cookie in cookies.split('&')])
        return cookie

    def get_link_config(self, token):
        try:
            data = self.cache.get(token.split("/")[0]).decode("utf-8")
            data = eval(data)
            return True, data
        except Exception as e:
            app_logging.error("[ERROR] SSH web socket, get_link_config error: {}, param: {}".format(
                    str(e), str(token))
            )
            return False, {}

    def check_link_user(self, user_id):
        self.user = self.get_user()
        if self.user:
            try:
                if self.user.id == user_id:
                    return True
                return False
            except Exception as e:
                app_logging.error("[ERROR] SSH web socket, check_link_user error: {}, param: {}".format(
                        str(e), str(user_id))
                )
                return False
        return False

    def check_link_time(self, data):
        """
        使用Token从缓存中读取验证数据
        """
        access_data = data.get("access_data")
        try:
            access_ip = self.scope.get("client")[0]
        except Exception as e:
            app_logging.error("[ERROR] SSH web socket, check_link_time error: {}, param: {}".format(
                str(e), str(self.scope)
            ))
            access_ip = ""
        status, _ = CheckUserHostComponent().check_access_strategy(access_data, access_ip)
        return status

    def check_token(self):
        request_param = self.get_request_param_dict()
        self.token = request_param.get("token")
        if not self.token:
            self.token = self.get_cookie().get("link_token")
        status, data = self.get_link_config(self.token)
        if status:
            status = self.check_link_user(data.get("user_id"))
            if status:
                if data.get("admin") or data.get("cache"):
                    return None, "", data
                status = self.check_link_time(data)
                if status:
                    return True, "", data
                return False, WebSocketStatusCode.ACCESS_ERROR, {}
            return False, WebSocketStatusCode.USER_ERROR, {}
        return False, WebSocketStatusCode.PARAM_ERROR, {}

    def connect(self):
        self.accept('guacamole')
        self.wait_time = time.time()
        status, code, data = self.check_token()
        if not status and status is not None:
            raise Exception(code)
        query_string = self.scope['query_string'].decode()
        if query_string:
            query_dict = dict([x.split('=', 1) for x in query_string.split('&')])
            if query_dict.get("width") and query_dict.get("height") and query_dict.get("dpi"):
                self.width = int(float(query_dict["width"]))
                self.height = int(float(query_dict["height"]))
                self.dpi = int(float(query_dict["dpi"]))
        if not data.get("cache"):
            server_ = HostModel.fetch_one(id=data.get("host_id"))
            credential_host = HostCredentialRelationshipModel.fetch_one(id=data.get("credential_host_id"))
            drive_path = os.path.join(settings.GUACD_PATH, str(server_.id))
            ori_drive_path = os.path.join(settings.ORI_GUACD_PATH, str(server_.id))
        else:
            server_ = None
            credential_host = None
            drive_path = os.path.join(settings.GUACD_PATH, str(data.get("host_id")))
            ori_drive_path = os.path.join(settings.ORI_GUACD_PATH, str(data.get("host_id")))
        guacamole_host = settings.GUACD_HOST
        guacamole_port = settings.GUACD_PORT
        if server_:
            network_proxy = server_.network_proxy
            if network_proxy:
                guacamole_host = network_proxy.windows_ip
                guacamole_port = network_proxy.windows_port
        self.GUACD_CLIENT = GuacamoleClient(guacamole_host, guacamole_port)
        if not os.path.exists(ori_drive_path + "/Download"):
            os.makedirs(ori_drive_path + "/Download")
        if not os.path.exists(self.recording_path):
            os.makedirs(self.recording_path)
        args = {
            "enable_drive": "true",
            "create_drive_path": "true",
            "drive_name": "G",
            "drive_path": drive_path
        }
        if server_:
            credential = credential_host.credential
            hostname = server_.host_address.strip()
            port = server_.port
            username = credential.login_name.strip()
            if credential.login_type == credential.LOGIN_AUTO:
                password = PasswordEncryption().decrypt(credential.login_password.strip())
            else:
                password = data.get("password")
            if server_.system_type.strip() == "Linux":
                protocol = "ssh"
            else:
                protocol = "rdp"
        elif data.get("cache"):
            protocol = "rdp"
            hostname = data.get("host_info").get("ip")
            port = int(data.get("host_info").get("port"))
            username = data.get("host_info").get("username")
            password = data.get("host_info").get("password")
        else:
            raise Exception("Server not exist!!!")
        args.update({
            "security": 'any',
            "ignore_cert": "true",
            "disable_audio": "true",
            "recording_path": self.recording_path,
            "recording_name": self.recording_name,
            "create_recording_path": 'true'
        })
        self.GUACD_CLIENT.handshake(
                protocol=protocol,
                hostname=hostname,
                port=port,
                username=username,
                password=password,
                width=self.width,
                height=self.height,
                dpi=self.dpi,
                **args
            )
        self.closed = threading.Event()
        guacamolethread = GuacamoleThread(self)
        guacamolethread.setDaemon = True
        guacamolethread.start()
        guacamolethreadwrite = GuacamoleThreadWrite(self)
        guacamolethreadwrite.setDaemon = True
        guacamolethreadwrite.start()
        if server_:
            SessionLogModel.objects.create(
                user=self.user.username,
                host=server_,
                channel=self.channel_name,
                host_name=server_.host_name,
                system_type=server_.system_type,
                host_address=server_.host_address,
                login_name=credential_host.credential.login_name,
                log_name=self.recording_name,
                guacamole_client_id=self.GUACD_CLIENT.id,
                width=self.width,
                height=self.height
                )
        else:
            SessionLogModel.objects.create(
                user=self.user.username,
                channel=self.channel_name,
                host_name=data.get("host_info").get("host_name"),
                system_type="Windows",
                host_address=data.get("host_info").get("ip"),
                login_name=data.get("host_info").get("username"),
                log_name=self.recording_name,
                guacamole_client_id=self.GUACD_CLIENT.id,
                width=self.width,
                height=self.height
                )

    def disconnect(self, code):
        self.closed.set()
        audit_log = SessionLogModel.objects.filter(channel=self.channel_name)
        if audit_log:
            audit_log.update(
                    is_finished=True,
                    end_time=datetime.datetime.now()
                )
            width = str(audit_log[0].width)
            height = str(audit_log[0].height)
            full_path = os.path.join(self.recording_path, self.recording_name)
            command = '/opt /guacamole-server-1.2.0/src/guacenc/guacenc -s '\
                      + width + "x" + height + ' -r 1000000 -f ' + full_path
            os.system(command)
        else:
            app_logging.error("[ERROR] Windows Terminal Not Find Session Log, Channel name: {}".format(self.channel_name))
        try:
            self.close()
        except:
            pass
        self.GUACD_CLIENT.client.close()
        try:
            self.close()
        except:
            pass
        self.closeguacamole()

    def queue(self):
        queue = SSHBaseComponent().get_redis_instance()
        queue.pubsub()
        return queue

    def closeguacamole(self):
        self.queue().publish(self.channel_name, json.dumps(['close']))

    def check_timeout_close(self):
        # 空闲超时退出
        current_time = time.time()
        if int(current_time - self.wait_time) > settings.TERMINAL_TIMEOUT:
            self.send("10.disconnect;")
            self.queue().publish(self.channel_name, "10.disconnect;")
            self.disconnect(1001)

    def receive(self, text_data=None, bytes_data=None, **kwargs):
        self.check_timeout_close()
        # status, _, _ = self.check_token()
        status = True
        if status:
            self.queue().publish(self.channel_name, text_data)
            if not text_data.startswith("4.sync,1"):
                self.wait_time = time.time()
            if text_data == '10.disconnect;':
                self.disconnect(1000)
        else:
            self.send("10.disconnect;")
            self.queue().publish(self.channel_name, "10.disconnect;")
            self.disconnect(1001)


class Database(WebsocketConsumer):
    ssh = paramiko.SSHClient()
    http_user = True
    channel_session = True
    channel_session_user = True
    first_flag = True
    wait_time = time.time()
    user = None
    cache = get_redis_connection("cache")
    token = ""
    database = None
    session_log = None

    def get_request_param_dict(self):
        query_string = self.scope.get("query_string").decode()
        request_param = dict([x.split('=', 1) for x in query_string.split('&')])
        return request_param

    def get_cookie(self):
        cookies = None
        cookie = {}
        for header in self.scope['headers']:
            if header[0] == b'cookie':
                cookies = header[1].decode()
                break
        if cookies:
            cookie = dict([cookie.split('=', 1) for cookie in cookies.split('&')])
        return cookie

    def get_link_config(self, token):
        try:
            data = self.cache.get(token).decode("utf-8")
            data = eval(data)
            return True, data
        except Exception as e:
            app_logging.error("[ERROR] Databases web socket, get_link_config error: {}, param: {}".format(
                    str(e), str(token))
            )
            return False, {}

    def get_user(self):
        user = GetUserInfo().get_user_info(bk_token=self.scope.get("cookies").get("bk_token"))
        return user

    def check_link_user(self, user_id):
        self.user = self.get_user()
        if self.user:
            try:
                if self.user.id == user_id:
                    return True
                return False
            except Exception as e:
                app_logging.error("[ERROR] Databases web socket, check_link_user error: {}, param: {}".format(
                        str(e), str(user_id))
                )
                return False
        return False

    def check_link_time(self, data):
        """
        使用Token从缓存中读取验证数据
        """
        access_data = data.get("access_data")
        try:
            access_ip = self.scope.get("client")[0]
        except Exception as e:
            app_logging.error("[ERROR] Databases web socket, check_link_time error: {}, param: {}".format(
                str(e), str(self.scope)
            ))
            access_ip = ""
        status, _ = CheckUserHostComponent().check_access_strategy(access_data, access_ip)
        return status

    def check_token(self):
        request_param = self.get_request_param_dict()
        if not self.token:
            if request_param.get("token"):
                self.token = request_param.get("token")
            else:
                self.token = self.get_cookie().get("link_token")
        status, data = self.get_link_config(self.token)
        if status:
            status = self.check_link_user(data.get("user_id"))
            if status:
                if data.get("admin") or data.get("cache"):
                    return None, "", data
                status = self.check_link_time(data)
                if status:
                    return True, "", data
                return False, WebSocketStatusCode.ACCESS_ERROR, {}
            return False, WebSocketStatusCode.USER_ERROR, {}
        return False, WebSocketStatusCode.PARAM_ERROR, {}

    def get_password(self, password):
        """
        密码解密
        """
        try:
            password = PasswordEncryption().decrypt(password)
        except Exception as e:
            app_logging.error("[ERROR] Databases web socket, get_password error: {}, param: {}".format(
                    str(e), str(password)
            ))
            password = ""
        return password

    def client_proxy_or_local_link(self, ip="127.0.0.1", port=22, username="", password=""):
        """
        创建本地连接或者代理连接
        """
        try:
            self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            if username:
                self.ssh.connect(hostname=ip, port=port, username=username, password=password)
            else:
                self.ssh.connect(hostname=ip, port=port, password=password)
            return True, ""
        except socket.timeout:
            return False, WebSocketStatusCode.TIME_OUT
        except Exception as e:
            app_logging.error("[ERROR] Databases web socket, client_proxy_or_local_link error: {}, param: {}".format(
                    str(e), str([ip, port, password])
            ))
            return False, WebSocketStatusCode.SSH_CHECK_ERROR

    def close_connect(self, text):
        self.send(text_data=str(text))
        self.close()
        return

    def get_login_database_command(self, database_type, ip="", port="", username="", password=""):
        try:
            database_type = database_type.lower()
        except Exception as e:
            app_logging.error("[ERROR] Databases web socket, get_login_database_command error: {}, param: {}".format(
                    str(e), str(database_type)
            ))
            database_type = ""
        if database_type in ["mysql", "redis", "mongodb"]:
            if database_type == "mysql":
                command = "mysql -u{} -p{}".format(username, password)
                command += " -h{}".format(ip) if ip else ""
                command += " -P{}".format(port) if port else ""
                return True, command
            if database_type == "redis":
                command = "redis-cli -a {}".format(password)
                command += " -h {}".format(ip) if ip else ""
                command += " -p {}".format(port) if port else ""
                return True, command
            if database_type == "mongodb":
                command = "mongo --username {} --password {}".format(username, password)
                command += " --host {}".format(ip) if ip else ""
                command += " --port {}".format(port) if port else ""
                return True, command
        return False, WebSocketStatusCode.DATABASE_TYPE_ERROR

    def _create_databases_link(self, credential, database, password):
        """
        获取数据库连接命令，创建代理/本地连接
        """
        if credential.login_type == CredentialModel.LOGIN_AUTO:
            password = self.get_password(credential.login_password)
            login_name = credential.login_name
            port = database.port
            host_address = database.host_address
            database_type = database.database_type
            command_status, command = self.get_login_database_command(
                    database_type,
                    host_address,
                    port,
                    login_name,
                    password
            )
        else:
            login_name = credential.login_name
            host_address = database.host_address
            database_type = database.database_type
            port = database.port
            command_status, command = self.get_login_database_command(
                    database_type,
                    host_address,
                    port,
                    login_name,
                    password
            )
        if not command_status:
            self.close_connect(command)
            return ""
        # 如果有代理
        if database.network_proxy:
            network_proxy = database.network_proxy
            status, code = self.client_proxy_or_local_link(
                ip=network_proxy.linux_ip,
                port=network_proxy.linux_port,
                username=network_proxy.linux_login_name,
                password=self.get_password(network_proxy.linux_login_password)
            )
        else:
            status, code = self.client_proxy_or_local_link()
        if not status:
            self.close_connect(code)
            return ""
        return command

    def _create_cache_databases_link(self, token_data):
        """
        创建外平台连接
        """
        host_info = token_data.get("host_info")

        command_status, command = self.get_login_database_command(
                    host_info.get("database_type"),
                    host_info.get("ip"),
                    host_info.get("port"),
                    host_info.get("username"),
                    host_info.get("password")
            )
        if not command_status:
            self.close_connect(command)
            return ""
        status, code = self.client_proxy_or_local_link()
        if not status:
            self.close_connect(code)
            return ""
        return command

    def create_database_link(self, data):
        """
        校验数据以及创建SSH连接
        """
        if not data.get("cache"):
            host_id = data.get("host_id")
            credential_host_id = data.get("credential_host_id")
            password = data.get("password")
            credential_host = HostCredentialRelationshipModel.fetch_one(id=credential_host_id)
            self.database = HostModel.fetch_one(id=host_id)
            if not self.database or not credential_host:
                self.close_connect(WebSocketStatusCode.PARAM_ERROR)
            if self.database.resource_type != HostModel.RESOURCE_DATABASE:
                self.close_connect(WebSocketStatusCode.HOST_TYPE_ERROR)
            command = self._create_databases_link(credential_host.credential, self.database, password)
        else:
            command = self._create_cache_databases_link(data)
        return command

    def create_session_log(self, data):
        try:
            query_string = self.scope['query_string'].decode()
            query_dict = dict([x.split('=', 1) for x in query_string.split('&')])
            width = int(float(query_dict["width"]))
            height = int(float(query_dict["height"]))
        except:
            width = 175
            height = 55
        """
        根据Token获取的缓存数据记录登陆日志
        """
        log_name = str(uuid.uuid4())
        if not data.get("cache"):
            try:
                login_name = HostCredentialRelationshipModel.fetch_one(id=data.get("credential_host_id")).credential.login_name
            except Exception as e:
                app_logging.error("[ERROR] Ws api error, get credential error: {} param: {}".format(
                        str(e), str(data.get("credential_host_id"))
                ))
                login_name = "root"
            session_log = SessionLogModel.create(**{
                "host_id": data.get("host_id"),
                "channel": self.channel_name,
                "host_name": self.database.host_name,
                "system_type": self.database.system_type,
                "host_address": self.database.host_address,
                "protocol_type": self.database.protocol_type,
                "login_type": 1,
                "port": self.database.port,
                "login_name": login_name,
                "log_name": log_name,
                "user": self.user.username,
                "width": width,
                "height": height
            })
        else:
            session_log = SessionLogModel.create(**{
                "channel": self.channel_name,
                "host_name": data.get("host_info").get("host_name"),
                "system_type": data.get("host_info").get("system_type"),
                "host_address": data.get("host_info").get("ip"),
                "protocol_type": "ssh",
                "login_type": 1,
                "port": data.get("host_info").get("port"),
                "login_name": data.get("host_info").get("username", ""),
                "log_name": log_name,
                "user": self.user.username,
                "width": width,
                "height": height
            })
        return session_log

    def start_ssh(self, command):
        chan = self.ssh.invoke_shell(width=self.session_log.width, height=self.session_log.height, term='xterm')
        chan.send(command + "\n")
        chan.recv(1024)
        sshterminal = SshTerminalThread(self, chan, self.user.username, self.token)
        sshterminal.setDaemon = True
        sshterminal.start()
        log_name = self.session_log.log_name + '.log'
        interactivessh = InterActiveShellThread(chan, self, log_name=log_name, width=self.session_log.width,
                                                height=self.session_log.height,
                                                database_client=command)
        interactivessh.setDaemon = True
        interactivessh.start()

    def connect(self):
        self.wait_time = time.time()
        self.accept()
        # 验证token
        status, code, data = self.check_token()
        if not status and status is not None:
            self.close_connect(code)
        try:
            command = self.create_database_link(data)
        except Exception as e:
            app_logging.error("[ERROR] Create database link error: {}".format(str(e)))
            command = ""
            self.close_connect(WebSocketStatusCode.SSH_CHECK_ERROR)
        self.session_log = self.create_session_log(data)
        self.start_ssh(command)

    def disconnect(self, close_code):
        self.close_ssh()
        time.sleep(0.5)
        try:
            self.session_log.update(**{
                "is_finished": True,
                "end_time": datetime.datetime.now()
            })
        except Exception as e:
            app_logging.error("[ERROR] Update Session Log error: {}, param: {}".format(str(e), str(self.session_log)))
        self.close()

    def close_ssh(self):
        self.queue.publish(self.channel_name, json.dumps(['close']))

    @property
    def queue(self):
        queue = SSHBaseComponent().get_redis_instance()
        queue.pubsub()
        return queue

    def receive(self, text_data=None, bytes_data=None, **kwargs):
        status, code, data = self.check_token()
        if not status and status is not None:
            self.close_connect(code)
        try:
            if text_data is not None:           # 普通命令执行
                self.queue.publish(self.channel_name, text_data)
            if bytes_data:                       # RZ SZ
                self.queue.publish(self.channel_name, bytes_data)
        except socket.error:
            self.disconnect(1000)
            return
        except ValueError:
            if self.first_flag:
                self.first_flag = False
            self.queue.publish(self.channel_name, smart_unicode(text_data))
        except Exception as e:
            self.disconnect(1000)
            return
