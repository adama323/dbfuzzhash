import argparse
import struct
import base64
import os
import ppdeep
import hashlib
import getpass
import mysql.connector

def get_all_7_char_chunks(h):
    #unpack 7-gram string into set of ints
    return set((struct.unpack("<Q", base64.b64decode(h[i:i+7] + "=") + b"\x00\x00\x00")[0] for i in range(len(h) - 6)))

def preprocess_hash(h):
    block_size, h = h.split(":", 1)
    block_size = int(block_size)
    # Reduce any sequence of the same char greater than 3 to 3
    for c in set(list(h)):
        while c * 4 in h:
            h = h.replace(c * 4, c * 3)
    block_data, double_block_data = h.split(":")
    return block_size, get_all_7_char_chunks(block_data), get_all_7_char_chunks(double_block_data)

def get_tokenized_ssdeep(inhash : str) -> tuple:
    return preprocess_hash(inhash)

def get_from_files(indir : str) -> dict:
    #print('get_from_files')
    paths = []
    for currentpath, folders, files in os.walk(indir):
        for file in files:
            paths.append(os.path.join(currentpath, file))

    print('generating hash from files...')
    out = dict()
    i = 0
    
    for fpath in paths:
        deep_hash = ppdeep.hash_from_file(fpath)
        md5 = hashlib.md5()
        sha1 = hashlib.sha1()
        sha256 = hashlib.sha256()
        with open(fpath, 'rb') as fd:
            while True:
                data = fd.read(65535)
                if not data:
                    break
                md5.update(data)
                sha1.update(data)
                sha256.update(data)
        out[i] = [fpath, md5.hexdigest(), sha1.hexdigest(), sha256.hexdigest(), deep_hash, get_tokenized_ssdeep(deep_hash)]
        i += 1
        if i % 100 == 0:
            print('processed: %d/%d' % (i, len(paths)))
    return out

def print_sql_result(q, mycur):
    try:
        print('\nquery "%s" returned: ' % q)
        r = [line[0] for line in mycur]
        for line in r:
            print('\t%s' % line)
    except Exception as e:
        print('\tno result')
        pass
    return


def upload_from_files(indir: str) -> bool:
    #setup our database connection
    print("\ngetting connection data, press <enter> for default...")
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
    DATABASE = input('Database name (hashproject):')
    if len(DATABASE) < 1:
        DATABASE = 'hashproject'
    q = 'use %s;' % DATABASE
    mycur.execute(q)
    #print_sql_result(q, mycur)
    q = 'show tables;'
    mycur.execute(q)
    #print_sql_result(q, mycur)
    
    # get the primary keys for each table
    q = 'select max(hash_id) from fuzzy_hash_table;'
    mycur.execute(q)
    r = [line[0] for line in mycur]
    try:
        hash_id = int(r[0])
        hash_id += 1
    except Exception as e:
        #errors for empty table
        print('hash_id error:',e)
        hash_id = 1
        pass

    q = 'select max(chunk_id) from ssdeep_chunk_table;'
    mycur.execute(q)
    r = [line[0] for line in mycur]
    try:
        chunk_id = int(r[0])
        chunk_id += 1
    except Exception as e:
        #errors for empty table
        print('chunk_id error:', e)
        chunk_id = 1
        pass

    q = 'select max(crypto_id) from crypto_hash_table;'
    mycur.execute(q)
    r = [line[0] for line in mycur]
    try:
        crypto_id = int(r[0])
        crypto_id += 1
    except Exception as e:
        #errors for empty table
        print('crypto_id error: ', e)
        crypto_id = 1
        pass
    
    hashes = get_from_files(indir)
    print('got %d files to upload...' % len(hashes))

    # put stuff in the database
    for k,v in hashes.items():
        md5 = v[1]
        sha1 = v[2]
        sha256 = v[3]
        ssd = v[4]
        ssd_t = v[5]
        q = 'insert into fuzzy_hash_table values(%d, "%s");' % (hash_id, ssd)
        #print(q)
        mycur.execute(q)
        #print_sql_result(q, mycur)
        chunk_size = ssd_t[0]
        for chunk in ssd_t[1]:
            q = 'insert into ssdeep_chunk_table values(%d, %d, %d, %d);' % (chunk_id, chunk_size, chunk, hash_id)
            #print(q)
            mycur.execute(q)
            #print_sql_result(q, mycur)
            chunk_id += 1
        for doublechunk in ssd_t[2]:
            q = 'insert into ssdeep_chunk_table values(%d, %d, %d, %d);' % (chunk_id, chunk_size, doublechunk, hash_id)
            #print(q)
            mycur.execute(q)
            #print_sql_result(q, mycur)
            chunk_id += 1
        q = 'insert into crypto_hash_table values(%d, "%s", "%s", "%s", %d);' % (crypto_id, md5, sha1, sha256, hash_id)
        #print(q)
        mycur.execute(q)
        #print_sql_result(q, mycur)
        crypto_id += 1
        hash_id += 1
        print('added file: "%s" to database' % v[0])
        mydb.commit()
    return True

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument("-p", "--path", required=False, help="Hash, tokenize, and upload all files from path")
    args = vars(ap.parse_args())
    if args['path']:
        upload_from_files(args['path'])
