from fastapi import FastAPI, Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from datetime import datetime, timedelta

app = FastAPI()

# JWT configuration
SECRET_KEY = "qwjkehkehqwk1837jhkde13dhq21093" # customeize secret key
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# create JWT token function
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes = ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp: expire"})
    encoded_jwt = jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )
    return encoded_jwt

# middleware to authenticate
@app.middleware("http")
async def jwt_authentication(request: Request, call_next):
    if request.url.path not in ["/token", "/open"]:
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Authorization header missing or invalid")
        
        token = auth_header.split(" ")[1]
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            request.state.user = payload # retain user's information in state request
        
        except JWTError:
            raise HTTPException(status_code=403, detail="Invalid token")
        
        response = await call_next(request)
        return response
    
# endpoint to get the token
@app.post("/token")
def login(username: str):
    # login simulation
    if username != "admin":
        raise HTTPException(status_code=401, detail="invalid credentials")
    access_token = create_access_token(data={"sub": username})
    return {"access_token": access_token, "token)type": "Bearer"}

# open endpoint, wihtout authentication
@app.get("/open")
def open_endpoint():
    return {"message": "This endpoint is open"}

# endpoint with authentication
@app.get("/secure")
def secure_endpoint(request: Request):
    user = request.state.user
    return {"message": f"welcome {user['sub']}, you have access to this endpoint"}