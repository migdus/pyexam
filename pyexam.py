#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import random
from random import shuffle
import argparse
import datetime
import os

'''
Constants for the script.
'''
class Constants:
	'''
	Internal tags
	Change them if you feel uncomfortable with the defaults
	'''
	QUESTION_TAG = ":QUESTION:"
	ANSWER_TAG = ":ANSWER:"
	RIGHT_ANSWER_TAG = ":RIGHT_ANSWER:"
	BEGIN_QUESTION_TAG = ":BEGIN_QUESTION:"
	END_QUESTION_TAG = ":END_QUESTION:"
	STUDENT_NAME_TAG = ":STUDENT_NAME:"
	STUDENT_CODE_TAG = ":STUDENT_CODE:"

	'''
	Default output directory
	'''
	OUTPUT_DIRECTORY = "output"

	'''
	Adds some terminal color support
	'''

	HEADER = '\033[95m'
	OKBLUE = '\033[94m'
	OKGREEN = '\033[92m'
	WARNING = '\033[93m'
	FAIL = '\033[91m'
	BOLD = '\033[1m'
	ENDC = '\033[0m'
	
	def enable_colors(self):
		HEADER = '\033[95m'
		OKBLUE = '\033[94m'
		OKGREEN = '\033[92m'
		WARNING = '\033[93m'
		FAIL = '\033[91m'
		BOLD = '\033[1m'
		ENDC = '\033[0m'

	def disable_colors(self):
		self.HEADER = ''
		self.OKBLUE = ''
		self.OKGREEN = ''
		self.WARNING = ''
		self.FAIL = ''
		self.ENDC = ''

'''
This keeps one question with the answer set in memory
'''
class Question:

	def __init__(self, question_statement=None, answers=None, 
				right_answer=None,question_line_number=None):
		# The question
		self._question_statement = (question_statement if question_statement 
			is not None else "")
		# Answers list
		self._answers = shuffle(self._answers) if answers is not None else []
		# Right answer. This will be separated from the rest of the answers
		self._right_answer = right_answer if right_answer is not None else ""
		# Location line of the question db file of this particular question
		self._question_line_number = (question_line_number if 
			question_line_number is not None else "0")
	# question statement setter
	def set_question_statement(self,question_statement):
		self._question_statement = question_statement
	# answers list setter 
	def set_answers(self,answers):
		self._answers = answers
	# right answer setter
	def set_right_answer(self,right_answer):
		self._right_answer = right_answer
	# question line number setter
	def set_question_line_number(self,question_line_number):
		self._question_line_number = question_line_number
	# add a new answer to the question
	def add_new_answer(self,answer):
		self._answers.append(answer)

	'''
	Generates a new question based on a random number of choices
	limited by the answer_set_size.

	Returns: question statement, answers set and the index of the right answer
	'''
	def generate_shuffled_question(self,answer_set_size):
		# Check if answer_set_size parameter is ok according to the number
		# of answers
		if len(self._answers)+1 < answer_set_size:
			error_msg = (
				Constants.FAIL + 'Error: The number of answer choices is less '
				'than the answer set size.'+Constants.ENDC + '\n'
				+ Constants.HEADER+'Question:'+Constants.ENDC + " "
				+ self._question_statement + '\n'
				+ Constants.HEADER + 'Line: ' + Constants.ENDC +
				str(self._question_line_number) + '\n'
				+ Constants.HEADER+'Answer choices provided: ' 
				+ Constants.ENDC + str(len(self._answers) + 1) + '\n'
				+ Constants.HEADER+'Set parameter: '
				+ Constants.ENDC +str(answer_set_size) + '\n'
				+ Constants.OKGREEN+'Check the number of answer choices and '
				'try again, or change the answer_set_size using the --answ '
				'parameter' + Constants.ENDC + '\n')
			print error_msg
			sys.exit()
		#shuffles and returns a random answers set
		answers = self._answers[:]
		shuffle(answers)
		answers = answers[:answer_set_size-1]
		answers.append(self._right_answer)
		shuffle(answers)
		return (self._question_statement, answers, 
			answers.index(self._right_answer))

