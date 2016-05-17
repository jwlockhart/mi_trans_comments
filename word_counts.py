# Script for calculating word counts in comment data
# v1.1

import nltk
import pandas as pd
import string
from collections import Counter
from datetime import datetime
import matplotlib.pyplot as plt

print 'reading data...'
data = pd.read_csv('parsed.tsv', sep='\t', index_col=0, encoding='utf-8')
data['author'] = data.author.astype(unicode)
data['occupation'] = data.occupation.astype(unicode)
data['text'] = data.text.astype(unicode)
data['time'] = pd.to_datetime(data['time'])

#fetch some natural language information and functions
stemmer = nltk.stem.porter.PorterStemmer()
remove_punctuation_map = dict((ord(char), None) for char in string.punctuation)
lem = nltk.stem.wordnet.WordNetLemmatizer()

def remove_stops(words):
    '''cut out stop words'''
    return [word for word in words if word not in nltk.corpus.stopwords.words('english')]

def lem_tokens(tokens):
    '''word lems'''
    return [lem.lemmatize(item) for item in tokens]

def stem_tokens(tokens):
    '''word stems'''
    return [stemmer.stem(item) for item in tokens]

def normalize(text):
    '''remove punctuation, lowercase, stem'''
    print 'cleaning...'
    clean = text.lower().translate(remove_punctuation_map)
    print 'tokenizing...'
    tokens = nltk.tokenize.word_tokenize(clean)
    print 'removing stops...'
    tokens = remove_stops(tokens)
    print 'stemming...'
    stems = stem_tokens(tokens)
    print 'lemming...'
    return lem_tokens(stems)

def get_freqs(raw):
    print 'cleaning up text...'
    clean = normalize(raw)
    print 'counting words...'
    freqs = Counter(clean)
    words = pd.DataFrame.from_dict({'count': freqs})
    print 'sorting by most common words...'
    return words.sort_values(by='count', ascending=False)

def count_matches(text, words):
    '''count the number of times anything from a list of words appear in a text'''
    n = 0
    for w in words:
        n += text.lower().count(w)
    return n

def test_matches(text, words):
    '''test whether anything in a list of words is in a text'''
    for w in words:
        if w in text.lower():
            return 1
    return 0

def wc(txt):
    '''word count'''
    return len(nltk.tokenize.word_tokenize(txt))

print 'figuring out most common author words...'
author = get_freqs('\n'.join(data.author.values))
author.to_csv('data/author_word_frequencies.tsv', sep='\t', encoding='utf-8')

print 'figuring out most common role words...'
occupation = get_freqs('\n'.join(data.occupation.values))
occupation.to_csv('data/role_word_frequencies.tsv', sep='\t', encoding='utf-8')

print 'figuring out most common words in comment text...'
comment = get_freqs('\n'.join(data.text.values))
#ignore words used less than 10 times in the ~1.6M word corpus
comment = comment[comment['count'] >= 10]
comment.to_csv('data/comment_word_frequencies.tsv', sep='\t', encoding='utf-8')

print 'Categorizing poster roles...'
occs = data.copy()
occs = occs[['time', 'occupation']]
occs['cid'] = occs.index
occs = occs.set_index('time')
occs['parent'] = occs.occupation.apply(
    count_matches, words=['parent', 'mother', 'father', 'mom', 'dad', 'grandp', 'grandm'])
occs['teacher'] = occs.occupation.apply(test_matches, words=['teacher'])
occs['citizen'] = occs.occupation.apply(test_matches, words=['citizen', 'public', 'voter', 'tax'])
occs['student'] = occs.occupation.apply(test_matches, words=['student'])
occs['concern'] = occs.occupation.apply(test_matches, words=['concern'])
occs['none'] = occs.occupation.apply(test_matches, words=['nan'])

print 'Calculating number of roles per day...'
daily_roles_abs = occs.groupby(pd.TimeGrouper(freq='D')).sum()
daily_roles_abs.to_csv('data/daily_roles_count.tsv', sep='\t', encoding='utf-8')
print 'Calculating ratio of roles per day...'
daily_roles_per = occs.groupby(pd.TimeGrouper(freq='D')).mean()
daily_roles_per.to_csv('data/daily_roles_percent.tsv', sep='\t', encoding='utf-8')

print 'Categorizing comment text roles...'
txts = data.copy()
txts = txts[['time','text']]
txts['cid'] = txts.index
txts = txts.set_index('time')
txts['bathroom'] = txts.text.apply(test_matches, words=['bathroom', 'locker', 'shower', 'assault'])
txts['rights'] = txts.text.apply(test_matches, words=['rights'])
txts['need'] = txts.text.apply(test_matches, words=['need'])
txts['safe'] = txts.text.apply(test_matches, words=['safe', 'protect', 'risk'])
txts['sex'] = txts.text.apply(test_matches, words=['sex '])
txts['gender'] = txts.text.apply(test_matches, words=['gender'])
txts['bully'] = txts.text.apply(test_matches, words=['bulli'])
txts['biology'] = txts.text.apply(test_matches, words=['biolog'])
txts['religion'] = txts.text.apply(test_matches, words=['god', 'christ', 'lord', 'faith'])
txts['family'] = txts.text.apply(test_matches, words=['famil'])

print 'Calculating number of posts with a topic per day...'
daily_txt_abs = txts.groupby(pd.TimeGrouper(freq='D')).sum()
daily_txt_abs.to_csv('data/daily_text_count.tsv', sep='\t', encoding='utf-8')
print 'Calculating ratio of posts with a topic per day...'
daily_txt_per = txts.groupby(pd.TimeGrouper(freq='D')).mean()
daily_txt_per.to_csv('data/daily_text_percent.tsv', sep='\t', encoding='utf-8')

print 'Doing word counts...'
summary = data.copy()
summary['wc'] = summary.text.apply(wc)
summary = summary[['time', 'wc']]
summary['cid'] = summary.index
summary.to_csv('data/word_counts.tsv', sep='\t', encoding='utf-8')
#summary = summary.set_index('time')

print 'Merging comment annotations...'
together = occs.merge(txts, left_on='cid', right_on='cid')
together = together.merge(summary, left_on='cid', right_on='cid')
together.to_csv('data/annotated_comments.tsv', sep='\t', encoding='utf-8')

print 'Done!'






