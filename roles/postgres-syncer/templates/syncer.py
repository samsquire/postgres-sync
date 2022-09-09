import time
import psycopg2
from psycopg2 import sql
from subprocess import PIPE, Popen
import yaml
from pprint import pprint
from hashlib import sha256


config = yaml.safe_load(open("/etc/postgres-sync/sync.yml").read())

print("Running syncer")
pprint(config)



sync_timestamp = int( time.time() )
print("Running sync timestamp", sync_timestamp)

def find_if_changed(table, row_number, column_number, column_name, item_number, new_column_hash, sync_timestamp, version):
    version_data = cur.execute( \
        sql.SQL("select hash from {} where row_number = %s and table_name = %s and column_name = %s order by version desc LIMIT 1") \
        .format(sql.Identifier("versions")), [row_number, table, column_name])
    hashes = cur.fetchall()
    if len(hashes) == 0:
        print("Data is not known by syncer database")
        return True
    pprint(hashes)
    if hashes[0][0] == new_column_hash:
        print("Data has not been changed")
        return False
    print("Data has been changed")
    return True

def find_version(conn, table_name, row_number, column, records):
    version_data = cur.execute( \
        sql.SQL("select version from {} where table_name = %s and column_name = %s order by version desc") \
        .format(sql.Identifier("versions")), [table_name, column[1].name])
    available_versions = cur.fetchall()
    if not available_versions:
        new_version = 0
    else:
        new_version = available_versions[0][0] + 1
    return new_version

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
        size = records[0]
        # TODO: Do scan in batches
        cur.execute( \
        sql.SQL("select * from {} order by id asc") \
        .format(sql.Identifier(table)))
        records = cur.fetchall() 
        pprint(records)
        column_names = [(desc[0], desc[1]) for desc in enumerate(cur.description)]
        column_names.sort()
        
        previous_column_hash = ""
        item_number = 0
        row_number = 0
        for record in records:
            print("Processing hashes for record {}".format(row_number))
            column_hash = ""
            
            for column in column_names:
                print("Processing hashes for column {}".format(item_number))
                print(column[1].name)
                this_column_hash = sha256(str(record[column[0]]).encode('utf-8')).hexdigest()
                new_column_hash = sha256((previous_column_hash + this_column_hash).encode('utf-8')).hexdigest()
                version = find_version(conn, table, row_number, column, records)
                changed = find_if_changed(table, row_number, column[0], column[1].name, item_number, new_column_hash, sync_timestamp, version)
                if changed:
                    
                    
                    cur.execute( \
                    sql.SQL("insert into {} (table_name, row_number, column_number, item_number, hash, timestamp, version, column_name) values (%s, %s, %s, %s, %s, %s, %s, %s)") \
                    .format(sql.Identifier("versions")),
                    [table, row_number, column[0], item_number, new_column_hash, sync_timestamp, version, column[1].name])
                previous_column_hash = new_column_hash
                item_number = item_number + 1
                
                
            
            row_number = row_number + 1
    conn.commit()
        
        
        
        
