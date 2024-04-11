import datetime
from sqlalchemy import MetaData, Column, Integer, String, ForeignKey, Float, Date
from sqlalchemy.sql import func
from sqlalchemy.types import DateTime
from sqlalchemy.orm import declarative_base, relationship

# Определяем схему в базе Oracle, чтобы пользователь не supermag выполнял запросы.
metadata_obj = MetaData(schema="SUPERMAG")
# определить базовый класс для моделей SQLAlchemy
Base = declarative_base(metadata=metadata_obj)


# определяем класс для таблицы SMCARD
class SMCard(Base):
    # указываем имя таблицы
    __tablename__ = "SMCARD"

    # определяем столбцы таблицы с соответствующими типами данных и ограничениями
    article = Column(String, primary_key=True)  # используем article как первичный ключ
    globalarticle = Column(String)
    arrivedfrom = Column(Integer)
    bornin = Column(String)
    name = Column(String)
    shortname = Column(String)
    idmeasurement = Column(Integer)
    idclass = Column(Integer)
    idscale = Column(Integer)
    subarticle = Column(String)
    accepted = Column(Integer)
    datatype = Column(Integer)
    datasubtype = Column(Integer)
    scaleload = Column(Integer)
    cashload = Column(Integer)
    receiptok = Column(Integer)
    storage = Column(Integer)
    deadline = Column(Integer)
    losses = Column(Integer)
    scrap = Column(Integer)
    waste = Column(Integer)
    mesname = Column(String)
    mesabbrev = Column(String)
    country = Column(String)
    cardcomment = Column(String)
    flags = Column(Integer)
    cutpricedays = Column(Integer)
    supplypricepercentp = Column(Integer)
    supplypricepercentm = Column(Integer)
    minprofit = Column(Integer)
    idthreetorg = Column(Integer)
    idonetorg = Column(Integer)
    idspiritcode = Column(Integer)
    idmarketinggroup = Column(Integer)
    idlossesgroup = Column(Integer)
    quantitydeviation = Column(Integer)
    usetime = Column(Integer)
    usetimedim = Column(Integer)
    weight = Column(Integer)
    idmeasweight = Column(Integer)
    width = Column(Integer)
    length = Column(Integer)
    height = Column(Integer)
    idmeasdim = Column(Integer)
    stateregulation = Column(Integer)
    icing = Column(Integer)
    altname1 = Column(String)
    altname2 = Column(String)
    nominalvalue = Column(String)
    idcodetnved = Column(String)
    proteins = Column(String)
    fats = Column(String)
    carbs = Column(String)
    calories = Column(String)
    idpersonalprotection = Column(String)
    idokpd2 = Column(String)

    # определяем отношение один-ко-многим с таблицей SMSTOREUNITS
    store_units = relationship("SMStoreUnits", back_populates="card")

    # определяем класс для таблицы SMSTOREUNITS


class SMStoreUnits(Base):
    # указываем имя таблицы
    __tablename__ = "SMSTOREUNITS"

    # определяем столбцы таблицы с соответствующими типами данных и ограничениями
    barcode = Column(String, primary_key=True)  # используем barcode как первичный ключ
    barcodetype = Column(Integer)
    unitname = Column(String)
    # указываем, что article ссылается на article в таблице SMCARD
    article = Column(String, ForeignKey("SMCARD.article"))
    quantity = Column(Integer)
    facequantity = Column(Integer)
    flags = Column(Integer)
    subarticle = Column(String)
    boxid = Column(String)
    nestedbar = Column(String)
    weight = Column(String)
    tareweight = Column(String)
    tarewidth = Column(String)
    tarelength = Column(String)
    tareheight = Column(String)
    maxy = Column(String)
    packid = Column(String)

    # определяем отношение многие-к-одному с таблицей SMCARD
    card = relationship("SMCard", back_populates="store_units")


class SACardClass(Base):
    __tablename__ = 'SACARDCLASS'

    id = Column(Integer, primary_key=True, nullable=False, default=-1)
    tree = Column(String(100), nullable=False)
    name = Column(String(255), nullable=False)
    flags = Column(Integer, nullable=False, default=0)
    creator = Column(Integer, nullable=False, default=-2)
    normtree = Column(String(80), nullable=False)


class SMClientInfo(Base):
    __tablename__ = 'SMCLIENTINFO'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    accepted = Column(Integer, default=0, nullable=False)
    inn = Column(String(20))
    kpp = Column(String(9))
    gln = Column(String(13))
    commentary = Column(String(255))


