#!/usr/bin/python3

n=int(input("how many numbers? "))
lst=[]

for i in range(0,n,1):
    lst.append(int(input("number?")))

aver_num=sum(lst)/len(lst)
print(aver_num)

