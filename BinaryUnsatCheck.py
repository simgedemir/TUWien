## binarySearch algorithm to find the critical point of the unsatCheck  
## Simge Demir
## July, 2018

import subprocess
import sys
import re
import json

def binarySearch(maxT):
	first = 1
	last = maxT-1
	found = False
	prev=None
	midpoint=maxT

	clingo = subprocess.Popen(
   		"clingo --outf=2 -c maxT={} {} ".format(midpoint,' '.join(sys.argv[1:])),
    	shell=True, stdout=subprocess.PIPE, stderr=sys.stderr)
	clingoout, clingoerr = clingo.communicate()
	del clingo
	clingoout = json.loads(clingoout.decode('utf-8'))
	result = clingoout['Result']

	if result=='SATISFIABLE':
		return ("NO PROBLEM")
	
	while not found:
		midpoint = int((first + last)/2)

		clingo = subprocess.Popen(
   				"clingo --outf=2 -c maxT={} {} ".format(midpoint,' '.join(sys.argv[1:])),
    			shell=True, stdout=subprocess.PIPE, stderr=sys.stderr)
		clingoout, clingoerr = clingo.communicate()
		del clingo
		clingoout = json.loads(clingoout.decode('utf-8'))
		result = clingoout['Result']

		if result=='UNSATISFIABLE':
			last = midpoint-1

			clingo = subprocess.Popen(
   				"clingo --outf=2 -c maxT={} {} ".format(midpoint-1,' '.join(sys.argv[1:])),
    			shell=True, stdout=subprocess.PIPE, stderr=sys.stderr)
			clingoout, clingoerr = clingo.communicate()
			del clingo
			clingoout = json.loads(clingoout.decode('utf-8'))
			result = clingoout['Result']
			
			if result=='SATISFIABLE':
				found=True
				return(midpoint-1)
			    
		else:
			first = midpoint+1

print(binarySearch(10))
