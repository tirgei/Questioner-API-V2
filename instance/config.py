class Config(object):
    """ Base Config class """

    DEBUG = False
    TESTING = False


class DevelopmentConfig(Config):
    """ Config class for Development environment """

    DEBUG = True


class TestingConfig(Config):
    """ Config class for Testing environment """

    TESTING = True


class StagingConfig(Config):
    """ Config class for Staging environment """

    DEBUG = True


class ProductionConfig(Config):
    """ Config class for Production environment """

    DEBUG = False
    TESTING = False
