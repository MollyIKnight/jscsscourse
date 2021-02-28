from subprocess import check_output
from os import system

code = input('base64code:')

f = open('base64code.txt','w')
f.writelines(code)
f.close()
cmd = 'base64 -d base64code.txt' 
output = check_output(cmd, shell = True)
print(str(output))
cmd = 'rm base64code.txt'
system(cmd)