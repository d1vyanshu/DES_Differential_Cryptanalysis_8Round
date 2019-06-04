import DES_8_Round as d
import random
import Bit_Key56 as extra
from textwrap import wrap
import possible_input_xors_distribution_table as p

# 111101111000010111111010110000010011101111111011
# 111101111000101000111010110000010011101111111011
# 111101111000101000111010110000010011101111111011
# 111101111000101000111010110000010011101111111011
# 111101 111000 101000 111010 110000 010011 101111 111011
# 111111111000111100111111110000010011101111111011
#                              010011101111111011
IP = [58, 50, 42, 34, 26, 18, 10, 2, 60, 52, 44, 36, 28, 20, 12, 4, 62, 54, 46, 38, 30, 22, 14, 6, 64, 56, 48, 40, 32, 24, 16, 8, 57, 49, 41, 33, 25, 17, 9, 1, 59, 51, 43, 35, 27, 19, 11, 3, 61, 53, 45, 37, 29, 21, 13, 5, 63, 55, 47, 39, 31, 23, 15, 7]
Inv_IP = [40,8,48,16,56,24,64,32,39,7,47,15,55,23,63,31,38,6,46,14,54,22,62,30,37,5,45,13,53,21,61,29,36,4,44,12,52,20,60,28,35,3,43,11,51,19,59,27,34,2,42,10,50,18,58,26,33,1,41,9,49,17,57,25]

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

def gen_string(n):
	left=bin(random.randint(0,2**n-1))[2:]
	left=add_zero(left,n)
	return left

def xor(string,key,num):
    answer=""
    for x in range(num):
        if string[x]==key[x] :
            answer+="0"
        elif string[x] == 'x' or key[x] == 'x' :
        	answer+="x"
        else :
            answer+="1"
    return answer

def opp_per_func(s_output):
  Inv_Per_Table=[9,17,23,31,13,28,2,18,24,16,30,6,26,20,10,1,8,14,25,3,4,29,11,19,32,12,22,7,5,27,15,21]
  s_final = ""
  for x in Inv_Per_Table:
    s_final += s_output[x-1]
  return s_final

char64=""

char_tmp=add_zero(bin(int("405C000004000000",16))[2:],64)

for m in Inv_IP:
	char64+=char_tmp[m-1]

char64=add_zero(char64,64)

possible_xors_sboxes=p.get_table()

correct_pairs_unfiltered=[]

def key_bits_18():
	correct_pairs_index=0
	arr_counters_18=[]
	for x in range(2**19):
		arr_counters_18.append(0)

	stri=""

	for top in range(150000):

		P1=gen_string(64)
		P2=xor(P1,char64,64)

		cipher_text1=""
		cipher_text2=""

		P1=add_zero(hex(int(P1,2))[2:],16)
		cipher_text1_tmp=add_zero(bin(int(d.enc(P1),16))[2:],64)
		P2=add_zero(hex(int(P2,2))[2:],16)
		cipher_text2_tmp=add_zero(bin(int(d.enc(P2),16))[2:],64)

		for m in IP:
			cipher_text1+=cipher_text1_tmp[m-1]

		for m in IP:
			cipher_text2+=cipher_text2_tmp[m-1]

		cipher_xor=xor(cipher_text1,cipher_text2,64)

		h_prime=cipher_xor[32:]
		H_prime=cipher_xor[:32]

		S_h_input=d.expand(cipher_text1[32:])
		S_h_input_star=d.expand(cipher_text2[32:])

		S_prime_e=xor(S_h_input,S_h_input_star,48)
		S_prime_o=opp_per_func(H_prime)

		S_h_input_list=wrap(S_h_input,6)
		S_h_input_star_list=wrap(S_h_input_star,6)
		S_prime_e_list=wrap(S_prime_e,6)
		S_prime_o_list=wrap(S_prime_o,4)


		Boxes=[1,4,5,6,7]
		
		#print(six_bit_key)
		flag=1
		six_bit_key=[[],[],[]]

		for u in Boxes:
			row1=int(S_prime_e_list[u],2)
			col1=int(S_prime_o_list[u],2)
			if len(possible_xors_sboxes[u][row1][col1]) == 0: 
				flag=0

		if flag == 1 :
			stri+="0"
			count = 0
			for x in Boxes :
				if x == 1 or x == 4:
					continue
				row = S_prime_e_list[x]
				row=int(row,2)
				col=S_prime_o_list[x]
				col=int(col,2)
				for poss in possible_xors_sboxes[x][row][col]:
					count = 1
					six_bit_key[x%5].append(xor(poss,S_h_input_list[x],6))
			
			if count == 1:
				correct_pairs_unfiltered.append([])
				correct_pairs_unfiltered[correct_pairs_index].append(P1)
				correct_pairs_unfiltered[correct_pairs_index].append(P2)
				correct_pairs_index+=1
				for a in six_bit_key[0]:
					for b in six_bit_key[1]:
						for c in six_bit_key[2]:
							# if a+b+c == "010011101111111011" :
							# 	correct_pairs.append([])
							# 	correct_pairs[correct_pairs_index].append(P1)
							# 	correct_pairs[correct_pairs_index].append(P2)
							# 	correct_pairs_index+=1
							index=int(a+b+c,2)
							arr_counters_18[index]+=1

	return add_zero(bin(arr_counters_18.index(max(arr_counters_18)))[2:],18)

