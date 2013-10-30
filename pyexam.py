import sys, random, argparse

'''
Reads a flat file of questions
'''
def readQuestionFile(path):
	questionindicator = ":QUEST:"
	answerindicator = ":ANSWER:"
	rightanswerindicator = ":RIGHT_ANSW:"

	questionobjs = []
	question = None
	first_item = True
	with open(path,"r") as f:
		for line in f:
			if questionindicator in line:
				
				if first_item is True:
					first_item = False
				else:
					questionobjs.append(question)
				question = Question();
				question.question_statement = line.strip().replace(questionindicator,"")
			if answerindicator in line:
				question.answers.append(line.strip().replace(answerindicator,""))
			if rightanswerindicator in line:
				question.right_answer = line.strip().replace(rightanswerindicator,"")
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
				right_answer=None):
		self.question_statement = question_statement if question_statement is not None else ""
		self.answers = shuffle(self.answers) if answers is not None else []
		self.right_answer = right_answer if right_answer is not None else ""

	
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
			print '[ERROR] The number of answer choices is less than the answer set size.'
			print 'Error question:'
			print ':QUEST:'+self.question_statement
			print 'Number of answer choices: ' + str(len(self.answers)+1)
			print 'Required at least '+str(answerSetSize)
			print 'Check the number of answer choices and try again.'
			sys.exit()
		answers = self.answers[:answerSetSize-1]
		answers.append(self.right_answer)
		shuffle(answers)
		return self.question_statement, answers, answers.index(self.right_answer)


parser = argparse.ArgumentParser(description='Creates exams')
parser.add_argument('--answ', dest='answerSetSize', default=5,
					help='Set the answer set size (default: 5)')
parser.add_argument('--qdb', dest='questionDatabasePath',
					required=True, help= 'Set the question database file')
parser.add_argument('--edb', dest='studentDatabasePath', required=True,
					help='Set the student database file')
parser.add_argument('--nq', dest='numberOfQuestions', required=True,
					help='Set the number of questions of the test')
args = parser.parse_args()

questionobjs = readQuestionFile(args.questionDatabasePath)
question_statement, answers, rigth_answer_index = questionobjs[2].generateNewVersionOfQuestion(int(args.answerSetSize))
print question_statement
print answers
print rigth_answer_index


