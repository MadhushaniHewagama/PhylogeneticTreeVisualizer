#valid file format extensions
ALLOWED_EXTENSIONS = set(['phy'])

#check validation
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS