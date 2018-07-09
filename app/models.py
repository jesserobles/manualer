from datetime import datetime
import csv
import hashlib
# import pandas as pd
from werkzeug.security import generate_password_hash, check_password_hash
from flask import current_app, request, url_for
from flask_login import UserMixin, AnonymousUserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from markdown import markdown
import bleach
from . import db
from . import login_manager


class Permission:
    READ = 0x01
    WRITE = 0x02
    APPROVE = 0x04
    ADMINISTER = 0x80