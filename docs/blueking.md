# 生产环境部署

- 方案一： 直接部署OpsAny社区版(官方文档)[https://docs.opsany.com/]
- 方案二： 在蓝鲸社区版的基础上快速部署OpsAny堡垒机

## 方案二：蓝鲸社区版部署OpsAny开源堡垒机

OpsAny Bastion是基于开源的bk-paas编写的SaaS，目前测试通过修改可以兼容蓝鲸社区版和企业版。但是当前由于bk-paas和社区版的paas不一致，有一些需要手工调整。

> 建议使用手工部署，可以了解和掌握堡垒机的部署和运行方式，自动化部署脚本准备中。

### 创建堡垒机数据库

1. 获取当前蓝鲸社区版的MySQL和Redis密码

```
[root@VM-16-3-centos install]# grep "BK_PAAS_MYSQL_PASSWORD" /data/install/bin/01-generate/paas.env
BK_PAAS_MYSQL_PASSWORD='IPQWfLZf6APE'
[root@VM-16-3-centos install]# grep "BK_PAAS_REDIS_PASSWORD" /data/install/bin/01-generate/paas.env
BK_PAAS_REDIS_PASSWORD=DRwsgTKXUsEY
```

> 如果你没有修改过蓝鲸社区版的MySQL和Redis的密码，可以从以下文件中获取。OpsAny堡垒机需要使用MySQL和Redis，建议直接使用蓝鲸社区版自带的。


2. 创建堡垒机使用的数据库，并进行授权

```
[root@VM-16-3-centos ~]# mysql --login-path=default-root
create database bastion DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
grant all on bastion.* to paas@'%' identified by "上面获取到的paas的密码"
grant all on bastion.* to bastion@'%' identified by "OpsAny@2020"
```
> 社区版的Smart应用，上传部署的时候会自动创建数据库和授权，这个当前无法完全兼容，需要手工创建数据库bastion并进行授权，仅支持修改密码。数据库名和用户名不要修改。

### 堡垒机SAAS部署

需要先将堡垒机打包为蓝鲸Smart应用的包，然后就可以直接在开发者中心上传部署。

1. Smart包打包方式

```
cd /opt && git clone https://gitee.com/unixhot/opsany-bastion.git
wget -c http://bkopen-1252002024.file.myqcloud.com/common/py36_e.tgz -O /opt/py.tgz
wget -c https://raw.githubusercontent.com/shpdnkti/saas-builder/main/build.sh -O /tmp/build.sh
tar xf /opt/py.tgz -C /opt
chmod +x /tmp/build.sh
bash /tmp/build.sh -s ./ -d /tmp/release --python3-home /opt/py36_e/bin/python3 --app-code opsany-bastion --app-version 1.0.0
```

将打包后的文件下载到本地。

2. 在开发中心上传并部署OpsAny Bastion

打开蓝鲸【开发者中心】->【S-mart应用】->【上传部署新应用】->【上传文件】进行部署。

3. 设置环境变量

```
#自定义修改配置文件
BKAPP_MYSQL_PASSWORD=OpsAny@2020
BKAPP_MYSQL_HOST=192.168.56.11
BKAPP_MYSQL_PORT=3306
BKAPP_REDIS_HOST=192.168.56.11
BKAPP_REDIS_PORT=6379
BKAPP_REDIS_PASSWORD=OpsAny@2020

#执行脚本，讲环境变量写入到PaaS
cd install/
python add_env_blueking.py
```

> 目前Smart的配置优先获取环境变量，当环境变量获取不到时，使用默认配置，所以需要使用脚本写入环境变量。

### 部署堡垒机Websocket容器

堡垒机Websocket是一个独立的服务，默认监听8004端口，使用Docker容器启动，需要准备一台安装了Docker的主机，由于蓝鲸社区版的Docker没有NAT网卡，所以不能复用社区版的主机。需要单独一台安装了Docker的主机。

1. 准备websocket配置文件。

> 配置文件也存放在opsany-bastion项目中。

```
#从配置模板生成配置文件
cd /opt/opsany-bastion/install && cp install.config.example install.config
#设置为蓝鲸社区版的访问域名
DOMAIN_NAME=demo.opsany.com
#设置本机的内网IP地址
LOCAL_IP=192.168.56.11

# 获取上面部署的堡垒机的APP_TOKEN，有时也叫做SECRET_KEY。因为要保证Websocket和Bastion的该值一致，才能通过验证。
BASTION_APP_TOKEN=xxx

#批量修改访问域名和IP地址
sed -i "s/demo.opsany.com/${DOMAIN_NAME}/g" install.config
sed -i "s/192.168.56.11/${LOCAL_IP}/g" install.config

#准备配置文件
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
sed -i "s/73a828d2-0cc1-11ec-bea7-00163e105ceb/${BASTION_APP_TOKEN}/g" ${INSTALL_PATH}/conf/settings_production.py.websocket.init

# 手工检查和修改配置，需要修改APP

vim ${INSTALL_PATH}/conf/settings_production.py.websocket.init
vim ${INSTALL_PATH}/conf/settings_production.py.websocket
```

2. 启动Websocket容器

```
docker run -d --restart=always --name opsany-paas-websocket \
    -p 8004:8004 -v ${INSTALL_PATH}/logs:/opt/opsany/logs \
    -v ${INSTALL_PATH}/uploads:/opt/opsany/uploads \
    -v ${INSTALL_PATH}/conf/settings_production.py.websocket:/opt/opsany/websocket/config/prod.py \
    -v ${INSTALL_PATH}/conf/settings_production.py.websocket.init:/opt/opsany/websocket/config/__init__.py \
    -v /etc/localtime:/etc/localtime:ro \
    opsany/opsany-paas-websocket:v3.2.9
```

3. 进入到Websocket容器里增加hosts

```
docker exec -it opsany-paas-websocket /bin/sh
echo "192.168.1.204 paas.bktencent.com" >>/etc/hosts

```

4. 修改蓝鲸PaaS的Openresty配置，增加以下内容。

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

5. ESB组件的添加：

  - 修改ESB配置文件：

    ```
    # 修改DOMAIN
    将 install/bastion_esb/bastion/toolkit/configs.py line10处，修改成正确的DOMAIN
    ```

  - 将组件移动至目标路径：

    ```
    # 在项目的install/bastion_esb/下有一个bastion目录
    mv bastion/ PAAS_INSTALL_PATH/esb/components/generic/apis/
    ```

  - 页面创建系统，添加组件：

    ```
    打开：http://{DOMAIN}/esb/manager/system/list/，点击添加系统
    系统名称：BASTION
    系统标签：OpsAny堡垒机
    文档分类：默认分类

    打开：http://{DOMAIN}/esb/manager/channel/list/，点击添加通道
    通道名称：获取堡垒机登录用Token
    通道路径：/bastion/get_cache_token/
    所属系统：[BASTION]OpsAny堡垒机
    对应组件代号：generic.bastion.get_cache_token
    API类型：执行API
    ```

  - 创建ESB组件文档，并重启ESB：

    ```
    # 创建组件文档
    source /root/.bkrc
    source $CTRL_DIR/functions
    export BK_ENV=production
    export BK_FILE_PATH=/data/bkce/open_paas/cert/saas_priv.txt
    export PAAS_LOGGING_DIR=/data/bkce/logs/open_paas

    workon open_paas-esb
    python manage.py sync_api_docs

    # 重启ESB
    systemctl restart bk-paas-esb.service
    ```
    
### 堡垒机测试

恭喜您，完成了部署操作，这是一个经典的蓝鲸SAAS的手工部署流程。
