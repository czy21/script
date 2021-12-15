## 工程结构
``` 
script
├── domain
├    ├── db_meta   -- 向各数据库文件脚本 添加前置处理语句及后置处理语句
|    |
├    ├── default   -- python全局构建缺省变量及缺省路径
|    |
├── groovy
├    ├── share     -- jenkins share library
├── server
|    |
├    ├── init      -- linux环境,k8s,docker,ansible初始化脚本
├    ├── utility   -- python工具方法
├    ├── docker    -- 本地构建
|    |    ├── compose
|-   |    |-   ├── frp       -- 点对点内网穿透代理工具
|-   |    |-   ├── hadoop    -- 分布式系统基础架构
|-   |    |-   ├── jenkins   -- 持续交付,自动化,标准化,流程化构建工具
|-   |    |-   ├── kafka     -- 日志收集系统和消息系统
|-   |    |-   ├── mongo     -- NoSQL数据库
|-   |    |-   ├── mssql     -- 关系数据库
|-   |    |-   ├── mysql     -- 关系数据库
|-   |    |-   ├── neo4j     -- 图形数据库
|-   |    |-   ├── nexus     -- maven私服仓库
|-   |    |-   ├── nginx     -- 反向代理web服务器
|-   |    |-   ├── portainer -- docker管理平台
|-   |    |-   ├── rabbitmq  -- 消息中间件
|-   |    |-   ├── redis     -- key-value存储
|-   |    |-   ├── storm     -- 大数据实时计算组件
├    ├── chart -- helm chart
|    |    ├── app 应用
|-   |    |-   ├──
|    |    ├── ops k8s集群监控,NFS数据卷挂载
├    ├── omv       -- openmediavalut nas
├    ├── raspberry -- 树莓派
├    ├── syno      -- 群晖
```