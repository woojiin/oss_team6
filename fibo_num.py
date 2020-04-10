#!/usr/bin/python3

arry=[1,1]
n=int(input("fibonacci number?"))

for i in range(2,n,1):
	new_num=arry[i-1]+arry[i-2]
	arry.append(new_num)

print(arry)
print("F%d = %d" % (n, arry[n-1]))
