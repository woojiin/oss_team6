#!/usr/bin/python3

def union(lst1,lst2):
	set1= set(lst1)
	set2= set(lst2)
	print("=> union ",set1|set2)
	print("=> intersection  ",set1&set2)


if __name__=='__main__': 
	lst1=input("1st list: ").replace(","," ").replace('[',' ').replace(']', ' ').split()
	lst1=list(map(int,lst1))
	print(lst1)
	lst2=input("2st list: ").replace(","," ").replace('[',' ').replace(']',' ').split()
	lst2=list(map(int,lst2))
	union(lst1,lst2)
