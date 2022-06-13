import os
import sys

from flask import Flask, render_template

app = Flask(__name__)      
app.config['SECRET_KEY'] = 'ecf6e975838a2f7bf3c5dbe7d55ebe5b'  ###
from web_for_undercut import routes
