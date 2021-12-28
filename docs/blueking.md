## 蓝鲸社区版部署OpsAny Bastion开源堡垒机

OpsAny Bastion是基于开源的bk-paas编写的SaaS，目前测试通过修改可以兼容蓝鲸社区版和企业版。但是当前由于bk-paas和社区版的paas不一致，所以需要手工调整的内容比较多。

### 创建堡垒机数据库

1. 获取当前蓝鲸社区版的MySQL和Redis密码

如果你没有修改过蓝鲸社区版的MySQL和Redis的密码，可以从以下文件中获取。

```
[root@VM-16-3-centos install]# grep "BK_PAAS_MYSQL_PASSWORD" /data/install/bin/01-generate/paas.env
BK_PAAS_MYSQL_PASSWORD='IPQWfLZf6APE'
[root@VM-16-3-centos install]# grep "BK_PAAS_REDIS_PASSWORD" /data/install/bin/01-generate/paas.env
BK_PAAS_REDIS_PASSWORD=DRwsgTKXUsEY
```

2. 创建堡垒机使用的数据库，并进行授权

```
[root@VM-16-3-centos ~]# mysql --login-path=default-root
create database bastion DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
grant all on bastion.* to paas@'%' identified by "paas的密码"
grant all on bastion.* to bastion@'%' identified by "OpsAny@2020"
```
> 社区版的Smart应用，上传部署的时候会自动创建数据库和授权，这个当前无法完全兼容，需要手工创建。

3. 设置环境变量

```
cd install/
add_env_blueking.py
```

> 目前Smart的配置优先获取环境变量，当环境变量获取不到时，使用默认配置，所以需要使用脚本写入环境变了。

### 部署堡垒机Websocket容器

1. 修改websocket配置

```
#克隆代码
cd /opt && git clone https://gitee.com/unixhot/opsany-paas.git
#从配置模板生成配置文件
cd /opt/opsany-paas/install && cp install.config.example install.config
#设置访问的域名或公网IP，或内网IP。
DOMAIN_NAME=demo.opsany.com
#设置本机的内网IP地址
LOCAL_IP=192.168.56.11
#批量修改访问域名和IP地址
sed -i "s/demo.opsany.com/${DOMAIN_NAME}/g" install.config
sed -i "s/192.168.56.11/${LOCAL_IP}/g" install.config

source install.config
mkdir -p /opt/opsany/{conf,uploads}

/bin/cp conf/settings_production.py.websocket ${INSTALL_PATH}/conf/
/bin/cp conf/settings_production.py.websocket.init ${INSTALL_PATH}/conf/

# Websocket
sed -i "s/WEBSOCKET_GUACD_HOST/${WEBSOCKET_GUACD_HOST}/g" ${INSTALL_PATH}/conf/settings_production.py.websocket
sed -i "s/REDIS_SERVER_IP/${REDIS_SERVER_IP}/g" ${INSTALL_PATH}/conf/settings_production.py.websocket
sed -i "s/REDIS_SERVER_PASSWORD/${REDIS_SERVER_PASSWORD}/g" ${INSTALL_PATH}/conf/settings_production.py.websocket
sed -i "s/MYSQL_SERVER_IP/${MYSQL_SERVER_IP}/g" ${INSTALL_PATH}/conf/settings_production.py.websocket
sed -i "s/MYSQL_OPSANY_PASSWORD/${MYSQL_OPSANY_PASSWORD}/g" ${INSTALL_PATH}/conf/settings_production.py.websocket
sed -i "s/dev.opsany.cn/${PAAS_PAAS_IP}/g" ${INSTALL_PATH}/conf/settings_production.py.websocket.init
```

2. 启动Websocket容器

```
docker run -d --restart=always --name opsany-paas-websocket \
    -p 8004:8004 -v ${INSTALL_PATH}/logs:/opt/opsany/logs \
    -v ${INSTALL_PATH}/uploads:/opt/opsany/uploads \
    -v ${INSTALL_PATH}/conf/settings_production.py.websocket:/opt/opsany/websocket/config/prod.py \
    -v ${INSTALL_PATH}/conf/settings_production.py.websocket.init:/opt/opsany/websocket/config/__init__.py \
    -v /etc/localtime:/etc/localtime:ro \
    opsany/opsany-paas-websocket:v3.2.6
```

### 堡垒机部署

1. Smart包打包方式

```
wget -c http://bkopen-1252002024.file.myqcloud.com/common/py36_e.tgz -O /opt/py.tgz
wget -c https://raw.githubusercontent.com/shpdnkti/saas-builder/main/build.sh -O /tmp/build.sh
tar xf /opt/py.tgz -C /opt
chmod +x /tmp/build.sh
bash /tmp/build.sh -s ./ -d /tmp/release --python3-home /opt/py36_e/bin/python3 --app-code ${APP_CODE} --app-version ${VERSION}
```

2.在开发中心上传并部署OpsAny Bastion

3.修改蓝鲸PaaS的Openresty配置，增加以下内容。

```
vim /usr/local/openresty/nginx/conf/conf.d/paas.conf 

upstream OPEN_PAAS_CONSOLE {
    server 10.11.24.70:8004;
}


# CONTROL WebSocket
     location /ws/bastion/ {
        proxy_pass http://OPEN_PAAS_CONSOLE;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_redirect off;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Host $server_name;
    }
/usr/local/openresty/nginx/sbin/nginx -t
/usr/local/openresty/nginx/sbin/nginx -s reload

```
