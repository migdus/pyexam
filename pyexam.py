import sys, random, argparse, pdb

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
Shuffles a list using the Knuth-Fisher-Yates shuffle algorithm
'''
def shuffle(aList):
	maxrange = len(aList)-1
	for i in xrange(maxrange,0,-1):
		n = random.randint(0,maxrange)
		aList[i], aList[n] = aList[n], aList[i]

class Question:

	def __init__(self, question_statement=None, answers=None, 
				right_answer=None,question_line_number=None):
		self._question_statement = (question_statement if question_statement 
			is not None else "")
		self._answers = shuffle(self._answers) if answers is not None else []
		self._right_answer = right_answer if right_answer is not None else ""
		self._question_line_number = (question_line_number if 
			question_line_number is not None else "0")
	
	def set_question_statement(self,question_statement):
		self._question_statement = question_statement

	def set_answers(self,answers):
		self._answers = answers

	def set_right_answer(self,right_answer):
		self._right_answer = right_answer

	def set_question_line_number(self,question_line_number):
		self._question_line_number = question_line_number
	
	def add_new_answer(self,answer):
		self._answers.append(answer)

	'''
	Generates a new question based on a random number of choices
	limited by the answer_set_size.

	Returns: question statement, answers and the index of the right answer
	'''
	def generate_shuffled_question(self,answer_set_size):
		if len(self._answers)+1 < answer_set_size:
			error_msg += (
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
		answers = self._answers[:answer_set_size-1]
		answers.append(self._right_answer)
		shuffle(answers)
		return (self._question_statement, answers, 
			answers.index(self._right_answer))



class Exam:
	_template_buffer = ""
	_question_buffer = ""
	_answer_buffer = ""

	def __init__(self, question_db_path, latex_template_path):
		self._question_db_path = question_db_path
		self._question_list = []
		self._latex_template_path = latex_template_path

	def read_latex_template(self):
		inside_question = False
		with open(self._latex_template_path,"r") as f:
			for line in f:
				if Constants.BEGIN_QUESTION_TAG in line:
					inside_question = True
				if inside_question == True:
					if Constants.ANSWER_TAG in line:
						self._answer_buffer = line
						self._template_buffer += ('\n' +
							Constants.ANSWER_TAG +'\n')
					elif Constants.QUESTION_TAG in line:
						self._question_buffer = line
						self._template_buffer += ('\n' +
							Constants.QUESTION_TAG + '\n')
					elif Constants.END_QUESTION_TAG in line:
						inside_question = False
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
					question.set_question_statement = (line.strip()
						.replace(Constants.QUESTION_TAG,""))
					question.set_question_line_number = line_number
				if Constants.ANSWER_TAG in line:
					question.add_new_answer(line.strip()
						.replace(Constants.ANSWER_TAG,""))
				if Constants.RIGHT_ANSWER_TAG in line:
					question.set_right_answer(line.strip()
					.replace(Constants.RIGHT_ANSWER_TAG,""))
				line_number += 1
		self._question_list.append(question)
					
def check_input_parameters(answer_set_size, question_database_path,
	student_database_path, number_of_questions, output_format,
	latex_template_location):

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

	if len(error_msg)>0:
		print error_msg
		sys.exit()

parser = argparse.ArgumentParser(description ='Creates exams')
parser.add_argument('--answ', dest = 'answer_set_size', default = 5,
					help = 'Set the answer set size (default: 5)')
parser.add_argument('--qdb', dest = 'question_database_path',
					required = True, help = 
					'Set the question database file path')
parser.add_argument('--edb', dest = 'student_database_path', required = True,
					help = 'Set the student database file')
parser.add_argument('--nq', dest = 'number_of_questions', required = True,
					help = 'Set the number of questions of the test')
parser.add_argument('--ouf', dest = 'output_format', default = 'latex',
					help = 'Set the output format')
parser.add_argument('--latemp', dest = 'latex_template_location',
					help = 'Set the latex template path')
args = parser.parse_args()

check_input_parameters(answer_set_size=args.answer_set_size,
	question_database_path = args.question_database_path,
	student_database_path = args.student_database_path,
	number_of_questions = args.number_of_questions, 
	output_format = args.output_format, 
	latex_template_location = args.latex_template_location)


if args.output_format == 'latex':
	exam = Exam(question_db_path = args.question_database_path,
		latex_template_path = args.latex_template_location)
	exam.read_question_file()
	exam.read_latex_template()
	question_statement, answers, rigth_answer_index = (exam._question_list[2]
		.generate_shuffled_question(int(args.answer_set_size)))
print "Question buffer ---"
print exam._question_buffer
print "Answers buffer---"
print exam._answer_buffer

print "Template buffer ---"
print exam._template_buffer


