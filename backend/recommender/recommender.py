import spacy
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import json


class Recommender:
    def __init__(self):
        """
        program_file = open('programs_v2.dat', 'r')
        lines = program_file.readlines()
        for i in range(0, len(lines)):
            lines[i] = unicode(lines[i], "utf-8")

        self.df = pd.DataFrame(lines, columns=['text'])
        print(self.df)
        """
        self.df = pd.read_csv("recommender/program_catalogs.tsv", sep='\t')
        #self.df['text'] = unicode(self.df['text'], "utf-8")
        #print(self.df)
        print("Initializing Recommender...")
        self.model = spacy.load("en_core_web_lg") 
        self.df['spacy_text'] = self.df['text'].apply(lambda x: self.model(x)) 
        self.word_embedding_matrix = self.df['spacy_text'].values
        print("Recommender finished initializing")


    def recommend(self, query_sentences, top_k):
        query_embed_1 = self.model(query_sentences[0])
        query_embed_2 = self.model(query_sentences[1])
        query_embed_3 = self.model(query_sentences[2])
    
        sim_score_mat = np.array([(query_embed_1.similarity(entry) + query_embed_2.similarity(entry) + query_embed_3.similarity(entry))/3.0 for entry in self.word_embedding_matrix])
        best_indices = np.argpartition(sim_score_mat, -top_k)[-top_k:]
        pd.set_option('display.max_colwidth', 1000)
        #print(self.df[['text']].iloc[best_indices])
        return self.df.iloc[best_indices]

    def recommend_programs(self, query_sentences=['computer science', 'data mining', 'machine learning']):
        best_rows = self.recommend(query_sentences, 3)
        idx = 1
        #return_dict = {}
        return_list = []
        for index, row in best_rows.iterrows():
            #return_dict[idx] = {'program_name': row['name'], 'university': row['university'], 'description': row['text'], 'link': row['link']}
            return_list.append({'id': index, 'program_name': row['name'], 'university': row['university'], 'description': row['text'], 'link': row['link']})
            #idx = idx + 1

        return json.dumps(return_list)
