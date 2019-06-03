import sys

def gen_key56(key_64):
  key_56 = ""
  p = [57,49,41,33,25,17,9,1,58,50,42,34,26,18,10,2,59,51,43,35,27,19,11,3,60,52,44,36,63,55,47,39,31,23,15,7,62,54,46,38,30,22,14,6,61,53,45,37,29,21,13,5,28,20,12,4]
  for x in p:
    key_56 += key_64[x-1]
  #print(key_56)
  return key_56

def circular_shift(key,n):
  temp=""
  temp=key[n:]+key[:n]
  return temp

def split_key(key_56):
  l,r=key_56[:28],key_56[28:]
  return l,r

def gen_48bit(key):
  key_48 = ""
  p =  [14,17,11,24,1,5,3,28,15,6,21,10,23,19,12,4,26,8,16,7,27,20,13,2,41,52,31,37,47,55,30,40,51,45,33,48,44,49,39,56,34,53,46,42,50,36,29,32]
  for x in p:
    key_48+=key[x-1]
  return key_48

def gen_key(key):
  key_64 = ""
  for i in range(16):
    key_64 += '{0:04b}'.format(int(key[i], base =16))               #Converting to binary
  #print(key_64)
  round_shifts = [1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1]
  key_56=gen_key56(key_64)                          #parity bits dropped
  left_key,right_key = split_key(key_56)            #key split
  round_keys = list()
  for index in range(8):                            #changeno
    L=circular_shift(left_key,round_shifts[index])
    R=circular_shift(right_key,round_shifts[index])
    round_key=gen_48bit(L+R)                        #48 bit key generated
    round_keys.append(round_key)                    #list of keys for all round
    left_key=L
    right_key=R
  return round_keys

def permutation(plain_text):
  p = ""
  IP = [58, 50, 42, 34, 26, 18, 10, 2, 60, 52, 44, 36, 28, 20, 12, 4, 62, 54, 46, 38, 30, 22, 14, 6, 64, 56, 48, 40, 32, 24, 16, 8, 57, 49, 41, 33, 25, 17, 9, 1, 59, 51, 43, 35, 27, 19, 11, 3, 61, 53, 45, 37, 29, 21, 13, 5, 63, 55, 47, 39, 31, 23, 15, 7]
  for x in IP :
    p += plain_text[x-1]
  return p

def inv_per(text):
  final = ""
  IP = [40,8,48,16,56,24,64,32,39,7,47,15,55,23,63,31,38,6,46,14,54,22,62,30,37,5,45,13,53,21,61,29,36,4,44,12,52,20,60,28,35,3,43,11,51,19,59,27,34,2,42,10,50,18,58,26,33,1,41,9,49,17,57,25]
  for x in IP:
    final += text[x-1]
  return final

def per_func(s_output):
  PERMUTATION_TABLE = [16,7,20,21,29,12,28,17,1,15,23,26,5,18,31,10,2,8,24,14,32,27,3,9,19,13,30,6,22,11,4,25]
  s_final = ""
  count=1;
  for x in PERMUTATION_TABLE:
    #print(f"{count} : {x}")
    count=count+1
    s_final += s_output[x-1]
  return s_final

def expand(text):
  temp = ""
  EXPANSION_TABLE = [32,1,2,3,4,5,4,5,6,7,8,9,8,9,10,11,12,13,12,13,14,15,16,17,16,17,18,19,20,21,20,21,22,23,24,25,24,25,26,27,28,29,28,29,30,31,32,1]
  for x in EXPANSION_TABLE :
    temp += text[x-1]
  return temp

count=0

