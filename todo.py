import sqlite3
from bottle import route, run, debug, template, request

@route('/todo')
def todo_list():
    conn = sqlite3.connect('todo.db')
    c = conn.cursor()
    c.execute("SELECT id, task FROM todo WHERE status LIKE '1'")
    result = c.fetchall()
    c.close()
    return template('make_table', rows=result)

@route('/new', method='GET')
def get_new_item():
    print "IN ITEM GET"
    return template('new_task.tpl')

@route('/new', method='POST')
def post_new_item():
    print "IN ITEM POST"
    new = request.POST.get('task', '').strip()
    print new
    conn = sqlite3.connect('todo.db')
    c = conn.cursor()

    c.execute("INSERT INTO todo (task,status) VALUES (?,?)", (new,1))
    new_id = c.lastrowid

    conn.commit()
    c.close()

    return template('new_task_submitted', no=new_id)
 
@route('/edit/<no:int>', method='GET')
def get_edit(no):

    conn = sqlite3.connect('todo.db')
    c = conn.cursor()
    c.execute("SELECT task FROM todo WHERE id LIKE ?", (str(no)))
    cur_data = c.fetchone()

    return template('edit_task', old=cur_data, no=no)

@route('/edit/<no:int>', method='POST')
def post_edit(no):

    edit = request.POST.get('task','').strip()
    status = request.POST.get('status','').strip()

    if status == 'open':
        status = 1
    else:
        status = 0

    conn = sqlite3.connect('todo.db')
    c = conn.cursor()
    c.execute("UPDATE todo SET task = ?, status = ? WHERE id LIKE ?", (edit, status, no))
    conn.commit()

    return '<p>The item number %s was successfully updated</p>' % no


debug(True)
run(reloader=True)
