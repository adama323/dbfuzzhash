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
    return out

def upload_from_files(indir: str) -> bool:
    hashes = get_from_files(indir)
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
        db2 = 'show databases'
    mycur.execute(db2)
    db2 = [line[0] for line in mycur]
    for line in db2:
        if line not in databases:
            print('Created new database from schema: "%s"' % line)
    return True


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument("-p", "--path", required=False, help="Hash, tokenize, and upload all files from path")
    args = vars(ap.parse_args())
    if args['path']:
        upload_from_files(args['path'])
