"""
 * bigbucket.py
 * 
 * Released under MIT license:
 * http://www.opensource.org/licenses/mit-license.php
 *
 * Written by
 * Andrew W Hill, Vizzuality
 *
"""
 
import sys
from Queue import Queue
import fnmatch
import os
import shutil
import threading
from boto.s3.connection import S3Connection
from boto.s3.key import Key
import random

KEY = '{AWS KEY}'
SECRET = '{AWS SECRET}'

class Upload:
    def __init__(self, conn, q, printLock, bucket, prefix, test):
        self.q = q
        self.printLock = printLock
        self.dirname = dirname
        self.conn = conn
        self.b = self.conn.create_bucket(bucket) #swap in bucket variable here
        self.k = Key(self.b)
        self.prefix = prefix.rstrip('/')
        self.test = test
        self.msg = None
        
    def upload(self,filename, s3file):
        #upload file here
        filename = os.path.join(os.getcwd(),filename)
        self.k.key = s3file
        self.k.set_contents_from_filename(filename)
        self.b.set_acl('public-read',s3file)
        self.msg = 'uploaded %s as %s' % (filename,s3file)
        
    def loop(self):
        while True:
            #Fetch a file from the queue and upload it
            r = self.q.get()
            if (r == None):
                self.q.task_done()
                break
            else:
                (filename) = r
            s3file = filename if self.prefix != '' else "%s/%s" % (self.prefix,filename)
            self.upload(filename, s3file)
            if random.randint(0,1000) == 500:
                self.printLock.acquire()
                print self.msg
                self.printLock.release()
            self.q.task_done()
            
def run(dirname, bucket, num_threads, prefix, test):
    os.chdir(dirname)
    queue = Queue(32)
    printLock = threading.Lock()
    renderers = {}
    for i in range(num_threads):
        conn = S3Connection(KEY, SECRET)
        renderer = Upload(conn, queue, printLock, bucket, prefix, test)
        render_thread = threading.Thread(target=renderer.loop)
        render_thread.start()
        #print "Started render thread %s" % render_thread.getName()
        renderers[i] = render_thread

    for dirname, dirnames, filenames in os.walk('.'):
        for filename in filenames:
            d = dirname.lstrip('./')
            #if d.rfind('tiles') == -1:
            f = os.path.join(d, filename)
            queue.put(f)
        
    # Signal render threads to exit by sending empty request to queue
    for i in range(num_threads):
        queue.put(None)
    # wait for pending rendering jobs to complete
    queue.join()
    for i in range(num_threads):
        renderers[i].join()

if __name__ == "__main__":
    er = False
    prefix = ''
    threads = 32
    test = False
    try: 
        dirname = sys.argv[1]
        print 'directory: %s' % dirname
    except:
        print 'Error: you need to include the directory you wish to upload'
        er = True
    try:
        bucket = sys.argv[2]
        print 'bucket: %s' % bucket
    except:
        print 'Error: you need to include the bucket name you wish to upload to'
        er = True
    try:
        th = sys.argv[3]
        th = int(tr.strip().lower())
        assert th > 0
        threads = th
    except:
        pass
    try:
        tr = sys.argv[4]
        if tr.strip().lower() == 'true' or tr.strip().lower() == '1':
            test = True
        elif tr.strip().lower() == 'false' or tr.strip().lower() == '0':
            test = False
    except:
        pass
    try:
        prefix = sys.argv[5].strip().lower()
    except:
        pass
        
        
    if er: 
        print ''
        print 'Format: bigbucket.py {dirname} {bucket} {threads} {test} {prefix}'
        print '    dirname - the directory with files you wish to upload'
        print '    bucket  - the name of you S3 bucket'
        print '    optional - '
        print '        threads - default = 32'
        print '        test    - if True the files will not be pushed to S3'
        print '        prefix  - for storing a directory as a subdirectory in an existing bucket'
        
    else: 
        run(dirname, bucket, threads, prefix, test)
    
