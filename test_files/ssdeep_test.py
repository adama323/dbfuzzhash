import ppdeep
import os
from subprocess import Popen, PIPE
def main():
    print('hello....\nrunning test...')
    working = os.getcwd()
    os.chdir('hash_testing' + os.path.sep + 'samples')    
    samples = ['lorem_01.txt', 'lorem_02.txt', 'lorem_03.txt']

    h1 = ppdeep.hash_from_file(samples[0])
    print('hash of %s is %s' % (samples[0], h1))
    h2 = ppdeep.hash_from_file(samples[1])
    print('hash of %s is %s' % (samples[1], h2))
    h3 = ppdeep.hash_from_file(samples[2])
    print('hash of %s is %s' % (samples[2], h3))
    
    val = ppdeep.compare(h1,h2)
    print('%s to %s scores: %d' % (samples[0], samples[1], val))
    
    val = ppdeep.compare(h1,h3)
    print('%s to %s scores: %d' % (samples[0], samples[2], val))
    
    val = ppdeep.compare(h2,h3)
    print('%s to %s scores: %d' % (samples[1], samples[2], val))

    os.chdir(working)
    process = Popen(["hash_testing\\bins\\ssdeep-2.14.1\\ssdeep.exe", "-s", "hash_testing\\samples\\*.txt"], stdout=PIPE, stderr=PIPE)
    stdout, stderr = process.communicate()
    print('\nssdeep.exe results')
    print(stdout.decode("utf-8"))
    print('done')
    
if __name__ == '__main__':
    main()