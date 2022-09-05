from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from .database import Base, engine

class User(Base):
    __tablename__ = "users"
    
    uid = Column(String(length=255), primary_key= True, index=True)
    name = Column(String(length=255))
    group = Column(String(length=255)) 
    manito = Column(String(length=5000))
    
    def __init__(self, uid, name, group, manito):
        self.uid = uid
        self.name = name
        self.group = group
        self.manito = manito

    def __repr__(self):
        return f"<User('{self.uid}', '{self.name}', '{self.group}', '{self.manito}')>"
    
class Group(Base):
    __tablename__ = "groups"
    
    code = Column(String(length=255), primary_key= True, index=True)
    name = Column(String(length=255))
    owner_uid = Column(String(length=255), ForeignKey("users.uid"))
    
    def __init__(self, code, name, owner_uid):
        self.code = code
        self.name = name
        self.owner_uid = owner_uid

    def __repr__(self):
        return f"<Group('{self.code}', '{self.name}', '{self.owner_uid}')>"
    
class Mission(Base):
    __tablename__ = "missions"
    
    uid = Column(String(length=255), primary_key=True)
    sets = Column(String(length=255), ForeignKey("missionsets.uid"))
    content = Column(String(length=255))
    users = Column(String(length=255))
    
    def __init__(self, uid, sets, content, users):
        self.uid = uid
        self.sets = sets
        self.content = content
        self.users = users

    def __repr__(self):
        return f"<Mission('{self.uid}', '{self.sets}', '{self.content}', '{self.users}')>"
    
class MissionSet(Base):
    __tablename__ = "missionsets"
    
    uid = Column(String(length=255), primary_key=True)
    groups = Column(String(length=255))
    missions = Column(String(length=255))
    
    def __init__(self, uid, groups, missions):
        self.uid = uid
        self.groups = groups
        self.missions = missions

    def __repr__(self):
        return f"<MissionSet('{self.uid}', '{self.groups}', '{self.missions}')>"
    
Base.metadata.create_all(bind=engine)