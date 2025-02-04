import psycopg

class database:
    def __init__(self, dbname, user, password, host, port):
        self.dbname = dbname
        self.user = user
        self.password = password
        self.host = host
        self.port = port

    def append(self, formatted_data):
        try:
            with psycopg.connect(
                dbname = self.dbname,
                user = self.user,
                password = self.password,
                host = self.host,
                port = self.port) as conn:

                # Create connection pipeline for commands
                with conn.cursor() as cur:

                    # Execute SQL command and store values
                    cur.executemany(
                        """INSERT INTO pit_antennas 
                        (uuid, date, time, reader_id, tag_id, latitude, 
                        longitude, ip_address) VALUES (uuid_generate_v4(), 
                        %s, %s, %s, %s, %s, %s, %s) ON CONFLICT 
                        (date, time, reader_id, tag_id) DO NOTHING""", 
                        formatted_data)

                # Commit changes 
                conn.commit()    

                # Close postgres connection    
                cur.close()
                conn.close()
        except psycopg.OperationalError as e:
            print("""OperationError, cannot connect to postgres DB
                  Please check connection credentials.
                  Error: {}""".format(e))
