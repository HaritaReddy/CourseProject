import math
import sys
import time
import metapy
import pytoml
import json

import config

class Search:

    def load_ranker(self):
        return metapy.index.OkapiBM25(k1=1.524, k3=2.29)

    def get_relevant_courses(self, input_query, top_k):
        ranker = self.load_ranker()

        with open('search/config-search.toml', 'r') as fin:
            cfg_d = pytoml.load(fin)

        query_cfg = cfg_d['query-runner']

        idx = metapy.index.make_inverted_index('search/config-search.toml')

        query = metapy.index.Document()

        #print('Running course query')
        query.content(input_query.strip())
        #print('Successfully ran query.content')
        results = ranker.score(idx, query, top_k)
        #print('got results of {}'.format(len(results)))
        content_results = []
        for item in results:
            content_results.append(idx.metadata(item[0]).get('content'))
        #print('got content results of {}'.format(content_results))

        complete_results = []
        for item in content_results:
            link = item.split(' ')[-1]
            university = None 
            for key, value in config.domain_to_university.items():
                if key in link:
                    university = value[1]

            complete_results.append({'course_content': item, 'link': link, 'university': university})
        
        complete_results_dict = {}

        for i in range(0, len(complete_results)):
            complete_results_dict[i+1] = complete_results[i]

        return json.dumps(complete_results_dict)

if __name__ == '__main__':
    search = Search()
    print("Searching for courses")
    print(search.get_relevant_courses('spanish colonial rule', 5))