from sys import argv, exit
if len(argv)<2:raise Exception("No file given!\nUsage: python3 m.py <filename> [-i] [-d] [-b]\n\tpython3 m.py -help")
if '-help' in argv:print('''
An interpreter for the Mini-Eslini erlang by Ave Christopher.

Language specifics:
	- the language is intended to be used like ASSEMBLY, except that it truly only uses bytes
	- it has a very minimal amount of commands (4, to be precise), which each take their following bytes as arguments:
		- the 0 (read '\033[34mdouble\033[0m') reads two bytes
		- the 1 (read '\033[34mpoint\033[0m') takes byte at the position in code pointed to by the next byte
		- the 2 (read '\033[34mink\033[0m') increments the byte pointed to by the next byte (no '\033[34mpoint\033[0m' needed) by the byte after that (modulo 256)
		- the 3 (read '\033[34migo\033[0m') moves the code pointer to the position in code pointed to by the overnext byte if the next byte is a 0 ('\033[34mpoint\033[0m' needed)
		- for technical reasons, if a '\033[34mdouble\033[0m' takes a 0 as first byte or a '\033[34mpoint\033[0m' points to a 1, a 0 or 1 is returned by default
		- a '\033[34mbyte\033[0m' can either be a number or a combination of numbers (this applies to '\033[34mdouble\033[0m' and '\033[34mpoint\033[0m')
	- it is Turing complete (I'm trying to write an OS in it, actually)

Inplementation details:
	- '-d' forces the interpreter to print debug messages at each step
	- programs are assumed to be ASCII lists of integers (e.g. '2 128 128 3 1 128 0 0'); to use input as bytes, use the '-b' suffix
	- the '\033[34mdouble\033[0m' only makes sense when using it with the '\033[34mpoint\033[0m', since arithmetics are done mod 256
	- the code is the original stack, thus you could say that the stack is executed instead (self-modifying code ftw!)
	- stack size is dynamically allocated
	- when the code pointer reaches the end of the input, the program is terminated, the original code is removed, and the rest is given as output (ASCII by default, '-i' forces it to return a list of integers)
	- the first element in the stack is the 0th element (OBOE)
''')
	exit()
if '-b' in argv: # read input as bytes
	with open(argv[1], 'rb') as x:stack=[int(i) for i in x.read()]
else:
	with open(argv[1], 'r') as x:
		try:
			stack=[int(i) for i in x.read().split()]
			if max(stack)>255:raise Exception("Programs cannot contain bytes larger than 256!")
		except ValueError:raise Exception("Programs must only consist of integers or whitespace!")
cl=len(stack) # code length (for I/O)
cp=0 # codepointer
io=0 # integer output
do=0 # debug
if '-i' in argv:io=1
if '-d' in argv:do=1
def get(x,g=0): # evaluate byte
	if do:print(x)
	global stack,cp
	if b(x)==0:
		a();a()
		if b(x+1)==0:return(0)
		else:return(get(b(x+1))*256+get(b(x+2))) # XXX
	elif b(x)==1:
		a();
		if len(stack)<b(x+1):raise Exception("Invalid code reference at byte {}".format(cp))
		elif g==1:return(1)
		else:return(get(b(x+1),1))
	else:a();return(b(x))
def a(x=None): # increment code pointer
	global cp, stack
	if x:cp=x
	else:cp+=1
	while len(stack)<=cp:stack.append(0)
def b(x): # get stack element
	global stack
	while len(stack)<=x:stack.append(0)
	return(stack[x])
def c(): # debug
	global stack, cp
	print(':'.join(['{:>3}'.format(i) for i in range(len(stack))]))
	print(':'.join(['{:>3}'.format(i) for i in stack]))
	print(' '.join([('   ','  ^')[i==cp] for i in range(len(stack))]))
while cp<cl:
	if do:c()
	i=b(cp)
	if i==2:
		a()
		x = get(cp)
		y = get(cp)
		while len(stack)<=x:stack.append(0)
		stack[x] = (stack[x]+y)%256
	elif i==3:
		a()
		x = get(cp)
		y = get(cp)
		if x==0:a(y)
	else:raise Exception("Invalid byte at {}".format(cp))
if do:c(),print("Output:")
if io:print(':'.join([str(i) for i in stack[cl:]]))
else:print(''.join([chr(i) for i in stack[cl:]]))
