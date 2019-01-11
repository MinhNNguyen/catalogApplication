from models import Base, Category, Item
from flask import (Flask,
                   jsonify,
                   request,
                   url_for,
                   abort,
                   g,
                   render_template,
                   redirect,
                   session,
                   make_response,
                   flash)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
from flask_bootstrap import Bootstrap
import re, random, string, requests, json, httplib2
import psycopg2

# Global variables needed to run the application
engine = create_engine('postgresql+psycopg2://catalog:catalog@localhost/catalog')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
data_session = DBSession()
app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
CLIENT_ID = json.loads(
    open('/var/www/catalog/catalogApplication/client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Catalog Application"
Bootstrap(app)



# Create anti-forgery state token
@app.route('/login')
def login():
    state = ''.join(random.choice(string.ascii_uppercase 
      + string.digits) for x in xrange(32))
    session['state'] = state
    # return "The current session state is %s" % session['state']
    return render_template('login.html', STATE=state)

# Helper function being called to process google authentication
@app.route('/gconnect', methods=['POST'])
def gconnect():
  # Validate state token
  if request.args.get('state') != session['state']:
    response = make_response(json.dumps
      ('Invalid state parameter.'), 401)
    response.headers['Content-Type'] = 'application/json'
    return response
  # Obtain authorization code
  code = request.data

  try:
    # Upgrade the authorization code into a credentials object
    oauth_flow = flow_from_clientsecrets('/var/www/catalog/catalogApplication/client_secrets.json',
     scope='')
    oauth_flow.redirect_uri = 'postmessage'
    credentials = oauth_flow.step2_exchange(code)
  except FlowExchangeError:
    response = make_response(
      json.dumps('Failed to upgrade the authorization code.'), 401)
    response.headers['Content-Type'] = 'application/json'
    return response

  # Check that the access token is valid.
  access_token = credentials.access_token
  url = ('https://www.googleapis.com/oauth2/v1/' +
   'tokeninfo?access_token=%s' % access_token)
  h = httplib2.Http()
  result = json.loads(h.request(url, 'GET')[1])
  # If there was an error in the access token info, abort.
  if result.get('error') is not None:
    response = make_response(json.dumps(result.get('error')), 500)
    response.headers['Content-Type'] = 'application/json'
    return response

  # Verify that the access token is used for the intended user.
  gplus_id = credentials.id_token['sub']
  if result['user_id'] != gplus_id:
    response = make_response(
      json.dumps("Token's user ID doesn't match given user ID."),
       401)
    response.headers['Content-Type'] = 'application/json'
    return response

  # Verify that the access token is valid for this app.
  if result['issued_to'] != CLIENT_ID:
    response = make_response(
      json.dumps("Token's client ID does not match app's."), 401)
    print("Token's client ID does not match app's.")
    response.headers['Content-Type'] = 'application/json'
    return response

  stored_access_token = session.get('access_token')
  stored_gplus_id = session.get('gplus_id')
  if stored_access_token is not None and gplus_id == stored_gplus_id:
    response = make_response(json.dumps(
      'Current user is already connected.'), 200 )
    response.headers['Content-Type'] = 'application/json'
    return response

  # Store the access token in the session for later use.
  session['access_token'] = credentials.access_token
  session['gplus_id'] = gplus_id

  # Get user info
  userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
  params = {'access_token': credentials.access_token, 'alt': 'json'}
  answer = requests.get(userinfo_url, params=params)

  data = answer.json()
  print('Logging in:')
  # print(data['name'])
  print(data['email'])
  # session['username'] = data['name']
  session['picture'] = data['picture']
  session['email'] = data['email']
  print(data)
  output = ''
  output += '<h1>Welcome, '
  # output += session['username']
  output += '!</h1>'
  output += '<img src="'
  output += session['picture']
  output += ' " style = "width: 300px; height: 300px;border-radius: \
   150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
  flash("you are now logged in as %s" % session['email'])
  print("done!")
  return output


# DISCONNECT - Revoke a current user's token and reset their session
@app.route('/gdisconnect')
def gdisconnect():
  access_token = session.get('access_token')
  if access_token is None:
    print('Access Token is None')
    response = make_response(json.dumps
      ('Current user not connected.'), 401)
    response.headers['Content-Type'] = 'application/json'
    return response
  print('In gdisconnect access token is %s', access_token)
  print('User email is: ')
  print(session['email'])
  url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' \
    % session['access_token']
  h = httplib2.Http()
  result = h.request(url, 'GET')[0]
  print('result is ')
  print(result)
  if result['status'] == '200':
    del session['access_token']
    del session['gplus_id']
    del session['email']
    del session['picture']
    response = make_response(json.dumps
      ('Successfully disconnected.'), 200)
    response.headers['Content-Type'] = 'application/json'
    return response
  else:
    response = make_response(json.dumps
      ('Failed to revoke token for given user.', 400))
    response.headers['Content-Type'] = 'application/json'
    return response

# Display the home page
@app.route('/', methods = ['GET'])
def home_page():
  if 'email' in session:
    print(session['email'])
  categories = data_session.query(Category).all()
  items = data_session.query(Item).all()
  return render_template('home_page.html',
   categories = categories, items = items)


''' Display list of items belong to specific category
  @cat_name: unique name of the category '''
@app.route('/catalog/<string:cat_name>/items')
def category_page(cat_name):
  category = data_session.query(Category).filter_by \
    (name = cat_name).one_or_none()
  return render_template('category_page.html',
   items = category.items)


''' Display detail of each item, allow logged in user 
  to edit or delete item
  @item_name: unique name of the item
  @cat_name: unique name of the category
  @GET: display the detail item screen
  @POST: process update, delete, and extract JSON action ''' 
@app.route('/catalog/<string:cat_name>/<string:item_name>',
 methods = ['GET','POST'])
def item_page(cat_name, item_name):
  if request.method == 'POST':
    if request.form['action'] == 'Update':
      return redirect(url_for('edit_item', item_name = item_name))
    if request.form['action'] == 'Delete':
      return redirect(url_for('delete_item', item_name = item_name))
    if request.form['action'] == 'Extract JSON':
      return redirect(url_for('item_json_endpoint', item_name = item_name))
  item = data_session.query(Item).filter_by(name = item_name).one()
  return render_template('item_detail.html', item = item)


''' Display the form to add item and progress it if there is POST
  method requested
  @GET: process the add item request
  @POST: display the form for user to fill in the information
  of new item '''
@app.route('/add_item', methods=['GET', 'POST'])
def add_item():
  if request.method == 'POST':
    if not re.match("^[a-zA-Z0-9_]*$", request.form['name']) \
     or not re.match("^[a-zA-Z0-9_,\. ]*$",
      request.form['description']):
      print('Item name or description contains invalid \
       special character')
      return redirect(url_for('add_item'))
    newItem = Item()
    newItem.name = request.form['name']
    newItem.description = request.form['description']
    newItem.creator_email = session['email']
    cat = data_session.query(Category).filter_by \
    (name = request.form['cat']).one_or_none()
    cat.items.append(newItem)
    data_session.add(cat, newItem)
    data_session.commit()
    return redirect(url_for('home_page'))
  categories = data_session.query(Category).all()
  return render_template('add_item.html', categories = categories)


''' Display the form to edit item and progress it if there is POST
  method requested
  @item_name: unique name of the item
  @POST: process the edit item request
  @GET: display the form for user to fill in the information
  of edited item '''
@app.route('/catalog/<string:item_name>/edit',
 methods=['GET', 'POST'])
def edit_item(item_name):
  item = data_session.query(Item).filter_by(name = item_name) \
  .one_or_none()
  if request.method == 'POST':
    if session['email'] != item.creator_email:
      print('User is not authrozized to attempt this action')
      return redirect(url_for('home_page'))
    if not re.match("^[a-zA-Z0-9_]*$", request.form['name']) or not \
      re.match("^[a-zA-Z0-9_,\. ]*$", request.form['description']):
      print('Item name or description contains \
       invalid special character')
      return redirect(url_for('edit_item'), item_name = item_name)
    item.name = request.form['name']
    item.description = request.form['description']
    cat = data_session.query(Category).filter_by \
    (name = request.form['cat']).one_or_none()
    cat.items.append(item)
    data_session.add(cat, item)
    data_session.commit()
    return redirect(url_for('home_page'))
  categories = data_session.query(Category).all()
  return render_template('edit_item.html',
   categories = categories, item = item)


''' Confirm if the user wants to delete the item again and progress
  if there is POST request 
  @item_name: unique name of the item
  @POST: process the delete function request
  @GET: display the warning message and button to submit if user
  really want to delete the item '''
@app.route('/catalog/<string:item_name>/delete',
 methods=['GET', 'POST'])
def delete_item(item_name):
  item = data_session.query(Item).filter_by(name = item_name) \
  .one_or_none()
  if request.method == 'POST':
    if session['email'] != item.creator_email:
      print('User is not authrozized to attempt this action')
      return redirect(url_for('home_page'))
    data_session.delete(item)
    data_session.commit()
    return redirect(url_for('home_page'))
  return render_template('delete_item.html', item = item)


''' Generate the JSON for the whole categories of list of items
  belong to each of those'''
@app.route('/catalog/json') 
def json_endpoint():
  categories = data_session.query(Category).all()
  return jsonify(categories = [r.serialize for r in categories])

''' Generate the JSON for each item''' 
@app.route('/catalog/<string:item_name>/json')
def item_json_endpoint(item_name):
  item = data_session.query(Item).filter_by(name = item_name) \
  .one_or_none()
  return jsonify(item.serialize)

''' New home page template utlizing Flask-bootstrap library '''
@app.route('/new_homepage')
def new_homepage():
  return render_template('new_homepage.html')

if __name__ == '__main__':
  app.debug = True
  app.run()
