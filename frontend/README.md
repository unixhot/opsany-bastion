###堡垒机前端工程
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
