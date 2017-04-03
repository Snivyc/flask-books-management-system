from flask import Blueprint

main = Blueprint('main', __name__)

from . import views, errors, user_views, admin_views, book_admin_views
