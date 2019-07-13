# Lucky
- **Lucky自动化测试平台**
  - [Lucky自动化测试平台是个啥？](https://github.com/xwsftst/Lucky/new/master?readme=1#lucky%E8%87%AA%E5%8A%A8%E5%8C%96%E6%B5%8B%E8%AF%95%E5%B9%B3%E5%8F%B0%E6%98%AF%E4%B8%AA%E5%95%A5)
  - [平台特点](https://github.com/xwsftst/Lucky/new/master?readme=1#%E5%B9%B3%E5%8F%B0%E7%89%B9%E7%82%B9)
  - [采用了哪些开源技术和框架？](https://github.com/xwsftst/Lucky/new/master?readme=1#%E9%87%87%E7%94%A8%E4%BA%86%E5%93%AA%E4%BA%9B%E5%BC%80%E6%BA%90%E6%8A%80%E6%9C%AF%E5%92%8C%E6%A1%86%E6%9E%B6)
  - [mysql安装与配置](https://github.com/xwsftst/Lucky/new/master?readme=1#mysql%E5%AE%89%E8%A3%85%E4%B8%8E%E9%85%8D%E7%BD%AE)
  - [Lucky下载及安装依赖](https://github.com/xwsftst/Lucky/new/master?readme=1#lucky%E4%B8%8B%E8%BD%BD%E5%8F%8A%E5%AE%89%E8%A3%85%E4%BE%9D%E8%B5%96)
  - [配置文件及相关环境配置说明](https://github.com/xwsftst/Lucky/new/master?readme=1#%E9%85%8D%E7%BD%AE%E6%96%87%E4%BB%B6%E5%8F%8A%E7%9B%B8%E5%85%B3%E7%8E%AF%E5%A2%83%E9%85%8D%E7%BD%AE%E8%AF%B4%E6%98%8E)
  - [Lucky的初始化](https://github.com/xwsftst/Lucky/new/master?readme=1#lucky%E7%9A%84%E5%88%9D%E5%A7%8B%E5%8C%96)
  - [内外网的访问和运行](https://github.com/xwsftst/Lucky/new/master?readme=1#%E5%86%85%E5%A4%96%E7%BD%91%E7%9A%84%E8%AE%BF%E9%97%AE%E5%92%8C%E8%BF%90%E8%A1%8C)
  - [如何支持不同的浏览器](https://github.com/xwsftst/Lucky/new/master?readme=1#%E5%A6%82%E4%BD%95%E6%94%AF%E6%8C%81%E4%B8%8D%E5%90%8C%E7%9A%84%E6%B5%8F%E8%A7%88%E5%99%A8)
  - [功能截图](https://github.com/xwsftst/Lucky/new/master?readme=1#%E5%8A%9F%E8%83%BD%E6%88%AA%E5%9B%BE)
  - [web测试流程示例截图](https://github.com/xwsftst/Lucky/new/master?readme=1#web%E6%B5%8B%E8%AF%95%E6%B5%81%E7%A8%8B%E7%A4%BA%E4%BE%8B%E6%88%AA%E5%9B%BE)
  - [api接口测试流程示例截图](https://github.com/xwsftst/Lucky/new/master?readme=1#api%E6%8E%A5%E5%8F%A3%E6%B5%8B%E8%AF%95%E6%B5%81%E7%A8%8B%E7%A4%BA%E4%BE%8B%E6%88%AA%E5%9B%BE)  

## Lucky自动化测试平台是个啥？  
Lucky自动化测试平台是一个开源自动化测试解决方案，基于RobotFramework进行二次开发，支持RobotFramework几乎所有的库，目前可进行web测试、app测试和api测试，也具有定时任务、测试结果邮件发送等功能。  

## 平台特点  
1. 支持Mac、Linux、windows平台
2. 支持Chrome、IE、Edge、Firefox、Safari、HtmlUnitDriver、PhantomJS、Appium、Requests HTTP
3. 支持与selenium-grid集成做分布式测试

## 采用了哪些开源技术和框架？
1. Python3
2. Flask
3. Robotframework
4. EasyUI
5. Chartjs
6. SQLAlchemy
7. PyMysql
8. Requests
9. Selenium3
10. Appium-Python-Client  
等技术相关的插件或技术包  

## mysql安装与配置  
先安装mysql数据库，使用utf-8字符编码新增autoline数据库  
修改.env中关于数据库的配置，如下：  
```
    ENGINE = 'mysql'
    DRIVER = 'pymysql'
    USER = 'root'
    PASSWORD = 'xxxxxxxx'
    HOST = 'localhost'
    PORT = '3306'
    NAME = 'db_name'

    SQLALCHEMY_DATABASE_URI = '{}+{}://{}:{}@{}:{}/{}'.format(ENGINE, DRIVER, USER, PASSWORD, HOST, PORT, NAME)
    TRIGGER_DATABASE_URL = '{}+{}://{}:{}@{}:{}/{}'.format(ENGINE, DRIVER, USER, PASSWORD, HOST, PORT, NAME)
```  

## Lucky下载及安装依赖  
git下载Lucky工程, 在Lucky根目录下有requirements.txt文件，该文件包含了所有依赖的包，安装好Python3并确保Python3的pip可用，使用以下命令安装Lucky依赖库  
> pip install requirements.txt  

## 配置文件及相关环境配置说明  
```
    DEBUG = True
    TESTING = False
    SECRET_KEY = 'JWH3h463237HTL37'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    FLASKY_ADMIN = 'xxx@126.com'

    TRIGGER = None
    RUNNERS = []

    MAIL_SERVER = 'smtp.126.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'xxx@126.com'
    MAIL_PASSWORD = 'xxxxxx'
    FLASKY_MAIL_SUBJECT_PREFIX = '[Lucky]'
    FLASKY_MAIL_SENDER = 'xxx<xxx@126.com>'
    MAIL_RECIPIENTS = ['xxx@126.com', 'xxxx@qq.com']
```  
**需要注意的还有几点：**  
1. 发送邮件如出现Ascii编码问题“ordinal not in range(128)”， 可以将虚拟环境Lib中smtplib.py第855行中的编码设置由ascii改为utf-8
2.此外虚拟环境的Lib/site-package/SleniumLibrary/utils/seleniumversion.py中“major, minor, micro = int(major), int(minor), int(micro)”应改为“major, minor, micro = int(major), int(minor), micro”  

## Lucky的初始化  
配置好上述配置后按照如下步骤进行初始化操作：  
1. 初始化数据库  
> python manage.py db init  
> python manage.py db migrate  
> python manage.py db upgrade  
2. 初始化数据  
> python manage.py deploy  

## 内外网的访问和运行  
1. 内网运行访问  
> python manage.py runserver  

然后打开浏览器访问：http://127.0.0.1:5000即可  

2. 外网运行访问  
> python manage.py runserver -h 0.0.0.0 -p 8000  

-h 用于指定ip（ip指定为0.0.0.0即可自定绑定本机IP）  
-p 指定端口号  

之后在其他设备通过： http://ip:8000 就可以访问Lucky自动化测试平台了  

![图片](https://github.com/xwsftst/Lucky/blob/master/guide/images/login.png?raw=true)  
使用admin/123456的默认超级管理员账号登录系统  
![图片](https://github.com/xwsftst/Lucky/blob/master/guide/images/home.png?raw=true)  

## 如何支持不同的浏览器 
对于浏览器支持，下载相应的driver放到python环境变量目录下即可  

chrome驱动：http://npm.taobao.org/mirrors/chromedriver/

firefox驱动：http://npm.taobao.org/mirrors/geckodriver/

Microsofe Edge驱动：https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/  

Safari驱动：https://webkit.org/blog/6900/webdriver-support-in-safari-10/  

Opera驱动：http://npm.taobao.org/mirrors/operadriver/  

PhantomJS驱动：http://phantomjs.org/releases.html  

HtmlUnit驱动：https://sourceforge.net/projects/htmlunit/files/htmlunit/  

## 功能截图
debug和运行项目，debug是用于检查用例步骤是否正确  
![图片](https://github.com/xwsftst/Lucky/blob/master/guide/images/run.png?raw=true)  
产品管理  
![图片](https://github.com/xwsftst/Lucky/blob/master/guide/images/product.png?raw=true)  
项目管理  
![图片](https://github.com/xwsftst/Lucky/blob/master/guide/images/project.png?raw=true)  
任务调度  
![图片](https://github.com/xwsftst/Lucky/blob/master/guide/images/scheduler.png?raw=true)  
用户管理  
![图片](https://github.com/xwsftst/Lucky/blob/master/guide/images/user.png?raw=true)  
关键字文档  
![图片](https://github.com/xwsftst/Lucky/blob/master/guide/images/key_help.png?raw=true)  
测试报告  
![图片](https://github.com/xwsftst/Lucky/blob/master/guide/images/report.png?raw=true)  
运行日志  
![图片](https://github.com/xwsftst/Lucky/blob/master/guide/images/log.png?raw=true)  
## web测试流程示例截图  
### 1、创建对象集  
![图片](https://github.com/xwsftst/Lucky/blob/master/guide/images/obj.png?raw=true)  
### 2、创建对象  
![图片](https://github.com/xwsftst/Lucky/blob/master/guide/images/web_var1.png?raw=true)  
![图片](https://github.com/xwsftst/Lucky/blob/master/guide/images/web_var2.png?raw=true)  
![图片](https://github.com/xwsftst/Lucky/blob/master/guide/images/web_var3.png?raw=true)  
![图片](https://github.com/xwsftst/Lucky/blob/master/guide/images/web_var4.png?raw=true)  
![图片](https://github.com/xwsftst/Lucky/blob/master/guide/images/web_var5.png?raw=true)  
![图片](https://github.com/xwsftst/Lucky/blob/master/guide/images/web_var6.png?raw=true)  
### 3、创建测试套件  
![图片](https://github.com/xwsftst/Lucky/blob/master/guide/images/suite.png?raw=true)  
### 4、创建测试用例  
![图片](https://github.com/xwsftst/Lucky/blob/master/guide/images/case.png?raw=true)  
### 5、创建测试步骤  
![图片](https://github.com/xwsftst/Lucky/blob/master/guide/images/web_step1.png?raw=true)  
![图片](https://github.com/xwsftst/Lucky/blob/master/guide/images/web_step2.png?raw=true)  
![图片](https://github.com/xwsftst/Lucky/blob/master/guide/images/web_step3.png?raw=true)  
![图片](https://github.com/xwsftst/Lucky/blob/master/guide/images/web_step4.png?raw=true)  
![图片](https://github.com/xwsftst/Lucky/blob/master/guide/images/web_step5.png?raw=true)  
![图片](https://github.com/xwsftst/Lucky/blob/master/guide/images/web_step6.png?raw=true)  
![图片](https://github.com/xwsftst/Lucky/blob/master/guide/images/web_step7.png?raw=true)  
![图片](https://github.com/xwsftst/Lucky/blob/master/guide/images/web_step8.png?raw=true)  
![图片](https://github.com/xwsftst/Lucky/blob/master/guide/images/web_step9.png?raw=true)  
![图片](https://github.com/xwsftst/Lucky/blob/master/guide/images/web_step10.png?raw=true)  
## app测试流程示例截图  
### 测试步骤：  
![图片](https://github.com/xwsftst/Lucky/blob/master/guide/images/app_step1.png?raw=true)  
![图片](https://github.com/xwsftst/Lucky/blob/master/guide/images/app_step2.png?raw=true)  
![图片](https://github.com/xwsftst/Lucky/blob/master/guide/images/app_step3.png?raw=true)  
![图片](https://github.com/xwsftst/Lucky/blob/master/guide/images/app_step4.png?raw=true)  
![图片](https://github.com/xwsftst/Lucky/blob/master/guide/images/app_step5.png?raw=true)  
![图片](https://github.com/xwsftst/Lucky/blob/master/guide/images/app_step6.png?raw=true)  
![图片](https://github.com/xwsftst/Lucky/blob/master/guide/images/app_step7.png?raw=true)  
## api接口测试流程示例截图  
### 测试步骤：  
![图片](https://github.com/xwsftst/Lucky/blob/master/guide/images/api_step1.png?raw=true)  
![图片](https://github.com/xwsftst/Lucky/blob/master/guide/images/api_step2.png?raw=true)  
![图片](https://github.com/xwsftst/Lucky/blob/master/guide/images/api_step3.png?raw=true)  
![图片](https://github.com/xwsftst/Lucky/blob/master/guide/images/api_step4.png?raw=true)  
![图片](https://github.com/xwsftst/Lucky/blob/master/guide/images/api_step5.png?raw=true)  
![图片](https://github.com/xwsftst/Lucky/blob/master/guide/images/api_step6.png?raw=true)  
![图片](https://github.com/xwsftst/Lucky/blob/master/guide/images/api_step7.png?raw=true)  
![图片](https://github.com/xwsftst/Lucky/blob/master/guide/images/api_step8.png?raw=true)  
![图片](https://github.com/xwsftst/Lucky/blob/master/guide/images/api_step9.png?raw=true)  
