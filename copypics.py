#!/usr/bin/python
# Note:  for this to run, exiftool must be installed.  If not, go to http://owl.phy.queensu.ca/~phil/exiftool/ to grab it

import subprocess
import os
from datetime import date
from time import sleep
from shutil import copy2 as copy
from shutil import rmtree
import re
import json


class Picture(object):
    def __init__(self, createdate=date.today(), filename = ''):
        self.createdate = createdate
        self.filename = filename

    def findcreatedate(self):
        """Finds when the JPEG was created"""
        try:
            exifdata = subprocess.check_output(['exiftool', '-j', '-TAG', '-CreateDate', self.filename])
        except OSError as e:
            print "exiftool may not be installed.  Please go check."
            print "Here is the error thrown: {}".format(e)
            raise

        data = json.loads(exifdata)
        self.createdate = date(*[int(elt) for elt in re.split('[ :]', data[0]['CreateDate'])][0:3])
        return self.createdate

    def fileparse(self, dir, givendate, i, j):		# i and j are counters that will be incremented by at most 1 (each) every time fileparse is called
        """Parses the files list.  Uses findcreatedate to determine whether or not to copy file"""
        if self.findcreatedate() > givendate:	# Test file's creation date against date passed into function
            if j != 0:				# If this is the first time (locally) we've found a self.filename that needs to be copied, reset j
                print "\n",
                j = 0
            dest = dir + self.filename
            copy(self.filename, dest)
            print "\r{} being copied".format(self.filename),
            i += 1					# increment our count of self.filenames that have been copied in a row
        else:
            j += 1					# otherwise, increment our count of self.filenames skipped
            print "\r{} files parsed after last success".format(j),
        countarf = [i, j]					# put i an j into an array, then return it
        return countarf


def getdatefromuser():
    """Get the cutoff date from user (stdin), return a date object for use in the main execution block"""
    date_str = raw_input("Enter the date cutoff in mm/dd/yyyy format: ")
    date_parts = re.split('[-/]', date_str)
    return date(*[int(elt) for elt in [date_parts[2], date_parts[0], date_parts[1]]])


def rmdir(dir):
    """Remove old directory if it exists, then create or recreate it.  Sleep so user can see progress"""
    print "Trying to remove old", dir, "directory"

    try:
        rmtree(dir)
    except OSError:
        print "No directory", dir, ".  Skipping removal."
        pass
    finally:
        sleep(2)

    os.mkdir(dir)
    print 'Created new directory', dir
    sleep(2)


def main():
    print "This must be run in the directory with JPG files"
    print "Note: for this to run, exiftool must be installed.  If not, go to http://owl.phy.queensu.ca/~phil/exiftool/ to grab it"
    # Initialize some variables
    newdir = 'NewPics/'

    userdate = getdatefromuser()			# get cutoff date from user, split it to pass in later to fileparse
    rmdir(newdir)					# set up our copy directory

    countar = [0, 0]					# initialize our counting array
    files = os.listdir('.')
    for file in files:
        if file.find('JPG') > -1:				# find() function returns -1 if the argument isn't found
            pic = Picture(filename = file)
            countar = pic.fileparse(newdir, userdate, countar[0], countar[1])	# work through the list of files, copying or skipping as needed

    print "\n{} files copied".format(countar[0])


if __name__ == '__main__':
    main()
