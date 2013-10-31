import sys, random, argparse, pdb

class Constants:
	questionindicator = ":QUESTION:"
	answerindicator = ":ANSWER:"
	rightanswerindicator = ":RIGHT_ANSWER:"
	begin_question = ":BEGIN_QUESTION:"
	end_question = ":END_QUESTION:"
	student_name = ":STUDENT_NAME:"

'''
Reads a flat file of questions
'''
def readQuestionFile(path):
	questionobjs = []
	question = Question()
	first_item = True
	with open(path,"r") as f:
		line_number = 1
		for line in f:
			if Constants.questionindicator in line:
				
				if first_item is True:
					first_item = False
				else:
					questionobjs.append(question)
				question = Question();
				question.question_statement = line.strip().replace(Constants.questionindicator,"")
				question.question_line_number = line_number
			if Constants.answerindicator in line:
				question.answers.append(line.strip().replace(Constants.answerindicator,""))
			if Constants.rightanswerindicator in line:
				question.right_answer = line.strip().replace(Constants.rightanswerindicator,"")
			line_number += 1
	questionobjs.append(question)
	return questionobjs

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
		self.question_statement = question_statement if question_statement is not None else ""
		self.answers = shuffle(self.answers) if answers is not None else []
		self.right_answer = right_answer if right_answer is not None else ""
		self.question_line_number = question_line_number if question_line_number is not None else "0"
	
	'''
	Generates a new question based on a random number of choices
	limited by the answerSetSize.

	Returns: question statement, answers and the index of the right answer
	'''
	def generateNewVersionOfQuestion(self,answerSetSize):
		if answerSetSize < 2:
			print 'The answer set size must be greater or equal to 2'
			sys.exit()
		if len(self.answers)+1 < answerSetSize:
			s = (bcolors.FAIL+'Error: The number of answer choices is less than the answer '
				'set size.'+bcolors.ENDC+'\n'
				+bcolors.HEADER+'Question:'+bcolors.ENDC+" "+self.question_statement+'\n'
				+bcolors.HEADER+'Line: '+bcolors.ENDC+str(self.question_line_number)+'\n'
				+bcolors.HEADER+'Answer choices provided: ' +bcolors.ENDC + str(len(self.answers)+1)+'\n'
				+bcolors.HEADER+'Set parameter: '+bcolors.ENDC +str(answerSetSize)+'\n'
				+bcolors.OKGREEN+'Check the number of answer choices and try again, or change '
				'the answerSetSize using the --answ parameter'+bcolors.ENDC)
			print s
			sys.exit()
		answers = self.answers[:answerSetSize-1]
		answers.append(self.right_answer)
		shuffle(answers)
		return self.question_statement, answers, answers.index(self.right_answer)

'''
Adds some terminal color support
'''
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    BOLD = '\033[1m'
    ENDC = '\033[0m'

    def disable(self):
        self.HEADER = ''
        self.OKBLUE = ''
        self.OKGREEN = ''
        self.WARNING = ''
        self.FAIL = ''
        self.ENDC = ''

class Exam:
	student_name_line_number = None
	student_code_line_number = None

	'''
		Template minus question and answer line
		The question location will be marked with the questionindicator.
	'''

	template_buffer = ""

	# Whole question text
	question_buffer = ""

	'''
		Answer line
		The location to replace with the answer will be marked with the
		answerindicator
		'''
	answer_buffer = ""

	def __init__(self,latexTemplatePath=None):
		pass

	def readLatexTemplate(self,path):
		flag_beginning = True
		flag_end = False
		inside_question = False

		with open(path,"r") as f:
			for line in f:
				# pdb.set_trace()
				if Constants.begin_question in line:
					inside_question = True
				
				if inside_question == True:
					#pdb.set_trace()
					if Constants.answerindicator in line:
						self.answer_buffer = line
						self.template_buffer += '\n'+Constants.answerindicator+'\n'
					elif Constants.questionindicator in line:
						self.question_buffer = line
						self.template_buffer += '\n'+Constants.questionindicator+'\n'
					elif Constants.end_question in line:
						inside_question = False
				else:
					self.template_buffer += line
					

parser = argparse.ArgumentParser(description='Creates exams')
parser.add_argument('--answ', dest='answerSetSize', default=5,
					help='Set the answer set size (default: 5)')
parser.add_argument('--qdb', dest='questionDatabasePath',
					required=True, help= 'Set the question database file path')
parser.add_argument('--edb', dest='studentDatabasePath', required=True,
					help='Set the student database file')
parser.add_argument('--nq', dest='numberOfQuestions', required=True,
					help='Set the number of questions of the test')
parser.add_argument('--ouf', dest='outputFormat', default='latex',
					help='Set the output format')
parser.add_argument('--latemp', dest='latexTemplateLocation',
					help='Set the latex template path')
args = parser.parse_args()

questionobjs = readQuestionFile(args.questionDatabasePath)

question_statement, answers, rigth_answer_index = questionobjs[2].generateNewVersionOfQuestion(int(args.answerSetSize))

exam = Exam()
if args.outputFormat == 'latex':
	exam.readLatexTemplate(args.latexTemplateLocation)

print "Question buffer ---"
print exam.question_buffer
print "Answers buffer---"
print exam.answer_buffer

print "Template buffer ---"
print exam.template_buffer


