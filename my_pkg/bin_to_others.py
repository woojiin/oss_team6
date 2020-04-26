#!/usr/bin/python3

def change(x):
	dec=int('0b'+x,2)
	o=format(dec,'o')
	h=format(dec, 'x')
	print("=> OCT> ",o)
	print("=> DEC> ",dec)
	print("=> HEX> ",h)

if __name__=='__main__':
	value=input("input binary number: ")
	change(value)

