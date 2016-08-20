from pymongo import Connection
from bson.objectid import ObjectId
from datetime import datetime
from math import log
from Reaction import *
from copy import deepcopy

class GrafterDB:

    def __init__(self, db_name):
        con = Connection("localhost")

        # con.drop_database(db_name)         # for test

        self.db =  con[db_name]

    def checkUser(self, name, password):
        users = self.db.userlist.find({"name":name, "password" : password})
        if users.count() is 1:
            return users[0]['_id'] # objid
        else:
            return None

    def addUser(self, name, password):
        if not self.checkUser(name, password) is None:
            return None
        else:
            objid = self.db.userlist.insert({"name":name, "password" : password})
            return objid

    def getReaction(self, reaction_id):
        reactions = self.db.allReactionList.find({"_id":reaction_id})
        if reactions.count() is 1:
            d = reactions[0]
            r = Reaction( d )
            r.author_name = self.db.userlist.find({"_id":r.author_id})[0]["name"]
            return r
        else:
            return None

    def saveReaction(self, reaction):
        reactions = self.db.allReactionList.find({"_id":reaction._id})
        if reactions.count() is 1:
            self.db.allReactionList.save( reaction.getDictionary() )

    def updateReactionFactor(self, reaction):
        if reaction.isCherry():
            weight = 1.0
            if reaction.haveComment():
                weight *= RATE_HAVE_COMMENT
            if reaction.evaluation != EVAL_NEUT:
                weight *= RATE_HAVE_OPINION
            reaction.reactionFactor = weight
        else:
            # reaction factor algorithm
            sumup = 0.0
            for r_id in reaction.reactionIdList:
                r = self.getReaction( r_id )
                weight = 1.0
                if r.haveComment():
                    weight *= RATE_HAVE_COMMENT
                if r.evaluation != EVAL_NEUT:
                    weight *= RATE_HAVE_OPINION
                sumup = r.reactionFactor*weight
            reaction.reactionFactor += sumup
        self.saveReaction(reaction)

    def backChainConnection(self, reaction):
        chain = [reaction]
        tmp_r = reaction
        self.updateReactionFactor( tmp_r )
        while True:
            target_r = self.getReaction( tmp_r.target_id )
            if not target_r is None:
                target_r.reactionIdList.append( tmp_r._id )
                self.updateReactionFactor( target_r )
                chain.append( deepcopy(target_r) )
                tmp_r = chain[-1]
            else:
                break
        return chain

    def getReactionChain(self, reaction):
        chain = [reaction]
        tmp_r = reaction
        while True:
            target_r = self.getReaction( tmp_r.target_id )
            if not target_r is None:
                chain.append( deepcopy(target_r) )
                tmp_r = chain[-1]
            else:
                break
        return chain

    def addReaction(self, reaction):
        users = self.db.userlist.find({"_id":reaction.author_id})
        if users.count() is 1:
            reaction.author_name = users[0]['name']
            reaction.time = datetime.now()
            d = reaction.getDictionary()
            d.pop("_id")
            objid = self.db.allReactionList.insert( d )
            reaction._id = objid
            self.backChainConnection(reaction)
        return reaction._id

    def getHotSeeds(self, maxN):
        seeds_dict = list(self.db.allReactionList.find({"target_id":None}))
        seeds_dict = sorted(seeds_dict, key=lambda s: s["time"])
        seeds = [ self.getReaction(s["_id"]) for s in seeds_dict ]
        return seeds[:maxN]
