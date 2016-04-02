"""
Flask Documentation:     http://flask.pocoo.org/docs/
Jinja2 Documentation:    http://jinja.pocoo.org/2/documentation/
Werkzeug Documentation:  http://werkzeug.pocoo.org/documentation/

This file creates your application.
"""

from app import app, db, lm, thumbnailer, emailscript
from app.models import User, Wishlist, Profile
from app.forms import RegistrationForm, LoginForm, ShareWishlistForm, UserProfileForm
from flask import render_template, request, redirect, url_for, flash, g, jsonify, abort
from flask.ext.login import login_user, logout_user, current_user, login_required
from datetime import datetime
from werkzeug import secure_filename


###
# Routing for your application.
###

@app.route('/')
def home():
    """Render website's home page."""
    if g.user.is_active:
        return render_template('home2.html')
    return render_template('home.html')


@app.route('/api/user/register', methods=['POST'])
def register():
    email=request.json.get('email')
    password=request.json.get('password')
    name=request.json.get('name')
    
    if email is None or password is None or name is None:
        abort(400)
    
    if db.session.query(User).filter_by(email=email).first() is not None:
        abort(400)
    
    user = User(email=email,password=password,name=name)
    db.session.add(user)
    db.session.commit()
    return jsonify({"error":None,"data":{"token":"","expires":"","user":{"_id":"","email":"","name":""}},"message":"Success"})        
    
    
@app.route('/api/user/login', methods=['POST'])
def login():
    return
    
    
@app.route('/api/token')
def get_auth_token():
    token = g.user.generate_auth_token()
    return jsonify({ 'token': token.decode('ascii') })
    
    
@app.route('/api/user/:id/wishlist', methods=['POST'])
@login_required
def add_item(id):
    return
    
    
@app.route('/api/user/:id/wishlist', methods=['GET'])
def get_wishlist(id):
    return


@app.route('/api/thumbnail/process',methods=['POST'])
@login_required
def processThumbnail():
    """Get information from url"""
    url = request.json["url"]
    return jsonify(thumbnailer.get_data(url))


@app.route('/signup/', methods=['GET', 'POST'])
def signup():
    """Render website's sign up page."""
    form = RegistrationForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            email       = request.form['email'].strip()
            password    = request.form['password'].strip()
            
            user = User(email=email, password=password)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('signin'))
    return render_template('signup.html', form=form)

@app.route('/signin/', methods=['GET', 'POST'])
def signin():
    """Login a user"""
    form = LoginForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            user = db.session.query(User).filter(User.email == form.email.data).first()
            if user is not None and user.verify_password(form.password.data):
                login_user(user, form.remember_me.data)
                return redirect(request.args.get('next') or url_for('wishlist'))
            flash('Invalid username or password.')
    return render_template('signin.html', form=form)
    
@lm.user_loader
def load_user(user_id):
    return db.session.query(User).get(user_id)
    
@app.route('/logout/')
@login_required
def logout():
    """Logout a user"""
    logout_user()
    return redirect(url_for('home'))

@app.route('/profile/', methods=['POST', 'GET'])
@login_required
def add_profile():
    """Add a profile"""
    userid  = g.user.get_id()
    form    = UserProfileForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            username    = request.form['username'].strip()
            firstname   = request.form['firstname'].strip()
            lastname    = request.form['lastname'].strip()
            sex         = request.form['sex']
            age         = request.form['age']
            image       = request.files['img']
            filename    = "{}-{}".format(userid,secure_filename(image.filename))
            filepath    = "app/static/uploads/{}".format(filename)
            image.save(filepath)
            
            profile     = Profile(username=username,userid=userid,firstname=firstname,lastname=lastname,image=filename,sex=sex,age=age,profile_added_on=datetime.now())
            db.session.add(profile)
            db.session.commit()

            return redirect(url_for('view_profile',userid=userid))
    user = db.session.query(Profile).filter(Profile.userid == userid).first()
    if user:
        return redirect(url_for('view_profile',userid=userid))
    else:
        return render_template('addProfile.html', form=form)    

