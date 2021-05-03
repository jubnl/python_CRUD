from environs import Env

env = Env()
env.read_env()

DB_HOST = env("DB_HOST")
DB_PORT = int(env("DB_PORT"))
DB_USER = env("DB_USER")
DB_PASSWORD = env("DB_PASSWORD")
DB_NAME = env("DB_NAME") if env("DB_NAME") else None
