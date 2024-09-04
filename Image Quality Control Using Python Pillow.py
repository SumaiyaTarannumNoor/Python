# Integrated In https://ahmedul.com/


#pip install pillow

# In the Database the image type should be BLOB

import base64
import io
from PIL import Image

@app.route('/carousel_image_upload', methods=['POST'])
def carousel_image_upload():
    image_name = request.form.get('image_name')
    carousel_image = request.form.get('carousel_image')  # Now expecting base64 encoded string

    if image_name and carousel_image:
        try:
            # Decode the base64 image
            header, image_data = carousel_image.split(',', 1)
            mime_type = header.split(';')[0].split(':')[1]
            if mime_type not in ['image/jpeg', 'image/png', 'image/jpg']:
                return jsonify({"message": "Unsupported image format. Only JPG, JPEG, and PNG are allowed."}), 400

            carousel_image_data = base64.b64decode(image_data)

            # Resize image to be under 60KB
            image = Image.open(io.BytesIO(carousel_image_data))
            image_format = image.format  # Get original image format

            # Define function to resize the image while maintaining quality
            def resize_image(image, max_size_kib):
                output_io = io.BytesIO()
                quality = 95  # Start with high quality
                while True:
                    output_io.seek(0)
                    image.save(output_io, format=image_format, quality=quality)
                    size = output_io.tell()
                    if size <= max_size_kib * 1024 or quality <= 5:
                        break
                    quality -= 5
                output_io.seek(0)
                return output_io

            resized_image_io = resize_image(image, 60)
            resized_image_data = resized_image_io.read()

            filename = secure_filename(image_name)  # Use image_name as filename

            # Connect to the database
            connection = pymysql.connect(**db_config)

            try:
                with connection.cursor(pymysql.cursors.DictCursor) as cursor:
                    sql_insert_carousel_image = '''
                    INSERT INTO carousel_images (image_name, carousel_image, status)
                    VALUES (%s, %s, %s)
                    '''
                    cursor.execute(sql_insert_carousel_image, (image_name, resized_image_data, False))

                # Commit changes
                connection.commit()

                return jsonify({"message": "Post successful"}), 200

            except Exception as e:
                print(f"Error processing request: {str(e)}")
                return jsonify({"message": "An error occurred. Please try again."}), 500

            finally:
                connection.close()
        
        except Exception as e:
            print(f"Error processing request: {str(e)}")
            return jsonify({"message": "An error occurred. Please try again."}), 500

    return jsonify({"message": "User not authenticated or request processing failed."}), 401
