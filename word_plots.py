# script for making charts of word frequencies
# v1.0

import pandas as pd
import string
from datetime import datetime
import matplotlib.pyplot as plt


print 'Reading roles data...'
daily_roles = pd.read_csv('data/daily_roles_percent.tsv', sep='\t', encoding='utf-8')
daily_roles['time'] = pd.to_datetime(daily_roles['time'])

print 'Plotting...'
for c in ['parent', 'teacher', 'citizen', 'student']:
    print c, 'per Day...'
    ax = daily_roles[c].plot(title = c + ' per Day')
    fig = ax.get_figure()
    fig.savefig('figures/'+c+'_per_day.png')
    fig.clear()
    ax.clear()

print 'Reading topics data...'
daily_txt_per = pd.read_csv('data/daily_text_percent.tsv', sep='\t', encoding='utf-8')
daily_txt_per['time'] = pd.to_datetime(daily_txt_per['time'])

print 'Plotting...'
for c in ['bathroom', 'rights', 'need', 'safe', 'sex', 'gender', 'bully',
          'biology', 'religion', 'family']:
    print c, 'per Day...'
    ax = daily_txt_per[c].plot(title = c + ' per Day')
    fig = ax.get_figure()
    fig.savefig('figures/'+c+'_per_day.png')
    fig.clear()
    ax.clear()

print 'Working with word counts...'
summary = pd.read_csv('data/word_counts.tsv', sep='\t', encoding='utf-8')
summary['time'] = pd.to_datetime(summary['time'])
summary = summary.set_index('time')
daily = summary.groupby(pd.TimeGrouper(freq='D')).mean()

ax = daily.wc.plot()
fig = ax.get_figure()
fig.savefig('figures/mean_word_count_per_day.png')
fig.clear()
ax.clear()

print 'Working with merged data...'
together = pd.read_csv('data/annotated_comments.tsv', sep='\t', encoding='utf-8')

roles = ['parent', 'teacher', 'citizen', 'student', 'concern']
themes = ['bathroom', 'rights', 'need', 'safe', 'sex', 'gender', 'bully',
       'biology', 'religion', 'family']

print 'Calculating cooccurances...'
cooccur = {}
for t in themes:
    d = {}
    for r in roles:
        n = len(together[r] > 0) * 1.0
        d[r] = len(together[(together[r] > 0) & (together[t] > 0)]) / n
    cooccur[t] = d

rel = pd.DataFrame.from_dict(cooccur)#, orient='index')

print 'Plotting...'
for c in rel.columns.values:
    print c, 'Topic Mention Frequency...'
    ax = rel[c].plot.bar(title = c + ' Topic Mention Frequency')
    fig = ax.get_figure()
    fig.savefig('figures/'+c+'_topic_Mention_Frequency.png')
    fig.clear()
    ax.clear()

ax = rel.plot.bar(title='Theme Frequency by Role')
fig = ax.get_figure()
fig.set_size_inches(7,7)
fig.savefig('figures/Theme_Frequency_by_Role.png')
fig.clear()
ax.clear()


