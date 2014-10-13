"""Custom filters for Jinja templating. Load with init_app function."""

from jinja2 import Markup, evalcontextfilter, escape


def init_app(app):
    """Initialize a Flask application with filters defined in this module."""
    app.jinja_env.filters['date'] = do_date
    app.jinja_env.filters['datetime'] = do_datetime
    app.jinja_env.filters['duration'] = do_duration

    # The nl2br filter uses the Jinja environment's context to determine
    # whether to autoescape
    app.jinja_env.filters['nl2br'] = evalcontextfilter(do_nl2br)


def do_datetime(dt, format=None):
    """
    Jinja template filter to format a datetime object with date & time.
    >>> do_datetime(None)
    ''

    >>> do_datetime(datetime(2012, 10, 17, 22, 00, 00))
    '2012-10-17 - Wednesday at 10:00pm'

    >>> do_datetime(None, datetime(2012, 10, 17, 22, 00, 00))
    ''

    >>> do_datetime(None, None)
    ''

    >>> do_datetime(datetime(2012, 10, 17, 22, 00, 00), None)
    '2012-10-17 - Wednesday at 10:00pm'
    """
    if dt is None:
        # By default, render an empty string.
        return ''
    if format is None:
        # No format is given in the template call. Use a default format.
        #
        # Format time in its own strftime call in order to:
        # 1. Left-strip leading 0 in hour display.
        # 2. Use 'am' and 'pm' (lower case) instead of 'AM' and 'PM'.
        formatted_date = dt.strftime('%Y-%m-%d - %A')
        formatted_time = dt.strftime('%I:%M%p').lstrip('0').lower()
        formatted = '%s at %s' % (formatted_date, formatted_time)
    else:
        formatted = dt.strftime(format)
    return formatted


def do_date(dt, format='%Y-%m-%d - %A'):
    """Jinja template filter to format a datetime object with date only.
    >>> do_date(None)
    ''
    >>> do_date(datetime(2012, 10, 17, 22, 00, 00))
    '2012-10-17 - Wednesday'

    >>> do_date(None, None)
    ''

    >>> do_date(None, datetime(2012, 10, 17, 22, 00, 00))
    ''

    """
    if dt is None:
        return ''
    # Only difference with do_datetime is the default format, but that is
    # convenient enough to warrant its own template filter.
    return dt.strftime(format)


def do_duration(seconds):
    """Jinja template filter to format seconds to humanized duration.

        3600 becomes "1 hour".
        258732 becomes "2 days, 23 hours, 52 minutes, 12 seconds".
    >>> do_duration(3600)
    '1 hour'

    >>> do_duration(258732)
    '2 days, 23 hours, 52 minutes, 12 seconds'

    >>> do_duration(60)
    '1 minute'

    """
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    d, h = divmod(h, 24)
    tokens = []
    if d != 0:
        tokens.append(formatoDia(d))
    if h != 0:
        tokens.append(formatoHora(h))
    if m != 0:
        tokens.append(formatoMinuto(m))
    if s != 0:
        tokens.append(formatoSegundo(s))

    template = ', '.join(tokens)
    return template.format(d=d, h=h, m=m, s=s)


def formatoDia(d):
    """
    Format para los dias
    >>> formatoDia(1)
    '{d} day'
    >>> formatoDia(2)
    '{d} days'
    """
    return '{d} days' if d > 1 else '{d} day'


def formatoHora(h):
    """
    format for hours

    >>> formatoHora(1)
    '{h} hour'

    >>> formatoHora(10)
    '{h} hours'
    """
    return '{h} hours' if h > 1 else '{h} hour'


def formatoMinuto(m):
    """
    formato para los minutos

    >>> formatoMinuto(1)
    '{m} minute'

    >>> formatoMinuto(10)
    '{m} minutes'
    """
    return '{m} minutes' if m > 1 else '{m} minute'


def formatoSegundo(s):
    """
    Format for seconds
    >>> formatoSegundo(1)
    '{s} second'
    >>> formatoSegundo(23)
    '{s} seconds'
    """

    return '{s} seconds' if s > 1 else '{s} second'


def do_nl2br(context, value):
    """
    Render newline \n characters as HTML line breaks <br />.

    By default, HTML normalizes all whitespace on display. This filter allows
    text with line breaks entered into a textarea input to later display in
    HTML with line breaks.

    The context argument is Jinja's state for template rendering, which
    includes configuration. This filter inspects the context to determine
    whether to auto-escape content, e.g. convert <script> to &lt;script&gt;.
    """
    formatted = u'<br />'.join(escape(value).split('\n'))
    if context.autoescape:
        formatted = Markup(formatted)
    return formatted
