from fastapi import Depends, FastAPI, Request, Response
import requestDataModels
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import business_logic
import utils
import json

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

@app.middleware("http")
async def get_user_id_from_header(request: Request, call_next):
    sessionId = request.cookies.get('sessionid')
    print(sessionId)
    authResponse = business_logic.getUserFromSessionId(sessionId)
    if (authResponse != None and 'authenticated' in authResponse):
        request.state.isLoggedInUser = True
        request.state.userId = authResponse['userId']
    else: 
        request.state.isLoggedInUser = False
        request.state.userId = 0
    request.state.sessionId = sessionId
    response = await call_next(request)
    return response

@app.get("/")
async def HealthCheck():
    return {
        "message": "Yes Its Working !!"
    }


@app.post("/register")
async def Register(request: Request, response: Response):
    if (request.state.isLoggedInUser):
        return {
            "message": "Already Logged In"
        }
    body = await request.body()
    body = utils.convert_bytes_to_json(body)
    registerResp = business_logic.registerUser(body)
    return {
        'status': registerResp
    }

@app.post("/login")
async def Login(request: Request, response: Response):
    if (request.state.isLoggedInUser):
        return {
            "message": "Already Logged In"
        }
    request_body = await request.body()
    request_body = utils.convert_bytes_to_json(request_body)
    login_resp = business_logic.logUserIn(request_body)
    if ('error' in login_resp):
        return {
            "status": False,
            "error": login_resp
        }
    elif ('userId' in login_resp and 'sessionId' in login_resp):
        sessionId = login_resp["sessionId"]
        response.set_cookie(key="sessionid", value=sessionId)
        return {
         "status": True   
        } 
    return {
        "status": False
    }


@app.post("/logout")
async def Logout(request: Request, response:Response):
    if (request.state.isLoggedInUser):
        session_id = request.cookies.get('sessionId')
        business_logic.logout_user_with_session_id(session_id)
        return {
            'status': True
        }
    return {
            "status": False,
            "message": "Already Logged Out"
        }
    

@app.get("/myprofile")
async def home(request:Request, response: Response):
    if (request.state.isLoggedInUser):
        return {
            "message": "Already Logged In",
            "userId": request.state.userId
        }
