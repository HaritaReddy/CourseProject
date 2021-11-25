import falcon
from search.search import get_relevant_docs
from recommender.recommender import Recommender


class MainResource:
    def on_get(self, req, resp):
        resp.status = falcon.HTTP_200
        resp.content_type = 'text/html'
        with open('static/index.html', 'r') as f:
            resp.body = f.read()

class SearchResource:
    def on_get(self, req, resp):
        query = req.params["q"]
        number = int(req.params["k"])
        if number == '' or number is None:
            number = 10 # a default number of results to return
        print('Entered search function with query = {}'.format(query))
        if query == '':
            resp.text = []
        else:
            results = get_relevant_docs(query, number)
            #print('About to send results of {}'.format(results))
            resp.media = {'results': results}
            resp.status = falcon.HTTP_200

class ProgramResource:
    def on_get(self, req, resp):
        query = req.params["q"]
        program_recommender = Recommender()
        results = program_recommender.recommend_programs(['computer science', 'data mining', 'machine learning'])
        print('got recommender results = {}'.format(query))
        resp.text = results
        resp.status = falcon.HTTP_200



app = falcon.App(cors_enable=True)
searchResource = SearchResource()
mainResource = MainResource()
programResource = ProgramResource()
app.add_route('/search', searchResource)
app.add_route('/main', mainResource)
app.add_route('/recommend', programResource)
app.add_static_route('/', '/code/static')