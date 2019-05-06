import os
from flask import Flask, flash, render_template,request, redirect, url_for
from werkzeug.utils import secure_filename
from flask import send_from_directory
from IPython.core.display import HTML
import plot_circular
import plotly
import plotly.graph_objs as go
import ipywidgets as ipw
import plotly.plotly as py
from plotly.offline import iplot, init_notebook_mode
import plotly.graph_objs as go
import plotly.io as pio
from IPython.display import Image
import plot_rectangular
import create_tree
import validation

app = Flask(__name__)

app.secret_key = 'super secret key'
#define variable to file name
file_name=''

@app.route('/')
def index():
    return render_template('home.html' )

@app.route('/about')
def about():
    return render_template('about.html' )

#upload file and check validation and show data
@app.route('/SelectFormat', methods = ['GET', 'POST'])
def uploader_file():
   error= None
   if request.method == 'POST':
      # check if the post request has the file part
      if 'file' not in request.files:
         error='No file part'
         return render_template('home.html', error=error)
      f = request.files['file']   
      global file_name
      file_name=f.filename   
      #check if the uploaded file is in correct format
      if validation.allowed_file(file_name):
         f.save(secure_filename(file_name))
         return redirect(url_for('show'))         
      else:   
         error="please select 'phy' file"
         return render_template('home.html',error=error)

#show data content of the file
@app.route('/show', methods=['GET','POST'])
def show():
   with open(file_name) as f:
      file_content=f.read().split('\n')
   return render_template('home.html',file_content=file_content)

#render next select form page 
@app.route('/confirm', methods=['GET','POST'])
def confirm():
   #call create tree method
   create_tree.createTree(file_name)
   return render_template('selectFormat.html', data=[{'name':'rectangular'}, {'name':'circular'}])
   

#select file format
@app.route("/PhylogeneticTree" , methods=['GET', 'POST'])
def format():
   select = request.form.get('comp_select')
   if(select=="rectangular"):
      return redirect(url_for('parse_rectangular'))
   else:
      return redirect(url_for('parse_circular'))

#plot rectangular phylogenetic tree
@app.route('/rectangular')
def parse_rectangular():
   plot_rectangular.create_rectangular_tree()
   return render_template("tree_rectangular.html")

#plot circular phylogenetic tree
@app.route('/circular')
def parse_circular():
   plot_circular.create_circular_tree()
   return render_template("tree_circular.html")


   


if __name__ == '__main__':
    app.run(debug=True)
