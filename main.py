from math import floor
from random import randint 
from abc import ABC

def boolString(x):  # snake_case чаще используется в питоне
	return  '\033[92m' + str(x) + '\033[0m' if x else '\033[91m' + str(x) + '\033[0m'

def randomValue():
	return randint(0, 100000)

def count(vector):
	counts = {}

	for v in vector:
		if v in counts:
			counts[v] += 1
		else:
			counts[v] = 1

	return counts

def mostCommonFrequency(vector):
	counts = count(vector)
	return sorted(counts.items(), key=lambda item: item[1])[-1]

class General(ABC):

	def __init__(self, n, name, value):
		self._n = n
		self._m = floor(n * 1/3)
		self._name = name
		self._value = value
		self._generalsValues = {}
		self._generalsVectors = []

	@property
	def name(self):
		return self._name

	@property
	def value(self):
		return self._value

	@property
	def vector(self):
		return self._generalsValues
	
	def receiveValue(self, name, value):
		self._generalsValues[name] = value

	def receiveVector(self, name, vectors):
		self._generalsVectors.append(vectors)

	def solution(self):
		answer = {}

		for key in self._generalsVectors[0].keys():
			values = [v[key] for v in self._generalsVectors]
			common, frequency = mostCommonFrequency(values)
			answer[key] = common if frequency > self._m else "None"

		return answer


class Loyal(General):

	def __str__(self):
		return str(self._name) + ' - ' + str(self._value)

class Imposter(General):
	
	@property
	def value(self):
		return randomValue()

	def receiveValue(self, name, value):
		self._generalsValues[name] = randomValue()

	def __str__(self):
		return str(self._name) + ' - ' + '\033[91mImposter\033[0m'

l = int(input('Loyals count: '))
m = int(input('Imposters count: '))
n = l + m

if n < 8:
	names = ['Alice', 'Bob', 'Carol', 'Dave', 'Eve', 'Frank', 'Grace']
else:
	names = ['G' + str(i) for i in range(1, n + 1)]

loyals = [Loyal(n, names[i], randomValue()) for i in range(l)]
imposters = [Imposter(n, names[i], randomValue()) for i in range(l, n)]
generals = loyals + imposters

print('Generals: ')
for g in generals:
	print(g)

print()
input()
print()


for recipient in generals:
	for sender in generals:
		recipient.receiveValue(sender.name, sender.value)

print('Vectors:')
for general in generals:
	print(general.name)
	print(general.vector)
	print()

input()
print()
print()


for recipient in generals:
	for sender in generals:
		recipient.receiveVector(sender.name, sender.vector)


print('Solution:')
for general in generals:
	print(general.name)
	print(general.solution())
	print()

solutions = [general.solution() for general in generals]
consensus = True
for s in solutions:
	for ss in solutions:
		consensus = consensus and (s == ss)

noneCounts = count(solutions[0].values())
if 'None' in noneCounts:
	noneCount = noneCounts['None']
else:
	noneCount = 0

consensus = consensus and (noneCount < n / 3)
print('Practicaly consensus:', boolString(consensus))
print('Theoreticaly consensus:', boolString(str(m < n / 3)))
# end