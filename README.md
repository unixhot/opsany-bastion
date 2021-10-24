# OpsAny堡垒机

【部署脚本准备中，预计月底发布，一键部署脚本】

opsany-bastion是OpsAny产品系列中首个开源的项目，使用Apache2.0开源协议。

opsany-bastion使用Python开发，遵循Web2.0规范，使用Web socket Terminal解决方案，具备完整的权限控制体系和
严谨的审计方案。

## 优势

- 开源：线上快速部署和安装。
- 无插件：仅需浏览器即可使用，推荐使用Google Chrome。
- 多云支持：支持同时管理多云资产。

## 安装方法：

- 环境：

  - CentOS 7
  - Python 3.6.8
  - Supervisord 3.4.0

- 安装部署：

  - 将项目文件放置在`/opt/bastion/`

  - 安装相应依赖

    ```
    [root@opsany ~]# cd /opt/
    [root@opsany opt]# mkdir bastion-runtime
    [root@opsany bastion-runtime]# python3 -m venv /opt/bastion-runtime/
    [root@opsany bastion-runtime]# source bin/activate
    (bastion-runtime) [root@opsany opt]# pip install -r /opt/bastion-backend/requirements.txt
    ```

  - 书写Supervisord配置文件：

    - supervisord.conf：

      ```
      [program: bastion_uwsgi]
      command = /opt/bastion-runtime/bin/uwsgi --ini /opt/bastion/bastion.ini
      stdout_logfile = /opt/bastion/logs/uwsgi.log
      redirect_stderr = true
      autorestart = true
      stopsignal = QUIT
      environment = BK_ENV="production",BK_LOG_DIR="/opt/bastion/logs/",BK_PAAS_INNER_HOST="http://",APP_ID="bastion",BK_PAAS_HOST="https://",APP_TOKEN="",BK_CC_HOST="https://",BK_JOB_HOST="https://"
      ```

    - bastion.ini:

      ```
      logdate = true
      log-format = [%(addr)] [%(ctime)] [%(method)] [%(uri)] [%(proto)] [%(status)] [%(msecs)] [%(referer)] [%(uagent)]
      
      memory-report = true
      
      master = true
      vacuum = true
      
      chdir = /opt/bastion/bastion-backend
      module = wsgi:application
      
      #cheaper = 4
      #cheaper-initial = 4
      
      #workers = 4
      processes = 4
      threads = 2
      #cheaper-algo = busyness
      #cheaper-overload = 5
      #cheaper-step = 2
      #cheaper-busyness-multiplier = 60
      
      #buffer-size = 8192
      #post-buffering = 8192
      
      max-requests = 1024
      mount = /t/bastion=wsgi.py
      manage-script-name = true
      ```

    - websocket.ini：

      ```
      [program:websocket]
      command=/opt/bastion-runtime/bin/daphne --proxy-headers -b 0.0.0.0 -p 8004 asgi:application
      directory=/opt/bastion/bastion-backend
      environment=BK_ENV="production",BK_LOG_DIR="/opt/opsany/logs",APP_ID="bastion",BK_PAAS_HOST="https://",APP_TOKEN=""
      startsecs=0
      stopwaitsecs=0
      autostart=true
      autorestart=true
      redirect_stderr=true
      stdout_logfile=/opt/bastion/logs/websocket.log
      ```

    - 声明：需要补齐APP_TOKEN，BK_PAAS_HOST，或使用PaaS部署，即可忽略uwsgi的supervisord配置，仅需配置websocket的内容即可

  - 启动：

    ```
    [root@opsany bastion]# supervisorctl reload
    ```

#### 目录结构

