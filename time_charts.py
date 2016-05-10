# Script for plotting charts of comment frequency over time
# v1.0

import pandas as pd
import datetime
import matplotlib.pyplot as plt

print 'Reading data...'
data = pd.read_csv('parsed.tsv', sep='\t', index_col=0)
data['time'] = pd.to_datetime(data['time'])

print 'Making charts...'
#index the data by its timestamp
df = data.set_index('time')
data["day"] = df.index.weekday
data["hour"] = df.index.hour

print 'Posts per Day...'
daily = df.groupby(pd.TimeGrouper(freq='D'))['text'].count()
ax = daily.plot(title='Posts per Day')
fig = ax.get_figure()
fig.savefig('figures/posts_per_day.png')
fig.clear()
ax.clear()

print 'Posts per Hour...'
hourly = df.groupby(pd.TimeGrouper(freq='H'))['text'].count()
ax = hourly.plot(title='Posts per Hour')
fig = ax.get_figure()
fig.savefig('figures/posts_per_hour.png')
ax.clear()
fig.clear()

print 'Posts by Day of Week...'
day = data.groupby('day').count()
ax = day['text'].plot(title='Posts by Day of Week')
fig = ax.get_figure()
fig.savefig('figures/posts_by_day_of_week.png')
ax.clear()
fig.clear()

print 'Posts by Time of Day...'
hrs = data.groupby('hour').count()
ax = hrs['text'].plot(title='Posts by Time of Day')
fig = ax.get_figure()
fig.savefig('figures/osts_by_time_of_day.png')
ax.clear()
fig.clear()