"""Environment settings."""
import os

MODEL_NAME = os.getenv("MODEL_NAME")
MATRYOSHKA_DIM = int(os.getenv("MATRYOSHKA_DIM", '512'))
