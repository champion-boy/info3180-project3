"""
Flask Documentation:     http://flask.pocoo.org/docs/
Jinja2 Documentation:    http://jinja.pocoo.org/2/documentation/
Werkzeug Documentation:  http://werkzeug.pocoo.org/documentation/

This file creates your application.
"""

from app import app, db, lm, thumbnailer, emailscript
from app.models import User, Wishlist, Profile, items, Item
from app.forms import RegistrationForm, LoginForm, ShareWishlistForm, UserProfileForm, WishlistForm, ItemForm
from flask import render_template, request, redirect, url_for, flash, g, jsonify, abort, session
from flask.ext.login import login_user, logout_user, current_user, login_required
from datetime import datetime
from werkzeug import secure_filename
from app.forms import RegistrationForm, LoginForm, ShareWishlistForm, UserProfileForm
from flask.ext.wtf import Form 
from wtforms.validators import Required, Email
from wtforms.fields import TextField
from flask.ext.login import login_user, logout_user, current_user, login_required
from app import app, db, lm, oid
from app import oid, lm
from app.models import Myprofile, AuthToken
from werkzeug.datastructures import MultiDict


###
# Routing for your application.
###
class ProfileForm(Form):
     first_name = TextField('First Name', validators=[Required()])
     last_name = TextField('Last Name', validators=[Required()])

@app.route('/home')
def home():
    """Render website's home page."""
    if g.user.is_active:
        return render_template('home.html')
    return render_template('home.html')


    
@oid.loginhandler
@app.route('/api/login', methods=['GET', 'POST'])
"""Logs in user"""
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is not None and user.password_hash == form.password.data:
            login_user(user, form.remember_me.data)
            flash('Successfully logged in!')
            return redirect(request.args.get('next') or url_for('home'))
        flash('Invalid username or password.')
    return render_template('login.html', form=form)

    print app.config['OPENID_PROVIDERS']
    
    if form.validate_on_submit():
        
        session['remember_me'] = form.remember_me.data
        return oid.try_login(form.openid.data, ask_for=['username', 'password'])
        
    return render_template('login.html', 
                           title='Sign In',
                           form=form,
                           providers=app.config['OPENID_PROVIDERS'])
    
    
@app.route('/api/token')
def get_auth_token():
    token = g.user.generate_auth_token()
    return jsonify({ 'token': token.decode('ascii') })
    
    
@app.route('/api/user/:id/wishlist', methods=['POST'])
@login_required
def add_item(id):
    return render_template('login.html')
    
    
@app.route('/api/:id/wishlist', methods=['GET'])
def get_wishlist(id):
    return


@app.route('/api/thumbnail/process',methods=['POST'])
@login_required
def processThumbnail():
    """Get information from url"""
    url = request.json["url"]
    return jsonify(thumbnailer.get_data(url))


@app.route('/api/register', methods=['POST'])
def register():
	data = MultiDict(mapping=request.json)	
	inputs = RegistrationForm(data, csrf_enabled=False)
	
	if not inputs.validate():
		return transform(300, message="Invalid inputs")
	else:
		firstName = data.get('first_name')
		lastName = data.get('last_name')
		email = data.get('email')
		password = data.get('password')

		user = User(email, password, firstName, lastName)
		auth = AuthToken()

		user.tokens.append(auth)

		try:
			db.session.add(user)
			# db.session.add(auth)

			db.session.commit()
		except IntegrityError as e:
			return jsonify({"error": "email already taken"})

		response = auth.__repr__()
		response.update({
			'user_id': user.id,
			'first_name': user.first_name,
			'last_name': user.last_name
		})

		return jsonify(response)

    
@lm.user_loader
def load_user(user_id):
    return db.session.query(User).get(user_id)
    
@app.route('/logout/')
@login_required
def logout():
    """Logout a user"""
    logout_user()
    return render_template('home.html')

@app.route('/profile', methods=['POST','GET'])
"""Adds A New Profile"""
def profile_add():
    if request.method == 'POST' or request.method == 'GET' :
        first_name = request.form['first_name']
        last_name = request.form['last_name']

        # write the information to the database
        newprofile = Myprofile(first_name=first_name,
                               last_name=last_name)
        db.session.add(newprofile)
        db.session.commit()

        return "{} {} was added to the database".format(request.form['first_name'],
                                             request.form['last_name'])

    form = ProfileForm()
    return render_template('profile_add.html',
                           form=form)

@app.route('/profile/<id>', methods=['POST','GET'])
def profile_view(id):
    """View a profile"""
    user =user = User.query.filter(User.id == id).first()
    if request.headers.get('content-type') == 'application/json' or request.method == 'POST' or request.method == 'GET':
            return jsonify(userid=user.userid, username=user.username, image=user.image, sex=user.sex, age=user.age,\
                                          profile_added_on=user.profile_added_on)
            return jsonify(user.__repr__())
    return render_template('profile_view.html', user=user)
    


    
    
