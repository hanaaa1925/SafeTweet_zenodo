from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
# data preprocess tools
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import RegexpTokenizer

import sys
import stanza
import joblib
import pandas as pd
import os

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
train_model = os.path.join(abs_dir, 'train_model.m')
train_cv = os.path.join(abs_dir, 'cv.f')
train_test = os.path.join(abs_dir, 'tfidf.f')

model = joblib.load(train_model)
cv_test = joblib.load(train_cv)
tfidf_test = joblib.load(train_test)

# stanza.download('en')
nlp = stanza.Pipeline(lang='en', processors='tokenize,ner')

text = sys.argv[1]
#text = "Happy Christams Alice!"
# text = "good"
if text == '':
    print("Empty!")
else:
    # text = "Happy Christams Alice!"
    df = pd.DataFrame({"text":text},index=["0"])

    df['text'] = df['text'].str.lower()
    df['text'] = df['text'].apply(lambda string: ' '.join([word for word in string.split(' ') if not word.rstrip(' ').startswith('@')]))
    df['text'] = df['text'].apply(lambda string: ' '.join([word for word in string.split(' ') if not word.rstrip(' ').startswith('#')]))
    df['text'] = df['text'].apply(lambda string: ' '.join([word for word in string.split(' ') if not word.rstrip(' ').startswith('http')]))
    df['text'] = df['text'].apply(text_process)

    text_content = [' '.join(content) for content in df['text']]
    text_count = cv_test.transform(text_content)
    text_tfidf_matrix = tfidf_test.fit_transform(text_count)
                    
    pre = model.predict(text_tfidf_matrix)
    #if pre ==1:
    #    print("You have sensitive message, please anonymous.\n")
    doc = nlp(text)
    # print(doc.ents)
    if pre ==1 and doc.ents == []:
        print("You have sensitive message, please anonymous.\n")
    else:
        for ent in doc.ents:
            if pre == 1 and ent.type == 'PERSON':
                print("You may leak 'name' information. Please encryption.\n")
            if pre == 1 and ent.type == 'MONEY':
                print("You may leak 'money' information.  Please encryption.\n")
            if pre == 1 and ent.type == 'LOC':
                print("You may leak 'location' information.  Please encryption.\n")
            if pre == 1 and ent.type == 'ORG':
                print("You may leak 'organise' information.  Please encryption.\n")
        
