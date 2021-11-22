import math
import sys
import time
import metapy
import pytoml

import config

class MOOCSearch:

    def load_ranker(self):
        return metapy.index.OkapiBM25(k1=1.524, k3=2.29)

    def get_relevant_moocs(self, input_query, top_k):
        ranker = self.load_ranker()

        with open('config-search-moocs.toml', 'r') as fin:
            cfg_d = pytoml.load(fin)

        query_cfg = cfg_d['query-runner']

        idx = metapy.index.make_inverted_index('config-search-moocs.toml')

        query = metapy.index.Document()
        query.content(input_query.strip())
        results = ranker.score(idx, query, top_k)
        content_results = []
        for item in results:
            content_results.append(idx.metadata(item[0]).get('content'))

        complete_results = []
        
        for item in content_results:
            link = item.split(' ')[-1]
            university = None 
            for key, value in config.domain_to_university.items():
                if key in link:
                    university = value[1]

            complete_results.append({'course_content': item, 'link': link, 'university': university})
        
        return complete_results

if __name__ == '__main__':
    search = MOOCSearch()
    print("Searching for MOOCs")
    print(search.get_relevant_moocs('business', 5))