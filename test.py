import matplotlib.pyplot as plt
import random
import string
import unittest

from wordfreq import top_n_list

from vocabulary import Vocabulary

class MockCorpora:
	def __init__(self, knownWords, unknownWords):
		self.knownWords = knownWords
		self.unknownWords = unknownWords

	def words(self):
		return list(self.knownWords) + list(self.unknownWords)

	def frequencyClasses(self):
		

def generateWord():
	MIN_WORD_LENGTH = 3
	MAX_WORD_LENGTH = 7
	length = random.randint(MIN_WORD_LENGTH, MAX_WORD_LENGTH)
	return ''.join(random.choice(string.ascii_lowercase) for _ in range(length))

def generateUniqueWords(n):
	result = set()
	while len(result) < n:
		result.add(generateWord())
	return result

def measurement(knownWords, unknownWords):
	corpora = MockCorpora(knownWords, unknownWords)
	v = Vocabulary(corpora)
	questions = v.getQuestions()
	for q in questions:
		q.setAnswer(q.word in knownWords)
	return v.calculate(questions)

def plot():
	ciDistribution = [measurement(knownWords, unknownWords) for _ in range(1000)]
	distribution = [(l + u) / 2 for l, u in ciDistribution]
	plt.hist(distribution)
	plt.show()

class TestVocabulary(unittest.TestCase):
	def test(self):
		N_KNOWN = 10000
		allWords = generateUniqueWords(N_KNOWN + 40000)
		knownWords, unknownWords = allWords[:10000], allWords[10000:]
		lower, upper = measurement(knownWords, unknownWords)
		print(lower, upper)
		self.assertLessEqual(lower, N_KNOWN)
		self.assertLessEqual(N_KNOWN, upper)
		self.assertLessEqual((upper - lower) / 2, 0.1 * N_KNOWN)
