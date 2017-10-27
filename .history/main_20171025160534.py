from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy 

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:blogz@localhost:8889/blogz'#mysql connection,how we will connect,user,user password,host,port#,database you want to connect to
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)#database object is now db
app.secret_key = 'ljksj3oi2hefjvsl'


class Blog(db.Model):#db has an object in it called Model

    id = db.Column(db.Integer, primary_key=True)#db type,type of key)#every class created to be stored in db will have an id
    title = db.Column(db.String(120))#max len))#tasks now stored in name instead of list
    body = db.Column(db.String(120))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))#
    #completed = db.Column(db.Boolean, default=False)
    
    def __init__(self, title, body, owner):
        self.title = title
        self.body = body
        self.owner = owner
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120))
    password = db.Column(db.String(120))
    blogs = db.relationship('Blog', backref='owner')
    
    def __init__(self,username,password):
        self.username = username
        self.password = password
        

@app.before_request#run this function before you run the request
def require_login(): #not a request handler, will run for every request to check and see if user has logged in
    allowed_routes = ['login',  'signup']#routes user don't have to login to see
    
    if request.endpoint not in allowed_routes and 'username' not in session:#not logged in yet,endpoint is the end route
        return redirect('/login')


@app.route('/login', methods=['POST','GET'])
def login ():
#    username_error = ''
#    password_error=''
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            session['username'] = username
            flash("Logged in")
            return redirect('/newpost')
        else:
            flash("User password incorrect, or User doesn't exist", "error")
#            if user.password != password:
#                password_error = "Incorrect Password"

#            if user != user:
#                user_error = "Incorrect Users"
    return render_template('login.html')



@app.route('/signup', methods=['POST','GET'])
def signup():
    username_error = ''
    password_error = ''
    verify_error = ''

    username_boolean = True
    password_boolean = True
    verify_boolean = True 
    exist_boolean = True
#    

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        verify = request.form['verify']
        
        existing_user = User.query.filter_by(username=username).first() 

    #if request.method == 'GET':
     #   blog_id = request.args.get('id')

      #  if blog_id:
            
       #     blogs = Blog.query.get(blog_id)
            #return redirect('/blogpost?id={0}'.format(blog.id))
        #    return render_template('blogpost.html', title="Blog Post!", blog= Blog.query.get(blog_id))
        
            
        #if existing_user == new_user:
         #   existing_error = flash('User exist','error')
          #  exist_boolean = False    
      
        if ' ' in username or len(username) < 3 or len(username) > 20:
            username_error = 'Invalid Username 3-20 Characters' 
            username = ''
            username_boolean = False
    
        if ' ' in password or len(password) <3 or len(password) > 20:
            password_error = 'Password 3-20 Length'
            password = ''
            password_boolean = False

        if verify != password :
            verify_error = 'Passwords must match'
            verify = ''
            verify_boolean = False  
            
        if username_boolean and password_boolean and verify_boolean and exist_boolean:
            new_user = User(username,password)
            
            if existing_user == new_user:
                flash('User exist','error')
                
            if not existing_user:     
                db.session.add(new_user)
                db.session.commit()
                session['username'] = username
                flash("New Post")
            return redirect('/newpost')
        else:
            flash("User Exist","error")        #flash("User name or Password not 3-20 characters or Passwords do not match","error")
    
    return render_template('signup.html',username_error=username_error,password_error=password_error, verify_error=verify_error)#, existing_error=existing_error)
    #return render_template('signup.html', username=username, username_boolean=username_boolean,verify_boolean=verify_boolean, 
     #       password=password,username_error=username_error, verify=verify)



@app.route('/logout')
def logout():
    del session['username']
    return redirect('/login')

@app.route('/blog', methods=['POST', 'GET'])
def blog():
    if request.method == 'GET':
        blog_id = request.args.get('id')

        if blog_id:
            
            blogs = Blog.query.get(blog_id)
            #return redirect('/blogpost?id={0}'.format(blog.id))
            return render_template('blogpost.html', title="Blog Post!", blog= Blog.query.get(blog_id))
            
        else:
            blogs = Blog.query.all()
            return render_template('main.html', title="Blog Post!", 
            blogs=blogs)

    else:#if incoming request is a post, todo submit
        title = request.form['title']#grab data and create new blog
        body = request.form['body']
        owner = User.query.filter_by(username=session['username']).first()
        new_post = Blog(title, body, owner)#creates new task object
        db.session.add(new_post)#input in to the data base
        db.session.commit()#commits change to database
    
        blogs = Blog.query.all()
        return render_template('main.html', title="Blog Post!", 
       blogs=blogs)#Pass the post into the template
    

@app.route('/newpost', methods=['POST', 'GET'])
def newpost():
    owner = User.query.filter_by(username=session['username']).first()
    
    title_error=""
    body_error=""

    if request.method == 'POST':#if incoming request is a post, todo submit
        title = request.form['title']#grab data and create new blog
        body = request.form['body']
        owner = User.query.filter_by(username=session['username']).first()
        new_post = Blog(title, body, owner)#creates new task object

    
        if title =="":
            title_error = "Please enter title"
        if body =="":
            body_error = "Please enter content"

        if not title_error and not body_error:
            db.session.add(new_post)#input in to the data base
            db.session.commit()
            id=new_post.id
            print(id)

            blogs = Blogs.query.filter_by(owner=owner).all()
            return redirect("/blog?id="+str(id))
        else:
            return render_template('post.html', title_error=title_error,body_error=body_error, title=title, body=body,blogs=blogs)
    else:
        return render_template('post.html', title="New Blog Post")

#request.args.get()

#    return render_template('todos.html')
@app.route('/')
def index():
    return redirect('/blog')


if __name__ == '__main__':#only start when using main.py from terminal
    app.run()