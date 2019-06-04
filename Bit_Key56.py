import code as c
import sys

p =  [14,17,11,24,1,5,3,28,15,6,21,10,23,19,12,4,26,8,16,7,27,20,13,2,41,52,31,37,47,55,30,40,51,45,33,48,44,49,39,56,34,53,46,42,50,36,29,32]
rotate= [1,1,2,2]
rotate_rev=[2,2,1,1]
from_64_to_56=[57,49,41,33,25,17,9,1,58,50,42,34,26,18,10,2,59,51,43,35,27,19,11,3,60,52,44,36,63,55,47,39,31,23,15,7,62,54,46,38,30,22,14,6,61,53,45,37,29,21,13,5,28,20,12,4]

def right_shift(string,d):
    Lfirst = string[0 : d]
    Lsecond = string[d :]
    Rfirst = string[0 : len(string)-d]
    Rsecond = string[len(string)-d : ]
    return Rsecond+Rfirst

def left_shift(string,d):
    Lfirst = string[0 : d]
    Lsecond = string[d :]
    Rfirst = string[0 : len(string)-d]
    Rsecond = string[len(string)-d : ]
    return Lsecond+Lfirst

def from_48_to_56(key):
	key_list=['x']*56
	i=0
	key=list(key)
	for x in p:
		key_list[x-1]=key[i]
		i=i+1
	string=''.join(key_list)
	return string

def blocks(key):
	block=['b']*9
	block[8]=key
	block[7]=right_shift(block[8][:28],2)+right_shift(block[8][28:],2)
	block[6]=right_shift(block[7][:28],2)+right_shift(block[7][28:],2)
	block[5]=right_shift(block[6][:28],1)+right_shift(block[6][28:],2)
	block[4]=right_shift(block[5][:28],1)+right_shift(block[5][28:],2)
	block[3]=right_shift(block[4][:28],2)+right_shift(block[4][28:],2)
	block[2]=right_shift(block[3][:28],2)+right_shift(block[3][28:],2)
	block[1]=right_shift(block[2][:28],1)+right_shift(block[2][28:],1)
	block[0]=right_shift(block[1][:28],1)+right_shift(block[1][28:],1)
	return block[7]

def brute_force(keyfinal):
	for x in range(2**14):
		digits=k.add_zero(bin(x)[2:],14)
		digits=list(digits)
		counter=0
		key=list(keyfinal)
		for i in range(56):
			if key[i] == 'x':
				key[i] = digits[counter]
				counter=counter+1
		key_56=''.join(key)
		key_64=['0']*64
		i=0
		for u in from_64_to_56:
			key_64[u-1]=key[i]
			i=i+1

		key_64=''.join(key_64)
		key_64=k.add_zero(hex(int(key_64,2))[2:],16)
		strng='133457799BBCDFF2'
		cipher=c.enc(strng)
		if c.enc2(strng,key_64) == cipher:
			return key_56
			break
	return










