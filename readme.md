### for start of database locally instal docker and thes write 
`docker-compose up -d`

### for db dump
`sudo sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt/ $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list'
wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -`
`sudo apt install postgresql-17`
`sudo apt install postgresql-client-17`

### apply dump

`psql -U husic/myuser -d iis -f iis_dump.sql`
