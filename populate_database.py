from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Category, Item
import json
import psycopg2

engine = create_engine('postgresql+psycopg2://catalog:catalog@localhost/catalog')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
data_session = DBSession()

Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)




category_json = json.loads(open('categories.json', 'r').read())

for e in category_json['categories']:
  category_input = Category( name=str(e['name']),
    id=str(e['id']),
    items = [])
  data_session.add(category_input)
  data_session.commit()

item_json = json.loads(open('items.json', 'r').read())

for i in item_json['items']:
	item_input = Item(
  	name=str(i['name']), 
  	id=str(i['id']), 
  	description=str(i['description']),
  	category_id = str(i['category_id']),
  	creator_email = str(i['creator_email'])
  )
	data_session.add(item_input)
	data_session.commit()
