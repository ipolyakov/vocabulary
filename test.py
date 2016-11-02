import matplotlib.pyplot as plt
import random
import string
import unittest

from vocabulary import Vocabulary

class MockCorpora:
	def __init__(self, knownWords, unknownWords):
		self.knownWords = knownWords
		self.unknownWords = unknownWords

	def words(self):
		return list(self.knownWords) + list(self.unknownWords)

def generateWord():
	MIN_WORD_LENGTH = 3
	MAX_WORD_LENGTH = 7
	length = random.randint(MIN_WORD_LENGTH, MAX_WORD_LENGTH)
	return ''.join(random.choice(string.ascii_lowercase) for _ in range(length))

def generateUniqueWords(n, ruleOut=[]):
	result = set()
	while len(result) < n:
		newWord = generateWord()
		if not newWord in ruleOut:
			result.add(newWord)
	return result

def measurement(knownWords, unknownWords):
	corpora = MockCorpora(knownWords, unknownWords)
	v = Vocabulary(corpora)
	questions = v.getQuestions()
	for q in questions:
		q.setAnswer(q.word in knownWords)
	return v.calculate(questions)

class TestVocabulary(unittest.TestCase):
	def test(self):
		N_KNOWN = 10000
		knownWords = generateUniqueWords(N_KNOWN)
		unknownWords = generateUniqueWords(50000, ruleOut=knownWords)
#		ciDistribution = [measurement(knownWords, unknownWords) for _ in range(1000)]
#		distribution = [(l + u) / 2 for l, u in ciDistribution]
#		plt.hist(distribution)
#		plt.show()
		lower, upper = measurement(knownWords, unknownWords)
		print(lower, upper)
		self.assertLessEqual(lower, N_KNOWN)
		self.assertLessEqual(N_KNOWN, upper)
		self.assertLessEqual((upper - lower) / 2, 0.1 * N_KNOWN)
