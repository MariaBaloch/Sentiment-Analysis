# -*- coding: utf-8 -*-
"""phone_user_review.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1nukita4V-FBP8yyYqsxgjRo4OnWpN3J_

Region library installation
"""

!pip install langdetect
!pip install boto3
!pip install fsspec
!pip install s3fs
!pip install pandasql
!pip install -qq transformers
!pip install nltk
#!pip install google_trans_new
#!pip install googletrans==4.0.0-rc1
#!pip install google-cloud-translate==2.0.1

import nltk
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

"""Importing region"""

import pandas as pd
pd.options.display.max_colwidth = 200
import numpy as np
import re
from langdetect import detect
import boto3
from pandasql import sqldf

import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split

from nltk.tokenize import word_tokenize
from nltk.tokenize import sent_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords

import transformers
from transformers import BertModel, BertTokenizer, AdamW, get_linear_schedule_with_warmup
import torch
from torch import nn, optim
from torch.utils.data import Dataset, DataLoader
from collections import defaultdict

device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

access_key = "AKIASV5GDKHTFTWVBJA2"
secret_key = "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"

#pd.read_csv('s3://arsalanmubeenbucket/CleanData.csv', error_bad_lines=False,encoding='latin1')

#access_key = "AKIAJ2ELTMC2LELTQDJQ"
#secret_key = "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"

s3_client = boto3.client('s3',  aws_access_key_id=access_key, aws_secret_access_key=secret_key)
s3 = boto3.resource('s3', aws_access_key_id=access_key, aws_secret_access_key=secret_key)

for bucket in s3.buckets.all():
  print(bucket.name)

csv_file_list = ["s3://arsalanmubeenbucket/phone_user_review_file_1.csv", 
                 "s3://arsalanmubeenbucket/phone_user_review_file_2.csv",
                 "s3://arsalanmubeenbucket/phone_user_review_file_3.csv",
                 "s3://arsalanmubeenbucket/phone_user_review_file_4.csv"]


#csv_file_list = ["s3://myclassbucket1/phone_user_review_file_1.csv", 
#                 "s3://myclassbucket1/phone_user_review_file_2.csv",
#                 "s3://myclassbucket1/phone_user_review_file_3.csv",
#                 "s3://myclassbucket1/phone_user_review_file_4.csv"]

"""Append all the CSV and extract only English labels sentence """

list_of_dataframes = []

for filename in csv_file_list:
    list_of_dataframes.append(pd.read_csv(filename, error_bad_lines=False,encoding='latin1'))

merged_df = pd.concat(list_of_dataframes)

def Round_F(row):
  try:
   rating = int(row['score'])
   val = round(rating)
  except:
    val = 0
  return val

print("number of null count in score column : ",merged_df.score.isnull().sum())

merged_df['score'] = merged_df.apply(Round_F, axis=1)

sns.countplot(merged_df.score)
plt.xlabel('review score');

"""We’re going to convert the dataset into negative, neutral and positive sentiment:"""

def to_sentiment(rating):
  rating = int(rating)
  if rating <= 4:
    return 0
  elif 4 < rating <= 6:
    return 1
  else:
    return 2

merged_df['sentiment'] = merged_df.score.apply(to_sentiment)

class_names = ['negative', 'neutral', 'positive']

ax = sns.countplot(merged_df.sentiment)
plt.xlabel('review sentiment')
ax.set_xticklabels(class_names);

encoder = LabelEncoder()
merged_df['encod_lang'] = encoder.fit_transform(merged_df.lang)

output = sqldf("select lang as Languages ,count(1) as Counts_of_Comments from merged_df group by lang")
print(output)

class_names = output['Languages']

ax = sns.countplot(merged_df.encod_lang)
plt.xlabel('Languages review')
ax.set_xticklabels(class_names);

"""Get Only English Sentences"""

df_ENG=merged_df.loc[merged_df['lang'] == 'en']

"""
Function that really checks that it's an English sentence
"""

def f(row):
    String = row['extract']
    try:
      val = detect(String)
    except TypeError:
      String= re.sub("[^a-zA-Z]"," ",str(String))
      val = detect(String)
    except :
      print(String)
      val = "nan"
    return val

df_ENG['lang2'] = df_ENG.apply(f, axis=1)

"""deleting outliers"""

indexNames = df_ENG[(df_ENG['lang2'] != 'en')].index
df_ENG.drop(indexNames , inplace=True)

df_ENG.count()

df_ENG = pd.read_csv('s3://arsalanmubeenbucket/CleanData.csv', error_bad_lines=False,encoding='latin1')

df_ENG.extract

"""to do lower case all English sentences """

df_ENG['extract']=df_ENG['extract'].str.lower()
#df_ENG.head(5)

