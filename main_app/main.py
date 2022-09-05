from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from .database import SessionLocal, engine
from . import schemas, models, crud

app = FastAPI()

def get_db():
   db = SessionLocal()
   try:
       yield db
   finally:
       db.close()

# @app.get("/group/{code}")
# def read_group(code: int, db: Session = Depends(get_db)):
#     try:
#         return {"status": "success", "users": crud.get_group_user(db, str(code))}
#     except:
#         return {"status": "error"}

# @app.post("/group")
# def make_group(group: schemas.GroupCreate, user: schemas.User, db: Session = Depends(get_db)):
#     try:
#         return {"status": "success", "data": crud.create_group(db, group, user)}
#     except:
#         return {"status": "error"}

# @app.post("/login")
# def login(user: schemas.UserCreate, db: Session = Depends(get_db)):
#     try:
#         return {"status": "success", "data": crud.create_user(db, user)}
#     except:
#         return {"status": "error"}

# @app.post("/group/{code}")
# def join_group(code:int, user: schemas.User, db:Session = Depends(get_db)):
#     try:
#         return {"status": "success", "data": crud.update_user_group(db, user, str(code))}
#     except:
#         return {"status": "error"}

# @app.get("/mission/{code}")
# def get_misson(code : int,  db:Session = Depends(get_db)):
#     try:
#         return {"status": "success", "mission": crud.get_group_mission(db, str(code).zfill(4))}
#     except:
#         return {"status": "error"}

# @app.post("/mission")
# def make_mission(mission: schemas.MissionCreate, db:Session = Depends(get_db)):
#     try:
#         return {"status": "success", "data": crud.create_mission(db, mission)}
#     except:
#         return {"status": "error"}

# @app.post("/manito/{code}")
# def post_manito(code: int, uid: schemas.UserCreate, db:Session = Depends(get_db)):
#     try:
#         return {"status" : "success", "data": crud.set_manito(db, uid, str(code).zfill(4))}
#     except:
#         return {"status": "error"}

# @app.get("/manito")
# def get_manito(uid : schemas.UserCreate, db: Session = Depends(get_db)):
#     try:
#         return {"status" : "success", "data": crud.get_manito(db, uid)}
#     except:
#         return {"status": "error"}

@app.get("/user/{uid}")
def get_user_info(uid:str, db: Session = Depends(get_db)):
    try:
        return crud.get_user_info(db, uid)
    except:
        return {}
    
@app.get("/user")
def get_user(uid:str, db:Session = Depends(get_db)):
    try:
        return crud.get_one_user(db, uid)
    except:
        return {}
    
@app.post("/user")
def post_user(user: schemas.User, db: Session = Depends(get_db)):
    try:
        return crud.create_user(db, user)
    except:
        return {"status": "err"}
    
@app.post("/group")
def post_group(group: schemas.Group, db: Session = Depends(get_db)):
    try:
        return crud.create_group(db, group)
    except:
        return {"status": "err"}
    
@app.post("/group/{code}")
def join_group(code: str, uid: str, db:Session = Depends(get_db)):
    try:
        return crud.join_group(db, code, uid)
    except:
        return {"status": "err"}

@app.get("/group/{code}")
def get_group_member(code: str, db : Session = Depends(get_db)):
    try:
        return crud.get_group_member(db, code)
    except:
        return {"status": "err"}

@app.post("/manito/{code}")
def set_manito(code:str, db: Session = Depends(get_db)):
    try:
        return crud.set_manito(db, code)
    except:
        return

@app.get("/manito/{code}")
def get_manito(code: str, db: Session = Depends(get_db)):
    try:
        return crud.get_manito(db, code)
    except:
        return {"status": "err"}

    
@app.post("/missionset")
def post_missionset(missionset: schemas.MissionSet, db: Session = Depends(get_db)):
    try:
        return crud.create_missionset(db, missionset)
    except:
        return {"status": "err"}
    
