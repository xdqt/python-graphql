from __main__ import db
from model.Models import *

class Database:
    def __init__(self) -> None:
        pass
    
    def insert(self,obj):
        try:
            db.session.add(obj)
            db.session.commit()
        except:
            db.session.rollback()
    
    
    def insertmany(self,values):
        try:
            db.session.add_all(values)
            db.session.commit()
        except:
            db.session.rollback()
    
        
    def query(self,obj,filter):
        return obj.query.filter(filter).first()
    
    
    def queryand(self,obj,filter):
        ...