key_18=key_bits_18()

def filter(correct_pairs_unfiltered):
	correct_pairs=[]
	correct_pairs_index=0

	stri=""

	for top in correct_pairs_unfiltered:

		P1=top[0]
		P2=top[1]

		cipher_text1=""
		cipher_text2=""

		cipher_text1_tmp=add_zero(bin(int(d.enc(P1),16))[2:],64)
		cipher_text2_tmp=add_zero(bin(int(d.enc(P2),16))[2:],64)

		for m in IP:
			cipher_text1+=cipher_text1_tmp[m-1]

		for m in IP:
			cipher_text2+=cipher_text2_tmp[m-1]

		cipher_xor=xor(cipher_text1,cipher_text2,64)

		h_prime=cipher_xor[32:]
		H_prime=cipher_xor[:32]

		S_h_input=d.expand(cipher_text1[32:])
		S_h_input_star=d.expand(cipher_text2[32:])

		S_prime_e=xor(S_h_input,S_h_input_star,48)
		S_prime_o=opp_per_func(H_prime)

		S_h_input_list=wrap(S_h_input,6)
		S_h_input_star_list=wrap(S_h_input_star,6)
		S_prime_e_list=wrap(S_prime_e,6)
		S_prime_o_list=wrap(S_prime_o,4)


		Boxes=[1,4,5,6,7]
		
		#print(six_bit_key)
		flag=1
		six_bit_key=[[],[],[]]

		for u in Boxes:
			row1=int(S_prime_e_list[u],2)
			col1=int(S_prime_o_list[u],2)
			if len(possible_xors_sboxes[u][row1][col1]) == 0: 
				flag=0

		if flag == 1 :
			stri+="0"
			count = 0
			for x in Boxes :
				if x == 1 or x == 4:
					continue
				row = S_prime_e_list[x]
				row=int(row,2)
				col=S_prime_o_list[x]
				col=int(col,2)
				for poss in possible_xors_sboxes[x][row][col]:
					count = 1
					six_bit_key[x%5].append(xor(poss,S_h_input_list[x],6))
			
			if count == 1:
				for a in six_bit_key[0]:
					for b in six_bit_key[1]:
						for c in six_bit_key[2]:
							if a+b+c == key_18 :
								correct_pairs.append([])
								correct_pairs[correct_pairs_index].append(P1)
								correct_pairs[correct_pairs_index].append(P2)
								correct_pairs_index+=1

	return correct_pairs

correct_pairs=filter(correct_pairs_unfiltered)

def key_bits_12(correct_pairs):
	arr_counters_18=[]
	for x in range(2**13):
		arr_counters_18.append(0)

	stri=""

	for top in range(len(correct_pairs)):
		char64=add_zero(bin(int("405C000004000000",16))[2:],64)

		P1=correct_pairs[top][0]
		P2=correct_pairs[top][1]

		cipher_text1=""
		cipher_text2=""

		cipher_text1_tmp=add_zero(bin(int(d.enc(P1),16))[2:],64)
		cipher_text2_tmp=add_zero(bin(int(d.enc(P2),16))[2:],64)

		for m in IP:
			cipher_text1+=cipher_text1_tmp[m-1]

		for m in IP:
			cipher_text2+=cipher_text2_tmp[m-1]

		cipher_xor=xor(cipher_text1,cipher_text2,64)

		h_prime=cipher_xor[32:]
		H_prime=cipher_xor[:32]

		S_h_input=d.expand(cipher_text1[32:])
		S_h_input_star=d.expand(cipher_text2[32:])

		S_prime_e=xor(S_h_input,S_h_input_star,48)
		S_prime_o=opp_per_func(H_prime)

		S_h_input_list=wrap(S_h_input,6)
		S_h_input_star_list=wrap(S_h_input_star,6)
		S_prime_e_list=wrap(S_prime_e,6)
		S_prime_o_list=wrap(S_prime_o,4)


		Boxes=[1,4,5,6,7]
		
		#print(six_bit_key)
		flag=1
		six_bit_key=[[],[]]

		for u in Boxes:
			row1=int(S_prime_e_list[u],2)
			col1=int(S_prime_o_list[u],2)
			if len(possible_xors_sboxes[u][row1][col1]) == 0: 
				flag=0

		if flag == 1 :
			stri+="0"
			count = 0
			for x in Boxes :
				if x == 5 or x == 6 or x == 7:
					continue
				row = S_prime_e_list[x]
				row=int(row,2)
				col=S_prime_o_list[x]
				col=int(col,2)
				for poss in possible_xors_sboxes[x][row][col]:
					count = 1
					l = 0
					if x == 4 :
						l = 1
					six_bit_key[l].append(xor(poss,S_h_input_list[x],6))
			
			if count == 1:
				for a in six_bit_key[0]:
					for b in six_bit_key[1]:
						index=int(a+b,2)
						arr_counters_18[index]+=1

	return add_zero(bin(arr_counters_18.index(max(arr_counters_18)))[2:],12)

