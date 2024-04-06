from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime 

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ToDo.db'
db = SQLAlchemy(app)

class ToDo(db.Model):
    Num = db.Column(db.Integer, primary_key=True)
    Title = db.Column(db.String(200), nullable=False) #nullable=False means that the column cannot be empty
    Description = db.Column(db.String(500), nullable=False)
    time = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"{self.Num} - Title: {self.Title} | Description: {self.Description} | Time: {self.time}"
    
    
@app.route('/', methods=['GET', 'POST'])
def hello_world():
    if request.method == 'POST':
       Ttilte= request.form['Title']
       Tdescription= request.form['Description']
       data = ToDo(Title=Ttilte, Description=Tdescription)
       db.session.add(data)
       db.session.commit()
       
    alltodo = ToDo.query.all()
    return render_template('index2.html', alltodo=alltodo)

@app.route('/delete/<int:Num>')
def delete(Num):
    todo = ToDo.query.filter_by(Num=Num).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect('/')

@app.route('/update/<int:Num>', methods=['GET', 'POST'])
def update(Num):
    if request.method == 'POST':
        todoTitle = request.form['Title']
        todoDescription = request.form['Description']
        
        data = ToDo.query.filter_by(Num=Num).first()
        data.Title = todoTitle
        data.Description = todoDescription
        
        db.session.add(data)
        db.session.commit()
        
        return redirect('/')
    
    todo = ToDo.query.filter_by(Num=Num).first()
    return render_template('update.html', todo=todo)
    
if __name__ == '__main__':
    app.run(debug=True)