@app.route('/profile/<int:userid>', methods=['POST','GET'])
def view_profile(userid):
    """View a profile"""
    user = db.session.query(Profile).filter(Profile.userid == userid).first()
    if not user:
        return render_template('404.html')
    else:
        if request.headers.get('content-type') == 'application/json' or request.method == 'POST':
            return jsonify(userid=user.userid, username=user.username, image=user.image, sex=user.sex, age=user.age,\
                          profile_added_on=user.profile_added_on)
        return render_template('profile.html', user=user)
    
    
@app.route('/profiles/', methods=['POST','GET'])
@login_required
def list_profiles():
    """View a list of profiles"""
    ulist   = []
    result  = db.session.query(Profile).all()
    for user in result:
        ulist.append({"username":user.username,"userid":user.userid})
    if request.headers.get('content-type') == 'application/json' or request.method == 'POST':
        return jsonify(users = ulist)
    return render_template('profiles.html',ulist=ulist)
    
    
@app.route('/wishlist/', methods=['GET','POST'])
@login_required
def wishlist():
    """View wishlist"""
    if request.method == 'POST':
        items = []
        wishlistItems = db.session.query(Wishlist).filter(Wishlist.userid == g.user.get_id()).all()
        for item in wishlistItems:
            items.append({"id":item.id,"itemUrl":item.itemUrl, "imgUrl":item.imgUrl, "title":item.title, "description":item.description})
        return jsonify(items=items)
    return render_template('wishlist.html')
    
@app.route('/wishlist/<int:userid>',methods=['GET'])
def user_wishlist(userid):
    """View wishlist"""
    items = []
    wishlistItems = db.session.query(Wishlist).filter(Wishlist.userid == int(userid)).all()
    for item in wishlistItems:
        items.append({"itemUrl":item.itemUrl, "imgUrl":item.imgUrl, "title":item.title, "description":item.description})
    return render_template('sharedWishlist.html', items=items)
    
@app.route('/wishlist/addtowishlist/',methods=['GET','POST'])
@login_required
def addtowishlist():
    """Add item to wishlist"""
    if request.method == 'POST':
        itemUrl = request.json['itemUrl']
        imgUrl = request.json['imgUrl']
        title = request.json['title']
        description = request.json['description']
        
        item = Wishlist(itemUrl=itemUrl, imgUrl=imgUrl, title=title, description=description, userid=g.user.get_id())
        db.session.add(item)
        db.session.commit()
        
        return jsonify({'StatusCode':'200','Message': 'Item successfully added'})
    return render_template('addItem.html')
    
    
@app.route('/wishlist/removefromwishlist/<int:itemid>', methods=['GET','POST'])
@login_required
def removefromwishlist(itemid):
    """Remove item from wishlist"""
    db.session.query(Wishlist).filter(Wishlist.id == itemid).delete()
    db.session.commit()
    return jsonify({"status":"ok"})
    
@app.route('/wishlist/edititem/<int:itemid>', methods=['GET','POST'])
@login_required
def edititem(itemid):
    """Edit item in wishlist"""
    item = db.session.query(Wishlist).filter(Wishlist.id == itemid).first()
    item.title = request.json['title']
    item.description=request.json['descript']
    db.session.commit()
    return jsonify({"status":"ok"})    
    

@app.route('/wishlist/share/', methods=['GET','POST'])
@login_required
def share():
    """email wishlist"""
    emails = []
    userid=g.user.get_id()
    user = db.session.query(User).filter(User.id == userid).first()
    form = ShareWishlistForm()
    if request.method == 'POST':
        print 'testing1'
        if form.validate_on_submit():
            print 'testing2'
            emails.append(request.form['email1'].strip())
            emails.append(request.form['email2'].strip())
            emails.append(request.form['email3'].strip())
            emails.append(request.form['email4'].strip())
            emails.append(request.form['email5'].strip())
            print emails
            for email in emails:
                print email
                if email:
                    
                    emailscript.sendemail("Friend",email,"{} just shared a wishlist!".format(user.firstname),"wishlist-tonitiffy-1.c9users.io/wishlist/{}".format(userid))
            return redirect(url_for('wishlist'))
            
    return render_template('share.html', form=form)
    

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


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0",port="8888")