"""removing annoying things"""

df_ENG['extract'].replace("[^a-zA-Z]"," ",regex=True, inplace=True)

from sklearn.feature_extraction.text import CountVectorizer
cv = CountVectorizer(max_features = 2500)
X = cv.fit_transform(df_ENG['extract']).toarray()

y=df_ENG['sentiment']

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=0).to(device)

cv.get_feature_names()[:20]

cv.get_params()

count_df = pd.DataFrame(X_train, columns=cv.get_feature_names())

count_df.head()

#applying model
from sklearn.naive_bayes import MultinomialNB

classifier=MultinomialNB()

from sklearn import metrics
import numpy as np
import itertools

classifier.fit(X_train, y_train)
pred = classifier.predict(X_test)
score = metrics.accuracy_score(y_test, pred)
print("accuracy:   %0.3f" % score)
cm = metrics.confusion_matrix(y_test, pred)
plot_confusion_matrix(X=cm,y_true=['FAKE', 'REAL'])

classifier.fit(X_train, y_train)
pred = classifier.predict(X_test)
score = metrics.accuracy_score(y_test, pred)
score

"""Data Preprocessing"""

PRE_TRAINED_MODEL_NAME = 'bert-base-cased'

tokenizer = BertTokenizer.from_pretrained(PRE_TRAINED_MODEL_NAME)

sample_txt = 'When was I last outside? I am stuck at home for 2 weeks.'

tokens = tokenizer.tokenize(sample_txt)
token_ids = tokenizer.convert_tokens_to_ids(tokens)

print(f' Sentence: {sample_txt}')
print(f'   Tokens: {tokens}')
print(f'Token IDs: {token_ids}')

tokenizer.sep_token, tokenizer.sep_token_id

tokenizer.cls_token, tokenizer.cls_token_id

tokenizer.pad_token, tokenizer.pad_token_id

tokenizer.unk_token, tokenizer.unk_token_id

"""**Choosing Sequence Length**

BERT works with fixed-length sequences. We'll use a simple strategy to choose the max length. Let's store the token length of each review:
"""

token_lens = []

for txt in df_ENG.extract:
  tokens = tokenizer.encode(txt, max_length=512)
  token_lens.append(len(tokens))

"""and plot the distribution:"""

sns.distplot(token_lens)
plt.xlim([0, 120]);
plt.xlabel('Token count');

"""Most of the reviews seem to contain less than 100 tokens, but we'll be on the safe side and choose a maximum length of 100."""

MAX_LEN = 100

"""We have all the building pieces required to form a PyTorch dataset."""

class GPReviewDataset(Dataset):
  # Contructor 
  def __init__(self, reviews, targets, tokenizer, max_len):
    self.reviews = reviews
    self.targets = targets
    self.tokenizer = tokenizer
    self.max_len = max_len
  # order method
  def __len__(self):
    return len(self.reviews)
  
  def __getitem__(self, item):
    review = str(self.reviews[item])
    target = self.targets[item]

    encoding = self.tokenizer.encode_plus(
      review,
      add_special_tokens=True,
      max_length=self.max_len,
      return_token_type_ids=False,
      pad_to_max_length=True,
      return_attention_mask=True,
      return_tensors='pt',
    )
     #dictionary
    return {
      'review_text': review,
      'input_ids': encoding['input_ids'].flatten(),
      'attention_mask': encoding['attention_mask'].flatten(),
      'targets': torch.tensor(target, dtype=torch.long)
    }

"""The tokenizer is doing most of the heavy lifting for us. We also return the review texts, so it'll be easier to evaluate the predictions from our model. Let's split the data:"""

RANDOM_SEED = 42

df_train, df_test = train_test_split(df_ENG, test_size=0.1, random_state=RANDOM_SEED)
df_val, df_test = train_test_split(df_test, test_size=0.5, random_state=RANDOM_SEED)

df_train.shape, df_val.shape, df_test.shape

"""wrap up into pytorch data loader"""

def create_data_loader(df, tokenizer, max_len, batch_size):
  # creating the Instance of GPReviewDataset class
  ds = GPReviewDataset(
    reviews=df.extract.to_numpy(),
    targets=df.sentiment.to_numpy(),
    tokenizer=tokenizer,
    max_len=max_len
  )

  return DataLoader(
    ds,
    batch_size=batch_size,
    num_workers=4 # for loading the data
  )

"""creating three loader for Training, validation and test data"""

BATCH_SIZE = 16

train_data_loader = create_data_loader(df_train, tokenizer, MAX_LEN, BATCH_SIZE)
val_data_loader = create_data_loader(df_val, tokenizer, MAX_LEN, BATCH_SIZE)
test_data_loader = create_data_loader(df_test, tokenizer, MAX_LEN, BATCH_SIZE)

