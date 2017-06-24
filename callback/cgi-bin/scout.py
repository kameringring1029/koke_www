# file name: call_from_php.py
 
import sys
import commands
 
if __name__=='__main__':
 
    check = commands.getoutput("cd /home/pi/sif/cap/manage_sif")
    check = commands.getoutput("ls")
    print 'parameter1 is ' + check
    print 'parameter2 is ' + sys.argv[2]
    print 'result is OK!'
    print 'result is NG!'

