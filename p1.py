import DES_8_Round as d
import random
import Bit_Key56 as extra
from textwrap import wrap
import possible_input_xors_distribution_table as p


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


char64=add_zero(bin(int("405C000004000000",16))[2:],64)

possible_xors_sboxes=p.get_table()

correct_pairs=[]

def key_bits_18():
	correct_pairs_index=0
	arr_counters_18=[]
	for x in range(2**19):
		arr_counters_18.append(0)

	stri=""

	for top in range(150000):

		P1=gen_string(64)
		P2=xor(P1,char64,64)

		P1=add_zero(hex(int(P1,2))[2:],16)
		cipher_text1=add_zero(bin(int(d.enc(P1),16))[2:],64)
		P2=add_zero(hex(int(P2,2))[2:],16)
		cipher_text2=add_zero(bin(int(d.enc(P2),16))[2:],64)

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
							if a+b+c == "010011101111111011" :
								correct_pairs.append([])
								correct_pairs[correct_pairs_index].append(P1)
								correct_pairs[correct_pairs_index].append(P2)
								correct_pairs_index+=1
							index=int(a+b+c,2)
							arr_counters_18[index]+=1

	return add_zero(bin(arr_counters_18.index(max(arr_counters_18)))[2:],18)

#key_bits_18()
correct_pairs=[['f0adee0676ff0125', 'b0f1ee0672ff0125'], ['9d2b69fded7d38a4', 'dd7769fde97d38a4'], ['f22a85fb53779489', 'b27685fb57779489'], ['60fc6f07af2ed00a', '20a06f07ab2ed00a'], ['9ba154bf9e0efb29', 'dbfd54bf9a0efb29'], ['8aa4424f193557b5', 'caf8424f1d3557b5'], ['b2f7be57c64a9ed4', 'f2abbe57c24a9ed4'], ['63826d0b295d9ad8', '23de6d0b2d5d9ad8'], ['6a7222324051a2d5', '2a2e22324451a2d5'], ['db3bcb3c5b1bc403', '9b67cb3c5f1bc403'], ['2eecd5f9cc20f65f', '6eb0d5f9c820f65f'], ['e9fd5432f4df70b0', 'a9a15432f0df70b0'], ['781530830680b78f', '384930830280b78f'], ['6a8bff7a28467599', '2ad7ff7a2c467599'], ['4826cd986cc21778', '087acd9868c21778'], ['874c2e057d0237e3', 'c7102e05790237e3'], ['a98fd3ecfb628173', 'e9d3d3ecff628173'], ['a1636babe68b6b63', 'e13f6babe28b6b63'], ['2bc9390a9b5a1f78', '6b95390a9f5a1f78'], ['797a88a3db7c0a81', '392688a3df7c0a81'], ['987d064981b44bd9', 'd821064985b44bd9'], ['1fad6b2f82872201', '5ff16b2f86872201'], ['7907d027090af09a', '395bd0270d0af09a'], ['e9aa35103b6f3a36', 'a9f635103f6f3a36'], ['3802b69ad483afc0', '785eb69ad083afc0'], ['dbc792062d6f601f', '9b9b9206296f601f'], ['106fe12e3f48ec9e', '5033e12e3b48ec9e'], ['0c0d617b2769237c', '4c51617b2369237c'], ['8fbfcfec2b2d39fc', 'cfe3cfec2f2d39fc'], ['66f7afeb8f66d096', '26abafeb8b66d096'], ['a5fdcff4ad35239a', 'e5a1cff4a935239a'], ['0cc6e3dad56067f6', '4c9ae3dad16067f6'], ['10ca4976e2fff986', '50964976e6fff986'], ['59fcee0e76fe0aab', '19a0ee0e72fe0aab'], ['6c9eeb033689cdf2', '2cc2eb033289cdf2'], ['4b986b07794dc3ba', '0bc46b077d4dc3ba'], ['0e2c148b49762b30', '4e70148b4d762b30'], ['fff08ed41b24937a', 'bfac8ed41f24937a'], ['9e21f1efcb3b4612', 'de7df1efcf3b4612'], ['1c294b56594e2b65', '5c754b565d4e2b65'], ['4dc5a6286a3e8249', '0d99a6286e3e8249'], ['6cf05c7056a47e2f', '2cac5c7052a47e2f'], ['d9247ab7fd2d2c3c', '99787ab7f92d2c3c'], ['d81b071dff061499', '9847071dfb061499'], ['d79f6e892a3e3ecb', '97c36e892e3e3ecb'], ['81437c0283cac77f', 'c11f7c0287cac77f'], ['83d66cb48c2a8281', 'c38a6cb4882a8281'], ['88a7006b2a1b3559', 'c8fb006b2e1b3559'], ['74cb933370febcb9', '3497933374febcb9'], ['56f1e11732ff057c', '16ade11736ff057c'], ['014d0b2e4b451e7b', '41110b2e4f451e7b'], ['2012a2012b086de5', '604ea2012f086de5'], ['14fea7ab75452af6', '54a2a7ab71452af6'], ['92cac5b87c4119f8', 'd296c5b8784119f8'], ['1f1da282cd93ecf1', '5f41a282c993ecf1'], ['07406e5d666bcb35', '471c6e5d626bcb35'], ['eb62cdd937d6f4f0', 'ab3ecdd933d6f4f0'], ['a0056a7d2c555511', 'e0596a7d28555511'], ['a87c1a8f1dec2973', 'e8201a8f19ec2973'], ['efc14dc92f2dc42b', 'af9d4dc92b2dc42b'], ['d1acbe02e56df555', '91f0be02e16df555']]