def sbox(s_input):
  global count
  s_out = ""
  S = [
  # Box-1
  [
  [14,4,13,1,2,15,11,8,3,10,6,12,5,9,0,7],
  [0,15,7,4,14,2,13,1,10,6,12,11,9,5,3,8],
  [4,1,14,8,13,6,2,11,15,12,9,7,3,10,5,0],
  [15,12,8,2,4,9,1,7,5,11,3,14,10,0,6,13]
  ],
  # Box-2

  [
  [15,1,8,14,6,11,3,4,9,7,2,13,12,0,5,10],
  [3,13,4,7,15,2,8,14,12,0,1,10,6,9,11,5],
  [0,14,7,11,10,4,13,1,5,8,12,6,9,3,2,15],
  [13,8,10,1,3,15,4,2,11,6,7,12,0,5,14,9]
  ],

  # Box-3

  [
  [10,0,9,14,6,3,15,5,1,13,12,7,11,4,2,8],
  [13,7,0,9,3,4,6,10,2,8,5,14,12,11,15,1],
  [13,6,4,9,8,15,3,0,11,1,2,12,5,10,14,7],
  [1,10,13,0,6,9,8,7,4,15,14,3,11,5,2,12]

  ],

  # Box-4
  [
  [7,13,14,3,0,6,9,10,1,2,8,5,11,12,4,15],
  [13,8,11,5,6,15,0,3,4,7,2,12,1,10,14,9],
  [10,6,9,0,12,11,7,13,15,1,3,14,5,2,8,4],
  [3,15,0,6,10,1,13,8,9,4,5,11,12,7,2,14]
  ],

  # Box-5
  [
  [2,12,4,1,7,10,11,6,8,5,3,15,13,0,14,9],
  [14,11,2,12,4,7,13,1,5,0,15,10,3,9,8,6],
  [4,2,1,11,10,13,7,8,15,9,12,5,6,3,0,14],
  [11,8,12,7,1,14,2,13,6,15,0,9,10,4,5,3]
  ],
  # Box-6

  [
  [12,1,10,15,9,2,6,8,0,13,3,4,14,7,5,11],
  [10,15,4,2,7,12,9,5,6,1,13,14,0,11,3,8],
  [9,14,15,5,2,8,12,3,7,0,4,10,1,13,11,6],
  [4,3,2,12,9,5,15,10,11,14,1,7,6,0,8,13]

  ],
  # Box-7
  [
  [4,11,2,14,15,0,8,13,3,12,9,7,5,10,6,1],
  [13,0,11,7,4,9,1,10,14,3,5,12,2,15,8,6],
  [1,4,11,13,12,3,7,14,10,15,6,8,0,5,9,2],
  [6,11,13,8,1,4,10,7,9,5,0,15,14,2,3,12]
  ],
  # Box-8

  [
  [13,2,8,4,6,15,11,1,10,9,3,14,5,0,12,7],
  [1,15,13,8,10,3,7,4,12,5,6,11,0,14,9,2],
  [7,11,4,1,9,12,14,2,0,6,10,13,15,3,5,8],
  [2,1,14,7,4,10,8,13,15,12,9,0,3,5,6,11]
  ]

  ]


  for i in range(8):
    row = int(s_input[6*i]+s_input[6*i+5] , base =2)
    column = int(s_input[6*i+1]+s_input[6*i+2]+s_input[6*i+3]+s_input[6*i+4] , base =2)
    s_out += '{0:04b}'.format(S[i][row][column])
    #print(f"{'{0:04b}'.format(S[i][row][column])}",end='')
    count=count+1

  s_final = per_func(s_out)
  #print()
  #print(s_final)
  return s_final

