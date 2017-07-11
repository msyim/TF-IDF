from os import listdir
import re
import math
from operator import itemgetter
from os.path import isfile, join

TF_SCHEME='COUNT'
#TF_SCHEME='BOOLEAN'
#TF_SCHEME='LOG'

# directory where all input files reside.
INPUTDIR='./data'

fileList = [join(INPUTDIR,f) for f in listdir(INPUTDIR) if isfile(join(INPUTDIR,f))]

TF = {}
docCount = {}
for f in fileList:
	# read each file data
	data = open(f,'r').read()
	
	# remove punctuations
	data = re.sub('[.,\'\"?!]','',data)

	termFrequency = {}	
	wordList = data.split()

	# fill out the term frequncy map for this file
	for term in wordList :
		if term in termFrequency : termFrequency[term] = termFrequency[term] + 1
		else : 
			termFrequency[term] = 1
			# increment the docCount for this term
			if term in docCount : docCount[term] = docCount[term] + 1
			else : docCount[term] = 1

	if TF_SCHEME == 'BOOLEAN' :
		for el in termFrequency: termFrequency[el] = 1
	if TF_SCHEME == 'LOG' :
		for el in termFrequency: termFrequency[el] = math.log10(termFrequency[el]) 

	TF[f] = termFrequency

def computTFIDF(doc, term):
	if term in TF[doc]:
		# idf = total_doc_count / # of docs containing 'term'
		idf = float(len(TF))/docCount[term]
		return TF[doc][term] * idf
	else : return 0

# get a query term from command line
qterm = raw_input('Enter a term. Type \'quit\' to quit\n\n')
while qterm != 'quit':
	pairList = [(f,computTFIDF(f,qterm)) for f in fileList]
	pairList = sorted(pairList, key=itemgetter(1), reverse=True)
	print "Doc ranking for the term \"%s\"\n" % qterm
	rank = 1
	for el in pairList:
		print "[rank : %d] doc: %s, score: %f" % (rank,el[0],el[1])
		rank += 1
		
	qterm = raw_input('\nEnter a term. Type \'quit\' to quit\n\n')

