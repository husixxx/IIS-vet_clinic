### for start of database locally instal docker and thes write 
`docker-compose up -d`

### for db dump

`sudo apt install postgresql-17`
`sudo apt install postgresql-client-17`

### apply dump

`psql -U husic/myuser -d iis -f iis_dump.sql`
