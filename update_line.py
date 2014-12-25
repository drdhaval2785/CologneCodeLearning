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
 """ Regular move statement is 'move X after Y'. So checking for possible errors"""
  if (len(parts) != 4): # the regular 'move' statement has to have four parts. If not, error is thrown 
   return 'move err2' 
  if (parts[2] != 'after'): # second word is not after
   return 'move err3'
  if not re.match(r'^[0-9]+$',parts[1]): # first word is not digit (the syntax of regex is not clear to me)
   return 'move err4'
  if not re.match(r'^[0-9]+$',parts[3]): # same for third word.
   return 'move err5'
  L1 = int(parts[1]) # storing 2nd and 4th member as L1 and L2 variables.
  L2 = int(parts[3]) # storing 2nd and 4th member as L1 and L2 variables.
  if (L1 < 1): # Can't move <1 line
   return 'move err6'
  if (L2 < 1): # Can't move to < 1 line
   return 'move err7'
  return 'OK' # No error found
 if (method == 'delete'): # If the method is delete
""" Regular Delete statement is 'delete X' """ 
  if (len(parts) != 2):  # the statement exceeds / less than the specified format.
   return 'delete err1'
  if not re.match(r'^[0-9]+$',parts[1]): # Second member is not digit
   return 'delete err2'
  L1 = int(parts[1]) # storing the second member as L1 variable
  if (L1 < 1): # Can't remove < 1 line
   return 'delete err3'
  return 'OK' # no error
 return 'UNKNOWN CHANGE ERR' # shouldn't happen

class Change(object): # defining a class Change
 def __init__(self,text): # initializing the class with one variable text
  status = change_check(text) # Calling change_check function
  if  status != 'OK': # Wrong format in change_lines.txt
   out = "Change init error 1 (%s): %s" %(status,text) # throw error
   print out.encode('utf-8') # print utf8 encoded error statement
   exit(1) # exit the function. I am not sure what 1 in the bracket does.
  parts = re.split(r' +',text) # regex format not clear
  method = parts[0] # move / delete
  self.method = method # initializing variable 'method'
  self.L1 = int(parts[1]) # initializing variable L1 
  if method == 'move': # if the method equals 'move'
   self.L2 = int(parts[3]) # initializing variable L2
   self.arglen = 2 # initializing variable arglen to 2
  elif method == 'delete': # if method equals 'delete'
   self.arglen = 1 # initializing variable arglen to 1

 def __repr__(self): # representing the class Change
  if self.arglen == 1: # for delete
   out = "Change(%s,%s)" %(self.method,self.L1) # e.g. Change(delete,123)
  elif self.arglen == 2: # for move
   out = "Change(%s,%s,%s)" %(self.method,self.L1,self.L2) # e.g. Change(move,123,234)
  else:
   out = "Change(%s unknown arglen)" % self.method # Shoudn't happen. Error message.
  return out # returning the out variable

def parse_changes(changein):
 changes = [] # a list (so mutable) # Does mutability mean that the list can be changed later on ? dhaval
 
 f = codecs.open(changein,encoding='utf-8',mode='r') # what is the use of codecs here ?
 n = 0 # variable n set to 0
 for line in f: # for loop - this loops the data in f
  line = line.rstrip() # trimming - removing whitespaces from the variable.
  if line.startswith(';'): # Dec 19, 2014. comment line.
   continue # we skip this line in change_lines.txt. ;Removing dOzcitya to dfadfasdf (this is for our record. Code doesn't do anything with it)
  change = Change(line) # e.g. Change(delete,123) or Change(move,123,234). Changing the move / delete statements in change_line.txt to this format and storing it to variable change.
  changes.append(change) # Adding this change variable to the array changes.
 f.close() # closing the open file handled by f
 return changes # Returning the array changes i.e. all the commands from change_line.txt in format Change(delete,123) or Change(move,123,234) stored in an array

