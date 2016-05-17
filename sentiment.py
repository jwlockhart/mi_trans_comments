# Code here is nearly lifted verbatim from reedcoke 's github repo for the camp:
# https://github.com/reedcoke/bigDataCamp2016
#
# also of note that this is very slow as it is implemented. If extended,
# this should be reworked to use the CoreNLP API (which does not currently
# support sentiment analysis) and to analyze comments in parallel. 

import pandas as pd
import subprocess
import os
import codecs
import numpy as np
import scipy
import sys

data = pd.read_csv('parsed.tsv', sep='\t', index_col=0)
data['time'] = pd.to_datetime(data['time'])

j = 0
n = len(data)
for (i, d) in data.iterrows():
    with open("data/" + i + '.txt','w') as out:
        out.write(d.text)
    j += 1
    if j % 1000 == 0:
        print j, 'of', n
        sys.stdout.flush()
        
print 'Done!'
    
def gatherSentiment():
    dataDir = 'data'
    speeches = [fname for fname in os.listdir(dataDir) if '.txt' in fname]

    #Stanford sentiment gives text ratings, we want numeric ratings
    points = {'very negative' : -3, 'negative' : -1, 'neutral' : 0,
              'positive' : 1, 'very positive' : 3}
    F = codecs.open('data/sentiment.txt', 'w', encoding='utf8', errors='ignore')
    
    i = 0
    n = len(speeches)*1.0
    
    for speech in speeches:
        speechF = os.path.join(dataDir, speech.replace(' ', '\ '))
        sentiment = runSentiment(speechF)
        scores = sentiment.split('\n')[1:]
        values = []
        for score in scores:
            try:
                values.append(str(points[score.strip().lower()]))
            except KeyError:                  
                continue
        F.write(speech + ',' + ','.join(values) + '\n')
        
        i += 1
        if i % 100 == 0:
            print i, 'of', n, ':', (100.0*i)/n, '%'
            sys.stdout.flush()

        
    F.close()

def runSentiment(fname):
    import subprocess
    
    classPath = '-cp "../stanford-corenlp-full-2015-12-09/*"'
    settings = ' -mx5g edu.stanford.nlp.sentiment.SentimentPipeline'
    inputFile = ' -file ' + fname
    command = 'java ' + classPath + settings + inputFile
    child = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
    results = []
    while True:
        out = child.stdout.read(1)
        if out == '' and child.poll() != None:
            return ''.join(results)
        if out != '':
            results.extend(out)

gatherSentiment()

print 'Done!'
