from flask import *
from flask_sqlalchemy import *
from flask_login import *

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.sqlite'
db = SQLAlchemy(app)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80),unique=True)
    password = db.Column(db.String(80))
    name = db.Column(db.String(30))
    age = db.Column(db.Integer)

class Posts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Integer, unique=False)
    post = db.Column(db.String(250))


app.config['SECRET_KEY'] = 'alksdifa;lksdif;alksdifa;lksdifa;lksdfj'
login_manager = LoginManager(app)
login_manager.init_app(app)

@login_manager.user_loader
def load_user(uid):
    user = User.query.filter_by(id=uid).first()
    return user

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user is not None and password == user.password:
            login_user(user)
            return redirect('/')
        else:
            return redirect('/login')

@app.route ('/secret')
def secret():
    loggedin = current_user.is_authenticated
    return render_template('secret.html',loggedin=loggedin)

@app. route ('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')

@app.route('/', methods=['GET', 'POST'])
def home():
    loggedin = current_user.is_authenticated
    if request.method == 'GET':
        return render_template('home.html', loggedin=loggedin)

@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'GET':
        return render_template('create.html')
    elif request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        name = request.form['name']
        age = request.form['age']
        if not User.query.filter_by(username=username).all():
            user = User(username=username, password=password, name=name, age=age)
            db.session.add(user)
            db.session.commit()
            login_user(user)
            return redirect('/')
        else:
            return redirect('/create')

@app.route('/view_all', methods=['GET', 'POST'])
@login_required
def view():
    if request.method == 'GET':
        loggedin = current_user.is_authenticated
        U = User.query.all()
        counter = 0
        for i in U:
            counter = counter + 1
        return render_template('view.html', users=U,total = counter,loggedin=loggedin)


@app.route('/update',methods = ['GET','POST'])
@login_required
def update():
    if request.method == 'GET':
        loggedin = current_user.is_authenticated
        return render_template('update.html', users=User.query.all(),loggedin=loggedin)
    elif request.method == 'POST':
        password = request.form['password']
        newpassword = request.form['newpassword']
        user = current_user
        if user.password == password:
            #user = User.query.filter_by(password=password).all()
            user.password = newpassword
            db.session.commit()
            return redirect('/')
        else:
            return redirect('/update')


@app.errorhandler(404)
@app.errorhandler(401)
def functionToRun(err):
    return render_template('errorpage.html', users=User.query.all(), err=err)

@app.route('/draft', methods=['GET','POST'])
@login_required
def draft():
    if request.method == 'GET':
        loggedin = current_user.is_authenticated
        return render_template('draft.html',loggedin=loggedin)
    elif request.method == 'POST':
        text = request.form['post']
        user = current_user
        username = user.username
        post = Posts(username=username, post=text)
        db.session.add(post)
        db.session.commit()
        return redirect('/')


@app.route('/chatroom', methods=['GET','POST'])
def chatroom():
    if request.method == 'GET':
        loggedin = current_user.is_authenticated
        P = Posts.query.all()
        U = User.query.all()
        P.reverse()
        U.reverse()
        return render_template('chatroom.html', posts=P,users=U,loggedin=loggedin)

@app.route('/profile', methods=['GET','POST'])
@login_required
def profile():

    if request.method == 'GET':
        loggedin = current_user.is_authenticated
        user = current_user
        username = user.username
        P = Posts.query.filter_by(username=username).all()
        P.reverse()
        return render_template('profile.html', posts=P, loggedin=loggedin)


@app.route('/delete/<id>',methods=['GET','POST'])
@login_required
def deletepost(id):
    if request.method == 'GET':
        currentpost = Posts.query.filter_by(id=id).first()
        db.session.delete(currentpost)
        db.session.commit()
        return redirect('/profile')

@app.route('/edit/<id>',methods=['GET','POST'])
@login_required
def editposts(id):
    if request.method == 'GET':
        loggedin = current_user.is_authenticated
        return render_template('editpost.html',posts=Posts.query.filter_by(id=id),loggedin=loggedin)

    elif request.method == 'POST':
        newpost = request.form['newpost']
        userpost = Posts.query.filter_by(id=id).first()
        userpost.post = newpost
        db.session.commit()
        return redirect('/profile')

@app.route('/Moderation', methods=['GET','POST'])
@login_required
def Mod():
    if request.method == 'GET':
        loggedin = current_user.is_authenticated
        user = current_user
        username = user.username
        if username == "admin":
            P = Posts.query.all()
            P.reverse()
            return render_template('Moderation.html', posts=P, loggedin=loggedin)
        else:
            return redirect('/')

if __name__ == '__main__':
  app.run(debug=True)
