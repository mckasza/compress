# This file contains utility functions to be used by the compress.py script

def isValidFilename(filename):
    if '.' in filename:
            return True
            
    return False

def appendToFilename(f_name,string):
    if '.' in f_name:
        i = f_name.index('.')
        f_name = f_name[:i]+string+f_name[i:]
    else:
        f_name += string
        
    return f_name
        
        
    
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
    
def lengthOfCommonSubseq(seq1,seq2):
    
    i = 0
    while i < len(seq1) and i < len(seq2):
        if not seq1[i] == seq2[i]:
            break
        i += 1
        
    return i
        
	
def longestPrefix(data,pos,win_size,pv_size):
    
    start = 0+(pos > win_size)*(pos - win_size)
    
    if pos+pv_size < len(data):
        end = pos+pv_size
    else:
        end = len(data)
        
    longest_start = start
    longest_len = 0
    
    i = start
    while i < pos:
        lcs = lengthOfCommonSubseq(data[i:end],data[pos:end])
        
        if lcs > longest_len:
            longest_len = lcs
            longest_start = abs(pos-i)
        
        i += 1
        
    return longest_start,longest_len
                
        
        
        
    
