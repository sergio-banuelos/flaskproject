from wtforms import Form, BooleanField, DateTimeField
from wtforms import TextAreaField, TextField
from wtforms.validators import Length, required

class AppointmentForm(Form):
    title = TextField('Title', [Length(max=255)])
    start = DateTimeField('Start', [required()])
    end = DateTimeField('End')
    allday = BooleanField('All Day')
    location = TextField('Location', [Length(max=255)])
    description = TextAreaField('Description')

if __name__ == "__main__":
    # Demonstration of a WTForms form by itself.
    form = AppointmentForm()
    print('Here is how a form field displays:')
    print(form.title.label)
    print(form.title)

    from werkzeug.datastructures import \
    ImmutableMultiDict as multidict
    data = multidict([('title', 'Hello, form!')])
    form = AppointmentForm(data)
    print('Here is validation...')
    print('Does it validate: {}'.format(form.validate()))
    print('There is an error attached to the field...')
    print('form.start.errors: {}'.format(form.start.errors))