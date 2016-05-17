# mi_trans_comments

This code was written collaboratively during the University of Michigan [2016 ICOS Big Data Summer Camp](https://ibug-um16.github.io/2016-summer-camp/). It aims to analyze trends and themes in the responses to the Michigan Department of Education's [Request for Public Comment](http://everyvoicecountsmi.org/136) on the State Board of Education Draft Statement and Guidance on Safe and Supportive Learning Environments for Lesbian, Gay, Bisexual, Transgender, and Questioning (LGBTQ) Students. 

**About the data:**
- Comments posted between March 16 and May 12, 2016
- 12,481 total comments
    - Total words: 1,899,056
    - Comment Length: 
        - Mean: 152 words (stddiv = 205.5)
        - Median: 99 words
        - Longest comment: 6,988 words

**Implemented functionality:**
- Scrape and parse comments
- Graph comment frequency over time
- Identify frequent words
- Categorize commenter roles
- Categorize basic themes in comments
- Sentiment analysis

**Packages used:**
- BeautifulSoup
- codecs
- datetime
- matplotlib
- nltk
- numpy
- os
- pandas
- scipy
- Stanford [CoreNLP](http://stanfordnlp.github.io/CoreNLP) (Java)
- subprocess
- sys
- time
- urllib2

**Group members:**
- Theresa Choe
- Erin Lane
- Jeff Lockhart
- Stephanie Miller
- Dave Ogden
- Emily Vargas
