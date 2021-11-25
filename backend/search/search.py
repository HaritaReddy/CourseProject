import math
import sys
import time
import metapy
import pytoml
import json

from .config import domain_to_university

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
            for key, value in domain_to_university.items():
                if key in link:
                    university = value[1]

            complete_results.append({'course_content': item, 'link': link, 'university': university})
        
        #complete_results_dict = {}

        #for i in range(0, len(complete_results)):
        #    complete_results_dict[i+1] = complete_results[i]

        #return json.dumps(complete_results_dict)
        return complete_results

if __name__ == '__main__':
    search = Search()
    print("Searching for courses")
    print(search.get_relevant_courses('spanish colonial rule', 5))


'''
Attaching to backend-web-1
backend-web-1  | [2021-11-25 18:32:56 +0000] [1] [INFO] Starting gunicorn 20.1.0
backend-web-1  | [2021-11-25 18:32:56 +0000] [1] [INFO] Listening at: http://0.0.0.0:80 (1)
backend-web-1  | [2021-11-25 18:32:56 +0000] [1] [INFO] Using worker: sync
backend-web-1  | [2021-11-25 18:32:56 +0000] [10] [INFO] Booting worker with pid: 10
backend-web-1  | [2021-11-25 18:32:56 +0000] [10] [ERROR] Exception in worker process
backend-web-1  | Traceback (most recent call last):
backend-web-1  |   File "/usr/local/lib/python3.7/site-packages/gunicorn/arbiter.py", line 589, in spawn_worker
backend-web-1  |     worker.init_process()
backend-web-1  |   File "/usr/local/lib/python3.7/site-packages/gunicorn/workers/base.py", line 134, in init_process
backend-web-1  |     self.load_wsgi()
backend-web-1  |   File "/usr/local/lib/python3.7/site-packages/gunicorn/workers/base.py", line 146, in load_wsgi
backend-web-1  |     self.wsgi = self.app.wsgi()
backend-web-1  |   File "/usr/local/lib/python3.7/site-packages/gunicorn/app/base.py", line 67, in wsgi
backend-web-1  |     self.callable = self.load()
backend-web-1  |   File "/usr/local/lib/python3.7/site-packages/gunicorn/app/wsgiapp.py", line 58, in load
backend-web-1  |     return self.load_wsgiapp()
backend-web-1  |   File "/usr/local/lib/python3.7/site-packages/gunicorn/app/wsgiapp.py", line 48, in load_wsgiapp
backend-web-1  |     return util.import_app(self.app_uri)
backend-web-1  |   File "/usr/local/lib/python3.7/site-packages/gunicorn/util.py", line 359, in import_app
backend-web-1  |     mod = importlib.import_module(module)
backend-web-1  |   File "/usr/local/lib/python3.7/importlib/__init__.py", line 127, in import_module
backend-web-1  |     return _bootstrap._gcd_import(name[level:], package, level)
backend-web-1  |   File "<frozen importlib._bootstrap>", line 1006, in _gcd_import
backend-web-1  |   File "<frozen importlib._bootstrap>", line 983, in _find_and_load
backend-web-1  |   File "<frozen importlib._bootstrap>", line 967, in _find_and_load_unlocked
backend-web-1  |   File "<frozen importlib._bootstrap>", line 677, in _load_unlocked
backend-web-1  |   File "<frozen importlib._bootstrap_external>", line 728, in exec_module
backend-web-1  |   File "<frozen importlib._bootstrap>", line 219, in _call_with_frames_removed
backend-web-1  |   File "/code/falconapp.py", line 2, in <module>
backend-web-1  |     from search.search import get_relevant_docs
backend-web-1  |   File "/code/search/search.py", line 8, in <module>
backend-web-1  |     import config
backend-web-1  | ModuleNotFoundError: No module named 'config'

'''