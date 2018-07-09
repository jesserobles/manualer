from flask import render_template, session, redirect, url_for, abort, flash, request, current_app, Response
from flask_login import login_required, current_user
# from flask_weasyprint import HTML, render_pdf
# import PyPDF2
# from reportlab.pdfgen import canvas
# from reportlab.lib.units import mm
# from reportlab.lib.pagesizes import letter
import io
from . import main
# from .forms import EditProfileForm, EditProfileAdminForm, LERForm, AddComponentForm
# from .. import db
# from ..models import User, Role, Permission, LER, Component, Facility, CFR, ComponentFailure, ComponentCause, \
#     EIISComponentType, System
# from ..decorators import admin_required, permission_required


@main.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')