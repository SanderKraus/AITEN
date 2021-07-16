from operator import index
from flask import Flask, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy, model
from flask_wtf import FlaskForm
import os
from flask_migrate import Migrate
from datetime import datetime

from wtforms.fields.core import StringField

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
    os.path.join(os.getcwd(), 'test.db')
db = SQLAlchemy(app)
migrate = Migrate(app, db)
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY


class ModelForm(FlaskForm):

    username = StringField('Benutzername')
    name = StringField('Modellname')
    definition = StringField('Modellbeschreibung')
    category = StringField('Kategorie des Modells')
    input = StringField('Input des Modells')
    definitioninput = StringField('Beschreibung Input und Output')
    reason = StringField('Wofür hast du das Modell entwickelt?')
    data = StringField('Daten')


class Model(db.Model):
    __tablename__ = 'Model'

    id = db.Column(db.Integer, primary_key=True)
    timecreate = db.Column(db.DateTime, default=datetime.now())
    timemodif = db.Column(db.DateTime, default=datetime.now())

    username = db.Column(db.String)
    name = db.Column(db.String, unique=True)
    definition = db.Column(db.String)
    category = db.Column(db.String)
    input = db.Column(db.String)
    definitioninput = db.Column(db.String)
    reason = db.Column(db.String)
    data = db.Column(db.String)

    def __repr__(self):
        return str(self.name)


@app.route('/')
def start():

    return render_template('start.html')

# Data


@app.route('/models', methods=['GET', 'POST'])
def models():

    models = Model.query.all()
    print(models[0].timecreate)
    return render_template('models.html', models=models)


@app.route('/model-create', methods=['POST', 'GET'])
def model_create():
    form = ModelForm()
    print('Hallo')
    if form.validate_on_submit():
        new_task = Model(
            username=form.username.data,
            name=form.name.data,
            category=form.category.data,
            input=form.input.data,
            data=form.data.data,
            definition=form.definition.data,
            definitioninput=form.definitioninput.data,
            reason=form.reason.data
        )
        db.session.add(new_task)
        db.session.commit()
        return redirect(url_for('models'))
    return render_template('model-create.html', form=form)


@app.route('/model-update/<id>', methods=['POST', 'GET'])
def model_update(id):
    model = Model.query.filter_by(id=id).first()
    if not model:
        return 'Model nicht gefunden!'

    form = ModelForm(obj=model)
    if form.validate_on_submit():
        form.populate_obj(model)
        db.session.commit()
        return redirect(url_for('models'))
    return render_template('model-update.html', form=form)


@app.route('/sensors')
def senosors():

    return render_template('index-data-sensor.html')


@app.route('/osensors')
def osensors():

    return render_template('index-data-othersensor.html')

# Predictiv Models Insights


@app.route('/pafq')
def pafq():

    return render_template('index-models-predictive.html')


@app.route('/darc')
def darc():

    return render_template('index-models-diagnostic.html')

# Early Warnings


@app.route('/recom')
def recom():

    return render_template('index-warnings-recommend.html')
