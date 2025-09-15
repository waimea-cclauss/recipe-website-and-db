#===========================================================
# App Creation and Launch
#===========================================================

from flask import Flask, render_template, request, flash, redirect
import html

from app.helpers.session import init_session
from app.helpers.db      import connect_db
from app.helpers.errors  import init_error, not_found_error
from app.helpers.logging import init_logging
from app.helpers.time    import init_datetime, utc_timestamp, utc_timestamp_now

import os
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename
UPLOAD_FOLDER = '/path/to/the/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

from flask import send_from_directory


# Create the app
app = Flask(__name__)

# Configure app
init_session(app)   # Setup a session for messages, etc.
init_logging(app)   # Log requests
init_error(app)     # Handle errors and exceptions
init_datetime(app)  # Handle UTC dates in timestamps


#-----------------------------------------------------------
# Home page route
#-----------------------------------------------------------
@app.get("/")
def index():
    with connect_db() as client:
        # Get all the things from the DB
        sql = "SELECT id, name, image_file FROM recipes ORDER BY name ASC"
        params = []
        result = client.execute(sql, params)
        recipes = result.rows

        # And show them on the page
        return render_template("pages/home.jinja", recipes=recipes)



#-----------------------------------------------------------
# Recipe page route - Show details of a single recipe
#-----------------------------------------------------------
@app.get("/recipe/<int:id>")
def show_one_recipe(id):
    with connect_db() as client:
        # Get the thing details from the DB
        sql = "SELECT id, name, instructions, ingredients, image_file FROM recipes WHERE id=?"
        params = [id]
        result = client.execute(sql, params)

        # Did we get a result?
        if result.rows:
            # yes, so show it on the page
            recipe = result.rows[0]
            return render_template("pages/recipe.jinja", recipe=recipe)

        else:
            # No, so show error
            return not_found_error()


#-----------------------------------------------------------
# Recipe form page route
#-----------------------------------------------------------
@app.get("/recipe/new")
def show_recipe_form():
    return render_template("pages/recipe-form.jinja")

#-----------------------------------------------------------
# Route for adding a recipe, using data posted from a form
#-----------------------------------------------------------
@app.post("/recipe/new")
def add_a_recipe():
    # Get the data from the form
    name  = request.form.get("name")
    ingredients = request.form.get("ingredients")
    instructions = request.form.get("instructions")
    image_file = request.form.get("image_file")

    # Sanitise the text inputs
    name = html.escape(name)

    with connect_db() as client:
        # Add the thing to the DB
        sql = "INSERT INTO recipes (name, ingredients, instructions, image_file) VALUES (?, ?, ?, ?)"
        params = [name, ingredients, instructions, image_file]
        client.execute(sql, params)

        # Go back to the home page
        flash(f"Recipe '{name}' added", "success")
        return redirect("/")
    
    #Add a image file
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return redirect(url_for('download_file', name=filename))
        
@app.route('/uploads/<name>')
def download_file(name):
    return send_from_directory(app.config["UPLOAD_FOLDER"], name)
    


#-----------------------------------------------------------
# Route for deleting a thing, Id given in the route
#-----------------------------------------------------------
@app.get("/delete/<int:id>")
def delete_a_thing(id):
    with connect_db() as client:
        # Delete the thing from the DB
        sql = "DELETE FROM things WHERE id=?"
        params = [id]
        client.execute(sql, params)

        # Go back to the home page
        flash("Thing deleted", "success")
        return redirect("/things")


