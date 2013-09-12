import paramiko
import os
import config

print "Connecting to host..."

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(config.server_address, port=config.server_port, username=config.server_username, password=config.server_password)

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

dump = ssh("mysqldump -u {0} -p{1} {2} --skip-comments".format(config.server_db_username, config.server_db_password, config.server_db_name))

print "Saving to dump.sql..."

file = open(config.dumpfile, 'w')
file.write("".join(dump))
file.close()

print "Importing to local database..."

os.system("mysql -u {0} {1} < {2}".format(config.local_db_username, config.local_db_name, config.dumpfile))
