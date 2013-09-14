from datetime import datetime as date

# Remote
server_address = ""
server_port = 22
server_username = ""
server_password = ""

server_db_name = ""
server_db_username = ""
server_db_password = ""

# Local
local_db_name = ""
local_db_username = ""
local_db_password = ""

# Dump file name relative to current date and remote db name
today = date.today().strftime("%y-%m-%d")
dumpfile = '{0}_{1}.sql'.format(server_db_name, today)
