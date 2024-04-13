from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, Boolean, SmallInteger, ForeignKey
from sqlalchemy.orm import relationship

Base = declarative_base()


class ConnectTap(Base):

    __tablename__ = 'ConnectTap'

    id = Column(Integer, primary_key=True)
    DocDate = Column(DateTime, nullable=False)
    Kpp = Column(String(10))
    FiasId = Column(String(50))
    Status = Column(Integer, nullable=False)
    Identity = Column(String(50))
    Error = Column(String(2000))
    OrgId = Column(Integer, nullable=False)
    Comment = Column(String(100))
    AfterDate = Column(DateTime)
    tap_spec = relationship("ConnectTapSpec")


class ConnectTapSpec(Base):

    __tablename__ = 'ConnectTapSpec'

    BaseId = Column(Integer, ForeignKey('ConnectTap.id'), primary_key=True)
    Mark = Column(String(100), primary_key=True)
    ExpDay = Column(Integer, nullable=False)


class Utms(Base):

    __tablename__ = 'Utms'

    Id = Column(Integer, primary_key=True)
    fsrarid = Column(String(50), nullable=False)
    UtmAddress = Column(String(100), nullable=False)
    Active = Column(Boolean, nullable=False)
    num = Column(SmallInteger, nullable=False)
    Comment = Column(String(100))


class ConnectTapLog(Base):
    __tablename__ = 'RinatConnectTapLog'

    id = Column(Integer, primary_key=True)
    DocDateSend = Column(DateTime, nullable=False)
    Status = Column(SmallInteger, nullable=False)
    Error = Column(String(2000))
