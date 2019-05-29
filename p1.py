import code as c
import random
from textwrap import wrap
char=""

def inverse_table(table,size):
	new=list()
	for x in range(size):
		if((x+1) in table) :
			num=table.index(x+1)+1
			new.append(num)
		else :
			new.append(x)
	return new

def add_zero(x,num):
    h=len(x)
    if h<num:
        for i in range(num-h):
            x="0"+x
    return x

char=add_zero(bin(int("405C000004000000",16))[2:],64)

char=add_zero(char,64)

def gen_string(n):
	left=bin(random.randint(0,2**n-1))[2:]
	left=add_zero(left,n)
	return left

def xor(string,key,num):
    answer=""
    for x in range(num):
        if string[x]==key[x] :
            answer+="0"
        else :
            answer+="1"
    return answer

def opp_per_func(s_output):
  Inv_Per_Table=[9,17,23,31,13,28,2,18,24,16,30,6,26,20,10,1,8,14,25,3,4,29,11,19,32,12,22,7,5,27,15,21]
  s_final = ""
  for x in Inv_Per_Table:
    s_final += s_output[x-1]
  return s_final

def key_42():
	key_42_bits=""
	for p in range(1,8):
		keys=[[],[],[],[],[],[],[]]
		final=set()
		for i in range(7):
			P1=gen_string(64)
			P2=xor(P1,char,64)

			P1=add_zero(hex(int(P1,2))[2:],16)
			cipher_text1_tmp=add_zero(bin(int(c.enc(P1),16))[2:],64)

			P2=add_zero(hex(int(P2,2))[2:],16)

			cipher_text2_tmp=add_zero(bin(int(c.enc(P2),16))[2:],64)

			cipher_text1=""
			cipher_text2=""

			for m in IP:
				cipher_text1+=cipher_text1_tmp[m-1]

			for m in IP:
				cipher_text2+=cipher_text2_tmp[m-1]

			d=xor(cipher_text1,cipher_text2,64)[32:]
			left=xor(cipher_text1,cipher_text2,64)[:32]

			B=c.per_func('11110000000000000000000000000000')

			D=xor(B,left,32)

			D_before=opp_per_func(D)

			So=wrap(D_before,4)

			input_last_round1=c.expand(cipher_text1[32:])
			input_last_round2=c.expand(cipher_text2[32:])

			Se=wrap(input_last_round1,6)
			Se_star=wrap(input_last_round2,6)

			for x in range(2**6):
				key=add_zero(bin(x)[2:],6)
				y=xor(Se[p],key,6)
				z=xor(Se_star[p],key,6)
				y1=c.s_box(y,p+1)
				y2=c.s_box(z,p+1)
				if xor(y1,y2,4) == So[p] :
					keys[i].append(key)

		for x in range(1,5):
			keys[x]=set(keys[x]).intersection(set(keys[x-1]))

		key_42_bits+=list(keys[4])[0]

	return("xxxxxx"+key_42_bits)