def key_bits_12():
	arr_counters_18=[]
	for x in range(2**13):
		arr_counters_18.append(0)

	stri=""

	for top in range(len(correct_pairs)-1):
		char64=add_zero(bin(int("405C000004000000",16))[2:],64)

		P1=correct_pairs[top][0]
		P2=correct_pairs[top][1]

		cipher_text1=add_zero(bin(int(d.enc(P1),16))[2:],64)
		cipher_text2=add_zero(bin(int(d.enc(P2),16))[2:],64)

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

def key_1and4():
	f_prime=char64[:32]
	counter=0

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
			cipher_text1=add_zero(bin(int(d.enc(P1),16))[2:],64)
			cipher_text2=add_zero(bin(int(d.enc(P2),16))[2:],64)


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

			#for brute in range(2**18):
			#111101 111000 101000 111010 110000 010011 101111 111011
			#111101111000101000111010110000010011101111111011
			#num=add_zero(bin(brute)[2:],18)
			# key1="111101"
			# key3="101000"
			# key4="111010"

			flag=1
			key_final=key1+"111000"+key3+key4+"110000"+"010011"+"101111"+"111011"
			#print(key_final)
			H=d.sbox(xor(h_input,key_final,48))
			H_star=d.sbox(xor(h_input_star,key_final,48))

			g=d.expand(xor(T[:32],H,32))
			g_star=d.expand(xor(T_star[:32],H_star,32))

			# key7=extra.blocks(extra.from_48_to_56(key_final))
			# keyg=d.gen_48bit(key7)
			input_xor_list=wrap(xor(g,g_star,48),6)
			output_xor_list=wrap(opp_per_func(G_prime),4)

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
			key1and4=key1+key4
	return key1+key4

#print(key1and4[:6],key1and4[6:])
key1and4="111101111010"

# -----------now 6 bit key !!! --------
def final_48_bit_key():
	return_key=""
	max_counter=0
	f_prime=char64[:32]

	for brute in range(2**6):
		counter=0
		num=add_zero(bin(brute)[2:],6)
		key1=key1and4[:6]
		key3=num
		# key4=num[12:18]
		key4=key1and4[6:]
		for p in correct_pairs :
			P1=p[0]
			P2=p[1]
			cipher_text1=add_zero(bin(int(d.enc(P1),16))[2:],64)
			cipher_text2=add_zero(bin(int(d.enc(P2),16))[2:],64)


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
			key_final="111101"+"111000"+key3+"111010"+"110000"+"010011"+"101111"+"111011"
			#print(key_final)
			H=d.sbox(xor(h_input,key_final,48))
			H_star=d.sbox(xor(h_input_star,key_final,48))

			g=d.expand(xor(T[:32],H,32))
			g_star=d.expand(xor(T_star[:32],H_star,32))

			# key7=extra.blocks(extra.from_48_to_56(key_final))
			# keyg=d.gen_48bit(key7)
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

