############# EX8 The length of the segment #############
import math
x1 = float(input())
y1 = float(input())
x2 = float(input())
y2 = float(input())

def distance(x1, y1, x2, y2):
    return(math.sqrt((x2-x1)**2 + (y2-y1)**2))
    
print(distance(x1, y1, x2, y2))


############# EX8 Negative Exponent #############
a = float(input())
n = float(input())

def power(a, n):
    return a**n
print(power(a, n))


############# EX 9 Maximum #############
import sys
inp = input()
row = int(inp.split()[0])
col = int(inp.split()[1])



arr = []
for i in range(row):
    arr.append([int(j) for j in input().split()])

maximum = -sys.maxsize - 1
x_out=0
y_out=0
for i in range(row):
    for j in range(col):
        if arr[i][j]>maximum:
            maximum = arr[i][j]
            x_out=i
            y_out=j
            
print(x_out, y_out)


############# EX9 Snowflake #############
n = int(input())
arr = []

for i in range(n):
    arr.append([0 for j in range(n)])


for row in range(n):
    for col in range(n):
        if row == col:
            arr[row][col] = '*'
            continue
        if row == (n//2):
            arr[row][col] = '*'
            continue
        if col == (n//2):
            arr[row][col] = '*'
            continue
        if (row + col) == n-1:
            arr[row][col] = '*'
            continue
        else:
            arr[row][col] = '.'
            continue

for i in range(n):
    for j in range(n):
        print(arr[i][j],end=' ')
    print()


############# EX10 The number of distinct numbers #############
print(len(set(input().split())))


############# EX10 The number of equal numbers #############
print(len(set(input().split()) & set(input().split())))


############# EX11 Number of occurrences #############

s = input()
s = s.split(' ')
occur = {}
occur_num = []
for word in s:
    if word in occur:
        occur[word] += 1
    else:
        occur[word] = 0
    occur_num.append(occur[word])

print(*occur_num)


############# EX11 Dictionary of synonyms #############num = int(input())
pairs = {}
for i in range(num):
    s = input().split()
    pairs[s[0]] = s[1]
single_word = input()

key_list = list(pairs.keys())
val_list = list(pairs.values())

if single_word in pairs.values():
    pos = val_list.index(single_word)
    print(key_list[pos])

else:
    print(pairs[single_word])
  
