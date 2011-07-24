What is bigbucket.py
---------------

bigbucket.py is a small python script that allows you to upload full folders to Amazon S3 quickly. To do so it uploads multiple files simultaneously by opening multiple connections to Amazon S3.

Why?
---------------
Well, if you need to upload thousands of files to S3 takes a looong time with most command clients. With this command tool this just work faster. 

If you need similar functionality on FTP, [lftp](http://lftp.yar.ru/) is an incredible tool that can do that.


How to use it
---------------
- Modify the bigbucket.py file and add your {AWS KEY} and {AWS SECRET}

- Run it via command line like, it looks like this:

		$ python bigbucket.py {dirname} {bucket} {threads} {test} {prefix}

where:

* dirname - the directory with files you wish to upload
* bucket  - the name of you S3 bucket

optional:

* threads - default = 32
* test    - if True the files will not be pushed to S3
* prefix  - for storing a directory as a subdirectory in an existing bucket


Authors:
---------------
The main developer of the tool is Andrew W Hill (@andrewxhill)