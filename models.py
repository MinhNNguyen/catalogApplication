from sqlalchemy import Column,Integer,String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine
from passlib.apps import custom_app_context as pwd_context
import random, string
from itsdangerous import(TimedJSONWebSignatureSerializer 
	as Serializer, BadSignature, SignatureExpired)


Base = declarative_base()
secret_key = ''.join(random.choice(string.ascii_uppercase + string.digits)
	for x in range(32))


class Category(Base):
	__tablename__ = 'category'

	id = Column(Integer, primary_key = True)
	name = Column(String(64), unique = True, nullable = False)

	items = relationship("Item", back_populates="category", cascade="save-update, merge, delete")

	@property
	def serialize(self):
		return {
			'name': self.name,
			'id': self.id,
			'items' : [r.serialize for r in self.items],
		}


class Item(Base):
	__tablename__ = 'item'
	id = Column(Integer, primary_key = True)
	name =  Column(String, unique = True, nullable = False)
	description = Column(String)
	category_id = Column(Integer, ForeignKey('category.id'))
	creator_email = Column(String)
	category = relationship("Category", back_populates = "items", cascade="save-update, merge, delete")

	
	def get_cat_name(self):
		return self.category.name

	@property
	def serialize(self):
		return {
			'name': self.name,
			'description': self.description,
			'id': self.id,
			'category_id': self.category_id,
			'creator_email': self.creator_email
		}


engine = create_engine('sqlite:///itemCatalog.db')

Base.metadata.create_all(engine)
