from bottle import Bottle, run, redirect, MakoTemplate
from beaker.middleware import SessionMiddleware
from bottle.ext.sqlite import Plugin as SQLitePlugin

from beaker_plugin import BeakerPlugin
from params_plugin import ParamsPlugin
from login_plugin import LoginPlugin

from webexceptions import WebUnauthorizedError

import logging

logger = logging.getLogger(__name__)


def login(db, session):
    username = session.get("username", None)
    userpass = session.get("userpass", None)
    # or check user info in db
    if username and userpass and username=="admin" and userpass=="password":
        return dict(username=username, userpass=userpass)
    else:
        return redirect("/")  # for login


app=Bottle()
app.install(SQLitePlugin(keyword="db", dbfile="test.db"))
app.install(BeakerPlugin(keyword="session"))
app.install(LoginPlugin(login_func=login, keyword="login", dbkeyword="db", sessionkeyword="session"))
app.install(ParamsPlugin())


mako = {"template_adapter": MakoTemplate}

#  parameters demo
#  curl http://localhost:8000/?hello=world
@app.get("/", template=("index.html", mako))
def get_index(hello=""):
    return dict(result=hello)


#  post parameters and session demo
@app.post("/")
def post_index(session, hello):
    session["hello"] = hello
    redirect("/session")


#  post json parameters demo
# curl -d '{"hello":"world"}' -H "content-type: application/json" http://localhost:8000/json
@app.post("/json", json_params=True)
def post_json(hello):
    return hello


#  session demo
@app.get("/session", template=("index.html", mako))
def get_session(session):
    return dict(result=session.get("hello", "no title"))


#  login demo
# curl -d "username=admin&userpass=password" http://localhost:8000/login
@app.post("/login")
def post_login(session, username, userpass):
    session["username"] = username
    session["userpass"] = userpass
    redirect("/admin")


#  require login
@app.get("/admin", template=("index.html", mako))
def get_admin(db, session, login):
    return dict(result=login["username"])


session_opts = {
        "session.type": "memory",
        "session.cookie_expires": 3600,
        "session.auto": True
        }


application = SessionMiddleware(app, session_opts)


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    run(application, host="127.0.0.1", port=8000, debug=True, reloader=True)
