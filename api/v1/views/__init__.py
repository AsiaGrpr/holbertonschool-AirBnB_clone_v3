#!/usr/bin/python3
"""script that init"""
from flask import Flask, Blueprint


app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')