key_12=key_bits_12(correct_pairs)

def key_s1_and_s4(correct_pairs,key_12,key_18):
	f_prime=char64[:32]

	key1and4=""
	max_counter=0

	for brute in range(2**12):
		counter=0
		num=add_zero(bin(brute)[2:],12)
		key1=num[:6]
		key4=num[6:]
		# key4=num[12:18]
		key3="0"*6
		for p in correct_pairs :
			P1=p[0]
			P2=p[1]

			cipher_text1=""
			cipher_text2=""


			cipher_text1_tmp=add_zero(bin(int(d.enc(P1),16))[2:],64)
			cipher_text2_tmp=add_zero(bin(int(d.enc(P2),16))[2:],64)

			for m in IP:
				cipher_text1+=cipher_text1_tmp[m-1]

			for m in IP:
				cipher_text2+=cipher_text2_tmp[m-1]


			T=cipher_text1
			T_star=cipher_text2

			cipher_xor=xor(cipher_text1,cipher_text2,64)

			h=cipher_text1[32:]
			h_star=cipher_text2[32:]

			h_prime=cipher_xor[32:]
			H_prime=cipher_xor[:32]

			h_input=d.expand(h)
			h_input_star=d.expand(h_star)

			G_prime=xor(h_prime,f_prime,32)

			counter_array=["0"*len(correct_pairs)]

			flag=1
			key_final=key1+key_12[:6]+key3+key4+key_12[6:]+key_18[:6]+key_18[6:12]+key_18[12:18]

			H=d.sbox(xor(h_input,key_final,48))
			H_star=d.sbox(xor(h_input_star,key_final,48))

			g=d.expand(xor(T[:32],H,32))
			g_star=d.expand(xor(T_star[:32],H_star,32))

			input_xor_list=wrap(xor(g,g_star,48),6)
			output_xor_list=wrap(opp_per_func(G_prime),4)


			# S box 5 used because it has g input like 31++4+
			row=input_xor_list[2]
			row=int(row,2)
			col=output_xor_list[2]
			col=int(col,2)
			if len(possible_xors_sboxes[2][row][col]) == 0 :
				flag = 0

			if flag == 1 :
				counter+=1

		if counter > max_counter:
			max_counter=counter
			#print(key4)
			key1and4=key1+key4
	return key1and4

key1and4=key_s1_and_s4(correct_pairs,key_12,key_18)



# -----------now 6 bit key !!! --------


def final_48_bit_key(correct_pairs,key1and4):
	return_key=""
	max_counter=0
	key_final=""
	f_prime=char_tmp[:32]

	for brute in range(2**6):
		counter=0
		num=add_zero(bin(brute)[2:],6)
		key1=key1and4[:6]
		key3=num
		key4=key1and4[6:]
		for p in correct_pairs :
			P1=p[0]
			P2=p[1]

			cipher_text1=""
			cipher_text2=""


			cipher_text1_tmp=add_zero(bin(int(d.enc(P1),16))[2:],64)
			cipher_text2_tmp=add_zero(bin(int(d.enc(P2),16))[2:],64)


			for m in IP:
				cipher_text1+=cipher_text1_tmp[m-1]

			for m in IP:
				cipher_text2+=cipher_text2_tmp[m-1]


			T=cipher_text1
			T_star=cipher_text2

			cipher_xor=xor(cipher_text1,cipher_text2,64)

			h=cipher_text1[32:]
			h_star=cipher_text2[32:]

			h_prime=cipher_xor[32:]
			H_prime=cipher_xor[:32]

			h_input=d.expand(h)
			h_input_star=d.expand(h_star)

			G_prime=xor(h_prime,f_prime,32)

			counter_array=["0"*len(correct_pairs)]
			
			flag=1

			key_final=key1+key_12[:6]+key3+key4+key_12[6:]+key_18[:6]+key_18[6:12]+key_18[12:18]

			H=d.sbox(xor(h_input,key_final,48))
			H_star=d.sbox(xor(h_input_star,key_final,48))

			g=d.expand(xor(T[:32],H,32))
			g_star=d.expand(xor(T_star[:32],H_star,32))

			input_xor_list=wrap(xor(g,g_star,48),6)
			output_xor_list=wrap(opp_per_func(G_prime),4)

			row=input_xor_list[4]
			row=int(row,2)
			col=output_xor_list[4]
			col=int(col,2)
			if len(possible_xors_sboxes[4][row][col]) == 0 :
				flag = 0

			if flag == 1 :
				counter+=1

		if counter > max_counter:
			max_counter=counter
			return_key=key_final
	return return_key



key_48=final_48_bit_key(correct_pairs,key1and4)
print(f"48 Bit key is : {key_48}")
print(f"56 Bit key is : {extra.answer(key_48)}")







