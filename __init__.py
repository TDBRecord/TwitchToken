class storage():
    def __init__(self):
        self.clientid = ""
        self.clientsecret = ""

class twitchlocal():
    def __init__(self, storage):
        self.storage = storage
        self.refresh = False
        pass
    
    def gettoken(self):
        from requests import post
        url = "https://id.twitch.tv/oauth2/token?client_id={clientid}&client_secret={clientsecret}&grant_type=client_credentials".format(clientid=storage.clientid,clientsecret=storage.clientsecret)
        rtn = post(url).json()
        rtn.update({"client_id": self.storage.clientid})
        return rtn

    def revoketoken(self, arg):
        from requests import post
        url = "https://id.twitch.tv/oauth2/revoke?client_id={clientid}&token={token}".format(clientid=arg["client_id"], token=arg["token"])
        rtn = post(url)
        try:
            return rtn.json()
        except:
            return {"status": 200}
    
    def refreshtoken(self, arg):
        if arg["client_id"] != storage.clientid: return {"status": 400, "line": "invalid client id"}
        rtn = self.revoketoken(arg)
        if  rtn["status"] != 200: return rtn
        else:
            rtn = self.gettoken()
            rtn.update({"mode": "refresh"})
            return rtn

from flask import app, Flask, render_template, request
from flask_compress import Compress
import json

compress = Compress()
app = Flask(__name__)
storage = storage()

@app.route('/gettoken', methods=['GET'])
def gettocken():
    return twitchlocal(storage).gettoken()

@app.route('/revoketoken', methods=['GET'])
def revoketocken():
    arg = request.args
    if "token" in arg:
        pass
    else: return {"status": 400, "line":"cannot find token"}

    if "client_id" in arg:
        pass
    else: return {"status": 400, "line":"cannot find clientid"}

    return twitchlocal(storage).revoketoken(arg)

@app.route('/refreshtoken', methods=['GET'])
def refreshtoken():
    arg = request.args
    if "token" in arg:
        pass
    else: return {"status": 400, "line":"cannot find token"}

    if "client_id" in arg:
        pass
    else: return {"status": 400, "line":"cannot find clientid"}

    return twitchlocal(storage).refreshtoken(arg)
