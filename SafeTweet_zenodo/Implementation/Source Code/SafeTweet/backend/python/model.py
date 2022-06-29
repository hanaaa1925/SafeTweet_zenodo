import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer

# data preprocess tools
from nltk import data
from nltk import download
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize, RegexpTokenizer

from sklearn.decomposition import PCA
from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score

import joblib


def text_process(text):
    tokenizer = RegexpTokenizer('[a-z0-9]+')
    token = tokenizer.tokenize(text)
    lemmatizer = WordNetLemmatizer()
    stop_words = set(stopwords.words('english'))
    stop_words.add('rt')
    token = [lemmatizer.lemmatize(w) for w in token if lemmatizer.lemmatize(w) not in stop_words]
    return token


abs_file = os.path.abspath(__file__)
abs_dir = abs_file[:abs_file.rfind('\\')] if os.name == 'nt' else abs_file[:abs_file.rfind(r'/')]	
dataset = os.path.join(abs_dir, 'dataset2.xlsx')

data = pd.read_excel(dataset)
data['content'] = data['content'].str.lower()
data['content'] = data['content'].apply(lambda string: ' '.join([word for word in string.split(' ') if not word.rstrip(' ').startswith('@')]))
data['content'] = data['content'].apply(lambda string: ' '.join([word for word in string.split(' ') if not word.rstrip(' ').startswith('#')]))
data['content'] = data['content'].apply(lambda string: ' '.join([word for word in string.split(' ') if not word.rstrip(' ').startswith('http')]))

data['content'] = data['content'].apply(text_process)
X = data['content']
y = data['label']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 118)

train = pd.concat([X_train, y_train], axis=1)
test = pd.concat([X_test, y_test], axis=1)

non_sensitive_train = train[train['label'] == 0]
sensitive_train = train[train['label'] == 1]

# non_sensitive_train_part = non_sensitive_train['content'].sample(139, random_state=42)
# sensitive_train_part = sensitive_train['content'].sample(139, random_state=42)

non_sensitive_trainset = non_sensitive_train['content']
sensitive_trainset = sensitive_train['content']

vocablist = []
for i in pd.concat([non_sensitive_trainset, sensitive_trainset]):
    vocablist += i

trainset_texts = [' '.join(content) for content in np.concatenate((non_sensitive_trainset.values, sensitive_trainset.values))]
train_all_texts = [' '.join(content) for content in train['content']]
test_all_texts = [' '. join(content) for content in test['content']]

cv = CountVectorizer()
trainset_fit = cv.fit(trainset_texts)
train_all_count = cv.transform(train_all_texts)
test_all_count = cv.transform(test_all_texts)


tfidf = TfidfTransformer()
train_tfidf_matrix = tfidf.fit_transform(train_all_count)
test_tfidf_matrix = tfidf.fit_transform(test_all_count)

model = MultinomialNB(alpha=1.1, fit_prior=True, class_prior=None).fit(train_tfidf_matrix, y_train)
#model.score(test_tfidf_matrix, y_test)

y_train_pdt = model.predict(train_tfidf_matrix)
y_test_pdt = model.predict(test_tfidf_matrix)

dts1 = len(np.where(y_train_pdt==y_train)[0])/len(y_train)
dts2 = len(np.where(y_test_pdt==y_test)[0])/len(y_test)

acc1 = accuracy_score(y_train_pdt, y_train)
acc2 = accuracy_score(y_test_pdt, y_test)

pre1 = precision_score(y_train_pdt, y_train)
pre2 = precision_score(y_test_pdt, y_test)

rec1 = recall_score(y_train_pdt, y_train)
rec2 = recall_score(y_test_pdt, y_test)

print("accuracy:{:.3f}%, precision:{:.3f}%, recall:{:.3f}%".format(acc1*100, pre1*100, rec1*100))
print("accuracy:{:.3f}%, precision:{:.3f}%, recall:{:.3f}%".format(acc2*100, pre2*100, rec2*100))


model_dir = os.path.join(abs_dir, 'train_model.m')
cv_dir = os.path.join(abs_dir, 'cv.f')
tfidf_dir = os.path.join(abs_dir, 'tfidf.f')

joblib.dump(model, model_dir, 1)
joblib.dump(cv, open(cv_dir, 'wb'))
joblib.dump(tfidf, open(tfidf_dir, 'wb'))