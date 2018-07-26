## binarySearch algorithm to find the critical point of the unsatCheck  
## Simge Demir
## July, 2018

import subprocess
import sys
import re
import json

def clingoResult(maxT):
	clingo = subprocess.Popen(
   		"clingo --outf=2 -c maxT={} {} ".format(maxT,' '.join(sys.argv[1:])),
    	shell=True, stdout=subprocess.PIPE, stderr=sys.stderr)
	clingoout, clingoerr = clingo.communicate()
	del clingo
	clingoout = json.loads(clingoout.decode('utf-8'))
	result = clingoout['Result']

	return result

def binarySearch(maxT):
	first = 1
	last = maxT-1
	found = False
	prev=None
	midpoint=maxT

	result=clingoResult(midpoint)

	if result=='SATISFIABLE':
		return ("NO PROBLEM")
	
	while not found:
		midpoint = int((first + last)/2)
		result=clingoResult(midpoint)

		if result=='UNSATISFIABLE':
			last = midpoint-1

			result=clingoResult(midpoint-1)

			if result=='SATISFIABLE':
				found=True
				return(midpoint-1)
			    
		else:
			first = midpoint+1

print(binarySearch(10))