@app.route('/profiles',methods=["POST","GET"])
"""Returns List of Profiles"""
def profile_list():
    users = db.session.query(User).all()
    if request.method == "POST" or request.method == "GET" :
        list_of_user = map(lambda x:x.__repr__(), users)
        return jsonify({'users': list_of_user})
    return render_template('profile_list.html',
                            users=users)
    
    

###
# The functions below should be applicable to all Flask apps.
###

@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)

@app.before_request
def before_request():
    g.user = current_user
    
@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def assets(path):
	""" Respond with static files """
	return app.send_static_file(path)



"""ITEM ROUTES"""
@app.route('/items', methods=['GET', 'POST'])
def Item_list():
	collection = db.session.query(Item).all()
	list_of_item = map(lambda x:x__repr__(), collection)
	return jsonify({'items': list_of_item})

@app.route('/users/<id_user>/wishlists/<wishlist_name>/items/<item_no>', methods=['GET', 'POST'])
def get_wishlist_item_by_index(id_user, wishlist_name, item_no):
	wishlist = db.session.query(Wishlist).filter_by(name=wishlist_name, id_user=id_user).first()
	collection = db.session.query(Item).filter_by(wishlist_id=wishlist.id,).all()
	return jsonify({
		'item': collection[0]
	})
	item_list = map(lambda z:z__repr__(), collection)


@app.route('/users/<id_user>/wishlists/<wishlist_name>/items', methods=['GET', 'POST'])
def get_wishlist_items(id_user, wishlist_name):
	wishlist = db.session.query(Wishlist).filter_by(name=wishlist_name, user_id=user_id).first()
	collection= db.session.query(Item).filter_by(wishlist_id=wishlist.id,).all()
	list_of_items = map(lambda z:z__repr__(), collection)
	return jsonify({
		'items': list_of_items,
		'count': len(collection)
	})

@app.route('/users/<id_user>/wishlists/<wishlist_name>/items', methods=['POST'])
def save_wishlist_item(id_user, wishlist_name):
	token = request.headers.get('auth-token')
	data = MultiDict(mapping=request.json)
	inputs = ItemForm(data, csrf_enabled=False)

	if not inputs.validate():
		return jsonify({'error': 'invalid inputs'})

	wishlist = db.session.query(Wishlist).filter(id_user=id_user, name=wishlist_name).first()
	
	name = data['name']
	description = data['description']

	collection = Item(name, description=description)

	wishlist.items.append(collection)

	db.session.add(collection)
	db.session.commit()

	return jsonify(item.__repr__())
	return jsonify(item.__repr__())

# ==============================================================
# 						Wishlist Routes
# ==============================================================
@app.route('/users/<id_user>/wishlists/<wishlist_name>', methods=['GET'])
def get_wishlist_by_name(id_user, wishlist_name):
	wishlist = db.session.query(Wishlist).filter_by(name=wishlist_name, id_user=id_user).first()
	collection = db.session.query(Item).filter_by(wishlist_id=wishlist.id).all()
	list_of_item = map(lambda y:y.__repr__(), collection)
	
	return jsonify({
		'wishlist': wishlist.__repr__(),
		'items': list_of_item,
		'item_count': len(collection)
	})

@app.route('/users/<user_id>/wishlists', methods=['GET'])
def get_all_wishlist(id_user):
	wishlists = db.session.query(Wishlist).filter_by(id_user=id_user).all()
	wishlist_list = map(lambda y:y.__repr__(), wishlists)
	return jsonify({
		'wishlists': wishlist_list,
		'count': len(wishlists)
	})

@app.route('/api/users/<user_id>/wishlists', methods=['POST'])
def save_wishlist(user_id):
	token = request.headers.get('auth-token')

	user = db.session.query(User).filter_by(id=user_id).first()
	auth = db.session.query(AuthToken).filter_by(token=token).first()

	# print auth

	if auth.user_id != user.id:
		return jsonify({'error': 'token not found'})

	data = MultiDict(mapping=request.json)

	inputs = WishlistForm(data, csrf_enabled=False)

	if not inputs.validate():
		return jsonify({'error': 'missing required fields'})

	name = data['name']
	description = data['description']

	wishlist = Wishlist(name, description)

	user.wishlists.append(wishlist)

	db.session.add(wishlist)
	db.session.commit()

	return jsonify(wishlist.__repr__())

# Helpers
def extract_json(request, form=None):
	data = MultiDict(mapping=request.json)
	# add form input extraction here
	
	return data #, input


def transform(status, data=None, message=None):
	response = {'status': status}

	if data is not None:
		response['data'] = data
	if message is not None:
		response['message'] = message

	return jsonify(response)



@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0",port="8888")