def s_box(str,num):
  S = [
  # Box-1
  [
  [14,4,13,1,2,15,11,8,3,10,6,12,5,9,0,7],
  [0,15,7,4,14,2,13,1,10,6,12,11,9,5,3,8],
  [4,1,14,8,13,6,2,11,15,12,9,7,3,10,5,0],
  [15,12,8,2,4,9,1,7,5,11,3,14,10,0,6,13]
  ],
  # Box-2

  [
  [15,1,8,14,6,11,3,4,9,7,2,13,12,0,5,10],
  [3,13,4,7,15,2,8,14,12,0,1,10,6,9,11,5],
  [0,14,7,11,10,4,13,1,5,8,12,6,9,3,2,15],
  [13,8,10,1,3,15,4,2,11,6,7,12,0,5,14,9]
  ],

  # Box-3

  [
  [10,0,9,14,6,3,15,5,1,13,12,7,11,4,2,8],
  [13,7,0,9,3,4,6,10,2,8,5,14,12,11,15,1],
  [13,6,4,9,8,15,3,0,11,1,2,12,5,10,14,7],
  [1,10,13,0,6,9,8,7,4,15,14,3,11,5,2,12]

  ],

  # Box-4
  [
  [7,13,14,3,0,6,9,10,1,2,8,5,11,12,4,15],
  [13,8,11,5,6,15,0,3,4,7,2,12,1,10,14,9],
  [10,6,9,0,12,11,7,13,15,1,3,14,5,2,8,4],
  [3,15,0,6,10,1,13,8,9,4,5,11,12,7,2,14]
  ],

  # Box-5
  [
  [2,12,4,1,7,10,11,6,8,5,3,15,13,0,14,9],
  [14,11,2,12,4,7,13,1,5,0,15,10,3,9,8,6],
  [4,2,1,11,10,13,7,8,15,9,12,5,6,3,0,14],
  [11,8,12,7,1,14,2,13,6,15,0,9,10,4,5,3]
  ],
  # Box-6

  [
  [12,1,10,15,9,2,6,8,0,13,3,4,14,7,5,11],
  [10,15,4,2,7,12,9,5,6,1,13,14,0,11,3,8],
  [9,14,15,5,2,8,12,3,7,0,4,10,1,13,11,6],
  [4,3,2,12,9,5,15,10,11,14,1,7,6,0,8,13]

  ],
  # Box-7
  [
  [4,11,2,14,15,0,8,13,3,12,9,7,5,10,6,1],
  [13,0,11,7,4,9,1,10,14,3,5,12,2,15,8,6],
  [1,4,11,13,12,3,7,14,10,15,6,8,0,5,9,2],
  [6,11,13,8,1,4,10,7,9,5,0,15,14,2,3,12]
  ],
  # Box-8

  [
  [13,2,8,4,6,15,11,1,10,9,3,14,5,0,12,7],
  [1,15,13,8,10,3,7,4,12,5,6,11,0,14,9,2],
  [7,11,4,1,9,12,14,2,0,6,10,13,15,3,5,8],
  [2,1,14,7,4,10,8,13,15,12,9,0,3,5,6,11]
  ]

  ]  
  answer=""
  r=int((str[0]+str[5]),2)
  c=int((str[1]+str[2]+str[3]+str[4]),2)
  e1=S[num-1][r]
  u=bin(e1[c])# u is a string
  length=len(u)
  if length<6 :
      for x in range(2,8-length):
          answer+="0"
      for x in range(length-2):
          answer+=u[x+2]
  else :
      answer=u[2]+u[3]+u[4]+u[5]

  return answer

def func(text, key):
  exp = expand(text)                    #32 bit data converted to 48 bit
  s_input = '{0:048b}'.format(int(exp, base=2) ^ int(key, base =2))
  s_out = sbox( s_input)                 #operating sbox
  return s_out

def encrypt(plain_text, sub_keys):
  plain_textb = ""
  for i in range(16):
    plain_textb += '{0:04b}'.format(int(plain_text[i], base =16))
  #plain_textp = permutation(plain_textb)       #Intital permutation
  plain_textp = plain_textb                   #Intital permutation removed
  left,right = plain_textp[:32],plain_textp[32:]
  for i in range(7):                   #changeno
    out = func(right,sub_keys[i])     #function called on right half data
    temp = int(out, base=2) ^ int(left, base=2)   #XOR
    left =right
    right = '{0:032b}'.format(temp)
    # if i == 5 :
    #   print(f"6th round output : {left+right}")

  out = func(right,sub_keys[7])
  temp = int(out, base=2) ^ int(left , base=2)
  left = '{0:032b}'.format(temp)
  #final = inv_per(left+right)            #Inverse permutation after 4 rounds
  final = left+right             #Inverse permutation removed
  cipher = hex(int(final,2))[2:]
  return cipher

def enc(plain_text):
  key_64= '133457799BBCDFF1'
  sub_keys= gen_key(key_64)
  #plain_text=str(sys.argv[1])
  #splain_text='133457799BBCDFF1'
  cipher_text = encrypt(plain_text,sub_keys)
  #print(cipher_text)
  return cipher_text

def enc2(plain_text,key):
  sub_keys= gen_key(key)
  cipher_text = encrypt(plain_text,sub_keys)
  return cipher_tex

#print(enc('133457799BBCDFF1'))