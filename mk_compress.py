#!/usr/bin/env python3

# This script is my implementation of the LZ77 compression algorithm.  The script takes in a
# file as input and outputs a file with compressed data.   

__author__ = 'Michael Kasza'
__status__ = 'Development'

import argparse
import datetime

from mk_compress_utils import *

def compress(data):
    
    comp_data = []
    literal_mode = {'status': False, 'index': 0}
    
    # The index of this loop indicates the position of the sliding window.  Everything before
    # the index is already compressed and everything after is uncompressed.
    
    i = 0
    
    while i < len(data):
            
        longest_start,longest_len = longestPrefix(data,i,127,10)
            
        # When the length of the longest sequence of data that can be compressed is less than
        # three bytes, it's not worth it to compress this sequence since compression adds two
        # bytes of overhead.  In this case, the better option is to turn on 'literal mode' and
        # keep adding the next byte to the compressed data until a sequence is found that is
        # worth compressing.
        
        if longest_len < 3:
            if literal_mode['status'] == True:
                
                # If literal mode is already on, get the current length of the literal sequence
                # and add one since one byte is about to be added
                
                literal_length = int.from_bytes(comp_data[literal_mode['index']],byteorder='big')
                literal_length += 1
                
                comp_data[literal_mode['index']] = literal_length.to_bytes(1,byteorder='big')
                comp_data.append(data[i])
                
                # Exit literal mode if the maximum length has been reached.  If the next byte
                # is still supposed to be part of a literal sequence, a new literal sequence
                # will have to be started
                
                if comp_data[literal_mode['index']] == 255:
                    literal_mode['status'] = False
                    
            
            else:
                # When literal mode is first turned on, one byte is added to the beginning of the
                # sequence.  The highest order bit indicates that literal mode is on, and the
                # remaining seven bits encode the length of the literal bytes to follow
                
                comp_data.append((129).to_bytes(1,byteorder='big'))
                comp_data.append(data[i])
                
                literal_mode['status'] = True
                literal_mode['index'] = len(comp_data)-2
                
            # When literal mode is on, only one byte will be added to the compressed data
            # on each iteration
            i += 1
        else:
            # Set the next_byte variable equal to the next byte in the data
            # list that comes after the data to be added to the dictionary.
            # If the index of this byte is past the end of the list, set
            # next_byte equal to the end character instead.  The end character
            # is '$' which has the decimal value 36 in UTF-8 encoding.
            
            if i+longest_len < len(data):
                next_byte = data[i+longest_len]
            else:
                next_byte = (36).to_bytes(1,byteorder='big')
                
            # Append the compressed data to the comp_data list
            
            comp_data.append(longest_start.to_bytes(1,byteorder='big'))
            comp_data.append(longest_len.to_bytes(1,byteorder='big'))
            comp_data.append(next_byte)
            
            # If literal mode was on, turn it off
            
            literal_mode['status'] = False
            
            # Since longest_len+1 bytes were just added to the compressed data,
            # advance the list index ahead by that many bytes
            
            i += longest_len+1
            
    return comp_data

def decompress(data):
    
    decomp = []
    
    literal_mode = {'status': False, 'length': 0}
    
    i = 0
    while i < len(data):
        
        if literal_mode['status'] == True:
            
            # If literal mode is on, simply append the next byte onto the
            # decompressed data list.  Decrement the count of remaining
            # literal bytes in this sequence by one
            
            decomp += [data[i]]
            literal_mode['length'] -= 1
            i += 1
            
            # If there are no remaining literal bytes in this sequence, exit
            # literal mode
            
            if literal_mode['length'] == 0:
                literal_mode['status'] = False
        
        else:
            start_param = int.from_bytes(data[i],byteorder='big')
            
            if start_param > 128:
                
                # If the first bit of the start parameter is on, the other
                # seven bits encode the length of the literal bytes to follow
                
                literal_mode['status'] = True
                literal_mode['length'] = start_param-128

                i += 1
            else:
                copy_len_param = int.from_bytes(data[i+1],byteorder='big')
            
                start = len(decomp)-start_param
                end = start+copy_len_param
            
                # Copy data onto the end of the decomp list from the dictionary, which is
                # made up of data that was previously decompressed.  Also add the next 
                # byte onto the end of the list as long as it's not the end character ('$').
                
                # If one or more '$' characters were part of the actual compressed data,
                # distinguish them from the end character by checking the value of the
                # loop index to see if it's at the end of the compressed data or not
            
                decomp += copy(decomp,start,end)+[((not data[i+2] == b'$') or (i < len(data)-3))*data[i+2]]
                
                i += 3
        
    return decomp

def main():
    parser = argparse.ArgumentParser(description='Uses the LZ77 algorithm to compress or decompress an input file')
    parser.add_argument('-i','--input',required=True,help='Enter the name of a file to compress or decompress. \
    Default action is to compress')
    parser.add_argument('-o','--output',required=False,default='',help='Specify an output filename.  \
    If argument isn\'t used, the default filename is the input filename with either _comp or _decomp \
    appended to the filename')
    parser.add_argument('-d','--decompress',required=False,action='store_true',help='Select decompress mode')
    args = parser.parse_args()
    
    input_filename = args.input
    output_filename = args.output
    
    if not args.decompress:
        if output_filename == '':
            output_filename = appendToFilename(input_filename,'_comp')
                    
        start_time = datetime.datetime.now()
        data = fileToList(input_filename)
        
        # Pass data to be compressed to the compress function.  Store returned compressed data in the
        # comp_data variable
        
        comp_data = compress(data)
        
        # Write compressed data to output file
        listToFile(output_filename,comp_data)
        
        end_time = datetime.datetime.now()
        time_delta = (end_time.microsecond-start_time.microsecond)/1000
        
        print('File successfully compressed')
        print('Compression ratio is: {0:1.2f}'.format(len(comp_data)/len(data)))
        print('Operation completed in:',round(time_delta),'milliseconds')
    
    else:
        output_filename = appendToFilename(input_filename,'_decomp')
        
        start_time = datetime.datetime.now()
        data = fileToList(input_filename)
        
        # Pass data to be decompressed to the decompress function.  Store returned decompressed data in the
        # decomp_data variable
        
        decomp_data = decompress(data)
        
        # Write decompressed data to output file
        listToFile(output_filename,decomp_data)
        
        end_time = datetime.datetime.now()
        time_delta = (end_time.microsecond-start_time.microsecond)/1000
        
        print('File successfully decompressed')
        print('Operation completed in:',round(time_delta),'milliseconds')

if __name__ == '__main__':
    main()
