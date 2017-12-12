# Python Automatic grader
This vanilla library automate python unittests. It is a simple library with simple capabilities. I used it to grade UMD CMSC426 computer vision course submissions. Thus, It integrates smooth with [UMD ELMS](https://elms.umd.edu/) submissions. The following assumptions must hold so the grader works properly. Yet, all these assumptions are easy to tweak for different preferences.

## Assumptions
* Student submissions are zip files named with students names
	* For example, smithjohn.zip
* CSV file containing student names exists. This allow grader to loop over students.
* All test cases are weighted equally.
* Require multiple runs for multiple tests like public, release and secret tests.


## How to use
1. Download the grader
2. Install the required python library (numpy,unittest,pickle,inspect)
3. Adjust the configuration in *config.py* file
4. Execute *auto_grade.py*


## Contributions
 The grader features are easy to extend. I think the following features are the most important to consider
 
* Define a unittest format to allow arbitary weighted test cases
* Extend library to run public, release and secret test in a single run 
