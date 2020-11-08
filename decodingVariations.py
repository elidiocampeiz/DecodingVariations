# Jose Elidio Campeiz Neto
import timeit

# helper
def toChar(num):
  if isinstance(num, str):
    num = int(num)
  return chr(ord('A') + num - 1)

# Decode top down using memo
def decodeDP(S, i, DP):
  
  if i == len(S):
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

# botton up approach
def decodeIterative(S, i=None, D=None):
  n = len(S)
  if n == 0:
      return 0
  dp = [None]*(n+2)
  dp[n] = 1
  dp[n+1] = 0
  for i in range(n-1, -1, -1):
    # print(i, S[i])
    if S[i] == '0':
      dp[i] = 0
    elif S[i] == '1':
      dp[i] = dp[i+1] + dp[i+2]
    elif S[i] == '2' and i+1 < len(S) and int(S[i+1]) < 7:
      dp[i] = dp[i+1] + dp[i+2]
    else:
      dp[i] = dp[i+1]
  return dp[0]

# helper function to normalize parameters 
def decodeS_util(S, i=None, DP = dict()):
    if '0' in set(S):
        return 0
    ret = decodeS(S, DP)
    return len(ret)

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
    #   print('B',combinations)
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

# General Interface function
def decodeVariations(S, algo ):
  if len(S) == 0:
    return 0
  #char_dict = { num: toChar(num) for num in range (1, 27)}
  i = 0
  DP = dict()
  ret = algo(S, i, DP)
  return ret

# Functions that tests and compares the running time of each algo implementation
def test_implementation():

    functions = {
        'dp_permut': lambda x: decodeVariations(x, decodeS_util),
        'dp_memo': lambda x:  decodeVariations(x, decodeDP),
        'dp_bottom': lambda x: decodeVariations(x, decodeIterative)
    }
    times = {
        'dp_permut': 0,
        'dp_memo': 0, 
        'dp_bottom': 0, 
    }
    test = [ 
        ('1262', 3), 
        ('26', 2), 
        ('127', 2), 
        ('1270', 0), 
        ('83778549129', 2), 
        ('8254779486', 2),
        ('122231131122', 120), 
        ('122212313113', 126),
        ('321121311231', 65),
        ('1222123130113', 0),
        ('', 0),
        ('12312121212112111232345432', 9582)
        ]

    for algo in functions:
        for s, ex in test:
            result = functions[algo](s)
            times[algo] += timeit.timeit( lambda:functions[algo](s), number=1)
            if ex != result:
                print('Fail ',s, algo, ex, result)
                assert ex == result
            
    print('Total times:')
    for algo in times:
        # Format and print result
        print(algo, '{:.10f}s'.format(times[algo]).rjust(30-len(algo),' '))
    
    print('Average times:')
    for algo in times:
        # Format and print result
        print(algo, '{:.10f}s'.format(times[algo]/len(test)).rjust(30-len(algo),' '))


'''
Recursion Relationship
                       ANS={ 1262 : {toChar(1) + call(262), toChar(12) + call(62)}  }
                       
                       ANS={ 1262 : {A + call(262) , L + call(62)}  }
                     
combination_call(1262): A+combination_call(262)    ,   L+combination_call(62) -> list of strings
                          B+c_call(62), Z+c_call(2)      F+call(2)
                            F+call(2),    B                   B
                              B


'''
#decodeVariations('1262')

if __name__ == "__main__":
    S = '1262'
    expected = 3
    # test_implementation()
    ret = 0
    DP = {}
    ret = decodeDP(S, 0, DP)
    dp_permut = timeit.timeit(lambda: decodeS_util(S, 0, DP), number=1)
    dp_memo = timeit.timeit(lambda : decodeDP(S, 0, DP), number=1)
    dp_bottom = timeit.timeit(lambda: decodeIterative(S, 0, DP), number=1)
    
    print('Permutations time:                   {:10f}s'.format(dp_permut))
    print('DP Top Down with Memoization time:   {:10f}s'.format(dp_memo))
    print('DP bottom up time:                   {:10f}s'.format(dp_bottom))