import argparse
import mysql.connector
import getpass

def read_schema(indbname : str) -> bool:
    print('read schema')
    print('NOT IMPLEMENTED!!!')
    return False

def create_db( infile : str ) -> bool:
    print('Creating db from schema file:\n')
    with open(infile, 'r') as fd:
        data = fd.read()
        fd.close()
    print("'''\n"+data+"\n'''")
    print("\nGetting connection data, press <enter> for default...")
    SERVER = input("Server (localhost):")
    if len(SERVER) < 1:
        SERVER = 'localhost'
    USERNAME = input('User name (root):')
    if len(USERNAME) < 1:
        USERNAME = 'root'
    PASS = getpass.getpass('Password:')
    try:
        mydb = mysql.connector.connect(host=SERVER,user=USERNAME,password=PASS, buffered=True)
    except Exception as e:
        print('Error connecting to database...')
        print(e)
        return False
    mycur = mydb.cursor()
    databases = 'show databases'
    mycur.execute(databases)
    print('\nAvailable databases:')
    databases = [ line[0] for line in mycur ]
    for line in databases:
        print('\t'+line)
    data = data.split(';')
    print('Executing SQL...')
    for line in data:
        if len(line) < 2:
            continue
        mycur.execute(line+';')
    db2 = 'show databases'
    mycur.execute(db2)
    db2 = [line[0] for line in mycur]
    for line in db2:
        if line not in databases:
            print('Created new database from schema: "%s"' % line)
    return True

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument("-c", "--create", required=False, help="Provide file to create database from schema")
    ap.add_argument("-l", "--list", required=False, help="Connect and list database schema")
    args = vars(ap.parse_args())
    if args['list']:
        read_schema(args['list'])
    elif args['create']:
        create_db(args['create'])
    else:
        ap.print_usage()
