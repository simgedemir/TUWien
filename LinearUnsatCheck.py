import subprocess
import sys
import re
import json

def linearSearch(maxT):
	arr=[]
	for i in range (0,maxT):
		clingo = subprocess.Popen(
	   		"clingo --outf=2 -c maxT={} {} ".format(i,' '.join(sys.argv[1:])),
	    	shell=True, stdout=subprocess.PIPE, stderr=sys.stderr)
		clingoout, clingoerr = clingo.communicate()
		del clingo
		clingoout = json.loads(clingoout.decode('utf-8'))
		#(clingoout)
		result = clingoout['Result']
		if result=='SATISFIABLE':
			arr.append(result)
	return (len(arr))	


print(linearSearch(10)-1)