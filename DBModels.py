from sqlalchemy import Column, Integer, String, Boolean, Date
from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

def get_engine(user, password, host, port, database):
    return create_engine('postgresql://{0}:{1}@{2}:{3}/{4}'.format(user, password, host, port, database))

def get_session():
    e = get_engine('artur', '1234', 'localhost', '5432', 'search_gkh')
    Base.metadata.create_all(e)
    Session = sessionmaker(bind=e)
    return Session()

def drop_bases():
    e = get_engine('artur', '1234', 'localhost', '5432', 'search_gkh')
    Base.metadata.drop_all(bind=e, tables=[SearchRequest.__table__, SearchResponse.__table__])

Base = declarative_base()

class SearchRequest(Base):
    __tablename__ = 'search_requests'

    id = Column(Integer, primary_key=True)
    KindPremises = Column(String)
    Adress_PostCode = Column(String)
    Adress_Region = Column(String)
    Adress_TypeCity = Column(String)
    Adress_City = Column(String)
    Adress_TypeStreet = Column(String)
    Adress_Street = Column(String)
    Adress_House = Column(String)
    Adress_Block = Column(String)
    Adress_Flat = Column(String)
    Adress = Column(String)
    is_searched = Column(Boolean, default=False)

    def __repr__(self):
        return "<SearchRequest(id='%s', Adress='%s', is_searched='%s')>" % (self.id, self.Adress, self.is_searched)

class SearchResponse(Base):
    __tablename__ = 'search_response'

    id = Column(Integer, primary_key=True)
    request_id = Column(Integer)
    exploit_year = Column(String)
    floor_num = Column(String)
    update_date = Column(Date)
    building_type = Column(String)
    house_type = Column(String)
    is_emergency = Column(Boolean)
    cadastral_num = Column(String)
    floor_type = Column(String)
    wall_material = Column(String)

    def __repr__(self):
        return "<SearchResponse(self_id='%s', request_id='%s', building_type='%s')>" % (self.id, self.request_id, self.building_type)
