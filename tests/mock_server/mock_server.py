from web import application
from web import ctx
from web.contrib.template import render_mako
import json


urls = ('/user-agent', 'UserAgent',
        '/', 'Home')

app = application(urls, globals())


class UserAgent:
    def GET(self):
        return json.dumps({'user-agent': ctx.env['HTTP_USER_AGENT']})


class Home:
    def GET(self):
        render = render_mako(directories=['templates/'])
        return render.python()


if __name__ == "__main__":
    app.run()
