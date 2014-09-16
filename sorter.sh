#!/usr/bin/env sh
# Julian Quick
# Context: Used as a tool for graders to quickly create a directory for each student 
# lab report with the grading rubric and unzipped submission moved inside

# Description: sorts student submissions by creating individual student lab directories 
# conainin the submission and grading rubric

# This is set up for a direcotry containing: 
#    The grading rubric spreadsheet as rubric
#    A directory called "Submissions" containing lab submissions

# replace spaces in submission filenames  with _
detox -r Submissions

# iterate through files in submissions
for f in `ls Submissions`
do
    # cut first 20 letters from submission name
    dir=`echo "$f"|cut -c 1-20`

    # new directory with that name
    mkdir -p "$dir"

    # copy that submission to the new directory,
    # as well as grading rubric
    cp Submissions/"$f" "./$dir"
    cp grader.py "$dir"
    tar -C $dir -zxvf $dir/$f
done
