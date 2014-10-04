from bottle import Bottle,route,run,debug,template,request
from bottle.ext import sqlalchemy
from sqlalchemy import Column,Boolean,String,Integer,create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

app=Bottle()

Base=declarative_base()
engine=create_engine('sqlite:////home/Gyandeep/projects/pro1/Bittu.db')
DBSession=sessionmaker(bind=engine)

plugin=sqlalchemy.Plugin(
       engine,
       Base.metadata,
       keyword='db',
       create=True,
       commit=True,
       use_kwargs=False)
app.install(plugin)

class TODO(Base):
 __tablename__ = 'Tasks'
 
 id = Column(Integer,primary_key=True)
 task = Column(String)
 status = Column(Boolean,unique=False,default=True)

 def __init__(self,task,status):
     self.task = task
     self.status = status

@route('/Tasks')
def TODO_list():
 session=DBSession()
 result=session.query(TODO).filter(TODO.status==1).all()
 return template('make_table',rows=result)

@route('/new', method='GET')
def get_new_item():
 print "IN ITEM GET"
 return template('new_task.tpl')

@route('/new', method='POST')
def post_new_item():
 print "IN ITEM POST"
 request.POST.get('save','').strip()
 task=request.POST.get('task', '').strip()
 status=1
 session=DBSession()
 new=TODO(task,status)
 session.add(new)
 session.commit()
 return template('new_task_submitted.tpl')

@route('/edit/<no:int>', method='GET')
def get_edit(no):
 session=DBSession()
 result=session.query(TODO).filter(TODO.id==no)
 return template('edit_task',old=result,no=no)

@route('/edit/<no:int>', method='POST')
def post_edit(no):
 session=DBSession()
 task=request.POST.get('task','').strip()
 status=request.POST.get('status','').strip()
 if status=='open':
  status=1
 else:
  status=0
 result=session.query(TODO).filter(TODO.id==no).first()
 result.task=task
 result.status=status
 session.commit()
 return '<p>The item number %s was successfully updated</p>' %no

debug(True)
run(reloader=True)
