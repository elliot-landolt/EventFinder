import functools
from flask import session, redirect, flash

def authenticated_route(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if session.get('current_user'):
            return view(**kwargs)
        else:
            print("UNAUTHENTICATED")
            flash('Unauthenticated. Please login!','warning')
            return redirect('/login')
    return wrapped_view