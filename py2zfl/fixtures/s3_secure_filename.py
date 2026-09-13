from werkzeug.utils import secure_filename
name = secure_filename(request.files['f'])
open(name)                    # EXPECT: EARNED (sanitised path)
