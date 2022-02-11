# Python program to explain os.makedirs() method

# importing os module
import os

# os.makedirs() method will raise
# an OSError if the directory
# to be created already exists
# But It can be suppressed by
# setting the value of a parameter
# exist_ok as True

# Directory
directory = "Raghu"

# Parent Directory path
parent_dir = "D:\Project\clinicalfirst_services"

# Path
path = os.path.join(parent_dir, directory)

# Create the directory
# 'Nikhil'
try:
	os.makedirs(path, exist_ok = True)
	print("Directory '%s' created successfully" % directory)
except OSError as error:
	print("Directory '%s' can not be created" % directory)

# By setting exist_ok as True
# error caused due already
# existing directory can be suppressed
# but other OSError may be raised
# due to other error like
# invalid path name
