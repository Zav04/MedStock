import os

class Config:
    """Base configuration."""
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('SECRET_KEY', 'default_secret_key')  # Para sessões e segurança
    DEBUG = False  # Por padrão, o debug está desativado
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL',
        'postgresql://postgres:123456@localhost:5432/MEDSUPPLY'
    )


class DevelopmentConfig(Config):
    """Configuration for development."""
    DEBUG = True
    SQLALCHEMY_ECHO = True  # Ativa o log das queries SQL para debug


class TestingConfig(Config):
    """Configuration for testing."""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'TEST_DATABASE_URL',
        'postgresql://postgres:123456@localhost:5432/MEDSUPPLY_TEST'
    )
    DEBUG = True
    SQLALCHEMY_ECHO = False  # Reduz a verbosidade nos testes


class ProductionConfig(Config):
    """Configuration for production."""
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    DEBUG = False


# Selecionando a configuração baseada na variável de ambiente
configurations = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
}

def get_config(env=None):
    env = env or os.getenv('FLASK_ENV', 'development')
    return configurations.get(env, DevelopmentConfig)
