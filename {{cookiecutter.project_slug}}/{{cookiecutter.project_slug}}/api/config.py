class Config(object):
    """ Default configuration """
    DEBUG = False


class ProductionConfig(Config):
    """ Production configuration """


class DevelopmentConfig(Config):
    """ Development configuration """
    DEBUG = True
