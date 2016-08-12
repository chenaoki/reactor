from flask import Flask
from flask import url_for
from flask import Markup
from flask import render_template

from GrafterDB import GrafterDB
from bson.objectid import ObjectId
from Reaction import *
from ReactionView import markup_reaction

application = Flask(__name__)

@application.route("/")
def hello():
    _css = url_for('static', filename='style.css')
    _js_login = url_for('static', filename='login.js')

    _content_seeds = ""
    _content_pros =""
    _content_cons = ""
    _content_neut = ""

    db = GrafterDB("GrafterTest")
    seeds = db.getHotSeeds(10)
    for s in seeds:
        _content_seeds += markup_reaction(s)
    for r_id in seeds[0].reactionIdList:
        r = db.getReaction(r_id)
        if r.evaluation == EVAL_PROS:
            _content_pros += markup_reaction(r)
        if r.evaluation == EVAL_CONS:
            _content_cons += markup_reaction(r)
        if r.evaluation == EVAL_NEUT:
            _content_neut += markup_reaction(r)

    return render_template('hello.html', **locals() )

@application.route("/reaction/<str_id>")
def detail(str_id=None):
    _css = url_for('static', filename='style.css')
    _js_login = url_for('static', filename='login.js')
    _content_context = ""
    _content_pros =""
    _content_cons = ""
    _content_info = ""
    if not (str_id is None):
        db = GrafterDB("GrafterTest")
        r = db.getReaction( ObjectId(str_id) )
        if not (r is None):
            chain = db.getReactionChain(r)
            chain.reverse()
            for pr in chain:
                _content_context += markup_reaction(pr)
            for frid in r.reactionIdList:
                r = db.getReaction(frid)
                print "r:", r.strFormat()
                if r.evaluation == EVAL_PROS:
                    _content_pros += markup_reaction(r)
                if r.evaluation == EVAL_CONS:
                    _content_cons += markup_reaction(r)
                if r.evaluation == EVAL_NEUT:
                    _content_info+= markup_reaction(r)
            return render_template('reaction.html', **locals() )


if __name__ == "__main__":
    application.debug = True
    application.run()