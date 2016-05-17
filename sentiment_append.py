import pandas as pd
import scipy.stats as stats
import numpy as np
import matplotlib.pyplot as plt

print 'Reading comment...'
comments = pd.read_csv('data/annotated_comments.tsv', sep='\t', index_col=0)

#dict for holding our data
summary = {}

print 'Reading and parsing sentiment data...'
with open('data/sentiment.txt', 'r') as f:
    #for each line (one comment)
    for l in f:
        s = {}
        #clean up the data
        tmp = l.strip().split(',')
        cid = tmp[0].replace('.txt', '')
        tmp = tmp[1:]
        
        for i in range(0, len(tmp)):
            tmp[i] = int(tmp[i])
            
        s['sentiment_mean'] = np.mean(tmp) #(1.0 * sum(tmp)) / len(tmp)
        s['sentiment_std'] = np.std(tmp)
        s['n_sentences'] = len(tmp)
            
        summary[cid] = s
        
print 'Merging sentiment and comment data...'
s = pd.DataFrame.from_dict(summary, orient='index')
test = comments.merge(s, how='left', left_on='cid', right_index=True)
test['time'] = pd.to_datetime(test['time'])
test.to_csv('data/annotated_comments_with_sentiment.tsv', sep='\t')

print 'Plotting average daily sentiment...'
test = test.set_index('time')
daily = test[['sentiment_mean']].groupby(pd.TimeGrouper(freq='D')).mean()
daily['sem'] = test[['sentiment_mean']].groupby(pd.TimeGrouper(freq='D')).apply(stats.sem)
daily.plot(x=daily.index, yerr='sem', title='Average Daily Sentiment')