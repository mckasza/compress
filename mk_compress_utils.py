# This file contains utility functions to be used by the compress.py script

def isValidFilename(filename):
	if '.' in filename:
		return True
		
	return False
	
def copy(data,start,end):

	length = len(data)-start

	ret_data = []

	for i in range(0,end-start):
		ret_data.append(data[start:len(data)][i%length])
		
	return ret_data
	
def fileToList(filename):

	# Read data from input file, store it in a list and then close

	data = []

	f_input = open(filename,'rb')
		
	while True:
		byte = f_input.read(1)
		if not byte:
			break
		data.append(byte)
		
	f_input.close()
	
	return data
	
def listToFile(filename,data):

	# Writes every element from a list of bytes to a file
	
	f_output = open(filename,'wb')
		
	for byte in data:
		f_output.write(byte)
	f_output.close()