data = next(iter(train_data_loader))
data.keys()

print(data['review_text'])
print(data['input_ids'].shape)
print(data['attention_mask'].shape)
print(data['targets'].shape)

"""so we have 16 example and 100 tokenizer we have

# **Sentiment Classification with BERT and Hugging Face**
"""

bert_model = BertModel.from_pretrained(PRE_TRAINED_MODEL_NAME)

"""we pass input_ids and attention_mask to the bert model it will give last last_hidden_state (which is to top most encoder from bert base) and also pooled output"""

class SentimentClassifier(nn.Module):

  def __init__(self, n_classes):
    super(SentimentClassifier, self).__init__()
    self.bert = BertModel.from_pretrained(PRE_TRAINED_MODEL_NAME)
    self.drop = nn.Dropout(p=0.3)
    self.out = nn.Linear(self.bert.config.hidden_size, n_classes)
  
  def forward(self, input_ids, attention_mask):
    _, pooled_output = self.bert(
      input_ids=input_ids,
      attention_mask=attention_mask,
      return_dict=False
    )
    output = self.drop(pooled_output)
    return self.out(output)

model = SentimentClassifier(len(class_names))
model = model.to(device)

input_ids = data['input_ids'].to(device)
attention_mask = data['attention_mask'].to(device)

print(input_ids.shape) # batch size x seq length
print(attention_mask.shape)

outputs  =  model(input_ids, attention_mask)

"""## Training

we'll use the AdamW optimizer provided by Hugging Face, we r doing the same thing as the original Bert paper did

How do we come up with all hyperparameters? The BERT authors have some recommendations for fine-tuning:

- Batch size: 16, 32
- Learning rate (Adam): 5e-5, 3e-5, 2e-5
- Number of epochs: 2, 3, 4

We're going to ignore the number of epochs recommendation but stick with the rest. Note that increasing the batch size reduces the training time significantly, but gives you lower accuracy.
"""

EPOCHS = 4

optimizer = AdamW(model.parameters(), lr=2e-5, correct_bias=False)
total_steps = len(train_data_loader) * EPOCHS

scheduler = get_linear_schedule_with_warmup(
  optimizer,
  num_warmup_steps=0,
  num_training_steps=total_steps
)

loss_fn = nn.CrossEntropyLoss().to(device)

"""the function go hit all the training data at least for one EPOCHS
and use than in backpropagation to our sentient classifier 
"""

def train_epoch(
  model, 
  data_loader, 
  loss_fn, 
  optimizer, 
  device, 
  scheduler, 
  n_examples
):
  model = model.train()

  losses = []
  correct_predictions = 0
  
  for d in data_loader:
    input_ids = d["input_ids"].to(device)
    attention_mask = d["attention_mask"].to(device)
    targets = d["targets"].to(device)

    outputs = model(
      input_ids=input_ids,
      attention_mask=attention_mask
    )

    _, preds = torch.max(outputs, dim=1)
    loss = loss_fn(outputs, targets)

    correct_predictions += torch.sum(preds == targets)
    losses.append(loss.item())

    loss.backward()
    nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
    optimizer.step()
    scheduler.step()
    optimizer.zero_grad()

  return correct_predictions.double() / n_examples, np.mean(losses)

"""Training the model should look familiar, except for two things. The scheduler gets called every time a batch is fed to the model. We're avoiding exploding gradients by clipping the gradients of the model using clip_grad_norm_."""

def eval_model(model, data_loader, loss_fn, device, n_examples):
  model = model.eval()

  losses = []
  correct_predictions = 0

  with torch.no_grad():
    for d in data_loader:
      input_ids = d["input_ids"].to(device)
      attention_mask = d["attention_mask"].to(device)
      targets = d["targets"].to(device)

      outputs = model(
        input_ids=input_ids,
        attention_mask=attention_mask
      )
      _, preds = torch.max(outputs, dim=1)

      loss = loss_fn(outputs, targets)

      correct_predictions += torch.sum(preds == targets)
      losses.append(loss.item())

  return correct_predictions.double() / n_examples, np.mean(losses)

"""Using those two, we can write our training loop. We'll also store the training history:"""

