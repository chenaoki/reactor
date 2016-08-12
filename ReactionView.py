from flask import Markup
from Reaction import *

def markup_reaction(reaction):
    ret = ""
    d = reaction.getDictionary()

    ret += Markup("<div class=\"reactionBox\">")

    ret += Markup("<div class=\'iconImageBox\'>")
    ret += Markup("<img src=\"/static/images/GrafterLogo.jpeg\" width:\"100%\" height =\"100%\" >")
    ret += Markup("</div>")

    ret += Markup("<a href=\"/reaction/%s\">" % reaction._id)
    ret += Markup("<div class=\"reactionInfoBox\">")

    ret += Markup("<div class=\'userNameBox\'>")
    ret += Markup( d["author_name"] )
    ret += Markup("</div>")

    ret += Markup("<div class=\'reactionTimeBox\'>")
    ret += Markup( d["time"] )
    ret += Markup("</div>")

    ret += Markup("<p class=\'left_balloon\'>")
    if reaction.haveComment():
        ret += Markup(d["comment"])
    else:
        ret += Markup("(No comment)")
    ret += Markup("</p>")

    ret += Markup("<br class=\"clear_balloon\"/>")

    ret +=  Markup("</div>") # reactionInfoBox
    ret += Markup("</a>")

    ret +=  Markup("</div>") # reactionBox
    return ret

