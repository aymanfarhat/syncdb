from datetime import datetime as date
import paramiko
import os
import json

def ssh(cmd):
    out = []
    msg = [stdin, stdout, stderr] = client.exec_command(cmd)

    for line in msg[1]:
        out.append(line.strip('\n'))

    return out

# load the config
config_json = open('config.json')
config_list = json.load(config_json)
config_json.close()

for config in config_list:
    print "Connecting to host..."

    remote_address = config["remote"]["address"] 
    remote_port = config["remote"]["port"]
    remote_user = config["remote"]["username"]
    remote_pass = config["remote"]["password"]

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(remote_address, port=remote_port, username=remote_user, password=remote_pass)

    print "Dumping database..."

    remote_dbname = config["remote"]["db_name"]
    remote_db_username = config["remote"]["db_username"]
    remote_db_pass = config["remote"]["db_password"]

    dump = ssh("mysqldump -u {0} --password='{1}' {2} --skip-comments".format(remote_db_username, remote_db_pass, remote_dbname))

    today = date.today().strftime("%y-%m-%d")
    dumpfile = "{0}_{1}.sql".format(remote_dbname, today)

    print "Saving to {0}".format(dumpfile)

    file = open(dumpfile, 'w')
    file.write("".join(dump))
    file.close()

    print "Importing to local database..."

    local_dbname = config["local"]["db_name"]
    local_db_username = config["local"]["db_username"]
    local_db_pass = config["local"]["db_password"]

    os.system("mysql -u {0} {1} < {2}".format(local_db_username, local_dbname, dumpfile))
