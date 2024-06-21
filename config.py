import os
import secrets


class Config:
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres.tziwiqlqeyxalzonjwgu:afrtiteabdo5enox@aws-0-eu-central-1.pooler.supabase.com:6543/postgres'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Generates a 32-character hexadecimal string
    SECRET_KEY = secrets.token_hex(16)


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False
