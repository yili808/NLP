#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 27 11:59:03 2018

@author: yili
"""


from flask import Flask, render_template, request
app = Flask(__name__, static_folder='')

import numpy as np
from nltk import word_tokenize
from keras.models import load_model

vocab_fn = "GoogleNews_100K_vocab.txt"
with open(vocab_fn, 'r') as vfn:
    index2word = vfn.read().split('\n')
#print(len(index2word),"words in vocab")
mat_fn = "GoogleNews_100K.npy"
embedding_mat = np.load(mat_fn)
#print(embedding_mat.shape,"embedding matrix")

#add NULL (0) and UNK (1) to our vocab
lookup_with_unk = {word:i+2 for i,word in enumerate(index2word)}
UNK_IND = 1

#add null and UNK vectors to our embedding matrix so it still lines up
embeddings_with_unk = np.zeros((embedding_mat.shape[0]+2, embedding_mat.shape[1]))
embeddings_with_unk[2:] = embedding_mat






@app.route('/')
def index():
   return render_template('index.html')

@app.route('/sentence',methods = ['POST', 'GET'])
def sentence():
   if request.method == 'POST':
        sentence = request.form['sentence']
      
        sent = sentence.lower().replace("n't"," not")
        tokens = word_tokenize(sent)
        # remove punctuations
        tokens_a = [token for token in tokens if token.isalpha()]
        # look for id
        tokens_id = [lookup_with_unk[s] if s in lookup_with_unk else UNK_IND for s in tokens_a]
        
        
        #limit the length of a sentence
        sent_len = 30
        #initial the X_sample
        X_sample = np.zeros((0, sent_len), dtype=np.int32)

        # add 0s if the sentence is too short
        if len(tokens_id) < sent_len:
            tokens_id.extend([0]*(sent_len-len(tokens_id)))
        X_sample = np.r_[X_sample, np.asmatrix(tokens_id[0:sent_len])] #row cat
         
        #load the trained model
        model = load_model('my_model.h5')
        score = model.predict(X_sample)
        score.tolist()
        ###for i, result in enumerate(results):
        if score > 0.8:
            sentence = "Positive, the score is " '%.4f' % score #+ "\nThe sentence you input is:" + sent)
            #print(sentence)
            return render_template("sentence.html", sentence = sentence)
        elif score < 0.2:
            sentence = "Negative, the score is " '%.4f' % score  #+ "\nThe sentence you input is:" + sent)
            #print(sentence)
            return render_template("sentence.html", sentence = sentence)
        else:
            sentence = "Neutral, the score is " '%.4f' % score  #+ "\nThe sentence you input is:" + sent)
            #print(sentence)
            return render_template("sentence.html", sentence = sentence)
        
        
        
        #return render_template('index.html')


if __name__ == '__main__':
   app.run(debug = True)




####### input your test sentence below ########
#print("Please input a sequence of words (in English):")
#sent = input()



###for i, sent in enumerate(sample_sents):

    