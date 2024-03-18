import os
from flask import Flask
from flask import render_template, request, redirect, url_for, flash
from flask import flash, redirect, url_for
from werkzeug.utils import secure_filename
from db import db
from config import Config
from flask_migrate import Migrate
from form import PropertyForm
import locale
from models import Property

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
migrate = Migrate(app, db)


@app.route('/')
def home():
    """Render website's home page."""
    return render_template('home.html')


@app.route('/properties/create', methods=['GET', 'POST'])
def create_property():
    form = PropertyForm()

    if form.validate_on_submit():
        photo = form.photo.data
        if photo:
            filename = secure_filename(photo.filename)
            photo.save(os.path.join(app.config['UPLOAD_FOLDER'], 'images/' + filename))
        else:
            flash("Please upload a photo for the property.", "danger")
            return render_template('create.html', form=form)

        # Add Properties to list of properties
        new_property = {
            'title': form.title.data,
            'description': form.description.data,
            'num_bedrooms': form.num_bedrooms.data,
            'num_bathrooms': form.num_bathrooms.data,
            'location': form.location.data,
            'photo': 'images/' + filename if photo else None,  # Store filename if uploaded
            'property_type': form.property_type.data,
            'price': form.price.data
        }
        # Create a new Property object from the form data
        new_property = Property(new_property)

        # Add the new property object to the database session
        db.session.add(new_property)

        # Commit the changes to the database
        db.session.commit()



        form.photo.data = None
        form.title.data = ''
        form.description.data = ''
        form.num_bedrooms.data = None
        form.num_bathrooms.data = None
        form.location.data = ''
        form.property_type.data = None
        form.price.data = None


        flash("Property added successfully!", "success")


    return render_template('create.html', form=form)


@app.route('/properties', methods=['GET'])
def get_properties():
    """
    1. return a list of properties from the database
    """

    locale.setlocale(locale.LC_ALL, '')
    properties = db.session.execute(db.select(Property)).scalars()

    return render_template('properties.html', properties=[
        {
            'price': locale.currency(prop.price, grouping=True),
            'id': str(prop.id),
            'title': prop.title,
            'description': prop.description,
            'num_bedrooms': prop.num_bedrooms,
            'num_bathrooms': prop.num_bathrooms,
            'location': prop.location,
            'photo': prop.photo,
            'property_type': prop.property_type
        } for prop in properties])


@app.route('/properties/<int:propertyid>', methods=['GET'])
def get_property(propertyid):
    """
    Return a single property from the database with the given id.
    """
    _property = db.get_or_404(Property, propertyid)
    return render_template('property.html', property=_property)


if __name__ == '__main__':

    app.run()
