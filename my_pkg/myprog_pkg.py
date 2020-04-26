#!/usr/bin/python3
import union as uni
import bin_to_others as binto
import sys

if __name__=='__main__':
	while True:
		num=int(input("Selcet menu: 1)conversion 2)union/intersection 3)exit ? "))
		if num==1:
			value=input("input binary number: ")
			binto.change(value)
		elif num==2:
			lst1=input("1st list: ").replace(',', ' ').replace('[',' ').replace(']',' ').split()
			lst1=list(map(int,lst1))
			lst2=input("2st list: ").replace(',',' ').replace('[',' ').replace(']',' ').split()
			lst2=list(map(int,lst2))
			uni.union(lst1,lst2)

		elif num==3:
			print("exit the program...")
			sys.exit()
