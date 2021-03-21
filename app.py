from flask import Flask, jsonify, render_template, request, url_for, redirect, session, abort, Response
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user 


from flask_wtf import Form
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired


#################### Instantiate APP ###################################

'''Application Factory'''
app = Flask(__name__)

app.config['SECRET_KEY'] = 'shhsecret'   #make this more random and secret, i recommend using os.urandom(50) 
#################### Authentication ####################################

# flask-login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


class LoginForm(Form):
    username = StringField('Your username', validators=[DataRequired()])
    password = PasswordField('Your password', validators=[DataRequired()])
    submit = SubmitField('Sign In')


# silly user model
class User(UserMixin):

    def __init__(self, username):

        self.id = username
        self.password = users_db[username]
        
    def __repr__(self):
        return "%s/%s" % ( self.id, self.password)
    
    def is_active(self):
        return True

#users database (used dictionary just as an example) 
users_db = { 'gullpavon':'password1'
            ,'jondoe': 'password2'
            ,'elonmusk' : 'passwordtesla'

}

# create users from our users database above     
users_activated = {User(key) for (key,value) in users_db.items()} 



  

# some protected url
@app.route('/protectedurl')
@login_required
def protectedurl_func():
    return Response("Hello World!")

 

# somewhere to login
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']        
        if (username, password) in users_db.items():
            login_user(User(username))
            return redirect(request.args.get("next"))
        else:
            return abort(401)
    else:
        return Response('''
        <form action="" method="post">
            <p><input type=text name=username>
            <p><input type=password name=password>
            <p><input type=submit value=Login>
        </form>
        ''')


# somewhere to logout
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return Response('<p>Logged out</p>')


# handle login failed
@app.errorhandler(401)
def page_not_found(e):
    return Response('<p>Login failed</p>')


# callback to reload the user object        
@login_manager.user_loader
def load_user(userid):
    return User(userid)
    
