from flask import Flask, render_template, redirect,url_for,session
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required
import pymongo
from bson import ObjectId
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField,EmailField,RadioField,URLField,IntegerField,TextAreaField
from wtforms.validators import DataRequired


app = Flask(__name__)
app.config['SECRET_KEY'] = 'sdfgeujkfh@nfjsduifdhe3^%$fhjsdfdsjf#$%#$rjkhjvhhdvdfhnjdmfldsjfsefjsif%^$^%#^%#$%#$fdkhkjfsaioudhyusjdisoadsdisadasdsdk'

#database

x='mongodb+srv://theaimcreator:archit123@database1.lnveyjh.mongodb.net/?retryWrites=true&w=majority'
client= pymongo.MongoClient(x)
db=client['rudrakash']

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

# Replace this with your actual user data storage mechanism (e.g., a database)
login_data = {'rudrakshaimthecreator@atc': {'password': 'Rudrakshatc123'}}
class User(UserMixin):
    def __init__(self, user_id):
        self.user_id = user_id

    def get_id(self):
        return str(self.user_id)

    @staticmethod
    def get(user_id):
        if user_id in login_data:
            return User(user_id)
        return None

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

#########################################################################
#                               ROUTE                                   #
#########################################################################

class LoginForm(FlaskForm):
    email=EmailField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class Add(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    sub_title=StringField('Sub-Title')
    dis = TextAreaField('description', validators=[DataRequired()], render_kw={"placeholder": "description", "rows": "5" })
    Image_link = URLField('Image Link', validators=[DataRequired()])
    Video_link = URLField('Video Link')
    submit = SubmitField('Add')

class Add_Products(FlaskForm):
    radio = RadioField('Select an categories', choices=['ppcp','pp'], validators=[DataRequired()])
    title = StringField('Title', validators=[DataRequired()])
    dis = StringField('Discription', validators=[DataRequired()])
    Image_link = URLField('Image Link', validators=[DataRequired()])
    submit = SubmitField('Add')

class Contact(FlaskForm):
    name = StringField('Name',validators=[DataRequired()],render_kw={"placeholder": "Your Name"})
    phone_no = IntegerField('Name',validators=[DataRequired()],render_kw={"placeholder": "Contact Number"}) 

    email=EmailField('Email', validators=[DataRequired()],render_kw={"placeholder": "Your Email"})
    Subject = StringField('Subject', validators=[DataRequired()],render_kw={"placeholder": "Subject"})
    message = TextAreaField('Message', validators=[DataRequired()], render_kw={"placeholder": "Message", "rows": "7"})
    submit = SubmitField('Submit')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.get(form.email.data)
        
        if user and (form.password.data==login_data[form.email.data]['password']):
            login_user(user)
            return redirect(url_for('dashboard'))
    return render_template('login.html', form=form)

@app.route('/dashboard')
@login_required
def dashboard():
    blogs_list=db.blog.find()  
    culture_list=db.cluture.find()  
 
    product_list_ppcp=db.other.find_one({'name':'ppcp'})
    product_list_pp=db.other.find_one({'name':'pp'})
    
    return render_template('dashboard.html',data=blogs_list,d2=product_list_ppcp,d3=product_list_pp,culture_list=culture_list)

@app.route('/add_blog',methods=['POST',"GET"])
@login_required
def Add_blog():
    form=Add()
    date = datetime.now().strftime("%d/%m/%y")
    if form.validate_on_submit():
        if not form.sub_title.data:
            subtitle=' '
        else:
            subtitle= form.sub_title.data
        if not form.Video_link.data:
            Video_link='NO'
        else:
            Video_link= form.Video_link.data
        data={'title':form.title.data,'sub-title':subtitle,'dic':form.dis.data,'Image_link':form.Image_link.data,' Video_link':Video_link,'date':date}
        db.blog.insert_one(data)
        return redirect(url_for('dashboard'))
    return render_template('add.html',form=form)

@app.route('/add_culture',methods=['POST',"GET"])
@login_required
def add_culture():
    form=Add()
    date = datetime.now().strftime("%d/%m/%y")
    if form.validate_on_submit():
        if not form.sub_title.data:
            subtitle=' '
        else:
            subtitle= form.sub_title.data
        if not form.Video_link.data:
            Video_link='NO'
        else:
            Video_link= form.Video_link.data
        data={'title':form.title.data,'sub-title':subtitle,'dic':form.dis.data,'Image_link':form.Image_link.data,' Video_link':Video_link,'date':date}
        db.cluture.insert_one(data)
        return redirect(url_for('dashboard'))
    return render_template('add.html',form=form)


@app.route('/del/product/<value>/<value2>',methods=['POST',"GET"])
@login_required
def blog_del(value,value2):
    if value2 == 'ppcp':
        db.other.update_one({'name': 'all'}, {'$pull': {'data_list': {'title': value}}})
        db.other.update_one({'name': 'ppcp'}, {'$pull': {'data_list': {'title': value}}})
    elif value2 == 'pp':
        db.other.update_one({'name': 'all'}, {'$pull': {'data_list': {'title': value}}})
        db.other.update_one({'name': 'pp'}, {'$pull': {'data_list': {'title': value}}})   
    return redirect(url_for('dashboard'))

@app.route('/blog/del/<value>',methods=['POST',"GET"])
@login_required
def Add_blog_del(value):
    document_id = ObjectId(value)
    db.blog.delete_one({'_id': document_id})
    return redirect (url_for('dashboard'))

@app.route('/culture/del/<value>',methods=['POST',"GET"])
@login_required
def del_culture(value):
    document_id = ObjectId(value)
    db.cluture.delete_one({'_id': document_id})
    return redirect (url_for('dashboard'))


@app.route('/add_Product',methods=['POST',"GET"])
@login_required
def Add_Product():
    form=Add_Products()
    if form.validate_on_submit():
        data={'title':form.title.data,'dic':form.dis.data,'Image_link':form.Image_link.data}
        if not db.other.find_one({'name':form.radio.data}):
             db.other.insert_one({'name':form.radio.data,'data_list':[]})
        if not db.other.find_one({'name':'all'}):
             db.other.insert_one({'name':'all','data_list':[]})       
        db.other.update_one({'name':form.radio.data},{"$push":{'data_list':data}})    
         
        return redirect(url_for('dashboard'))
    return render_template('add_product.html',form=form)

@app.route('/', methods=['GET', 'POST'])
def index():
    blog_Data=list(db.blog.find())[0:3]
    form=Contact()   
    if db.other.find_one({'name':'ppcp'}):
        ppcp=(db.other.find_one({'name':'ppcp'}))['data_list']
    else:
        ppcp=[]

    if db.other.find_one({'name':'pp'}):
        pp=(db.other.find_one({'name':'pp'}))['data_list']
    else:
        pp=[]
    # print(ppcp)
    if form.validate_on_submit():
        date = datetime.now().strftime("%d/%m/%y")
        data={'name':form.name.data,'phone':form.phone_no.data,'email':form.email.data,'Subject':form.Subject.data,'message':form.message.data,'date':date}
        db.contact.insert_one(data)
        return redirect (url_for('suc'))
    if session.get('message'):
        session.pop('message')
        return render_template('index.html',form=form,m="Submitted Successfully",blog_Data=blog_Data,pp=pp,ppcp=ppcp)
    else:
        return render_template('index.html',form=form,blog_Data=blog_Data,pp=pp,ppcp=ppcp)

@app.route('/suc', methods=['GET', 'POST'])
def suc():
    session['message']=True
    return redirect (url_for('index'))

@app.route('/view_contact')
@login_required
def view_contact():
    x=db.contact.find()
    return render_template('view_contact.html',records=x)

@app.route('/blog')
def blog():
    type='blog'  
    name="Blog"
    blog_Data=list(db.blog.find())
    return render_template('blog.html',blog_Data=blog_Data,name=name,type=type)

@app.route('/blog/<value>')
def blog_read(value):
    blog_Data=list(db.blog.find())[0:5]
    blog_Data.reverse()
    type='blog'  
    
    listi=db.blog.find_one({'_id':ObjectId(value)})    
    return render_template('blog_det.html',list=listi,blog_Data=blog_Data,type=type)

@app.route('/Rudrax-culture')
def Rudraxculture():  
    type='Rudrax-culture'
    name="Rudrax Culture"
    
    blog_Data=list(db.cluture.find())
    return render_template('blog.html',blog_Data=blog_Data,name=name,type=type)

@app.route('/Rudrax-culture/<value>')
def Rudraxculture_read(value):
    blog_Data=list(db.cluture.find())[0:5]
    blog_Data.reverse()
    listi=db.cluture.find_one({'_id':ObjectId(value)})    
    type='Rudrax-culture'  
    
    return render_template('blog_det.html',list=listi,blog_Data=blog_Data,type=type)


@app.route('/journey')
def journy():
    return render_template('journey.html')




@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')



if __name__ == '__main__':
    app.run(debug=True)
