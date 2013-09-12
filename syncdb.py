import paramiko
import os

dumpfile = 'dump.sql'

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

print "Connecting to host..."

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(server_address, port=server_port, username=server_username, password=server_password)

print "Dumping database..."

def ssh(cmd):
    out = []
    msg = [stdin, stdout, stderr] = client.exec_command(cmd)
    for item in msg:
        try:
            for line in item:
                out.append(line.strip('\n'))
        except: pass

    return(list(out))

dump = ssh("mysqldump -u {0} -p{1} {2} --skip-comments".format(server_db_username, server_db_password, server_db_name))

print "Saving to dump.sql..."

file = open(dumpfile, 'w')
file.write("".join(dump))
file.close()

print "Importing to local database..."

os.system("mysql -u {0} {1} < {2}",format(local_db_username, local_db_name, dumpfile))