class SMDocuments(Base):
    __tablename__ = 'SMDOCUMENTS'

    DOCTYPE = Column(String(2), primary_key=True, nullable=False)
    ID = Column(String(50), nullable=False)
    BORNIN = Column(String(16), nullable=False)
    CREATEDAT = Column(DateTime, nullable=False, default=datetime.datetime.now)
    DOCSTATE = Column(Integer, nullable=False)
    OPCODE = Column(Integer, nullable=False)
    USEROP = Column(Integer)
    CLIENTINDEX = Column(Integer)
    LOCATIONFROM = Column(Integer)
    LOCATIONTO = Column(Integer)
    LOCATION = Column(Integer)
    CURRENCYTYPE = Column(Integer, nullable=False)
    CURRENCYRATE = Column(Float)
    CURRENCYMULTORDER = Column(Integer, nullable=False, default=0)
    TOTALSUM = Column(Float)
    TOTALSUMCUR = Column(Float)
    PRICEROUNDMODE = Column(Integer, nullable=False)
    ISROUBLES = Column(String(1), nullable=False, default='1')
    COMMENTARY = Column(String)


class SADocDefaults(Base):
    __tablename__ = 'SADOCDEFAULTS'

    doctype = Column(String(2), primary_key=True, nullable=False)
    location = Column(Integer, primary_key=True, nullable=False)
    nameprefix = Column(String(10))
    nameoutprefix = Column(String(10))
    numbersize = Column(Integer, nullable=False)
    pricekind = Column(Integer)


class SMStoreLocations(Base):
    __tablename__ = 'SMSTORELOCATIONS'

    ID = Column(Integer, primary_key=True, nullable=False)
    NAME = Column(String(255), nullable=False)
    IDCLASS = Column(Integer, nullable=False)
    ACCEPTED = Column(String(1), nullable=False)
    PRTY = Column(Integer, nullable=False)
    FLAGS = Column(Integer, nullable=False)
    LOCTYPE = Column(Integer, nullable=False)
    PARENTLOC = Column(Integer)
    RGNID = Column(Integer, default=-1, nullable=False)
    ADDRESS = Column(String(255))
    TEL = Column(String(40))
    FAX = Column(String(40))
    COMMENTARY = Column(String(255))
    ORDERALG = Column(String(255), default='*', nullable=False)
    CARDTYPE = Column(Integer)
    FORMATID = Column(Integer)
    PRICINGMETHOD = Column(Integer, default=0, nullable=False)
    SUGGESTORDERALG = Column(String(50), default='EFFECTIVE', nullable=False)
    FLOORSPACE = Column(Float)
    GLN = Column(String(13))
    SHORTNAME = Column(String(255))
    SPOILAGELOC = Column(Integer)
    CLOSEDEDITDATE = Column(DateTime)
    KPP = Column(String(9))
    CLOSEDEDITDOCID = Column(String(50))
    CLOSEDEDITDATEOLD = Column(DateTime)
    CLOSEDEDITDOCIDOLD = Column(String(50))


class SMSpecor(Base):
    __tablename__ = 'SMSPECOR'

    DOCTYPE = Column(String(2), primary_key=True, nullable=False)
    DOCID = Column(String(50), primary_key=True, nullable=False)
    SPECITEM = Column(Integer, primary_key=True, nullable=False)
    DISPLAYITEM = Column(Integer, primary_key=True, nullable=False)
    ARTICLE = Column(String(50), nullable=False)
    QUANTITY = Column(Float)
    SUGGESTQUANTITY = Column(Float)
    ITEMPRICE = Column(Float)
    TOTALPRICE = Column(Float)
    ITEMPRICECUR = Column(Float)
    TOTALPRICECUR = Column(Float)


class SMPostQueue(Base):
    __tablename__ = 'SMPOSTQUEUE'

    ENQTIME = Column(Date, default=func.current_date(), nullable=False)
    # ENQTIME = Column(DateTime, nullable=False, default=func.now())
    ENQSEQ = Column(Integer, primary_key=True, nullable=False)
    TARGET = Column(Integer)
    OBJTYPE = Column(String(2), nullable=False)
    OBJID = Column(String(150), nullable=False)
    PARAMINT = Column(Integer)
    PARAMSTR = Column(String(4000))
    TRANSFLAGS = Column(Integer, nullable=False, default=0)
    COMMENTARY = Column(String(255))


class SMPostLocMap(Base):
    __tablename__ = 'SMPOSTLOCMAP'

    STORELOC = Column(Integer, primary_key=True)
    DBASEID = Column(Integer)
