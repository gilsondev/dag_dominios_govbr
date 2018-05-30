from collections import OrderedDict

from sqlalchemy import Column, Integer, String, DateTime
from rows import fields

from dag_dominios_govbr.core.database import Base


DOMAIN_CSV_FIELDS = OrderedDict([
    ('domain', fields.TextField),
    ('document', fields.TextField),
    ('name', fields.TextField),
    ('state', fields.TextField),
    ('city', fields.TextField),
    ('zipcode', fields.TextField),
    ('created_at', fields.DatetimeField),
    ('updated_at', fields.DatetimeField),
    ('ticket', fields.TextField),
])


class Domain(Base):
    __tablename__ = 'domains'
    id = Column(Integer, primary_key=True)
    domain = Column(String(255), unique=True)
    document = Column(String(100))
    name = Column(String(255))
    state = Column(String(2))
    city = Column(String(80))
    zipcode = Column(String(10))
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    ticket = Column(String(10))
