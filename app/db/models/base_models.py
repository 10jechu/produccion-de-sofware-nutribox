from sqlalchemy.orm import declarative_mixin, declared_attr
from sqlalchemy import Integer
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

@declarative_mixin
class PKMixin:
    @declared_attr
    def id(cls):
        return mapped_column(Integer, primary_key=True, index=True)