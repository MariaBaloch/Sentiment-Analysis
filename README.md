# Sentiment-Analysis
Text Mining and Sentiment Analysis
Business Objective:
Text mining is the process of examining large collections of text and converting the unstructured text data 
into structured data for further analysis like visualization and model building. We will utilize the power of 
text mining to do an in-depth analysis of customer reviews on a cell phone model.
Customer reviews are a great source of “Voice of customer” and could offer tremendous insights into 
what customers like and dislike about a product. As an investigative tool, TM is capable of supplying 
insights and knowledge from social media data, of a company. It is able to reveal the competitor strategy, 
by mining their Facebook or Twitter, for information on how customer engagement, promotion of services 
and customer bonding should be conducted.
The Project is about applying Text mining and sentiment Analysis to user generated content from distinct 
sources, in the cell phones domain, with the purpose of detection and discovery of defects in a product.
The business value is derived as an early discovery of defects can help manufacturers in quality 
improvement, thus minimize selling and production of defective product units. Meaning, customer 
dissatisfaction is decreased as well as the warranties costs and defect-associated costs.
Our main objective is to gain insights and knowledge by applying TM on data gathered from online forums 
on reviews, related to cell phones. Revealing how different entities (brands), by their frequency in the 
discussions, co-occur in the data. The analysis showcase's the ability to quantify what consumers wrote 
about each Phone Model, being externally validated with survey data. The Project shows TM value in 
capable of specifying a sentiment e.g. “problem”, and its co-occurrence with terms like camera, battery 
for the brand Samsung or any other brand. Applying a similar approach could be used to identify ways of 
quality improvement, by using the technology for quality control, identifying what aspects of a cell phone 
(or product) that lead to customers’ disapproval. By applying Applied Analysis techniques to identify and 
monitor underlying sentiments in text, written by consumers in reviews. The result is the capability of 
monitoring emotion such as surprise, anger, fear or sadness, on events or topics in the project. The 
findings give implications of benefits for use in large scale projects, to highlight issues needing to be 
addressed, for quality assurance
User Story:
As TM reveal how the words, as they appear in a review and in what context, lead to certain ratings, 
Mobile Phone brands can gain the insights and knowledge about their products. The analysis therefore 
suggests, what the factors leading to better satisfaction, for a phone experience, are. Here, for example, 
battery life was an important factor to high satisfaction rating, and words related to features. Knowing 
what factors tacitly lead to certain ratings is of high business value, as the knowledge lets the Brand know 
exactly what they could improve for better customer relationships (also service improvement).
Underlying data science problem:
Our vision for this project is to work with opinion driven resources such as online reviews and blogs. Our 
project focuses on text mining and sentiment analysis where the problem drills down to classification for 
modern data scientists in the form of factual (objective) based and opinion (subjective) based 
classification. Primarily, the focus will be on solving the problem of recommending the right product to 
customers pertaining to cell phone devices.
The aim is to use text from surveys/reviews and determine likelihood of a product being recommended 
by a customer. The model will be such that it will follow a supervised machine learning technique with 
being labelled with a positive or negative sentiment being trained on some test data sample.
This further supports the concept of predicting user experience which is one of the known and popular 
data science problem that majority data scientists are working to optimize.
Tools and Techniques:
About the data set:
The dataset that we will be using for the project is from Kaggle and is about different mobile phone 
models, revolving around the reviews written by customers. This data set includes 7 csv data files, which 
have a total of 1.4 million user ratings and reviews for different brands of cell phones. Each row 
corresponds to a customer review, and includes the variables: phone_url, date, lang, country, source, 
domain, score, score_max, extract, author and product.
We'll be using the Classification Models to understand various aspects of text mining, that are based on 
the review text as the independent variable to predict whether a customer recommends a product. The
focus will be to understand differences between customers who recommend a product and those who 
don't. Text Mining includes the following steps:
Step 1: Text Extraction
Sklearn.model_selection is package in python for splitting data into training and test sets.
CountVectorizer is a great tool provided by the scikit-learn library in Python. It is used to transform a given 
text into a vector on the basis of the frequency (count) of each word that occurs in the entire text.
Step 2: Text Pre-processing:
Text pre-processing includes data cleanup techniques and transformation of the documents in the training 
data to a document-term matrix.
Step 3: Document-Term-Matrix:
A document-term matrix is a mathematical matrix that describes the frequency of terms that occur in a 
collection of documents. The pre-processed and cleaned up data is converted into a matrix called the 
document term matrix.
Step 4: Exploratory text analysis:
We can use TFIDFVectorizer for word frequency scores that try to highlight words that are more frequent 
in a document. We will then look at how to create bi-grams and tri-grams and perform some exploratory 
analysis on the same.
n-gram: All the analysis that we have done so far have been based on single words that are called as 
Unigrams. However, it can be very insightful to look at multiple words. This is called as N-grams in text 
mining, where N stands for the number of words. For example, bi-gram contains 2 words.
Step 5: Feature Extraction
The exploratory text analysis has given several insights based on the customer reviews. In terms of 
classification algorithms used, there is not much of a difference between data and text input. We will try 
3 of the most popular classification algorithms — XGBOOST, Random forest and logistic regression.
Tokenisation: Tokenisation is the process of decomposing text into distinct pieces or tokens. Once 
tokenisation is done, after all the pre-processing, it is possible to construct a dataframe where each row 
represents a document and each column represents a distinct token and each cell gives the count of the 
token for a document.
Step 6: Building the Classification Models
In this step, we will have the document frequency matrix which is pre-processed, treated and ready to be 
used for classification.
