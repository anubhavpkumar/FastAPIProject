from SqliteUtil import SqliteUtil
import queries
from pymemcache.client import base
import json
from memCache import memCache 
import utils

def getUserFromSessionId(sessionId):
    if (sessionId != None):
        memcacheInstance = memCache()
        sessionResponse = memcacheInstance.getCache(sessionId)
        print((sessionResponse))
        if (sessionResponse == None):
            return {
                'authenticated': False,
                'userId': 0
            }
        respJson = json.loads(sessionResponse)
        return {
            'authenticated': True,
            'userId': respJson["userId"]
        }
    return None

def registerUser(body):
    if (body != None and 'emailAddress' in body and 'firstName' in body):
        sqlLiteUtils = SqliteUtil('kink.db')
        sqlLiteUtils.insertRowIntoTable('users', body)
        return True
    return False

def logUserIn(requestBody):
    if (requestBody != None and 'emailAddress' in requestBody and 'userpassword' in requestBody):
        sqlLiteUtils = SqliteUtil('kink.db')
        query = 'SELECT * FROM users WHERE emailAddress = \"' + requestBody["emailAddress"] + "\" AND userpassword = \"" + requestBody['userpassword'] + "\""
        dbResponse = sqlLiteUtils.executeQuery(query)
        if (len(dbResponse) > 0):
            sessionKey = utils.generateSessionId()
            userObject = {
                "userId": dbResponse[0][0]
            }
            memCacheInstance = memCache()
            memCacheInstance.setCache(sessionKey, userObject)
            return {
                "sessionId": sessionKey,
                "userId": dbResponse[0][0]
            }
        return {
            "error": 'User Not Found'
        }
    return {
        "error": 'Bad Request'
    }

def logout_user_with_session_id(session_id):
    if (session_id.length > 0):
        memCache.delete_key(session_id)