def perform_move(lines,change,ichange): # function to perform move. Difficult to comprehend for now without Jim commenting it.
 n = len(lines) # number of lines in a file
 ifrom = change.L1 - 1 #ifrom is index in lines - Not clear
 ito = change.L2 - 1 #ditto - Not clear
 if (n <= ifrom) or (n <= ito): # the line number of from and to positions are too big. Bigger than the whole list length.
  out = "Change error line number too big: %s  %s" %(n,change) # error message
  print out.encode('utf-8')
  exit(1)
 fromlines = lines[ifrom] # data in the from line.
 if len(fromlines) != 1: # more than two members in the array fromlines. Throw an error
  out = "Error 2: %s %s " %(change,lines[ifrom])
  print out.encode('utf-8')
  exit(1)
 tolines = lines[ito] # data in to line.
 # Dec 19, 2014. Allow multiple moves to a given line.
 #if len(tolines) != 1:
 # out = "Error 3: %s %s " %(change,lines[ito])
 # print out.encode('utf-8')
 # exit(1)
 linetomove = fromlines[0]
 out = "%s %s" % (ichange,change) 
 print out.encode('utf-8') # printing ichange and change
 out = "line %s : %s" %(change.L1,linetomove)
 print out.encode('utf-8') # printing change.L1 and linetomove
 out = "line %s : %s\n" %(change.L2,tolines[0])
 print out.encode('utf-8') # printing change.L2 and tolines[0]
 tolines.append(linetomove) # pasting linetomove after tolines.
 lines[ifrom]=[] # empty, not printed. This removes data from the from index
 lines[ito] = tolines # back to tolines. Original data which it stored.

def perform_delete(lines,change,ichange): # Actual delete function
 n = len(lines)  # number of entries
 idel = change.L1 - 1 # doing -1 because for python counting starts from 0. For human beings it starts from 1.
 if (n <= idel): # Error 
  out = "Change error line number too big: %s  %s" %(n,change)
  print out.encode('utf-8')
  exit(1)
 dellines = lines[idel] # remembering dellines.
 if len(dellines) != 1: # Error
  out = "Error 2: %s %s " %(change,dellines)
  print out.encode('utf-8')
  exit(1)
 linetodelete = dellines[0] # line to delete defined.
 out = "%s %s" % (ichange,change)
 print out.encode('utf-8')
 out = "line %s : %s" %(change.L1,linetodelete)
 print out.encode('utf-8')
 lines[idel]=[] # empty, not printed. Deleted the lines[idel]. So, the line is deleted.
 
def update(filein,changein,fileout): # Function to update the file.
 changes = parse_changes(changein) # Reads from change_line.txt and converted to array like ['Change(delete,123)','Change(move,123,234)']
 f = codecs.open(filein,encoding='utf-8',mode='r') # opens file to be changed.
 lines = [] # blank array
 for line in f:
  lines.append([line]) # add line by line data to lines array.
 f.close()
 # apply changes to lines
 n = len(lines) # counting members of lines array
 ichange=0 # counter value set to 0
 for change in changes: # for each change
  if change.method == 'move':
   ichange = ichange+1 # adding 1 
   perform_move(lines,change,ichange) # Doing move
  elif change.method == 'delete':
   ichange = ichange+1
   perform_delete(lines,change,ichange) # doing delete
 # write output
 n1 = 0
 fout = codecs.open(fileout,'w','utf-8') # creating handle for outfile.
 for linelists in lines: # I can't comprehend why two for statements here.
  for line in linelists:
   n1 = n1 + 1
   fout.write(line)  
 fout.close()
 out = "%s lines read from %s" % (n,filein) # Writing the log for the next lines.
 print out.encode('utf-8')
 out = "%s lines written to %s" % (n1,fileout)
 print out.encode('utf-8')
 out = "%s change records read from %s" %(len(changes),changein)
 print out.encode('utf-8')
 out = "%s changes applied" % ichange
 print out.encode('utf-8')

#-----------------------------------------------------
if __name__=="__main__":
 changein = sys.argv[1] # argument 1
 filein = sys.argv[2] # argument 2
 fileout = sys.argv[3] # argument 3
 update(filein,changein,fileout)

