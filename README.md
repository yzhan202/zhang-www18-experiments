A Structured Approach to Understanding Recovery and Relapse in AA

This repository contains the code for the paper:

"A Structured Approach to Understanding Recovery and Relapse in AA." Yue Zhang, Arti Ramesh, Jennifer Golbeck, Dhanya Sridhar and Lise Getoor. WWW 2018.

This code includes two parts. 'aa-feature' includes code for extracting linguistic features, psycho-linguistic features, structural features from collected data set. And these features are used as input for PSL model.

Linguistic Features: include Term Frequency, Alcohol/Sober Word Usage, Topic Distribution from Seeded Topic Modeling, Sentiment Scores.

Psycho-linguistic Features: we extract psycho-linguistic
features using LIWC[Linguistic Enquiry Word Count (LIWC). https://liwc.wpengine.com/]

Structural Features: Friends, Replies, Retweets, Similarity.

'PSL-aa' includes variations HL-MRF recovery prediction models. All these models are based on the Probabilistic Soft Logic framework[http://psl.linqs.org/].

PSL-Recovery-All: 

PSL-Linguistic:

PSL-Relational:

PSL-Topic:

PSL-Psychological(Affect):

PSL-Psychological(Social):

PSL-Sentiment: 

PSL-LIWCSimilarity: 

