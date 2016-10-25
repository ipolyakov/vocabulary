import random
import string
import unittest

from vocabulary import Vocabulary

class MockCorpusParams:
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

class TestVocabulary(unittest.TestCase):
	def test(self):
		knownWords = generateUniqueWords(1000)
		unknownWords = generateUniqueWords(3000, ruleOut=knownWords)
		print(knownWords)
		params = MockCorpusParams(knownWords, unknownWords)
		v = Vocabulary(params)
		questions = v.getQuestions()
		for q in questions:
			q.setAnswer(q.word in knownWords)
		vocabularyEstimate = v.calculate(questions)
		self.assertEquals(vocabularyEstimate, 1000)
