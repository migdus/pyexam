# pyEXAM

## Overview
**pyEXAM** is a simple script for generating exams. 

## Usage

Here is a complete example:

	python pyexam.py --answ 4 --qdb path/to/question_database --edb /path/to/student_database --nq 25

#### Parameters

* **qdb**: Path to the questions database file.
* **edb**: Path to the student names database.
* **nq**: Number of questions of the exam.
* **answ**: Answer set size per question. This must be greater or equal to 2 and less than the number of choices of each question.

All parameters must have the -- **before** using them  (refer to the ***Usage*** example).

### Question database

See *examples* directory for a working example.

### Students database

## Author

Miguel Dussán

Homepage [http://www.migueldussan.com](http://www.migueldussan.com)

Twitter [@migdus](http://twitter.com/migdus)

From Colombia with love <3