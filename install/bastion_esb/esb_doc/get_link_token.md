#### 获取OpsAny堡垒机登陆Token

- API地址：`/api/c/compapi/bastion/get_cache_token/`

- Method： POST

- 参数说明：

  | 字段            | 类型     | 必选   | 描述                                       |
  | ------------- | ------ | ---- | ---------------------------------------- |
  | bk_app_code   | string | 是    | 应用ID                                     |
  | bk_app_secret | string | 是    | 安全密钥(应用 TOKEN)，可以通过 开发者中心 -> 点击应用ID -> 基本信息 获取 |
  | bk_token      | string | 否    | 当前用户登录态，bk_token与bk_username必须一个有效，bk_token可以通过Cookie获取 |
  | bk_username   | string | 否    | 当前用户用户名，应用免登录态验证白名单中的应用，用此字段指定当前用户       |
  | ip            | string | 是    | 连接主机的IP地址                                |
  | name          | string | 是    | 主机名                                      |
  | ssh_port      | int    | 是    | 连接端口                                     |
  | system_type   | string | 是    | 系统类型：Linux/Windows                       |
  | username      | string | 是    | 登陆主机用户名                                  |
  | password      | string | 是    | 登陆主机密码                                   |

- 返回结果示例：

  ```json
  {
      'code': 200,
      'api_code': 20001,
      'result': true,
      'request_id': 'b3ae5ce6ac324099b5b87d0b6c604fcc',
      'message': '操作成功',
      'data': 'fccda313-5f73-4b41-8dfb-63cf0694ac80'
  }
  ```

  ​