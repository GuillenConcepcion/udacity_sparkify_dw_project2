import configparser
import psycopg2

from sql_queries import create_table_queries,drop_table_queries

def drop_tables(cur, conn):
    status = False
    try:
        for query in drop_table_queries:
            cur.execute(query)
            conn.commit()
        print("Tables dropped successfully")
        status = True

    except psycopg2.Error as error:
        print("An unexpected error in Database occurred:",error) 

    except Exception as error:   
        print("An unexpected error occurred:",error) 

    return status


def create_tables(cur, conn):
    try:
        for query in create_table_queries:
            cur.execute(query)
            conn.commit()

        print("Tables created successfully")
    
    except psycopg2.Error as error:
        print("An unexpected error in Database occurred:",error) 

    except Exception as error:   
        print("An unexpected error occurred:",error) 


def main():
    config = configparser.ConfigParser()
    config.read('dwh.cfg')

    try:
        conn = psycopg2.connect("host={} dbname={} user={} password={} port={}".format(*config['CLUSTER'].values()))
        print(conn)
        cur = conn.cursor()
        
        if (drop_tables(cur, conn)):
            create_tables(cur, conn)
        else:
            create_tables(cur, conn)
        
        conn.close()
        cur.close()
	    
    except (psycopg2.DatabaseError, Exception) as error:
        print("Connection failed!! Error:", error)
        
if __name__ == "__main__":
    main()
