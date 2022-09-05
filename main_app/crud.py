from random import randint
import string
from tokenize import group
from uuid import uuid4
from sqlalchemy.orm import Session

from . import models, schemas

# def get_group_user(db: Session, group_code: str):
#     return db.query(models.User).filter(models.User.code.like(f"%{group_code}%")).all()

# def get_group_mission(db: Session, group_code: str):
#     return db.query(models.Mission).filter(models.Mission.code == group_code).all()

# def create_user(db: Session, user: schemas.UserCreate):
#     db_user = models.User(uid = user.uid, name = user.name, age = user.age, code="")
#     db.add(db_user)
#     db.commit()
#     db.refresh(db_user)
#     return db_user

# def update_user_group(db: Session, user: schemas.User, new_code: str):
#     db_user = db.query(models.User).filter(user.uid == models.User.uid).first()
#     db_user.code =  db_user.code + (new_code).zfill(4) + ';' 
#     db.commit()
#     return db_user

# def create_mission(db: Session, mission: schemas.MissionCreate):
#     db_mission = models.Mission(code = mission.code, id = str(uuid4()), content = mission.content)
#     db.add(db_mission)
#     db.commit()
#     db.refresh(db_mission)
#     return db_mission

# def create_group(db: Session, group:schemas.GroupCreate, user: schemas.User):
#     code = str(randint(0, 9999)).zfill(4)
#     db_group = models.Group(code = code, name = group.name, owner_id = user.uid)
#     db.add(db_group)
#     db.commit()
#     db.refresh(db_group)
#     update_user_group(db, user, code)
#     return db_group

# def set_manito(db: Session, user:schemas.User, group_code: str):
#     data = db.query(models.User).filter(models.User.code.like(f"%{group_code}%")).filter(models.User.has_manito == False).all()
#     if len(data) == 0:
#         return "마니또를 설정할 멤버가 없어요"
#     uid = data[randint(0, len(data))].__dict__["uid"]
#     db_user = db.query(models.User).filter(user.uid == models.User.uid).first()
#     manito_user = db.query(models.User).filter(uid == models.User.uid).first()
#     db_user.manito = uid
#     manito_user.has_manito = True
#     db.commit()
#     return db_user

# def get_manito(db: Session, user:schemas.User):
#     data = db.query(models.User).filter(user.uid == models.User.uid).first()
#     if (data.manito == None):
#         return "마니또가 없어요"
#     return data.manito

def get_user_info(db:Session, uid:str):
    data = db.query(models.User).filter(uid == models.User.uid).first()
    groups = data.group.split(";")
    try:
        while True:
            groups.remove("")
    except ValueError:
        pass
    group_list = []
    for i in groups:
        group = db.query(models.Group).filter(models.Group.code == i).first()
        group_list.append({"name": group.name, "code": group.code, "owner": get_one_user(db, group.owner_uid)})
    try:
        while True:
            group_list.remove(None)
    except ValueError:
        pass
    missions = db.query(models.Mission).filter(models.Mission.users.like(f"%{uid}%")).all()
    return {"groups": group_list, "missions": missions, "user": get_one_user(db, uid)}

def get_one_user(db:Session, uid:str):
    return db.query(models.User).filter(uid == models.User.uid).first()

def create_group(db:Session, group:schemas.Group):
    try:
        ncode = str(len(db.query(models.Group).all())).zfill(4)
        db_group = models.Group(code = ncode, name = group.name, owner_uid= group.user_uid)
        db.add(db_group)
        user = db.query(models.User).filter(group.user_uid == models.User.uid).first()
        user.group = user.group + ncode + ";"
        db.commit()
        db.refresh(db_group)
        return db_group
    except:
        return {"status": "error"}
    
def join_group(db:Session, code:str, uid: str):
    try:
        if (db.query(models.Group).filter(code == models.Group.code).first() != None):
            db_user = db.query(models.User).filter(models.User.uid == uid).first()
            if (db_user in db.query(models.User).filter(models.User.group.like(f"%{code}%")).all()):
                return db_user
            db_user.group = db_user.group + code + ';'
            db.commit()
            db_user = db.query(models.User).filter(models.User.uid == uid).first()
            return db_user
        else:
            return {"status": "error"}
    except:
        return {"status": "error"}
    
def get_group_member(db: Session, code: str):
    datas = db.query(models.User).filter(models.User.group.like(f"%{code}%")).all()
    member_list = []
    for data in datas:
        groups = data.group.split(";")
        group_list = []
        for i in groups:
            group_list.append(db.query(models.Group).filter(models.Group.code == i).first())
        try:
            while True:
                group_list.remove(None)
        except ValueError:
            pass
        manitos = data.manito.split(";")
        manito_list = []
        try:
            while True:
                manitos.remove("")
        except ValueError:
            pass
        for i in manitos:
            x = i.split('|')
            manito_list.append({"group": x[0], "manito_uid": x[1]})
        try:
            while True:
                manito_list.remove(None)
        except ValueError:
            pass
        member_list.append({"name" : data.name, "group" : group_list, "manito": manito_list, "uid": data.uid})
    return {"members" : member_list}
    
        
def set_manito(db:Session, code:str):
    try:
        users = db.query(models.User).filter(models.User.group.like(f"%{code}%")).all()
        rand_list = [(i, users[i].__dict__["uid"] ,randint(1, 9999999)) for i in range(len(users))]
        rand_list.sort(key=lambda x:x[2], reverse=True)
        res = []
        if users:
            user_groups = users[0].manito.split(";")
            for user_group in user_groups:
                if (user_group.split("|")[0] == code):
                    return users
        for i in range(len(users)):
            user = db.query(models.User).filter(models.User.uid == rand_list[i][1]).first()
            user.manito = user.manito + code + "|" + rand_list[rand_list[i][0]][1] + ";"
            res.append(user)
        db.commit()
        print(res)
        return res
    except:
        return {"status": "error"}

def create_missionset(db: Session, missionset: schemas.MissionSet):
    try:
        sets = models.MissionSet(uid=missionset.uid, groups="", missions="")
        for i in missionset.missions:
            mission = models.Mission(uid=i.uid,sets=missionset.uid, content=i.content, users="")
            db.add(mission)
            sets.missions = sets.missions + mission.uid + ";"
            db.commit()
            db.refresh(mission)
        return sets
    except:
        return {"status": "error"}

def create_user(db: Session, user: schemas.User):
    try:
        db_user = models.User(uid=user.uid, name=user.name, group="", manito="")
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except:
        return
    
def get_manito(db:Session, code:str):
    try:
        return
    except:
        return