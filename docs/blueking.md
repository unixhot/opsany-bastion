# 生产环境部署

- 方案一： 直接部署OpsAny社区版(官方文档)[https://docs.opsany.com/]【适合所有用户】
- 方案二： 在蓝鲸社区版的基础上快速部署OpsAny堡垒机【适合对于腾讯蓝鲸特别熟悉的用户】

## 方案二：蓝鲸社区版部署OpsAny开源堡垒机

OpsAny Bastion是基于开源的bk-paas编写的SaaS，目前测试通过修改可以兼容蓝鲸社区版和企业版。但是当前由于bk-paas和社区版的paas不一致，有一些需要手工调整。

> 建议使用手工部署，可以了解和掌握堡垒机的部署和运行方式。

### 创建堡垒机数据库

1. 获取当前蓝鲸社区版的MySQL和Redis密码

```
[root@VM-16-3-centos install]# grep "BK_PAAS_MYSQL_PASSWORD" /data/install/bin/01-generate/paas.env
BK_PAAS_MYSQL_PASSWORD='IPQWfLZf6APE'
[root@VM-16-3-centos install]# grep "BK_PAAS_REDIS_PASSWORD" /data/install/bin/01-generate/paas.env
BK_PAAS_REDIS_PASSWORD=DRwsgTKXUsEY
```

> 如果你没有修改过蓝鲸社区版的MySQL和Redis的密码，可以从以上文件中获取。OpsAny堡垒机需要使用MySQL和Redis，建议直接使用蓝鲸社区版自带的。


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
cd /opt && git clone https://github.com/unixhot/opsany-bastion.git
wget -c http://bkopen-1252002024.file.myqcloud.com/common/py36_e.tgz -O /opt/py.tgz
wget -c https://raw.githubusercontent.com/shpdnkti/saas-builder/main/build.sh -O /tmp/build.sh
tar xf /opt/py.tgz -C /opt
chmod +x /tmp/build.sh
cd /opt/opsany-bastion && bash /tmp/build.sh -s ./ -d /tmp/release --python3-home /opt/py36_e/bin/python3 --app-code opsany-bastion --app-version 1.2.1
```

将打包后的文件下载到本地。

2. 在开发中心上传并部署OpsAny Bastion

打开蓝鲸【开发者中心】->【S-mart应用】->【上传部署新应用】->【上传文件】进行部署。

3. 部署完毕之后，点击opsany-bastion应用名称，进入到应用详情，点击环境变量，请根据实际情况修改下面的值。

```
#自定义修改后执行
MYSQL_PASSWORD=上面获取到的MySQL密码
MYSQL_HOST=mysql-default.service.consul
MYSQL_PORT=3306
REDIS_HOST=redis.service.consul
REDIS_PORT=6379
REDIS_PASSWORD=上面获取到的Redis密码
```

添加完毕之后，点击【发布部署】-【正式环境】进行部署操作，会自动重启堡垒机服务，使设置的环境变量。

4. 初始化IAM

- 设置环境变量

```
#自定义修改后执行
export BK_IAM_V3_INNER_HOST=http://bkiam.service.consul:5001   #请修改为正确配置，这个是默认值。
export APP_ID=opsany-bastion #请不要修改此配置，APP_ID是固定的，不允许修改。
export APP_TOKEN=b7d83351-0f0a-4918-adaa-a4860bc2fced #请修改为正确的配置,可以在开发中心，S-Mart应用，查看opsany-bastion详情可以获取到。
export BK_PAAS_HOST=https://ce.bktencent.com #请修改为正确的配置，你当前部署的蓝鲸的访问地址。
```

- 执行脚本进行初始化
```
cd /opt/opsany-bastion/install/init_iam
python3 init_iam_system.py
python3 init_action.py
```

> 如何可以正常打开所有的堡垒机页面，就证明部署正常，接下来需要部署底层的Websocket服务，用于Web SSH。

---

### 部署堡垒机Websocket容器

堡垒机Websocket是一个独立的服务，默认监听8004端口，使用Docker容器启动，需要准备一台安装了Docker的主机，由于蓝鲸社区版的运行SAAS的Docker没有NAT网卡，所以需要单独一台安装了Docker的主机。

1. 准备websocket配置文件。

> 配置文件也存放在opsany-bastion项目中。

```
#克隆项目代码
cd /opt && git clone https://github.com/unixhot/opsany-bastion.git
#从配置模板生成配置文件
cd /opt/opsany-bastion/install && cp install.config.example install.config
#设置为蓝鲸社区版的访问域名
DOMAIN_NAME=demo.opsany.com
#设置本机的内网IP地址
LOCAL_IP=192.168.56.11

# 获取上面部署的堡垒机的APP_TOKEN，有时也叫做SECRET_KEY。因为要保证Websocket和Bastion的该值一致，才能通过验证。由于蓝鲸社区版上传部署后是自动生成SECRET_KEY，可以打开【开发中心】-【S-Mart应用】-【OpsAny-bastion】，点击对应的应用名称，即可打开详情页面。

[root@VM-1-52-centos ~]# BASTION_APP_TOKEN=

#批量修改访问域名和IP地址
[root@VM-1-52-centos ~]# sed -i "s/demo.opsany.com/${DOMAIN_NAME}/g" install.config
[root@VM-1-52-centos ~]# sed -i "s/192.168.56.11/${LOCAL_IP}/g" install.config

#准备配置文件
source install.config
mkdir -p ${INSTALL_PATH}/{conf,uploads}
mkdir -p ${INSTALL_PATH}/uploads/guacamole
/bin/cp conf/settings_production.py.websocket ${INSTALL_PATH}/conf/
/bin/cp conf/settings_production.py.websocket.init ${INSTALL_PATH}/conf/

# Websocket
sed -i "s/WEBSOCKET_GUACD_HOST/${WEBSOCKET_GUACD_HOST}/g" ${INSTALL_PATH}/conf/settings_production.py.websocket
sed -i "s/REDIS_SERVER_HOST/${REDIS_HOST}/g" ${INSTALL_PATH}/conf/settings_production.py.websocket
sed -i "s/REDIS_SERVER_PASSWORD/${REDIS_PASSWORD}/g" ${INSTALL_PATH}/conf/settings_production.py.websocket
sed -i "s/REDIS_SERVER_PORT/${REDIS_PORT}/g" ${INSTALL_PATH}/conf/settings_production.py.websocket
sed -i "s/MYSQL_SERVER_HOST/${MYSQL_HOST}/g" ${INSTALL_PATH}/conf/settings_production.py.websocket
sed -i "s/MYSQL_SERVER_PORT/${MYSQL_PORT}/g" ${INSTALL_PATH}/conf/settings_production.py.websocket
sed -i "s/MYSQL_BASTION_PASSWORD/${MYSQL_BASTION_PASSWORD}/g" ${INSTALL_PATH}/conf/settings_production.py.websocket
sed -i "s/demo.opsany.com/${PAAS_DOMAIN_NAME}/g" ${INSTALL_PATH}/conf/settings_production.py.websocket.init
sed -i "s/73a828d2-0cc1-11ec-bea7-00163e105ceb/${BASTION_APP_TOKEN}/g" ${INSTALL_PATH}/conf/settings_production.py.websocket.init

# 手工检查和修改配置，需要修改APP

vim ${INSTALL_PATH}/conf/settings_production.py.websocket.init
vim ${INSTALL_PATH}/conf/settings_production.py.websocket
```

2. 安装Docker，并启动Websocket容器

- 安装Docker

```
curl -o /etc/yum.repos.d/docker-ce.repo https://mirrors.aliyun.com/docker-ce/linux/centos/docker-ce.repo
yum install -y git wget docker-ce python3 python3-pip
systemctl enable --now docker
```

- 启动Websocket容器
```
docker run -d --restart=always --name opsany-bk-websocket \
    -p 8004:8004 -v ${INSTALL_PATH}/logs:/opt/opsany/logs \
    -v ${INSTALL_PATH}/uploads:/opt/opsany/uploads \
    -v ${INSTALL_PATH}/conf/settings_production.py.websocket:/opt/opsany/websocket/config/prod.py \
    -v ${INSTALL_PATH}/conf/settings_production.py.websocket.init:/opt/opsany/websocket/config/__init__.py \
    -v /etc/localtime:/etc/localtime:ro \
    -v /usr/share/zoneinfo:/usr/share/zoneinfo \
    ${PAAS_DOCKER_REG}/opsany-bk-websocket:v1.2.1
```

- 启动Guacd容器

```
docker run -d --restart=always --name opsany-paas-guacd \
    -p 4822:4822 \
    -v ${INSTALL_PATH}/uploads/guacamole:/srv/guacamole \
    -v /etc/localtime:/etc/localtime:ro \
    ${PAAS_DOCKER_REG}/guacd:1.2.0
```

3. 进入到Websocket容器里增加hosts

需要保证Websocket能和PAAS进行通信，需要绑定hosts，访问到PAAS的Nginx的内网IP地址。

```
docker exec -it opsany-bk-websocket /bin/sh
echo "10.0.1.65 ce.bktencent.com" >>/etc/hosts
```

4. 修改蓝鲸PaaS的Openresty配置，增加以下内容。

```
[root@VM-1-65-centos ~]# cd /data/install/support-files/templates/nginx/
[root@VM-1-65-centos nginx]# vim paas.conf

#修改为websocket的地址
upstream OPEN_PAAS_CONSOLE {
    {{ range service "paas-console" }}server {{ .Address }}:{{ .Port }} max_fails=1 fail_timeout=30s;
    {{else}}server 127.0.0.1:8004;{{ end }}
#将127.0.0.1修改为运行WebSocket主机的IP地址。

}

# OpsAny Bastion WebSocket
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

# 重新生成Nginx配置    
systemctl reload consul-template
```

### 堡垒机测试

恭喜您，完成了部署操作，这是一个经典的蓝鲸SAAS的手工部署流程。
