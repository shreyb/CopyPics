#!/usr/bin/python


#Note:  for this to run, exiftool must be installed.  If not, go to http://owl.phy.queensu.ca/~phil/exiftool/ to grab it


import subprocess
import os
from datetime import datetime, date
from time import sleep
from shutil import copy2 as copy
from shutil import rmtree
import re
import json



#Get the cutoff date from user (stdin), return a date object for use in the main execution block
def getdatefromuser():
    date_str = raw_input("Enter the date cutoff in mm/dd/yyyy format: ")
    date_parts = re.split('[-/]',date_str)
    return date(*[int(elt) for elt in [date_parts[2],date_parts[0],date_parts[1]]])


#Remove old directory if it exists, then create or recreate it.  Sleep so user can see progress
def rmdir(dir):
	print "Trying to remove old", dir, "directory"
		
	try:
		rmtree(dir)
	except OSError:
		print "No directory", dir,".  Skipping removal."
		pass
	finally:
		sleep(2)

	os.mkdir(dir)
	print 'Created new directory',dir 
	sleep(2)
	


#Finds when the JPEG was created
def findcreatedate(file):
    try:
        exifdata = subprocess.check_output(['exiftool','-j','-TAG','-CreateDate',file])	
    except OSError as e:
        print "exiftool may not be installed.  Please go check."
        print "Here is the error thrown: {}".format(e)
        raise 
    
    data = json.loads(exifdata)
    return date(*[int(elt) for elt in re.split('[ :]',data[0]['CreateDate'])][0:3])


#Parses the files list.  Uses findcreatedate to determine whether or not to copy file
def fileparse(file,dir,givendate,i,j):		#i and j are counters that will be incremented by at most 1 (each) every time fileparse is called
	if file.find('JPG')>-1:				# find() function returns -1 if the argument isn't found
		if findcreatedate(file)>givendate:	# Test file's creation date against date passed into function
			if j<> 0:				#If this is the first time (locally) we've found a file that needs to be copied, reset j  
				print "\n",
				j=0
			dest = dir+file				
			copy(file,dest)
			print "\r{} being copied".format(file),
			i +=1					#increment our count of files that have been copied in a row
		else:						
			j+=1					#otherwise, increment our count of files skipped
			print "\r{} files parsed after last success".format(j), 
	countarf = [i,j]					# put i an j into an array, then return it
	return countarf



def main():
	#Initialize some variables

    print "Note:  for this to run, exiftool must be installed.  If not, go to http://owl.phy.queensu.ca/~phil/exiftool/ to grab it"
    newdir = 'NewPics/'
	
    userdate = getdatefromuser()			#get cutoff date from user, split it to pass in later to fileparse
    rmdir(newdir)					#set up our copy directory
	
    filestring = subprocess.check_output(['ls'])	#grab our list of files in the current directory
    filelist = filestring.split('\n')		
	
    countar = [0,0]					#initialize our counting array
    for fil in filelist:
        countar = fileparse(fil,newdir,userdate,countar[0],countar[1])	#work through the list of files, copying or skipping as needed
	
    print "\n{} files copied".format(countar[0])

if __name__ == '__main__':
	main()


