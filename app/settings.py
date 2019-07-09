def get_db_uri(dbinfo):
    ENGINE = dbinfo.get('ENGINE') or 'mysql'
    DRIVER = dbinfo.get('DRIVER') or 'pymysql'
    USER = dbinfo.get('USER') or 'root'
    PASSWORD = dbinfo.get('PASSWORD') or 'xws123456'
    HOST = dbinfo.get('HOST') or 'localhost'
    PORT = dbinfo.get('PORT') or '3306'
    NAME = dbinfo.get('NAME') or 'LuckyDevelop'

    return '{}+{}://{}:{}@{}:{}/{}'.format(ENGINE, DRIVER, USER, PASSWORD, HOST, PORT, NAME)


class Config:
    DEBUG = True
    TESTING = False
    SECRET_KEY = 'JWH3h463237HTL37'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    FLASKY_ADMIN = 'xwsftst@126.com'

    TRIGGER = None
    RUNNERS = []

    MAIL_SERVER = 'smtp.126.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'xwsftst@126.com'
    MAIL_PASSWORD = 'yahong940316'
    FLASKY_MAIL_SUBJECT_PREFIX = '[Lucky]'
    FLASKY_MAIL_SENDER = 'xwsftst<xwsftst@126.com>'
    MAIL_RECIPIENTS = ['xwsftst@126.com', '739650977@qq.com']

    @classmethod
    def init_app(cls, app):
        Config.init_app(app)

        # 发送初始化错误信息给管理员
        import logging
        from logging.handlers import SMTPHandler
        credentials = None
        secure = None
        if getattr(cls, 'MAIL_USERNAME', None) is not None:
            credentials = (cls.MAIL_USERNAME, cls.MAIL_PASSWORD)
            if getattr(cls, 'MAIL_USE_TLS', None):
                secure = ()

        mail_handler = SMTPHandler(
            mailhost=(cls.MAIL_SERVER, cls.MAIL_PORT),
            fromaddr=cls.FLASKY_MAIL_SENDER,
            toaddrs=[cls.FLASKY_ADMIN],
            subject=cls.FLASKY_MAIL_SUBJECT_PREFIX + ' Lucky Startup Error',
            credentials=credentials,
            secure=secure)

        mail_handler.setLevel(logging.ERROR)
        app.logger.addHandler(mail_handler)


class DevelopConfig(Config):
    DEBUG = True
    DATABASE = {
        'ENGINE': 'mysql',
        'DRIVER': 'pymysql',
        'USER': 'root',
        'PASSWORD': 'xws123456',
        'HOST': 'localhost',
        'PORT': '3306',
        'NAME': 'LuckyDevelop'
    }

    SQLALCHEMY_DATABASE_URI = get_db_uri(DATABASE)
    TRIGGER_DATABASE_URL = get_db_uri(DATABASE)


class TestingConfig(Config):
    TESTING = True
    DATABASE = {
        'ENGINE': 'mysql',
        'DRIVER': 'pymysql',
        'USER': 'root',
        'PASSWORD': 'xws123456',
        'HOST': '127.0.0.1',
        'PORT': '3306',
        'NAME': 'LuckyTesting'
    }

    SQLALCHEMY_DATABASE_URI = get_db_uri(DATABASE)


class StagingConfig(Config):

    DATABASE = {
        'ENGINE': 'mysql',
        'DRIVER': 'pymysql',
        'USER': 'root',
        'PASSWORD': 'xws123456',
        'HOST': 'localhost',
        'PORT': '3306',
        'NAME': 'LuckyStaging'
    }

    SQLALCHEMY_DATABASE_URI = get_db_uri(DATABASE)


class ProductConfig(Config):

    DATABASE = {
        'ENGINE': 'mysql',
        'DRIVER': 'pymysql',
        'USER': 'root',
        'PASSWORD': 'xws123456',
        'HOST': 'localhost',
        'PORT': '3306',
        'NAME': 'LuckyProduct'
    }

    SQLALCHEMY_DATABASE_URI = get_db_uri(DATABASE)


environments = {
    'develop': DevelopConfig,
    'testing': TestingConfig,
    'staging': StagingConfig,
    'product': ProductConfig,
    'default': DevelopConfig
}

# 关键字自定义配置
USER_KEYS = {
    "web": ["BuiltIn", "Collections", "String", "DateTime", "Screenshot", "SeleniumLibrary"],
    "app": ["BuiltIn", "Collections", "String", "DateTime", "Screenshot", "AppiumLibrary"],
    "http": ["BuiltIn", "Collections", "String", "DateTime", "RequestsLibrary"],
    "all": ["BuiltIn", "Collections", "String", "Screenshot", "DateTime", "SeleniumLibrary", "AppiumLibrary",
            "RequestsLibrary", "Process", "Telnet", "OperatingSystem"]
}
