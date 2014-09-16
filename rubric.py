#!/usr/bin/env python
# Julian Quick
#
# Requests info for Engr325 Fortran Programming Rubric
# ======================================================
# req_info asks user for grade, prints result to output grading file, and 
# returns the grade value
# VARIABLE DICTIONARY:
#   ans: user input
#   half 1: prompt untill score fraction
#   half2: prompt after and including score fraction
def req_info(half1,half2,outfile):
  
   # request info
   ans=raw_input(str(half1)+str(half2))

   # write results to output file
   print >>outfile,half1+str(ans)+half2

   return int(ans)

# req_info asks the user to grade an assigned program 
# using the progrramming grading rubric
# VARIABLE DICTIONARY
#    num: name of program being evaluated
#    output: output feedback file
def reqinf(num,output):

  # Create program specific feedback heading
  print >>output, 'PROGRAM '+str(num)+':'

  # request critereon grades, add to score
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

  # Add whitespaces to output file
  print >>output,''
  print >>output, 'Score is '+str(score)+'/100'
  print >>output,''
  print >>output,'Comments: '+coms
  print >>output,''
  print >>output,''

  return score

# ======================================================

# Open output file
rubric=open('rubric.txt','w')

# Determine score
score=0
score+=reqinf('ch.6 problem 7',rubric)
score+=reqinf('ch.7 problem 9',rubric)

# Final score is average score
print >>rubric,'Total Score is ',score/2
