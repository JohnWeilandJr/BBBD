
# coding: utf-8

# In[1]:


import os

import pandas as pd
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine

from flask import Flask, jsonify, render_template


# In[2]:


# Flask Instance

app = Flask(__name__)


# In[3]:


#################################################
# Database Setup
#################################################

engine = create_engine("sqlite:///belly_button_biodiversity.sqlite", echo=False)

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
Samples_Metadata = Base.classes.samples_metadata
OTU = Base.classes.otu
Samples = Base.classes.samples

# Create our session (link) from Python to the DB
session = Session(engine)


# In[4]:


@app.route("/")
def index():
    """Return the homepage."""
    return render_template('index.html')


# In[5]:


@app.route('/names')
def names():
    """Return a list of sample names."""

    # Use Pandas to perform the sql query
    names = session.query(Samples).statement
    names_df = pd.read_sql_query(names, session.bind)
    names_df.set_index('otu_id', inplace=True)

    # Return a list of the column names (sample names)
    return jsonify(list(df.columns))


# In[6]:


@app.route('/otu')
def otu():
    otu = session.query(OTU).statement
    otu_df = pd.read_sql_query(otu, session.bind)
    otu_df.set_index('otu_id', inplace=True)
    return jsonify(list(otu_df["lowest_taxonomic_unit_found"]))


# In[11]:


@app.route('/metadata/<sample>')
def metadata_sample(sample):
    sample_id = sample.replace('BB_','')
    result = session.query(Samples_Metadata).filter(Samples_Metadata.SAMPLEID == sample_id).first()
    metadata_dict = {
        'AGE':result.AGE,
        'BBTYPE':result.BBTYPE,
        'ETHNICITY':result.ETHNICITY,
        'GENDER':result.GENDER,
        'LOCATION':result.LOCATION,
        'SAMPLEID':result.SAMPLEID
    }
    
    return jsonify(metadata_dict)

