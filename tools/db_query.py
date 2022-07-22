import argparse
import ppdeep 
import struct 
import getpass
import mysql.connector
import base64

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

def query_by_ssdeep(deep_hash):
    #setup our database connection
    token_hash = get_tokenized_ssdeep(deep_hash)
    #print(token_hash)
    chunk_size = token_hash[0]
    all_chunks = []
    for chunk in token_hash[1]:
        all_chunks.append(str(chunk))
    for chunk in token_hash[2]:
        all_chunks.append(str(chunk))
    all_chunks = list(set(all_chunks))
    tmp = ' or chunk = '.join(all_chunks)
    q1 = 'select distinct fuzzy_hash_table_hash_id from ssdeep_chunk_table where chunk_size = ' + str(chunk_size) + ' and chunk = '+ ' ' + tmp + ';' 
    q2 = 'select distinct fuzzy_hash_table_hash_id from ssdeep_chunk_table where chunk_size = ' + str(chunk_size/2) + ' and chunk = '+ ' ' + tmp + ';' 
    q3 = 'select distinct fuzzy_hash_table_hash_id from ssdeep_chunk_table where chunk_size = ' + str(chunk_size*2) + ' and chunk = '+ ' ' + tmp + ';' 
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

    print('querying database...')
    mycur.execute(q1)
    r1 = [line[0] for line in mycur]

    mycur.execute(q2)
    r2 = [line[0] for line in mycur]

    mycur.execute(q3)
    r3 = [line[0] for line in mycur]
    hash_ids = list(set(r1+r2+r3))
    out = []
    print('retrieving hashes')
    for hid in hash_ids:
        q = 'select ssdeep_hash from fuzzy_hash_table where hash_id = %d;' % hid
        mycur.execute(q)
        r = [line[0] for line in mycur]
        out.append(r[0])
    print('checking %d hashes for similarity' % (len(out)))
    for i in range(0, len(out)):
        print('checking: %s to %s' % (deep_hash, out[i]))
        print('\t similarity:', ppdeep.compare(deep_hash, out[i]))
        print('\t hash_id: ', hash_ids[i])
        print('')

def query_by_hashid(hashid):
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
    print('querying database...')
    q = 'select md5_hash, sha1_hash, sha256_hash from crypto_hash_table where fuzzy_hash_table_hash_id = %s;' % hashid
    mycur.execute(q)
    r = [line for line in mycur][0]
    print('matching hashes: ')
    print('\tmd5: ', r[0])
    print('\tsha1: ', r[1])
    print('\tsha256: ', r[2])

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument("-s", "--ssdeep", required=False, help="query for matching ssdeep hashes")
    ap.add_argument("-i", "--hashid", required=False, help="query for hashes matching hash id")
    args = vars(ap.parse_args())
    if args['ssdeep']:
        query_by_ssdeep(args['ssdeep'])
    if args['hashid']:
        query_by_hashid(args['hashid'])
