#!/usr/bin/env python
# Julian Quick
# This program is used to help me grade E325 assignments

def handProb(name,outfile):
   ans = int(raw_input("how was problem "+name+"? __ / 100      "))
   print >>outfile, name+':'
   print >>outfile, "   Score: "+str(ans)+'/100'
   coms=str(raw_input("comments?"))
   if coms=="": coms="Nice Job"
   if coms=='m':coms='Missing'
   print >>outfile, "   ("+coms+")"
   return(ans)

# req_info asks user for grade, prints result to output grading file, and 
# returns the grade value
def req_info(half1,half2,outfile):
   ans=raw_input(str(half1)+str(half2))
   print >>outfile,half1+str(ans)+half2
   coms=str(raw_input("comments?"))
   if coms=="": coms="Nice Job"
   if coms=='m':coms='Missing'
   print >>outfile, "   ("+coms+")"
   return int(ans)

# reqinf uses req)info to request info based on Engr325 Fortran Programming Rubric
def reqinf(num,output):
  print >>output, 'PROGRAM '+str(num)+':'
  score=0
  print 'how was Program '+str(num)+'\'s...'
  score+=req_info('Program Description ','/10: What does the program do and how?',output)
  score+=req_info('Variable Library ','/10: What variables are used and for what purpose?',output)
  score+=req_info('Code Formatting ','/10 indenting, commenting, etc.',output)
  score+=req_info('Algorithm Implementation ','/30: functions, subroutines, modules, etc',output)
  score+=req_info('Solution Accuracy ','/30: How close was the solution to the answer?',output)
  score+=req_info('Solution Presentation ','/10: significant figures, description to the user, etc',output)

  # Ask for comments
  coms=str(raw_input('comments?'))
  print >>output,''
  print >>output, 'Score is '+str(score)+'/100'
  print >>output,''
  print >>output,'Comments: '+coms
  print >>output,''
  print >>output,''
  return score

rubric=open('rubric.txt','w')
score=0
score+=handProb('5.1',rubric)
score+=handProb('5.18',rubric)
score+=reqinf('5.24',rubric)
score=score/3
print >>rubric,'Total Score is ',score
