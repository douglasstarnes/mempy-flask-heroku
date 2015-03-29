from flask import Flask, render_template, request, redirect
from mongoengine import connect, Document, StringField, IntField, BooleanField, DateTimeField
import os
import datetime

sort_icons = {
    'asc': 'arrow-up',
    'desc': 'arrow-down'
}

app = Flask(__name__)
app.debug = True

if os.getenv('MONGOLAB_URI') is not None: # on Heroku
    mongolab_uri = os.getenv('MONGOLAB_URI')
    db = mongolab_uri[mongolab_uri.rfind('/')+1:]
    connect(db, host=mongolab_uri)
else: # on Cloud9
    connect('mempydemo')
    

class TodoItem(Document):
    task = StringField()
    due_date = DateTimeField()
    priority = IntField()
    complete = BooleanField()
    
    def is_overdue(self):
        return self.due_date.date() < datetime.datetime.now().date()
        
    def days_till_due(self):
        delta = self.due_date.date() - datetime.datetime.now().date()
        return delta.days
        
    def compute_style(self):
        the_class = ''
        if self.priority > 5:
            the_class += ' hi-priority'
        if self.days_till_due() == 0:
            the_class += ' due-today'
        if self.is_overdue():
            the_class = ' overdue'
        
        return the_class
            
    
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        sort_by = 'due_date'
        direction = 'asc'
        
        if request.args.get('sort_by') is not None:
            sort_by = request.args.get('sort_by')
            
        if request.args.get('direction') is not None:
            direction = request.args.get('direction')
            
        query = '-' if direction == 'desc' else ''
        query += sort_by
        
        return render_template('index.html', todos=TodoItem.objects.order_by(query), sort_by=sort_by, direction=direction, sort_url=sort_url, sort_icon=sort_icon)
    elif request.method == 'POST':
        task = request.form['task']
        duedays = int(request.form['duedays'])
        priority = int(request.form['priority'])
        complete = False
        
        due_date = datetime.datetime.now() + datetime.timedelta(days=duedays)
        
        todo = TodoItem(task=task, 
                        due_date=due_date, 
                        priority=priority, 
                        complete=complete)
        todo.save()
        
        return redirect('/')
        
@app.route('/mark_complete')
def mark_complete():
    the_id = request.args.get('id')
    print(the_id)
    TodoItem.objects(id=the_id).update_one(set__complete=True)
    return redirect('/')
    
def sort_url(current, direction):
    return '/?sort_by={0}&direction={1}'.format(current, 'asc' if direction == 'desc' else 'desc')
    
def sort_icon(current, sort_by, direction):
    if current == sort_by:
        return '<i class="fa fa-{0}"></i>'.format(sort_icons[direction])
    return ''
    
if __name__ == '__main__':
    port = int(os.getenv('PORT', 8080))
    host = os.getenv('IP', '0.0.0.0')
    app.run(port=port, host=host)