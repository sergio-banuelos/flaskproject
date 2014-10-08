import doctest
from flask import Flask
from flask import url_for
from flask.ext.sqlalchemy import SQLAlchemy
from sched.models import Base
from flask import abort, jsonify, redirect, render_template
from sched.forms import AppointmentForm
from sched.models import Appointment

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sched.db'
# Use Flask-SQLAlchemy for its engine and session
# configuration. Load the extension, giving it the app object,
# and override its default Model class with the pure
# SQLAlchemy declarative Base class.
db = SQLAlchemy(app)
db.Model = Base

# ... skipping ahead. Keep previous code from app.py here.
@app.route('/appointments/create/', methods=['GET', 'POST'])
def appointment_create():
    """Provide HTML form to create a new appointment."""
    form = AppointmentForm(request.form)
    if request.method == 'POST' and form.validate():
        appt = Appointment()
        form.populate_obj(appt)
        db.session.add(appt)
        db.session.commit()
        # Success. Send user back to full appointment list.
        return redirect(url_for('appointment_list'))
    # Either first load or validation error at this point.
    return render_template('appointment/edit.html',
        form=form)

@app.route('/appointments/<int:appointment_id>/edit/',methods=['GET', 'POST'])
def appointment_edit(appointment_id):
    """Provide HTML form to edit a given appointment."""
    appt = db.session.query(Appointment).get(appointment_id)
    if appt is None:
        abort(404)
    form = AppointmentForm(request.form, appt)
    if request.method == 'POST' and form.validate():
        form.populate_obj(appt)
        db.session.commit()
        # Success. Send the user back to the detail view.
        return redirect(url_for('appointment_detail',appointment_id=appt.id))
    return render_template('appointment/edit.html',form=form)

@app.route('/string/')
def return_string():
        return 'Hello, world!'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/object/')
def return_object():
    headers = {'Content-Type': 'text/plain'}
    return make_response('Hello, world!', status=200,headers=headers)

@app.route('/tuple/')
def return_tuple():
    return 'Hello, world!', 200, {'Content-Type':'text/plain'}

@app.route('/appointments/')
def appointment_list():
    return 'Listing of all appointments we have.'

@app.route('/appointments/<int:appointment_id>/',endpoint='some_name')
def appointment_detail(appointment_id):
    """Provide HTML page with a given appointment."""
    # Query: get Appointment object by ID.
    appt = db.session.query(Appointment).get(appointment_id)
    if appt is None:
        # Abort with Not Found.
        abort(404)
    return render_template('appointment/detail.html',
        appt=appt)

@app.route(
    '/appointments/<int:appointment_id>/delete/',methods=['DELETE'])
def appointment_delete(appointment_id):
    raise NotImplementedError('DELETE')

if __name__ == "__main__":
    doctest.testmod()
    app.run('0.0.0.0', 5000)
