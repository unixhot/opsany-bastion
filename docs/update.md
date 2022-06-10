# 生产环境更新部署

更新OpsAny堡垒机需要以下3个步骤。

- 更新最新代码
- 构建SAAS安装包
- 构建Websocket镜像

## 直接使用官方提供的包部署

- https://opsany-saas.oss-cn-beijing.aliyuncs.com/opsany-bastion_V1.2.3.tar.gz
- registry.cn-beijing.aliyuncs.com/opsany/opsany-bk-websocket:v1.2.3

## 自己手工构建部署

需要先将堡垒机打包为蓝鲸Smart应用的包，然后就可以直接在开发者中心上传部署。

### 构建并部署SAAS包

1. 更新之前克隆的代码并打包。

```
cd /opt/opsany-bastion && git pull
wget -c http://bkopen-1252002024.file.myqcloud.com/common/py36_e.tgz -O /opt/py.tgz
/bin/cp install/build.sh /tmp/build.sh
tar xf /opt/py.tgz -C /opt
chmod +x /tmp/build.sh
APP_VERSION=1.2.3
cd /opt/opsany-bastion && bash /tmp/build.sh -s ./ -d /tmp/release --python3-home /opt/py36_e/bin/python3 --app-code opsany-bastion --app-version $APP_VERSION
```

打包后的文件在/tmp/release目录下，将打包后的文件下载到本地。

```
ls /tmp/release/
opsany-bastion_V1.2.3.tar.gz
```

2. 在开发中心上传并部署OpsAny Bastion

打开蓝鲸【开发者中心】->【S-mart应用】，找到部署的opsany-bastion，点击操作中的【部署】。

![更新截图](./static/bastion-update.png)

上传完毕之后，点击【发布部署】，选择【生产环境】可以进行部署更新。

![部署截图](./static/bastion-deploy.png)


### 替换Websocket容器

1. 停止老版本websocket容器

```
docker stop opsany-bk-websocket && docker rm opsany-bk-websocket
```

2. 启动新的Websocket容器

```
INSTALL_PATH=/data/bkce/opsany-bastion

docker run -d --restart=always --name opsany-bk-websocket \
    -p 8004:8004 -v ${INSTALL_PATH}/logs:/opt/opsany/logs \
    -v ${INSTALL_PATH}/uploads:/opt/opsany/uploads \
    -v ${INSTALL_PATH}/conf/settings_production.py.websocket:/opt/opsany/websocket/config/prod.py \
    -v ${INSTALL_PATH}/conf/settings_production.py.websocket.init:/opt/opsany/websocket/config/__init__.py \
    -v /etc/localtime:/etc/localtime:ro \
    -v /usr/share/zoneinfo:/usr/share/zoneinfo \
    registry.cn-beijing.aliyuncs.com/opsany/opsany-bk-websocket:v1.2.3
```

3. 进入到Websocket容器里增加hosts

需要保证Websocket能和PAAS进行通信，需要绑定hosts，访问到PAAS的Nginx的内网IP地址。请自行进行修改。

```
docker exec -it opsany-bk-websocket /bin/sh
echo "10.0.1.65 ce.bktencent.com" >>/etc/hosts
```

### 堡垒机测试

恭喜您，完成了部署操作，这是一个经典的蓝鲸SAAS的手工部署流程。
