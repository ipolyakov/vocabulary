import math
import matplotlib.pyplot as plt
import numpy
import random
import string
import sys
import unittest

from wordfreq import top_n_list, word_frequency, zipf_frequency

from vocabulary import Vocabulary

class MockCorpora:
	def __init__(self, nWords):
		self.__nWords = nWords
		self.__words = top_n_list('en', self.__nWords, wordlist='large')
#		sys.stdout.buffer.write(str(self.__words).encode('utf-8'))
		self.__frequencies = numpy.array([word_frequency(w, 'en') for w in self.__words])

	def words(self):
		return self.__words

	def frequencyClasses(self):
		fc = [round(zipf_frequency(w, 'en')) for w in self.__words]
		fc[0] = 7 # Hardcode workaround the single-member class '8' (word 'the')
		return fc

	def probabilities(self):
		return self.__frequencies / sum(self.__frequencies)

def measurement(nKnownWords, nUnknownWords):
	corpora = MockCorpora(nKnownWords + nUnknownWords)
	# We're using theoretical distribution of real person's vocabulary
	# it would be interesting to test it later against real vocabularies
	# but for now let's proceed with it
	knownWords = set(numpy.random.choice(corpora.words(), p=corpora.probabilities(), size=nKnownWords))
	print(knownWords)
	v = Vocabulary(corpora)
	questions = v.getQuestions()
	for q in questions:
		q.setAnswer(q.word in knownWords)
	print([q.word for q in questions])
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
