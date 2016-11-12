import matplotlib.pyplot as plt
import random
import string
import unittest

from wordfreq import top_n_list

from vocabulary import Vocabulary

class MockCorpora:
	def __init__(self, nWords):
		self.__nWords = nWords

	def words(self):
		return top_n_list('en', self.__nWords, wordlist='large')

	def frequencyClasses(self):
		return [0] * self.__nWords

def measurement(nKnownWords, nUnknownWords):
	corpora = MockCorpora(nKnownWords + nUnknownWords)
	# say if one knows every 4th word in the entire vocabulary
	# that means if word1 appears twice more frequent that word2 in corpora
	# then probability of one knowing it should be twice higher as well
	v = Vocabulary(corpora)
	questions = v.getQuestions()
	for q in questions:
		# TODO: how to specify which words do I know
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
		lower, upper = measurement(N_KNOWN, 40000)
		print(lower, upper)
		self.assertLessEqual(lower, N_KNOWN)
		self.assertLessEqual(N_KNOWN, upper)
		self.assertLessEqual((upper - lower) / 2, 0.1 * N_KNOWN)
