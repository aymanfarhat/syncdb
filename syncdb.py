from datetime import datetime as date
import paramiko
import os
import json

def ssh_cmd(client, cmd):
    """Execute a command on the remote via paramiko client and return the stdout output"""
    out = []
    msg = [stdin, stdout, stderr] = client.exec_command(cmd)

    for line in msg[1]:
        out.append(line.strip('\n'))

    return out

def load_config(file_name):
    """Loads the selected json config file and parses it"""
    config_json = open(file_name)
    config_list = json.load(config_json)
    config_json.close()

    return config_list

def ssh_connect(config):
    """Connects to a remote host via paramiko and returns paramiko client object"""
    remote_address = config["remote"]["address"] 
    remote_port = config["remote"]["port"]
    remote_user = config["remote"]["username"]
    remote_pass = config["remote"]["password"]

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(remote_address, port=remote_port, username=remote_user, password=remote_pass)

    return client

def get_dump_filename(db_name):
    """Formats the dump file name """
    today = date.today().strftime("%y-%m-%d")
    dumpfile = "{0}_{1}.sql".format(db_name, today)

    return dumpfile

def write_dump_to_file(file_name, dump):
    """Write string dump to file """
    file = open(file_name, 'w')
    file.write("".join(dump))
    file.close()

if __name__ == "__main__":

    config_list = load_config("config.json")

    for config in config_list:
        print "Syncing {0}".format(config["description"])
        print "Connecting to host..."

        client = ssh_connect(config)

        print "Dumping database..."

        remote_dbname = config["remote"]["db_name"]
        remote_db_username = config["remote"]["db_username"]
        remote_db_pass = config["remote"]["db_password"]

        dump = ssh_cmd(client, "mysqldump -u {0} --password='{1}' {2} --skip-comments".format(remote_db_username, remote_db_pass, remote_dbname))

        print "saving to file..."

        dumpfile = get_dump_filename(remote_dbname)
        write_dump_to_file(dumpfile, dump)

        if config["import"]:
            print "Importing to local database..."
            local_dbname = config["local"]["db_name"]
            local_db_username = config["local"]["db_username"]
            local_db_pass = config["local"]["db_password"]
            os.system("mysql -u {0} {1} < {2}".format(local_db_username, local_dbname, dumpfile))

    end = raw_input("Press enter to continue...")