'''
Generates a new exam
'''
class Exam:
	# The latex template
	_template_buffer = ""

	# The question statement text
	_question_statement_buffer = ""

	# Holds a complete question with the answer option, taken from the latex
	# template
	_question_buffer = ""

	# The buffer of the line in the latex template that holds an answer for a 
	# question
	_answer_buffer = ""

	def __init__(self, question_db_path, latex_template_path,
			student_database_path, number_of_questions, answer_set_size, 
			output_path):
		self._question_db_path = question_db_path
		self._question_list = []
		self._latex_template_path = latex_template_path
		self._student_database_path = student_database_path
		self._number_of_questions = number_of_questions
		self._student_database = []
		self._answer_set_size = answer_set_size
		self._output_directory = output_path

	def read_latex_template(self):

		print Constants.OKGREEN + 'Reading latex template' + Constants.ENDC
		
		inside_question = False
		
		with open(self._latex_template_path,"r") as f:
			
			for line in f:
				
				if (Constants.BEGIN_QUESTION_TAG in line or
					inside_question == True):

					inside_question = True
				
					if Constants.ANSWER_TAG in line:
						self._answer_buffer = line
						self._question_buffer += ('\n' + Constants.ANSWER_TAG +'\n')

					elif Constants.QUESTION_TAG in line:
						self._question_statement_buffer = line
						self._question_buffer += ('\n' + Constants.QUESTION_TAG + '\n')
					
					elif Constants.END_QUESTION_TAG in line:
						inside_question = False
						self._template_buffer += ('\n' + Constants.QUESTION_TAG + '\n')
					elif Constants.BEGIN_QUESTION_TAG not in line:
						self._question_buffer += line

				else:
					self._template_buffer += line

	'''
	Reads a flat file of questions
	'''
	def read_question_file(self):
		question = Question()
		first_item = True
		with open(self._question_db_path,"r") as f:
			line_number = 1
			
			for line in f:
				if Constants.QUESTION_TAG in line:
					
					if first_item is True:
						first_item = False
					else:
						self._question_list.append(question)
					question = Question();
					question.set_question_statement((line.strip()
						.replace(Constants.QUESTION_TAG,"")))
					question.set_question_line_number = line_number
				if Constants.ANSWER_TAG in line:
					question.add_new_answer(line.strip()
						.replace(Constants.ANSWER_TAG,""))
				if Constants.RIGHT_ANSWER_TAG in line:
					question.set_right_answer(line.strip()
					.replace(Constants.RIGHT_ANSWER_TAG,""))
				line_number += 1
		self._question_list.append(question)

		if self._number_of_questions > len(self._question_list) - 1:
			error_msg =  (Constants.FAIL
			+ 'Error: The number of questions in the question file is less '
			'than the number of questions provided as option\n' 
			+ Constants.HEADER + 'Option provided: ' + Constants.ENDC
			+ str(self._number_of_questions) + Constants.HEADER 
			+ '\nQuestions in question db: ' + Constants.ENDC
			+ str(len(self._question_list) - 1)
			+ Constants.ENDC + '\n')
			print error_msg
			sys.exit()

	def read_student_file(self):
		flag_expected_student_name_tag = True
		flag_error_found = False
		line_counter = 1

		error_msg = (Constants.FAIL + 'Error: Expected EXPECTED_TAG_NAME.'
						'\nAt line: ' + str(line_counter) + '\nAt file: '
						 + self._student_database_path + Constants.ENDC)

		with open(self._student_database_path, "r") as f:
			new_student = {}
			for line in f:
				if Constants.STUDENT_NAME_TAG in line:
					if flag_expected_student_name_tag == True:
						new_student['name'] = line.replace(
							Constants.STUDENT_NAME_TAG, '').strip()
						flag_expected_student_name_tag = False
					else:
						error_msg.replace("EXPECTED_TAG_NAME",
							'Student name tag')
						flag_error_found = True

				elif Constants.STUDENT_CODE_TAG in line:
					if flag_expected_student_name_tag == False:
						new_student['code'] = line.replace(
							Constants.STUDENT_CODE_TAG, '').strip()
						self._student_database.append(new_student)
						new_student = {}
						flag_expected_student_name_tag = True
					else:
						error_msg.replace("EXPECTED_TAG_NAME",
							'Student code tag')
						flag_error_found = True

				if flag_error_found == True:
					print error_msg
					sys.exit()

				line_counter += 1
	def _index_to_choice(self,index):
		if index == 0:
			return 'a'
		elif index == 1:
			return 'b'
		elif index == 2:
			return 'c'
		elif index == 3:
			return 'd'
		elif index == 4:
			return 'e'
		else:
			error_msg +=  (Constants.FAIL
			+ 'Error: The index is greater than 4' + Constants.ENDC + '\n')
			sys.exit()

	'''
	Generate the exam
	'''
	def generate(self):
		# Checks if the user added the output directory path.
		# If not, then create a new directory in the current path
		# with date and time in its name.
		if len(self._output_directory) == 0:
			self._output_directory = (Constants.OUTPUT_DIRECTORY + '/' +
			datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S"))
			os.makedirs(self._output_directory)
			print (Constants.OKGREEN + 'Output directory created at ' +
			self._output_directory + Constants.ENDC)
		# Get a copy of the student db
		student_database = self._student_database[:]

		output_tex_file_names = []

		# Create a exam for each student in the database
		for student in student_database:

			# Copy the buffer, then add the student name and code to
			# the template according to the tags (see Constants class)
			template_buffer = self._template_buffer
			template_buffer = template_buffer.replace(
				Constants.STUDENT_NAME_TAG, student['name'])
			template_buffer = template_buffer.replace(
				Constants.STUDENT_CODE_TAG, student['code'])
			
			# Shuffle the questions and get a subset according to the number of 
			# questions set by the user.
			shuffle(self._question_list)
			question_list = (self._question_list[:int(self._number_of_questions)])
			

			question_answer = []
			for question in question_list:
				
				question_statement, answers, rigth_answer_index = (
					question.generate_shuffled_question(self._answer_set_size))

				# Adds a list to the question_answer with two elements:
				# the statement and the index of the right answer
				question_answer.append([question_statement,
					self._index_to_choice(rigth_answer_index)])

				# Creates a copy of the question statement buffer and replaces
				# the question tag with the current question
				question_statement_buffer = self._question_statement_buffer
				question_statement_buffer = question_statement_buffer.replace(
					Constants.QUESTION_TAG, question_statement)
				
				# Creates a copy of the question and replaces
				# the question tag with the current question statement buffer
				question_buffer = self._question_buffer
				question_buffer = question_buffer.replace(
					Constants.QUESTION_TAG, question_statement_buffer)

				answer_str = ''
				answer_right_str=''
				
				for answer in answers:
					# Takes an answer and adds to the answer buffer
					answer_buffer = self._answer_buffer
					answer_buffer = answer_buffer.replace(
						Constants.ANSWER_TAG, answer)
					answer_str += answer_buffer 

				# Replaces the section of the answers with the text of 
				# the answers
				question_buffer = question_buffer.replace(
					Constants.ANSWER_TAG, answer_str)

				# Split the whole template in two: before and after the question
				# tag
				template_buffer_before_tag = (template_buffer
					[:template_buffer.find(Constants.QUESTION_TAG)])
				
				template_buffer_after_tag = (template_buffer
					[len(template_buffer_before_tag) +
					len(Constants.QUESTION_TAG):])
				
				# Rebuild the template but adding the question
				template_buffer = (template_buffer_before_tag + question_buffer  
					+ Constants.QUESTION_TAG + template_buffer_after_tag)
			
			output_path = (self._output_directory + '/exam_' + student['code']
				+ '.tex')

			with open(output_path,'w') as f:
				template_buffer = (template_buffer.
					replace(Constants.QUESTION_TAG,''))
				f.write(template_buffer)

			output_tex_file_names.append('exam_' + student['code']
				+ '.tex')

			output_answer_path = output_path.replace('.tex','.answer.txt')

			with open(output_answer_path,'w') as f:
				for element in question_answer:
					f.write('Question: '+ element[0] + '\n' + 'Answer: ' 
						+ element[1] + '\n')

		with open(self._output_directory + '/exam_all_compile.sh', 'w') as f:
			complete_path = os.path.abspath(self._output_directory)
			for element in output_tex_file_names:
				f.write('pdflatex \"' +  complete_path + "\"/" + element + '\n')



def check_input_parameters(answer_set_size, question_database_path,
	student_database_path, number_of_questions, latex_template_location,
	output_path):

	error_msg = ''
	'''
	TO DO
	check question_database_path, student_database_path
	for right number of tags 

	number_of_questions, output_format, latex_template_location
	'''

	# Path validation
	path = [question_database_path,question_database_path]
	for element in path:
		try:
			f = open(element)
		except IOError:
			error_msg += (Constants.FAIL + 'Error: I/O for path: ' + element 
				+ Constants.ENDC + '\n')
	
	# Answer set size validation
	if answer_set_size < 2:
		error_msg +=  (Constants.FAIL
			+ 'Error: The answer set size must be greater '
			'or equal to 2' + Constants.ENDC + '\n')

	if len(output_path) > 0 and os.path.exists(output_path) == False:
		error_msg += (Constants.FAIL
			+ 'Error: The given output path does not exist.' + Constants.ENDC 
			+ '\n')

	if len(error_msg)>0:
		print error_msg
		sys.exit()

parser = argparse.ArgumentParser(description ='Creates exams')
parser.add_argument('--answ', dest = 'answer_set_size', default = 5,
					help = 'Set the answer set size (default: 5)')
parser.add_argument('--qdb', dest = 'question_database_path',
					required = True, help = 
					'Set the question database file path')
parser.add_argument('--sdb', dest = 'student_database_path', required = True,
					help = 'Set the student database file')
parser.add_argument('--nq', dest = 'number_of_questions', required = True,
					help = 'Set the number of questions of the test')
parser.add_argument('--latemp', dest = 'latex_template_location',
					help = 'Set the latex template path')	
parser.add_argument('--output', dest = 'output_path', required = False,
					help = 'Set the output path', default ='')
args = parser.parse_args()

check_input_parameters(answer_set_size=args.answer_set_size,
	question_database_path = args.question_database_path,
	student_database_path = args.student_database_path,
	number_of_questions = args.number_of_questions,
	latex_template_location = args.latex_template_location,
	output_path = args.output_path)

exam = Exam(question_db_path = args.question_database_path,
	latex_template_path = args.latex_template_location,
	student_database_path = args.student_database_path,
	number_of_questions = int(args.number_of_questions),
	answer_set_size = int(args.answer_set_size),
	output_path = args.output_path)
exam.read_question_file()
exam.read_latex_template()
exam.read_student_file()
exam.generate()
	



