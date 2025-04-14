"""
Flask Documentation:     https://flask.palletsprojects.com/
Jinja2 Documentation:    https://jinja.palletsprojects.com/
Werkzeug Documentation:  https://werkzeug.palletsprojects.com/
This file creates your application.
"""

import os

from flask import jsonify, request, send_from_directory
from flask_wtf.csrf import generate_csrf
from werkzeug.utils import secure_filename

from app import app, db

from .forms import MovieForm
from .models import Movie

###
# Routing for your application.
###


@app.route("/api/v1/movies", methods=["POST", "GET"])
def movies():
    """
    POST endpoint for adding a new movie
    """
    if request.method != "POST" and request.method != "GET":
        return jsonify({"error": "Method not allowed"}), 405

    if request.method == "GET":
        # Query all movies from the database
        all_movies = Movie.query.order_by(Movie.created_at.desc()).all()

        # Format the movies for JSON response
        movies_list = []
        for movie in all_movies:
            movies_list.append(
                {
                    "id": movie.id,
                    "title": movie.title,
                    "description": movie.description,
                    "poster": f"/api/v1/posters/{movie.poster}",
                    "created_at": movie.created_at.strftime(
                        "%Y-%m-%d %H:%M:%S"
                    ),
                }
            )

        return jsonify({"movies": movies_list})
    else:
        form = MovieForm()

        if form.validate_on_submit():
            # Save the poster file
            poster_filename = save_poster(form.poster.data)

            # Create and save the movie to the database
            movie = Movie(
                title=form.title.data,
                description=form.description.data,
                poster=poster_filename,
            )

            db.session.add(movie)
            db.session.commit()

            # Return success response
            return jsonify(
                {
                    "message": "Movie Successfully added",
                    "title": movie.title,
                    "poster": movie.poster,
                    "description": movie.description,
                }
            ), 201

        # Return validation errors
        return jsonify({"errors": form_errors(form)}), 400


@app.route("/api/v1/posters/<filename>", methods=["GET"])
def get_poster(filename):
    """Serve poster images from the uploads folder"""
    return send_from_directory(
        os.path.join(os.getcwd(), UPLOAD_FOLDER),
        filename,
        as_attachment=True,
    )


@app.route("/api/v1/csrf-token", methods=["GET"])
def get_csrf():
    """Generate and return a CSRF token"""
    return jsonify({"csrf_token": generate_csrf()})


###
# The functions below should be applicable to all Flask apps.
###
# Configuration for file uploads
UPLOAD_FOLDER = "uploads"
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


def save_poster(file):
    """Save the poster file to the uploads folder and return the filename"""
    filename = secure_filename(file.filename)
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(file_path)
    return filename


# Here we define a function to collect form errors from Flask-WTF
# which we can later use
def form_errors(form):
    error_messages = []
    """Collects form errors"""
    for field, errors in form.errors.items():
        for error in errors:
            message = "Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error,
            )
            error_messages.append(message)

    return error_messages


@app.route("/<file_name>.txt")
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + ".txt"
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also tell the browser not to cache the rendered page. If we wanted
    to we could change max-age to 600 seconds which would be 10 minutes.
    """
    response.headers["X-UA-Compatible"] = "IE=Edge,chrome=1"
    response.headers["Cache-Control"] = "public, max-age=0"
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return jsonify({"error": "Route not found"}), 404
