import falcon
from search.search import Search
from moocs.mooc_search import MOOCSearch
from recommender.recommender import Recommender
from wsgiref.simple_server import make_server


mainSearch = Search()
moocSearch = MOOCSearch()
program_recommender = Recommender()

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
            results = mainSearch.get_relevant_courses(query, number)
            #print('About to send results of {}'.format(results))
            #resp.media = {'results': results}
            resp.media = results
            resp.status = falcon.HTTP_200

class MoocResource:
    def on_get(self, req, resp):
        query = req.params["q"]
        number = int(req.params["k"])
        if number == '' or number is None:
            number = 10 # a default number of results to return
        print('Entered search function with query = {}'.format(query))
        if query == '':
            resp.text = []
        else:
            results = moocSearch.get_relevant_moocs(query, number)
            #print('About to send results of {}'.format(results))
            #resp.media = {'results': results}
            resp.media = results
            resp.status = falcon.HTTP_200

class ProgramResource:
    def on_get(self, req, resp):
        query1 = str(req.params["q1"])
        query2 = str(req.params["q2"])
        query3 = str(req.params["q3"])

        results = program_recommender.recommend_programs([query1, query2, query3])
        #print('got recommender results = {}'.format(query))
        resp.text = results
        resp.status = falcon.HTTP_200



app = falcon.App(cors_enable=True)
searchResource = SearchResource()
moocResource = MoocResource()
mainResource = MainResource()
programResource = ProgramResource()
app.add_route('/search', searchResource)
app.add_route('/mooc', moocResource)
app.add_route('/main', mainResource)
app.add_route('/recommend', programResource)
app.add_static_route('/', '/code/static')

if __name__ == '__main__':
    with make_server('', 80, app) as httpd:
        print('Server ready. Open your browser to http://localhost/main to get started')

        # Serve until process is killed
        httpd.serve_forever()