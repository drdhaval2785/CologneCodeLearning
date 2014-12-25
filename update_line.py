"""  update_line.py  Based on a transaction file, change the 
     order of lines in the output.
Each line of the transaction file has one of the forms:
(a) move L1 after L2
   L1 and L2 are line numbers (starting at 1) in sch_orig_utf8_slp1.txt
   This command means to move L1 so, in the output, it occurs just after L2
(b) delete L
   This command means to omit line#L in the output
Dec 19, 2014.  Allow multiple 'moves' with the same L2.
  Insert them in the order encountered in file.
"""

import re,sys # importing regular expressions and system
import codecs, unicodedata # importing codecs and unicodedata
def change_check(text): # defining the function change_check with a variable text
 """ check for errors in change file """
 parts = re.split(r' +',text) # This part I am unable to comprehend. I understood that this splits the sentence into word by splitting with ' ', but how is not clear to me.
 method = parts[0] # Getting the first word (move / delete from change_line.txt to work as command)
 if method not in ['move','delete']:
  return "method err ('%s')" % method # Throwing error if method is not move / delete
 if (method == 'move'): # in case the method is 'move'
  if (len(parts) != 4): # the regular 'move' statement has to have four parts. If not, error is thrown
   return 'move err2'
  if (parts[2] != 'after'):
   return 'move err3'
  if not re.match(r'^[0-9]+$',parts[1]):
   return 'move err4'
  if not re.match(r'^[0-9]+$',parts[3]):
   return 'move err5'
  L1 = int(parts[1])
  L2 = int(parts[3]) 
  if (L1 < 1):
   return 'move err6'
  if (L2 < 1):
   return 'move err7'
  return 'OK' 
 if (method == 'delete'):
  if (len(parts) != 2):
   return 'delete err1'
  if not re.match(r'^[0-9]+$',parts[1]):
   return 'delete err2'
  L1 = int(parts[1])
  if (L1 < 1):
   return 'delete err3'
  return 'OK'
 return 'UNKNOWN CHANGE ERR' # shouldn't happen

class Change(object):
 def __init__(self,text):
  status = change_check(text)
  if  status != 'OK':
   out = "Change init error 1 (%s): %s" %(status,text)
   print out.encode('utf-8')
   exit(1)
  parts = re.split(r' +',text)
  method = parts[0]
  self.method = method
  self.L1 = int(parts[1])
  if method == 'move':
   self.L2 = int(parts[3])
   self.arglen = 2
  elif method == 'delete':
   self.arglen = 1

 def __repr__(self):
  if self.arglen == 1:
   out = "Change(%s,%s)" %(self.method,self.L1)
  elif self.arglen == 2:
   out = "Change(%s,%s,%s)" %(self.method,self.L1,self.L2)
  else:
   out = "Change(%s unknown arglen)" % self.method
  return out

def parse_changes(changein):
 changes = [] # a list (so mutable)
 
 f = codecs.open(changein,encoding='utf-8',mode='r')
 n = 0
 for line in f:
  line = line.rstrip()
  if line.startswith(';'): # Dec 19, 2014. comment line.
   continue
  change = Change(line)
  changes.append(change)
 f.close()
 return changes

def perform_move(lines,change,ichange):
 n = len(lines) 
 ifrom = change.L1 - 1 #ifrom is index in lines
 ito = change.L2 - 1 #ditto
 if (n <= ifrom) or (n <= ito):
  out = "Change error line number too big: %s  %s" %(n,change)
  print out.encode('utf-8')
  exit(1)
 fromlines = lines[ifrom]
 if len(fromlines) != 1:
  out = "Error 2: %s %s " %(change,lines[ifrom])
  print out.encode('utf-8')
  exit(1)
 tolines = lines[ito]
 # Dec 19, 2014. Allow multiple moves to a given line.
 #if len(tolines) != 1:
 # out = "Error 3: %s %s " %(change,lines[ito])
 # print out.encode('utf-8')
 # exit(1)
 linetomove = fromlines[0]
 out = "%s %s" % (ichange,change)
 print out.encode('utf-8')
 out = "line %s : %s" %(change.L1,linetomove)
 print out.encode('utf-8')
 out = "line %s : %s\n" %(change.L2,tolines[0])
 print out.encode('utf-8')
 tolines.append(linetomove)
 lines[ifrom]=[] # empty, not printed
 lines[ito] = tolines

def perform_delete(lines,change,ichange):
 n = len(lines) 
 idel = change.L1 - 1
 if (n <= idel):
  out = "Change error line number too big: %s  %s" %(n,change)
  print out.encode('utf-8')
  exit(1)
 dellines = lines[idel]
 if len(dellines) != 1:
  out = "Error 2: %s %s " %(change,dellines)
  print out.encode('utf-8')
  exit(1)
 linetodelete = dellines[0]
 out = "%s %s" % (ichange,change)
 print out.encode('utf-8')
 out = "line %s : %s" %(change.L1,linetodelete)
 print out.encode('utf-8')
 lines[idel]=[] # empty, not printed
 
def update(filein,changein,fileout):
 changes = parse_changes(changein)
 f = codecs.open(filein,encoding='utf-8',mode='r')
 lines = []
 for line in f:
  lines.append([line])
 f.close()
 # apply changes to lines
 n = len(lines) 
 ichange=0
 for change in changes:
  if change.method == 'move':
   ichange = ichange+1
   perform_move(lines,change,ichange)
  elif change.method == 'delete':
   ichange = ichange+1
   perform_delete(lines,change,ichange)
 # write output
 n1 = 0
 fout = codecs.open(fileout,'w','utf-8')
 for linelists in lines:
  for line in linelists:
   n1 = n1 + 1
   fout.write(line)  
 fout.close()
 out = "%s lines read from %s" % (n,filein)
 print out.encode('utf-8')
 out = "%s lines written to %s" % (n1,fileout)
 print out.encode('utf-8')
 out = "%s change records read from %s" %(len(changes),changein)
 print out.encode('utf-8')
 out = "%s changes applied" % ichange
 print out.encode('utf-8')

#-----------------------------------------------------
if __name__=="__main__":
 changein = sys.argv[1]
 filein = sys.argv[2]
 fileout = sys.argv[3]
 update(filein,changein,fileout)

