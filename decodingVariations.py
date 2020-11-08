# Jose Elidio Campeiz Neto
def toChar(num):
  if isinstance(num, str):
    num = int(num)
  return chr(ord('A') + num - 1)

def decodeDP(S, i, DP):
  
  if i == len(S) :
    return 1
  if i >= len(S) or S[i] == '0':
    return 0
  if not i in DP:
    
    if S[i] == '1':
      DP[i] = decodeDP(S, i+1, DP) + decodeDP(S, i+2, DP)
      
    elif S[i] == '2' and i+1 < len(S) and int(S[i+1]) < 7:
      DP[i] = decodeDP(S, i+1, DP) + decodeDP(S, i+2, DP)
      
    else:
      DP[i] = decodeDP(S, i+1, DP)
      
  return DP[i]

def decodeS(S, DP = dict()): # return list of strings
  #print(S, DP)
  
  if len(S) == 0:
    return set()
  if len(S) == 1:
    return set(toChar(S))
  #elif len(S) == 2:
    #return set([ toChar(S[0]) + toChar(S[1]) , toChar(S) ])
  if not S in DP:
    # set of combinations of S
    combinations = set()
    
    # char of first idx
    first_letter = toChar(S[0]) 
    # set of strings that can be formed from the complement of first index
    first_comps = decodeS(S[1:], DP) 
    # combine the first letter with each word in complements 
    for word in first_comps:

      new_word = first_letter + word 
       # add to combinations of S
      combinations.add(new_word)

    # if char at idx 0 and 1 are within '10' and '26'
    if S[0] == '1' or (S[0] == '2' and int(S[1]) < 7 and int(S[1]) > 0):
      print('B',combinations)
      # first letter is char of idx 0 and 1
      first_letter = toChar(S[0:2]) 
      # set of strings that can be formed from the complement of second index
      second_comps = decodeS(S[2:], DP) 
      # combine the first letter with each word in complements 
      if len(second_comps) == 0:
        combinations.add(first_letter)
      for word in second_comps:
        new_word = first_letter + word 
        # add to combinations of S
        combinations.add(new_word)
    DP[S] = combinations
  
  return DP[S]
    
def decodeVariations(S):
  #char_dict = { num: toChar(num) for num in range (1, 27)}
  #print(char_dict)
  #print("!23")
  #print(char_map)
  #if '0' in set(S):
    #return 0
  
  DP = dict()
  ret = decodeDP(S, 0, DP)
  #a = decodeS(S,DP)
  #ret = len(a)
  #print(a)
  #input = '123'
  
  #print(ret)
  return ret
#print(decodeVariations('12'))
#print(get_char(12))

'''
                       ANS={ 1262 : {toChar(1) + call(262), toChar(12) + call(62)}  }
                       
                       ANS={ 1262 : {A + call(262) , L + call(62)}  }
                     
combination_call(1262): A+combination_call(262)    ,   L+combination_call(62) -> list of strings
                          B+c_call(62), Z+c_call(2)      F+call(2)
                            F+call(2),    B                   B
                              B


'''
#decodeVariations('1262')