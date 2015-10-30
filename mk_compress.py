#!/usr/bin/env python

# This script is my implementation of the LZ77 compression algorithm.  The script takes in a
# file as input and outputs a file with compressed data.   

__author__ = 'Michael Kasza'
__status__ = 'Development'

import argparse

from mk_compress_utils import *
	
def compress(data):

	# The index of this loop indicates the position of the sliding window.  Everything before
	# the index is already compressed and everything after is uncompressed.  

	comp_data = []
	
	i = 0
	
	while i < len(data):
	
		longest_start = i
		longest_len = 0
		
		window_start = 0+(i > 12)*(i-12)
		
		for j in range(window_start,i):
		
			start = j
			k = 0
			
			while j < len(data) and j < i+9:
				
				if data[start:j] == data[i:i+k]:
					
					if (j-start) > longest_len:
						
						longest_start = start
						longest_len = j-start
						
				j += 1
				k += 1
		
		next_byte = (36).to_bytes(1,byteorder='big')
		
		if i+longest_len < len(data):
			next_byte = data[i+longest_len]

		comp_data.append(abs(longest_start-i).to_bytes(1,byteorder='big'))
		comp_data.append(longest_len.to_bytes(1,byteorder='big'))
		comp_data.append(next_byte)
	
		i += longest_len+1
		
	return comp_data
	
def decompress(data):

	decomp = []

	for i in range(0,len(data),3):
	
		start_param = int.from_bytes(data[i],byteorder='big')
		copy_len_param = int.from_bytes(data[i+1],byteorder='big')

		start = len(decomp)-start_param
		end = start+copy_len_param
		
		decomp += copy(decomp,start,end)+[((not data[i+2] == b'$') or (i < len(data)-3) )*data[i+2]]
		
	return decomp
	


def main():
	parser = argparse.ArgumentParser(description='Uses the LZ77 algorithm to compress an input file')
	parser.add_argument('-i','--input',required=True,help='Enter the name of a file to compress')
	parser.add_argument('-o','--output',required=False,default='',help='Specify an output filename.  \
	If argument isn\'t used, the default filename is the input filename with the .mkc extension added')
	parser.add_argument('-m','--mode',required=True,help='Select which action you would like to perform on \
	the input file.  Options are \'compress\' or \'decompress\'')
	args = parser.parse_args()
	
	input_filename = args.input
	output_filename = args.output
	
	if not isValidFilename(input_filename):
		print('Invalid argument for input filename')
		return
		
	if args.mode == 'compress':
	
		if output_filename == '':
			output_filename = input_filename + '.mkc'
		elif not isValidFilename(output_filename):
			print('Invalid argument for output filename')
			return
			
		data = fileToList(input_filename)
		
		# Pass data to be compressed to the compress function.  Store returned compressed data in the
		# comp_data variable
		
		comp_data = compress(data)
		
		# Write compressed data to output file
		
		listToFile(output_filename,comp_data)
		
		print('File successfully compressed')
		print('Compression ratio is: {0:1.2f}'.format(len(comp_data)/len(data)))
				
	elif args.mode == 'decompress':
	
		if output_filename == '':
			if input_filename[len(input_filename)-4:] == '.mkc':
				output_filename = input_filename[0:len(input_filename)-4]
			else:
				print('Invalid argument for output filename')
				return
		elif not isValidFilename(output_filename):
			print('Invalid argument for output filename')
			return
	
		data = fileToList(input_filename)
		
		# Pass data to be decompressed to the decompress function.  Store returned decompressed data in the
		# decomp_data variable
		
		decomp_data = decompress(data)
		
		# Write decompressed data to output file
		
		listToFile(output_filename,decomp_data)
	
	else:
		print('Unknown mode: %s' % args.mode)
		return

if __name__ == '__main__':
	main()