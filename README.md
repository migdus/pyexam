# pyEXAM

## Overview
**pyEXAM** is a simple script for generating exams.

It takes a question database, an student database, mix them and generate unique exams.

## Usage

Here is a complete example:

	python pyexam.py --answ 4 --qdb /path/to/question_database --nq 5 --ouf latex --latemp /path/to/latex_template --edb /path/to/student_database

#### Options 

* **--qdb**: Path to the questions database file.
* **--edb**: Path to the student names database.
* **--nq**: Number of questions of the exam.
* **--answ**: Answer set size per question. This must be greater or equal to 2 and less than the number of choices of each question.
* **--ouf**: Output format. *txt* and *latex* supported. Default: *txt*. If *latex* supported, you must use the **--latemp** option.
* **--latemp**: Location of the latex template. Use together with **--ouf** option.

All flags must have the -- **before** using them  (refer to the ***Usage*** example).

#### Output

The script generates a folder with the date and hour as its name. Inside of it you'll find:

* **EXAM.ALL**: All exams in one single file.
* **ANSWERS.ALL**: Solved exams in one single file.
* **EXAM.STUDENT_CODE_STUDENT_NAME**: A file containing a exam for the student. There's one for each student in the student database.
* **ANSWERS.STUDENT_CODE_STUDENT_NAME**: Solved exam for one student.  There's one for each student in the student database.

The format of the output depends on the **--ouf** option. Refer to the **Options** section for more information.

##### Latex Output

If you use:

		... --ouf latex --latemp /path/to/latex/template
Then you have to define the latex template. This template is a simple latex file with your information, page configuration, etc, but contains the following tags:

* **:STUDENT_NAME:** The location where you want the student name to be placed.
* **:STUDENT_CODE:** The location where you want the student code to be placed.
* **:QUESTION:** The location where you want your question to be placed.
* **:ANSWER:** The location where you want your answer to be placed. The script will use this location to place all answers related to that question.

You need to write **only one tag** per type. For more, see *examples* directory for a working example.

### Question database

The questions database file holds the question information. **Use only one tag per line**. Lines without tags are not taken into account: they are considered as comments.

Each question contains the following tags:

* **:QUESTION:**: Contains the question statement. One per question.
* **:ANSWER:** An answer choice. A question can hold multiple answers.
* **:RIGHT_ANSWER:** The right answer for the question. A question can hold only one right answer.

####Example 

**:QUESTION:** What's the capital of Huila?

**:ANSWER:** Bogotá

**:ANSWER:** Cali

**:ANSWER:** Bucaramanga

**:RIGHT_ANSWER:** Neiva

**:ANSWER:** Cartagena

**:ANSWER:** Santa Marta

For more, see *examples* directory for a working example.

### Students database 

**TO DO**

## Author

I'm Miguel Dussán, and my homepage is [http://www.migueldussan.com](http://www.migueldussan.com). You can reach me on Twitter [@migdus](http://twitter.com/migdus)

From Colombia with love <3