#!/usr/bin/python
import urllib2
response = urllib2.urlopen('http://cloud.example.com/myvm')
representation = response.read()
metadata = response.info()
print metadata['occi-compute-cores']