# Commented out IPython magic to ensure Python compatibility.
# %%time
# 
# history = defaultdict(list)
# best_accuracy = 0
# 
# for epoch in range(EPOCHS):
# 
#   print(f'Epoch {epoch + 1}/{EPOCHS}')
#   print('-' * 10)
# 
#   train_acc, train_loss = train_epoch(
#     model,
#     train_data_loader,    
#     loss_fn, 
#     optimizer, 
#     device, 
#     scheduler, 
#     len(df_train)
#   )
# 
#   print(f'Train loss {train_loss} accuracy {train_acc}')
# 
#   val_acc, val_loss = eval_model(
#     model,
#     val_data_loader,
#     loss_fn, 
#     device, 
#     len(df_val)
#   )
# 
#   print(f'Val   loss {val_loss} accuracy {val_acc}')
#   print()
# 
#   history['train_acc'].append(train_acc)
#   history['train_loss'].append(train_loss)
#   history['val_acc'].append(val_acc)
#   history['val_loss'].append(val_loss)
# 
#   if val_acc > best_accuracy:
#     torch.save(model.state_dict(), 'best_model_state.bin')
#     best_accuracy = val_acc

plt.plot(history['train_acc'], label='train accuracy')
plt.plot(history['val_acc'], label='validation accuracy')

plt.title('Training history')
plt.ylabel('Accuracy')
plt.xlabel('Epoch')
plt.legend()
plt.ylim([0, 1]);

"""## Evaluation

So how good is our model on predicting sentiment? Let's start by calculating the accuracy on the test data:
"""

test_acc, _ = eval_model(
  model,
  test_data_loader,
  loss_fn,
  device,
  len(df_test)
)

test_acc.item()

test_acc

"""A helper function to get the predictions from our model:"""

def get_predictions(model, data_loader):
  model = model.eval()
  
  review_texts = []
  predictions = []
  prediction_probs = []
  real_values = []

  with torch.no_grad():
    for d in data_loader:

      texts = d["review_text"]
      input_ids = d["input_ids"].to(device)
      attention_mask = d["attention_mask"].to(device)
      targets = d["targets"].to(device)

      outputs = model(
        input_ids=input_ids,
        attention_mask=attention_mask
      )
      _, preds = torch.max(outputs, dim=1)

      probs = F.softmax(outputs, dim=1)

      review_texts.extend(texts)
      predictions.extend(preds)
      prediction_probs.extend(probs)
      real_values.extend(targets)

  predictions = torch.stack(predictions).cpu()
  prediction_probs = torch.stack(prediction_probs).cpu()
  real_values = torch.stack(real_values).cpu()
  
  return review_texts, predictions, prediction_probs, real_values

"""This is similar to the evaluation function, except that we're storing the text of the reviews and the predicted probabilities (by applying the softmax on the model outputs):"""

y_review_texts, y_pred, y_pred_probs, y_test = get_predictions(
  model,
  test_data_loader
)

"""classification report"""

print(classification_report(y_test, y_pred, target_names=class_names))

"""confusion matrix:"""

def show_confusion_matrix(confusion_matrix):
  hmap = sns.heatmap(confusion_matrix, annot=True, fmt="d", cmap="Blues")
  hmap.yaxis.set_ticklabels(hmap.yaxis.get_ticklabels(), rotation=0, ha='right')
  hmap.xaxis.set_ticklabels(hmap.xaxis.get_ticklabels(), rotation=30, ha='right')
  plt.ylabel('True sentiment')
  plt.xlabel('Predicted sentiment');

#Converting into DataFrame
cm = confusion_matrix(y_test, y_pred)
df_cm = pd.DataFrame(cm, index=class_names, columns=class_names)
show_confusion_matrix(df_cm)

"""let's have a look at an example from our test data:"""

#example number from our model
idx = 2

review_text = y_review_texts[idx]
true_sentiment = y_test[idx]
#tell us probability of each class
pred_df = pd.DataFrame({
  'class_names': class_names,
  'values': y_pred_probs[idx]
})

print("\n".join(wrap(review_text)))
print()
print(f'True sentiment: {class_names[true_sentiment]}')

"""Now we can look at the confidence of each sentiment of our model:"""

sns.barplot(x='values', y='class_names', data=pred_df, orient='h')
plt.ylabel('sentiment')
plt.xlabel('probability')
plt.xlim([0, 1]);

"""### Predicting on Raw Text

Let's use our model to predict the sentiment of some raw text:

"""

review_text = "I love completing my todos! Best app ever!!!"

"""We have to use the tokenizer to encode the text:"""

encoded_review = tokenizer.encode_plus(
  review_text,
  max_length=MAX_LEN,
  add_special_tokens=True,
  return_token_type_ids=False,
  pad_to_max_length=True,
  return_attention_mask=True,
  return_tensors='pt',
)

"""Let's get the predictions from our model:"""

input_ids = encoded_review['input_ids'].to(device)
attention_mask = encoded_review['attention_mask'].to(device)

output = model(input_ids, attention_mask)
_, prediction = torch.max(output, dim=1)

print(f'Review text: {review_text}')
print(f'Sentiment  : {class_names[prediction]}')