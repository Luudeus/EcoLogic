import mysql.connector as SQL
from flask import Flask, render_template, flash, redirect, url_for, request, session
from flask_session import Session