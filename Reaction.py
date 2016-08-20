# Reaction.py
#--------------------------------------------------------#

from datetime import datetime
from bson.objectid import ObjectId

# Constants
RATE_HAVE_COMMENT = 1.2
RATE_HAVE_OPINION = 1.2
EVAL_PROS = 1
EVAL_CONS = -1
EVAL_NEUT = 0

class Reaction:

    def __init__( self, dict ):
        self.setDictionary(dict)

    def setDictionary(self, dict):
        self._id = dict['_id']
        self.author_id = dict['author_id']
        self.author_name = dict['author_name']
        self.target_id= dict['target_id']
        self.comment = dict['comment']
        self.evaluation = dict['evaluation']
        self.reactionFactor = dict['reactionFactor']
        self.time = datetime.now()
        if not dict['time'] is None:
            self.time = datetime.strptime(dict['time'], '%Y/%m/%d %H:%M:%S')
        self.reactionIdList = []
        reactions = dict['strReactionIdList'].split('_')
        if len(reactions) > 0:
            self.reactionIdList = [ObjectId(r_str) for r_str in reactions[1:]]

    def getDictionary(self):
        ret = {}
        ret['_id'] = self._id
        ret['author_id']  = self.author_id
        ret['author_name'] = self.author_name
        ret['target_id'] = self.target_id
        ret['comment'] = self.comment
        ret['evaluation'] = self.evaluation
        ret['reactionFactor'] = self.reactionFactor
        ret['time'] = self.time.strftime('%Y/%m/%d %H:%M:%S')
        ret['strReactionIdList'] =''
        for r_id in self.reactionIdList:
            ret['strReactionIdList'] += '_' + str(r_id)
        return ret

    def isSeed(self):
        if ( self.target_id is None ) and len(self.comment) != 0:
            return True
        else:
            return False

    def isCherry(self):
        if len(self.reactionIdList) == 0:
            return True
        else:
            return False

    def haveComment(self):
        if len(self.comment) >  0:
            return True
        else:
            return False

    def strFormat(self):
        return "%s(%s) >  \"%s\" @ %s (%s:%.2f)"  % (self.author_name, self.author_id,  self.comment, self.time.strftime('%Y/%m/%d %H:%M:%S'), self._id, self.reactionFactor)

