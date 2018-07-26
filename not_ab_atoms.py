## Simge Demir
## June, 2018
## program for adding no ab() atoms to the constraints 

import re
import sys

def regex(atom,searchVariable):
	return re.findall(atom+r"\((\w+)\)",searchVariable)

def removeConstraint():
	#searches the constraints and ignores the one that does not include given atoms
	removal=[]
	for i in range(0,len(r1)):
		for x in range (2,len(sys.argv)):
			temp=regex(sys.argv[x],r1[i])
			if len(temp)==0:
				print(r1[i] + " does not include the atom: "+ sys.argv[x] +"\n")
				removal.append(r1[i])
				break
			elif r1[i].find("}", r1[i].find(sys.argv[x])) != -1:
				print(r1[i] + " include '}' at the end of the line \n")
				removal.append(r1[i])
				break

	for element in range(0,len(removal)):
		r1.remove(removal[element])
		
def createNewline(i):
	newLine=""
	newLine+="\n{ab(r"+str(i)
	for y in range(0,len(r2)):
		newLine+="," + r2[y]
	newLine+=(") : ")

	for x in range (2,len(sys.argv)):
		temp=regex(sys.argv[x],r1[i])
		#print(temp)
		if len(temp)==1:
			if x>2:
				newLine+="," + sys.argv[x]+ "("+ r2[x-2] + ")"
			else:
				newLine+=sys.argv[x]+ "("+ r2[x-2] + ")"
		else:
			if x>2:
				newLine+="," + sys.argv[x]
				newLine+="("+ r2[x-2] + ")"
				for j in range(1,len(temp)):
					newLine+=","+ sys.argv[x]
					newLine+= "("+ r2[x-2+j] + ")"
			else:
				newLine+=sys.argv[x]
				newLine+="("+ r2[x-2] + ")"
				for j in range(1,len(temp)):
					newLine+=","+ sys.argv[x]
					newLine+= "("+ r2[x-2+j] + ")"

	newLine+="}."
	#print (newLine)
	newLine2=""
	newLine2+="\n:~ ab(r" + str(i)
	for y in range(0,len(r2)):
		newLine2+="," + r2[y]
	newLine2+="). [1" 
	for y in range(0,len(r2)):
		newLine2+="," + r2[y]
	newLine2+=",r" +str(i)+ "]\n"
						
	return newLine,newLine2
	
inputFile=sys.argv[1]
try:
	with open(inputFile) as f:
		lines=f.readlines()
	f.close()
except FileNotFoundError:
	print(inputFile+ " does not exist. ")
	
else:
	txt=""
	#getting the text in the file 
	for i in range (0,len(lines)):
		txt+=lines[i]
	#print (lines)

	## finding all the constraints in the .lp file
	r1=re.findall(r"\n(:-.*).",txt)
	
	removeConstraint() ## removing the constraint if it does not include the given atom

	if len(r1)==0: ##if there is no constraint with the given atoms
		print("THERE IS NO CONSTRAINT WITH THE GIVEN ATOMS, OUTPUT FILE IS NOT CREATED")
		sys.exit()

	for i in range(0,len(r1)):

		r2=[] ##list for the variables that will be written in not ab() atom.
		for x in range (2,len(sys.argv)):
			temp=regex(sys.argv[x],r1[i])
			r2+=temp

		for k in range(0,len(lines)):
			if (lines[k]== (r1[i]+".\n")): ##finding the constraint in the file

				##adding not ab() atoms 
				r1[i]+= ",not ab(r" +str(i)
				for y in range(0,len(r2)):
					r1[i]+= "," + r2[y]  
				r1[i]+= ")." + "\n"	
				lines[k]=r1[i] ##changing the line with the new one which is overwritten with not ab()

				## adding the following new line at the end:
				## {ab(r#,T,T1) : timea(T),timea(T1)}.
				#print (newLine)
				newline,newline2=createNewline(i)
				lines.append(newline) 

				##adding the second new line:	
				#:~ ab(r#,T,T1). [1,T,T1,r#]
				lines.append(newline2)		

	lines.append("\n#show ab/2.\n")
	lines.append("#show ab/3.\n")
	
	## creating the output file and writing the last version of the text 
	out=open('output.lp','w')

	for i in range (0,len(lines)):
		out.write(lines[i])
