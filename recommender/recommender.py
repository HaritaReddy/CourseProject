import spacy
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

file1 = open('programs.dat', 'r')
lines = file1.readlines()


for i in range(0, len(lines)):
    lines[i] = unicode(lines[i], "utf-8")

df = pd.DataFrame(lines, columns=['text'])
print(df)



def recommend(model, query_sentences, word_embedding_matrix, top_k):
    query_embed_1 = model(query_sentences[0])
    query_embed_2 = model(query_sentences[1])
    query_embed_3 = model(query_sentences[2])
    
    sim_score_mat = np.array([(query_embed_1.similarity(entry) + query_embed_2.similarity(entry) + query_embed_3.similarity(entry))/3.0 for entry in word_embedding_matrix])
    best_indices = np.argpartition(sim_score_mat, -top_k)[-top_k:]
    return best_indices


query_sentences = ['machine learning', 'computer science', 'scientific computing']
for i in range(0, len(query_sentences)):
    query_sentences[i] = unicode(query_sentences[i], "utf-8")


en_core_web_lg = spacy.load("en_core_web_lg") 
df['spacy_text'] = df['text'].apply(lambda x: en_core_web_lg(x)) 
word_embedding_matrix = df['spacy_text'].values

best_indices = recommend(en_core_web_lg, query_sentences, word_embedding_matrix, 5)
pd.set_option('display.max_colwidth', 1000)
print(df[['text']].iloc[best_indices])