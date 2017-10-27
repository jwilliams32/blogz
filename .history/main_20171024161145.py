from flask import Flask, request, redirect, render_template, session
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
    completed = db.Column(db.Boolean, default=False)

    def __init__(self, title, body):
        self.title = title
        self.body = body

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120))
    password = db.Column(db.String(120))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    
    def __init__(self,username,owner):
        self.username = username
        self.owner = owner

@app.route('/')
def index():
    return redirect('/blog')

@app.route('/signup')
def signup():

    username = request.form['username']
    password = request.form['password']
    verify = request.form['verify']

    return render_template('signup.html')
@app.route('/login')
def login ():
    user_error = ''
    password_error=''


    username = request.form['username']
    password = request.form['password']
    verify = request.form['verify']

    user = User.query.filter_by(username=username).first()

    if user.password != password:
        password_error = "Incorrect Password"

    if user != user:
        user_error = "Incorrect Users"

        return("hello")

    return redirect('/login')

@app.route('/logout', methods=['POST'])
def logout():
    return redirect('/blog')

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
        new_post = Blog(title, body)#creates new task object
        db.session.add(new_post)#input in to the data base
        db.session.commit()#commits change to database
    
        blogs = Blog.query.all()
        return render_template('main.html', title="Blog Post!", 
       blogs=blogs)#Pass the post into the template
    

@app.route('/newpost', methods=['POST', 'GET'])
def newpost():
    owner = User.query.filter_by(email=session['username']).first()
    
    title_error=""
    body_error=""

    if request.method == 'POST':#if incoming request is a post, todo submit
        title = request.form['title']#grab data and create new blog
        body = request.form['body']
        new_post = Blog(title, body)#creates new task object

        if title =="":
            title_error = "Please enter title"
        if body =="":
            body_error = "Please enter content"

        if not title_error and not body_error:
            db.session.add(new_post)#input in to the data base
            db.session.commit()
            id=new_post.id
            print(id)
            return redirect("/blog?id="+str(id))
        else:
            return render_template('post.html', title_error=title_error,body_error=body_error, title=title, body=body)
    else:
        return render_template('post.html', title="New Blog Post")

#request.args.get()

#    return render_template('todos.html')

if __name__ == '__main__':#only start when using main.py from terminal
    app.run()