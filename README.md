# mi_trans_comments

This code was written collaboratively during the University of Michigan [2016 ICOS Big Data Summer Camp](https://ibug-um16.github.io/2016-summer-camp/). It aims to analyze trends and themes in the responses to the Michigan Department of Education's [Request for Public Comment](http://everyvoicecountsmi.org/136) on the State Board of Education Draft Statement and Guidance on Safe and Supportive Learning Environments for Lesbian, Gay, Bisexual, Transgender, and Questioning (LGBTQ) Students. 

**About the data:**
- 12,328 comments from the public between March 16 and May 11, 2016
    - Total words: 1,875,502
    - Comment Length: 
        - Mean: 152 words
        - Standard deviation: 205.7
        - Median: 99 words
        - Longest comment: 6,988 words

**Implemented functionality:**
- Scrape and parse comments
- Graph comment frequency over time
- Identify frequent words
- Categorize commenter roles
- Categorize basic themes in comments

**Packages used:**
- BeautifulSoup
- datetime
- matplotlib.pyplot
- nltk
- pandas
- time
- urllib2

**Group members:**
- Theresa Choe
- Erin Lane
- Jeff Lockhart
- Stephanie Miller
- Dave Ogden
- Emily Vargas
