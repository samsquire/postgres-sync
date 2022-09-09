import psycopg2
from psycopg2 import sql
from subprocess import PIPE, Popen
import yaml
from pprint import pprint

config = yaml.load(open("/etc/postgres-sync/sync.yml").read())

print("Running syncer")
pprint(config)

for database in config["databases"]:
    conn = psycopg2.connect("dbname={} user=postgres".format(database["name"]))
    for table in database["tables"]:

        # Connect to your postgres DB

        # Open a cursor to perform database operations
        cur = conn.cursor()

        # Execute a query
        cur.execute( \
        sql.SQL("select count(*) from {}") \
        .format(sql.Identifier(table)))

        # Retrieve query results
        records = cur.fetchall() 
        pprint(records)
