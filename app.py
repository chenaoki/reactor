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

    db = GrafterDB("GrafterTest")
    seeds = db.getHotSeeds(10)
    for s in seeds:
        _content_seeds += markup_reaction(s)
    return render_template('hello.html', **locals() )

@application.route("/reaction/<str_id>")
def detail(str_id=None):
    _css = url_for('static', filename='style.css')
    _js_login = url_for('static', filename='login.js')
    _content_context = ""
    _content_react = ""
    _content_parents = ""
    if not (str_id is None):
        db = GrafterDB("GrafterTest")
        temp_r = db.getReaction( ObjectId(str_id) )
        if not (temp_r is None):
            chain = db.getReactionChain(temp_r)
            for pr in reversed(chain):
                _content_context += markup_reaction(pr)
            if temp_r.isSeed():
                for frid in temp_r.reactionIdList:
                    r = db.getReaction(frid)
                    _content_parents += markup_reaction(r)
            else:
                for frid in chain[1].reactionIdList:
                    if frid != ObjectId(str_id):
                        r = db.getReaction(frid)
                        _content_parents += markup_reaction(r)
                for frid in temp_r.reactionIdList:
                    r = db.getReaction(frid)
                    _content_react += markup_reaction(r)
            return render_template('reaction.html', **locals() )


if __name__ == "__main__":
    application.debug = True
    application.run()
