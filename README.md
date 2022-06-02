## Flask后端基础教程项目

### 本教程项目涉及技术文档
**Flask**：[官方文档中文翻译](https://dormousehole.readthedocs.io/en/latest/)

**Mysql-Connector-Python**：[官方文档](https://dev.mysql.com/doc/connector-python/en/)

**Gravatar**：[官网](https://cn.gravatar.com/)

### 这个项目是什么？
本教程项目仿照的是Gravatar的功能所实现的一个基础的后端，只有后端，没有前端。
目前所实现的接口有：
- 登录
- 登出
- 注册
- 查看用户信息
- 通过USER_HASH获取头像
- 修改个人头像

### 什么是Gravatar？
请自行查阅Gravatar官网以及教程。
[Gravatar官网](https://cn.gravatar.com/)

### How to start?
请准备一下软件：
- Python3.6+
- Pycharm
- 任一一款可以用来调试API接口的工具，如：Postman, Apifox, 甚至你想用`curl`也可以
- 网络

#### 环境搭建

- 克隆项目

    1. cd到想要存放项目目录的位置
    2. 执行克隆操作，`git clone https://github.com/myzhbit/Flask_Backend_Tutorial.git`

- 准备虚拟Python环境

    1. 使用主Python安装virtualenv，如：`pip install virtualenv`
    2. 在项目目录执行`virtualenv venv`，创建一个虚拟Python环境
    3. 在命令行中切换到虚拟Python环境
       1. CMD: cd到venv目录下的Scripts目录下，执行`activate`
       2. Bash: `source venv/Scripts/activate`
    4. 在虚拟Python环境中安装依赖，如：`pip install -r requirements.txt`
    
    **如果这一步的pip安装缓慢，请自行百度切换pip源**

- 配置项目

    1. 按照`etc/config.py.sample`的样式配置`etc/config.py`

#### 启动项目
使用Pycharm启动main.py，项目即在本地的5000端口上启动。随后请查看项目代码以及搭配接口调试工具进行学习。