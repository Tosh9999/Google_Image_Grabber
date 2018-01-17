from lib import app
from flask import request, Response
from urllib.request import urlretrieve
from PIL import Image

@app.route('/dataApi/saveImage', methods=['POST'])
def saveImage():
    image_url = request.values['image_url']

    try:
        set_image_height = request.values['image_height']
    except (KeyError, ValueError):
        set_image_height = 0

    try:
        set_image_width = request.values['image_width']
    except (KeyError, ValueError):
        set_image_width = 0

    try:
        search_term = request.values['search_term']
        result_index = request.values['result_index']

        image_extension = request.values['image_mime'].split('/')[1]
        image_extension = 'jpg' if image_extension == 'jpeg' else image_extension

        path_to = './images/' + search_term + '/'
        file_path = path_to + search_term + '_image_' + str(result_index) + '.' + image_extension

        urlretrieve(image_url, file_path)    

        if set_image_height > 0 or set_image_width > 0:
            saved_image = Image.open(file_path)
            old_width = saved_image.size[0]
            old_height = saved_image.size[1]

            new_height = set_image_height if set_image_height > 0 else (set_image_width / old_width) * old_height
            new_width = set_image_width if set_image_width > 0 else (set_image_height / old_height) * old_width

            resized_image = saved_image.resize((new_width, new_height), Image.ANTIALIAS)
            resized_image.save(path_to + search_term + '_resized_' + str(result_index) + '.' + image_extension)
        
        response_code = 201
        response_string = f'File successfully downloaded from {image_url} to {file_path}'

    except:
        response_code = 500
        response_string = 'Something went wrong'


    return Response(response=response_string, status=response_code)

