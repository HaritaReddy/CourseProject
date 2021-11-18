import falcon
from search.search import get_relevant_docs


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



app = falcon.App()
searchResource = SearchResource()
mainResource = MainResource()
app.add_route('/search', searchResource)
app.add_route('/main', mainResource)
app.add_static_route('/', '/code/static')