import random

class Question:
	def __init__(self, word):
		self.word = word
		self.__answer = None

	# TODO: for some words we'll need proof that user knows their definition
	# not just yes/no
	def setAnswer(self, answer):
		self.__answer = answer

	def answer(self):
		return self.__answer

class Vocabulary:
	def __init__(self, corpora):
		self.__corpora = corpora

	def __sample(self):
		N_QUESTIONS = 50
		# Strictly sampling should be with replacements, but for simplicity we
		# try to leave it without
		return random.sample(self.__corpora.words(), N_QUESTIONS)

	def getQuestions(self):
		return [Question(word) for word in self.__sample()]

	# TODO: user can modify questions on the outside - even change the number.
	# think if it is acceptable for us
	def calculate(self, questionsNAnswers):
		answers = [q.answer() for q in questionsNAnswers]
		if None in answers:
			raise ValueError()
		known = answers.count(True)
		return known / len(questionsNAnswers) * len(self.__corpora.words())
