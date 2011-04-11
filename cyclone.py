import sys
import os.path
import time
import logging
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.template
import tornado.httpclient

from tornado.options import define, options

define("port", default=8888, help="run on the given port", type=int)


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", MainHandler),
            (r"/updates", UpdatesHandler),
        ]
        settings = dict(
            static_path="static",
            cookie_secret="61oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo=",
            login_url="/login",
            xsrf_cookies=True,
        )
        tornado.web.Application.__init__(self, handlers, **settings)
        
        
class MainHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    def get(self):
        """Index page of test app."""
        self.render("templates/index.html")
        
        
class UpdatesHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    def post(self):
        """Call to update words, returns raw JSON."""
        
        http = tornado.httpclient.AsyncHTTPClient()
        
        # for specifying a search term
        # url = 'http://api.flickr.com/services/rest/?method=flickr.photos.search&format=json&api_key='+api_key+'&text=cat&per_page=2'        
        
        # for getting most recent
        api_key = sys.argv[1]
        url = 'http://api.flickr.com/services/rest/?method=flickr.photos.getRecent&format=json&nojsoncallback=1&api_key='+api_key+'&per_page=1'
        
        # try with NYT headlines?
        # url = 'http://api.nytimes.com/svc/news/v3/content/nyt/all/6.json?api-key='
        
        time.sleep(1)
        http.fetch(url, callback=self.on_response)

    def on_response(self, response):
        """Callback for GETing update of recent Wordnik words."""
        if response.error: raise tornado.web.HTTPError(500)
        if self.request.connection.stream.closed():
            return
        logging.info(response.body)
        
        self.finish(response.body)
        
        
def main():
    tornado.options.parse_command_line()
    app = Application()
    app.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()