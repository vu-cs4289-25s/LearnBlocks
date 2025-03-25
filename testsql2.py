import psycopg2
import pandas as pd
import os

conn = psycopg2.connect(
            dbname="postgres",
            user="postgres",
            password="password",
            host="localhost",
            port=5432
        )