"""Env settings."""
import os

POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_DB = os.getenv("POSTGRES_DB")

MATRYOSHKA_DIM = int(os.getenv("MATRYOSHKA_DIM", '512'))