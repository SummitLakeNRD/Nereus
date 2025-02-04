# Nereus
Program to download Biomark IS1001 pit antennas and append to a postgres database

## Prerequisites
In your PostgreSQL database, the superuser will need to add the uuid-ossp extension. 
This can be done with the following command: ```CREATE EXTENSION IF NOT EXISTS "uuid-ossp";```. 
Additionally, when you create the table for this in postgres, you will need to register  
the date, time, reader_id, and tag_id fields as 'unique()' fields so the upsert SQL 
command can function properly.


