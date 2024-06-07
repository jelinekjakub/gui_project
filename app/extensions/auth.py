from flask import session, redirect, url_for
import wrapt


# Decorators
@wrapt.decorator
def auth(wrapped, instance, args, kwargs):
    if 'auth' not in session:
        return redirect(url_for('route.login'))
    return wrapped(*args, **kwargs)