- 本项目基于蓝鲸SaaS开发框架进行开发，框架代码内容概不介绍，仅介绍本项目所用内容

  ```
  ├── bastion										# 主要业务逻辑代码目录
  │   ├── admin.py
  │   ├── apps.py
  │   ├── audit									# 审计类API目录
  │   │   ├── audit_views.py
  │   │   └── __init__.py
  │   ├── component								# 业务组件目录
  │   │   ├── audit.py
  │   │   ├── common.py
  │   │   ├── core.py
  │   │   ├── credential.py
  │   │   ├── __init__.py
  │   │   ├── resource.py
  │   │   ├── strategy.py
  │   │   └── strategy_v2.py
  │   ├── core									# 堡垒机核心组件
  │   │   ├── consumers.py
  │   │   ├── guacamole
  │   │   │   ├── client.py
  │   │   │   ├── component.py
  │   │   │   ├── exceptions.py
  │   │   │   ├── __init__.py
  │   │   │   └── instruction.py
  │   │   ├── __init__.py
  │   │   ├── status_code.py
  │   │   ├── terminal
  │   │   │   ├── component.py
  │   │   │   └── __init__.py
  │   │   └── views.py
  │   ├── credential								# 凭证类API目录
  │   │   ├── credential_views.py
  │   │   └── __init__.py
  │   ├── forms									# form表单目录
  │   │   ├── core_form.py
  │   │   ├── forms.py
  │   │   ├── __init__.py
  │   │   ├── strategy_from.py
  │   │   └── strategy_v2_form.py
  │   ├── __init__.py
  │   ├── migrations
  │   │   ├── 0001_initial.py
  │   │   └── __init__.py
  │   ├── models.py								# 项目模型
  │   ├── resource								# 资源类API目录
  │   │   ├── __init__.py
  │   │   └── resource_views.py
  │   ├── routing.py								# Webscocket路由文件
  │   ├── strategy								# 策略类API目录
  │   │   ├── __init__.py
  │   │   ├── views.py
  │   │   └── views_v2.py
  │   ├── tests.py
  │   ├── urls.py									# 基础路由文件
  │   ├── utils									# 常用工具目录
  │   │   ├── base_model.py
  │   │   ├── base_views.py
  │   │   ├── constants.py
  │   │   ├── decorator.py
  │   │   ├── encryption.py
  │   │   ├── esb_api.py
  │   │   ├── __init__.py
  │   │   ├── init_script.py
  │   │   ├── middleware.py
  │   │   └── status_code.py
  │   └── views.py
  ├── config										# 项目配置文件目录
  │   ├── default.py
  │   ├── dev.py
  │   ├── __init__.py
  │   ├── prod.py
  │   └── stag.py
  ├── index										# 调取前端入口html APP
  │   ├── admin.py
  │   ├── apps.py
  │   ├── __init__.py
  │   ├── migrations
  │   │   └── __init__.py
  │   ├── models.py
  │   ├── tests.py
  │   ├── urls.py
  │   └── views.py
  ├── manage.py
  ├── README.md
  ├── requirements.txt
  ├── runtime.txt
  ├── app.yml
  ├── asgi.py
  ├── settings.py
  ├── static
  ├── templates
  │   └── index.html
  ├── urls.py
  ├── VERSION
  └── wsgi.py
  ```

#### 堡垒机前端工程

- 安装依赖

```
npm i
```

- 启动本地服务

```
npm run serve
```

- 打包

```
npm run build
```

- 目录结构

```
├── public
│   └── logo.png             # LOGO
|   └── index.html           # Vue 入口模板
|   └── css                  # 静态css
|   └── js          	     # 静态js
├── src
│   ├── api                  # Api ajax 等
│   ├── assets               # 本地静态资源
│   ├── config               # 项目基础配置，包含路由，全局设置
│   ├── components           # 业务通用组件
│   ├── core                 # 项目引导, 全局配置初始化，依赖包引入等
│   ├── router               # Vue-Router
│   ├── store                # Vuex
│   ├── utils                # 工具库
│   ├── locales              # 国际化资源 项目中暂时没有用到
│   ├── views                # 业务页面入口和常用模板
│   ├── App.vue              # Vue 模板入口
│   └── main.js              # Vue 入口 JS
│   └── permission.js        # 路由守卫(路由权限控制)
│   └── global.less          # 全局样式
├── tests                    # 测试工具
├── README.md
└── package.json
└── vue.config.js
```
