import math
import sys
import time
import metapy
import pytoml

import config


def load_ranker():
    return metapy.index.OkapiBM25(k1=1.524, k3=2.29)

def get_relevant_docs(input_query, top_k):
    ranker = load_ranker()

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
        
    return complete_results

if __name__ == '__main__':
    print(get_relevant_docs('spanish colonial rule', 5))

    """
    print('Building or loading index...')
    idx = metapy.index.make_inverted_index('config.toml')

    ranker = load_ranker()
    ev = metapy.index.IREval('config.toml')

    with open('config.toml', 'r') as fin:
        cfg_d = pytoml.load(fin)

    query_cfg = cfg_d['query-runner']

    start_time = time.time()
    top_k = 10
    query_path = query_cfg.get('query-path', 'queries.txt')
    query_start = query_cfg.get('query-id-start', 0)

    query = metapy.index.Document()
    ndcg = 0.0
    num_queries = 0

    print(idx.num_docs())
    print(idx.avg_doc_length())
    query = metapy.index.Document()
    query.content("african history")
    top_docs = ranker.score(idx, query, num_results=5)
    print(top_docs)
    for num, (d_id, _) in enumerate(top_docs):
        content = idx.metadata(d_id).get('content')
        print(content)

    print('Running sample queries')
    with open(query_path) as query_file:
        for query_num, line in enumerate(query_file):
            query.content(line.strip())
            results = ranker.score(idx, query, top_k)
            ndcg += ev.ndcg(results, query_start + query_num, top_k)
            num_queries+=1
    ndcg= ndcg / num_queries

    print("NDCG@{}: {}".format(top_k, ndcg))
    print("Elapsed: {} seconds".format(round(time.time() - start_time, 4)))
    
    
    #Testing on courses dataset
    
    ranker = load_ranker()
    #ev = metapy.index.IREval('config-search.toml')

    with open('config-search.toml', 'r') as fin:
        cfg_d = pytoml.load(fin)

    query_cfg = cfg_d['query-runner']

    start_time = time.time()
    top_k = 10
    query_path = query_cfg.get('query-path', 'queries.txt')
    query_start = query_cfg.get('query-id-start', 0)
    idx = metapy.index.make_inverted_index('config-search.toml')

    query = metapy.index.Document()
    ndcg = 0.0
    num_queries = 0

    print('Running course queries')
    with open(query_path) as query_file:
        for query_num, line in enumerate(query_file):
            query.content(line.strip())
            results = ranker.score(idx, query, top_k)
            print("Query:")
            print(line)
            print("Results:")
            for item in results:
                content = idx.metadata(item[0]).get('content')
                print(content)
            print('------------------------------------------------')
            #ndcg += ev.ndcg(results, query_start + query_num, top_k)
            #num_queries+=1
    #ndcg= ndcg / num_queries
    
    #print("NDCG@{}: {}".format(top_k, ndcg))
    #print("Elapsed: {} seconds".format(round(time.time() - start_time, 4)))
    """