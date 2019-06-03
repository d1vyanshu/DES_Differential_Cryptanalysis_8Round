import DES_8_Round as d
import random
from textwrap import wrap
import possible_input_xors_distribution_table as p


#Convention is that after expansion is input_num before is input_num_before_exp
#task is to find F_prime , where we know T_l_prme and e_prime and h_prime is right of cipher
# 00540000 = 00000000010101000000000000000000
# d.expand()=000000000000001010101000000000000000000000000000
# 00100000 = 00000000000100000000000000000000

# key is 010011101111111011
#        010011101111111011
# 04000000 = 00000100000000000000000000000000
# d.expand()=000000001000000000000000000000000000000000000000
# 0A000000 = 00001010000000000000000000000000

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
    if len(string) != len(key) :
    	print("hahaha")
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

possible_xors_sboxes=p.get_table()

arr_counters_18=[]
for x in range(2**19):
	arr_counters_18.append(0)

stri=""

for top in range(150000):
	char64=add_zero(bin(int("405C000004000000",16))[2:],64)

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


	Boxes=[1,5,6,7]
	
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
			if x == 1:
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
						index=int(a+b+c,2)
						arr_counters_18[index]+=1

print(add_zero(bin(arr_counters_18.index(max(arr_counters_18)))[2:],18))

































# # Second round with low probability
# #In S[][] first is the round, second is the sbox
# expanded_second_round_input_xor="000000000000001010101000000000000000000000000000"
# reverse_per_second_round_output_xor="00000000000000000000000001000000"
# list_expanded_second_round_input_xor=wrap(expanded_second_round_input_xor,6)
# list_reverse_per_second_round_output_xor=wrap(reverse_per_second_round_output_xor,4)

# for x in range(8):
# 	for i in range(2**6):
# 		input_xor=add_zero(bin(i)[2:],6)
# 		output_xor=list_reverse_per_second_round_output_xor[x]
# 		if d.s_box(input_xor,x+1) == output_xor :
# 			S[1][x].append(input_xor)



# # First round with 1/4 probability
# #In S[][] first is the round, second is the sbox

# expanded_first_round_input_xor="000000001000000000000000000000000000000000000000"
# reverse_per_first_round_output_xor="00001010000000000000000000000000"
# list_expanded_first_round_input_xor=wrap(expanded_first_round_input_xor,6)
# list_reverse_per_first_round_output_xor=wrap(reverse_per_first_round_output_xor,4)

# for x in range(8):
# 	for i in range(2**6):
# 		input_xor=add_zero(bin(i)[2:],6)
# 		output_xor=list_reverse_per_first_round_output_xor[x]
# 		if d.s_box(input_xor,x+1) == output_xor :
# 			S[0][x].append(input_xor)
