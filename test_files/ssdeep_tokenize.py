import argparse
import struct
import base64
import os
import ppdeep
import hashlib


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
    #print('Tokenized ssdeep hash...')
    return preprocess_hash(inhash)

def get_from_files(indir : str) -> bool:
    #print('get_from_files')
    paths = []
    for currentpath, folders, files in os.walk(indir):
        for file in files:
            paths.append(os.path.join(currentpath, file))
    print('generating hash from files...')
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
        print('\tfile path: ' + fpath)
        print('\tmd5 hash:' + md5.hexdigest())
        print('\tsha1 hash:' + sha1.hexdigest())
        print('\tsha256 hash:' + sha256.hexdigest())
        print('\tssdeep hash: ' + deep_hash)
        print('\ttokenized ssdeep hash: ', get_tokenized_ssdeep(deep_hash))
    return True


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument("-t", "--token", required=False, help="Tokenize ssdeep hash to ngram")
    ap.add_argument("-p", "--path", required=False, help="Calculate and tokenize ssdeep hash for all files from path")
    args = vars(ap.parse_args())
    if args['token']:
        get_tokenized_ssdeep(args['token'])
    elif args['path']:
        get_from_files(args['path'])
    else:
        ap.print_usage()
