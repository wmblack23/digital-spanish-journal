from flask import Flask, request, render_template, redirect, url_for, flash, session, make_response, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from utils import correct_spanish_entry, is_spanish
from dotenv import load_dotenv
from langdetect import detect
import os
import random

load_dotenv()

application = Flask(__name__)
CORS(application)

env = os.getenv("ENV", "dev")
clusterUrl = os.environ["clusterUrl"]
client = MongoClient(clusterUrl)
application.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

if env == "prod":
    db = client["spanish-diary-prod"]
else:
    db = client["spanish-diary-dev"]

entries = db["entries"]
users = db["prompts"]
prompts = db["prompts"]

@application.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        # Post signup info to MongoDB 'users' collection
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")
        email = request.form.get("email")
        password = request.form.get("password")

        # Flash error for if someone signs up with an existing email
        if users.find_one({"email": email}):
            flash('Email already exists. Try logging in instead!', 'error') 
            return render_template("signup.html")
        
        # Hash and store the password and all user info
        h_password = generate_password_hash(password)
        users.insert_one({"first_name": first_name, "last_name": last_name, "email": email, "password": h_password})
        session["email"] = email

        return redirect(url_for("index"))
    return render_template("signup.html")

@application.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # Grab username and password from matching MongoDB document
        email = request.form.get("email")
        password = request.form.get("password")

        user = users.find_one({"email": email})
        if user and check_password_hash(user["password"], password):
            # Create session for user if username and password are a match
            session["email"] = email
            return redirect(url_for("index"))
        else:
            # Flash error for invalid login credentials
            flash('Invalid login credentials', 'error') 
            return render_template("login.html")

    return render_template("login.html")

@application.route("/", methods=["GET", "POST"])
def index():
    if "email" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":
        # Send journal title and journal body to the 'entries' collection
        title = request.form.get("title")
        body = request.form.get("body").strip()
        user_timestamp = request.form.get("timestamp")

        # Check for a different language or gibberish
        if not is_spanish(body):
            flash("Please write your blog in Spanish :)", 'error')
            return redirect(url_for("index"))
        
        # Call function from utils.py which sends journal entry to Chat GPT API
        # for fixes and recommendations
        api_corrections = correct_spanish_entry(body)
        corrected_body = api_corrections['corrected_text'].strip()
        corrections = api_corrections['corrections'].strip()
        score = api_corrections['score'].strip()
        
        # Insert the entry with the corrected version
        if title and body:
            entries.insert_one({
                "email": session["email"],
                "title": title,
                "body": body, 
                "corrected_body": corrected_body,
                "corrections": corrections,
                "timestamp": user_timestamp,
                "score": score
            })
        
        return redirect(url_for("index"))
    
    # Grab all posts from the specified user from the 'entries' collection - reverse the order
    # so that latest show first
    posts = list(entries.find({"email": session["email"]}, {"_id": 0}))
    posts.reverse()

    # Allows for greater security so the webpage does not cache and when we logout we
    # cannot re-access the journal entry page by using the back button
    response = make_response(render_template("index.html", posts=posts))
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response

@application.route("/generate_prompt", methods=["POST"])
def fetch_prompt():
    if "email" not in session:
        return redirect(url_for("login"))

    data = request.get_json()
    level = data.get("level")

    levelPrompts = list(prompts.find({"level": level}, {"_id": 0, "text": 1}))

    if not levelPrompts:
        return jsonify({"prompt": "No prompts found for that level."})

    # Choose a random prompt
    random_prompt = random.choice(levelPrompts)["text"]

    return jsonify({"prompt": random_prompt})

@application.route("/delete_blog", methods=["POST"])
def delete_blog():
    timestamp = request.form.get("timestamp")
    email = request.form.get("email")
    if timestamp and email:
        entries.delete_one({"timestamp": timestamp, "email": email})
    return redirect(url_for("index"))  # or wherever your homepage is


@application.route("/logout")
def logout():
    session.pop("email", None)
    return redirect(url_for("login"))

@application.route("/health")
def health_check():
    return "OK", 200

if __name__ == "__main__":
    application.run(debug=True)