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
    DEBUG = False
    TESTING = False
    SECRET_KEY = 'JWH3h463237HTL37'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    FLASKY_ADMIN = 'xwsftst@126.com'

    TRIGGER = None


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
    "all": ["BuiltIn", "Collections", "String", "Screenshot", "DateTime","SeleniumLibrary", "AppiumLibrary",
            "RequestsLibrary", "Process", "Telnet", "OperatingSystem"]
}
