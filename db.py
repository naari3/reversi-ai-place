# -*- coding: utf-8 -*-
import os
from os.path import join, dirname
from dotenv import load_dotenv

import psycopg2
from playhouse.postgres_ext import PostgresqlExtDatabase

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

db = PostgresqlExtDatabase(
    database=os.environ.get("POSTGRES_DATABASE"),
    user=os.environ.get("POSTGRES_USERNAME"),
    password=os.environ.get("POSTGRES_PASSWORD"),
    host=os.environ.get("POSTGRES_HOST"),
    port=os.environ.get("POSTGRES_PORT"),
    register_hstore=False,
)
