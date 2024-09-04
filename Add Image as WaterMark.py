# Integrated In https://ahmedul.com/

# Water Mark with 95% Transparancy 
from PIL import Image

@app.route('/upload_portfolio', methods=['POST'])
def upload_portfolio():
    if request.method == 'POST':
        portfolio_name = request.form.get('portfolio_name')
        portfolio_description = request.form.get('portfolio_description')
        file_photo = request.files.get('file_photo')

        if not portfolio_name or not file_photo:
            return jsonify({'error': 'Portfolio name and file are required.'}), 400

        photo_name = file_photo.filename
        original_filename = secure_filename(photo_name)
        new_filename = original_filename.replace(' ', '')

        try:
            # Save the uploaded image temporarily
            temp_path = os.path.join('static/mainassets/images/temp', new_filename)
            file_photo.save(temp_path)

            # Open the uploaded image
            with Image.open(temp_path) as base_image:
                base_image = base_image.convert('RGBA')  # Ensure the base image has an alpha channel

                # Open the watermark image
                watermark_path = os.path.join('static/mainassets/images/logos', 'Techknowgramlogo.jpg')
                with Image.open(watermark_path) as watermark:
                    watermark = watermark.convert('RGBA')  # Ensure the watermark has an alpha channel

                    # Adjust the opacity of the watermark image
                    watermark_alpha = watermark.split()[3]  # Get the alpha channel
                    watermark_alpha = watermark_alpha.point(lambda p: int(p * 0.05))  #(90% transparent)
                    watermark.putalpha(watermark_alpha)

                    # Resize watermark to fit the base image (optional)
                    watermark_with_opacity = watermark.resize(
                        (int(base_image.width * 0.6), int(base_image.height * 0.6)),
                        Image.LANCZOS
                    )

                    # Calculate position for the watermark to be centered
                    watermark_position = (
                        (base_image.width - watermark_with_opacity.width) // 2,
                        (base_image.height - watermark_with_opacity.height) // 2
                    )

                    # Create a new image with an alpha channel (RGBA) for transparency
                    transparent = Image.new('RGBA', base_image.size, (0, 0, 0, 0))
                    transparent.paste(base_image, (0, 0))
                    transparent.paste(watermark_with_opacity, watermark_position, mask=watermark_with_opacity)

                    # Convert back to RGB and save the image
                    final_image = transparent.convert('RGB')
                    file_path = os.path.join('static/mainassets/images/portfolios', new_filename)
                    final_image.save(file_path)

            # Insert record into the database
            with connection.cursor() as cursor:
                cursor.execute(
                    'INSERT INTO portfolios (portfolio_name, portfolio_description, portfolio, created_at) VALUES (%s, %s, %s, NOW())',
                    (portfolio_name, portfolio_description, new_filename)
                )
                connection.commit()

            # Clean up the temporary file
            os.remove(temp_path)

            return jsonify({'success': 'Portfolio Upload Success'})

        except Exception as e:
            return jsonify({'error': f"Request error: {str(e)}"}), 500

    return jsonify({'error': 'Invalid request method.'}), 405


# Add Image as watermark in Edit Functionality
@app.route('/portfolio_edit', methods=['POST'])
def portfolio_edit():
    if request.method == 'POST':
        try:
            # Retrieve form and JSON data
            form_data = request.form
            json_data = request.form.get('json_data')

            if not json_data:
                return jsonify({'error': 'No JSON data provided'}), 400

            json_data_dict = json.loads(json_data)
            portfolio_id = json_data_dict.get('portfolio_id')
            portfolio_name = json_data_dict.get('portfolio_name')
            portfolio_description = json_data_dict.get('portfolio_description')

            # Get the existing portfolio image filename
            with connection.cursor() as cursor:
                cursor.execute("SELECT portfolio FROM portfolios WHERE portfolio_id = %s", (portfolio_id,))
                result = cursor.fetchone()
                existing_portfolio_image = result['portfolio'] if result else None

            # File handling
            file_photo = request.files.get('file_photo')
            if file_photo and file_photo.filename != '':
                photo_name = secure_filename(file_photo.filename)
                new_filename = photo_name.replace(' ', '_')
                temp_path = os.path.join('static/mainassets/images/temp', new_filename)
                final_file_path = os.path.join('static/mainassets/images/portfolios', new_filename)

                # Save the uploaded image temporarily
                file_photo.save(temp_path)

                try:
                    # Open the uploaded image
                    with Image.open(temp_path) as base_image:
                        base_image = base_image.convert('RGBA')  # Ensure the base image has an alpha channel

                        # Open the watermark image
                        watermark_path = os.path.join('static/mainassets/images/logos', 'Techknowgramlogo.jpg')
                        with Image.open(watermark_path) as watermark:
                            watermark = watermark.convert('RGBA')  # Ensure the watermark has an alpha channel

                            # Adjust the opacity of the watermark image
                            watermark_alpha = watermark.split()[3]  # Get the alpha channel
                            watermark_alpha = watermark_alpha.point(lambda p: int(p * 0.05))  # 95% transparent watermark
                            watermark.putalpha(watermark_alpha)

                            # Resize watermark to fit the base image (optional)
                            watermark_with_opacity = watermark.resize(
                                (int(base_image.width * 0.6), int(base_image.height * 0.6)),
                                Image.LANCZOS
                            )

                            # Calculate position for the watermark to be centered
                            watermark_position = (
                                (base_image.width - watermark_with_opacity.width) // 2,
                                (base_image.height - watermark_with_opacity.height) // 2
                            )

                            # Create a new image with an alpha channel (RGBA) for transparency
                            transparent = Image.new('RGBA', base_image.size, (0, 0, 0, 0))
                            transparent.paste(base_image, (0, 0))
                            transparent.paste(watermark_with_opacity, watermark_position, mask=watermark_with_opacity)

                            # Convert back to RGB and save the image
                            final_image = transparent.convert('RGB')
                            final_image.save(final_file_path)

                    # Delete the old file if it exists
                    if existing_portfolio_image:
                        old_file_path = os.path.join('static/mainassets/images/portfolios', existing_portfolio_image)
                        if os.path.exists(old_file_path):
                            os.remove(old_file_path)

                    # Update the database with the new file name
                    with connection.cursor() as cursor:
                        sql = """
                            UPDATE portfolios 
                            SET portfolio_name=%s, portfolio_description=%s, portfolio=%s 
                            WHERE portfolio_id=%s
                        """
                        cursor.execute(sql, (portfolio_name, portfolio_description, new_filename, portfolio_id))
                        connection.commit()

                    # Clean up the temporary file
                    os.remove(temp_path)

                    return jsonify({'success': 'Portfolio Edited Successfully'})

                except Exception as e:
                    return jsonify({'error': f"Request error during image processing: {str(e)}"}), 500

            else:
                # Update only portfolio name and description if no new file is uploaded
                with connection.cursor() as cursor:
                    sql = """
                        UPDATE portfolios 
                        SET portfolio_name=%s, portfolio_description=%s 
                        WHERE portfolio_id=%s
                    """
                    cursor.execute(sql, (portfolio_name, portfolio_description, portfolio_id))
                    connection.commit()

                return jsonify({'success': 'Portfolio Edited Successfully'})

        except Exception as e:
            return jsonify({'error': f"Request error: {str(e)}"}), 500

    return jsonify({'error': 'Invalid request method.'}), 405


# In the middle
from PIL import Image

@app.route('/upload_portfolio', methods=['POST'])
def upload_portfolio():
    if request.method == 'POST':
        portfolio_name = request.form.get('portfolio_name')
        portfolio_description = request.form.get('portfolio_description')
        file_photo = request.files.get('file_photo')

        if not portfolio_name or not file_photo:
            return jsonify({'error': 'Portfolio name and file are required.'}), 400

        photo_name = file_photo.filename
        original_filename = secure_filename(photo_name)
        new_filename = original_filename.replace(' ', '')

        try:
            # Save the uploaded image temporarily
            temp_path = os.path.join('static/mainassets/images/temp', new_filename)
            file_photo.save(temp_path)

            # Open the uploaded image
            with Image.open(temp_path) as base_image:
                base_image = base_image.convert('RGBA')  # Ensure the base image has an alpha channel

                # Open the watermark image
                watermark_path = os.path.join('static/mainassets/images/logos', 'Techknowgramlogo.jpg')
                with Image.open(watermark_path) as watermark:
                    watermark = watermark.convert('RGBA')  # Ensure the watermark has an alpha channel

                    # Create a white watermark with 10% opacity
                    watermark_with_opacity = Image.new('RGBA', watermark.size, (255, 255, 255, int(255 * 0.1)))
                    watermark_with_opacity.paste(watermark, (0, 0), mask=watermark)

                    # Resize watermark to fit the base image (optional)
                    watermark_with_opacity = watermark_with_opacity.resize(
                        (int(base_image.width * 0.6), int(base_image.height * 0.6)),
                        Image.LANCZOS
                    )

                    # Calculate position for the watermark to be centered
                    watermark_position = (
                        (base_image.width - watermark_with_opacity.width) // 2,
                        (base_image.height - watermark_with_opacity.height) // 2
                    )

                    # Create a new image with an alpha channel (RGBA) for transparency
                    transparent = Image.new('RGBA', base_image.size, (0, 0, 0, 0))
                    transparent.paste(base_image, (0, 0))
                    transparent.paste(watermark_with_opacity, watermark_position, mask=watermark_with_opacity)

                    # Convert back to RGB and save the image
                    final_image = transparent.convert('RGB')
                    file_path = os.path.join('static/mainassets/images/portfolios', new_filename)
                    final_image.save(file_path)

            # Insert record into the database
            with connection.cursor() as cursor:
                cursor.execute(
                    'INSERT INTO portfolios (portfolio_name, portfolio_description, portfolio, created_at) VALUES (%s, %s, %s, NOW())',
                    (portfolio_name, portfolio_description, new_filename)
                )
                connection.commit()

            # Clean up the temporary file
            os.remove(temp_path)

            return jsonify({'success': 'Portfolio Upload Success'})

        except Exception as e:
            return jsonify({'error': f"Request error: {str(e)}"}), 500

    return jsonify({'error': 'Invalid request method.'}), 405





# On the right bottom 

from PIL import Image

@app.route('/upload_portfolio', methods=['POST'])
def upload_portfolio():
    if request.method == 'POST':
        portfolio_name = request.form.get('portfolio_name')
        portfolio_description = request.form.get('portfolio_description')
        file_photo = request.files.get('file_photo')

        if not portfolio_name or not file_photo:
            return jsonify({'error': 'Portfolio name and file are required.'}), 400

        photo_name = file_photo.filename
        original_filename = secure_filename(photo_name)
        new_filename = original_filename.replace(' ', '')

        try:
            # Save the uploaded image temporarily
            temp_path = os.path.join('static/mainassets/images/temp', new_filename)
            file_photo.save(temp_path)

            # Open the uploaded image
            with Image.open(temp_path) as base_image:
                base_image = base_image.convert('RGBA')  # Ensure the base image has an alpha channel

                # Open the watermark image
                watermark_path = os.path.join('static/mainassets/images/logos', 'Techknowgramlogo.jpg')
                with Image.open(watermark_path) as watermark:
                    watermark = watermark.convert('RGBA')  # Ensure the watermark has an alpha channel

                    # Resize watermark to fit the base image (optional)
                    watermark = watermark.resize(
                        (int(base_image.width * 0.3), int(base_image.height * 0.3)),
                        Image.LANCZOS
                    )

                    # Set the position for the watermark
                    watermark_position = (
                        base_image.width - watermark.width - 10,
                        base_image.height - watermark.height - 10
                    )

                    # Create a new image with an alpha channel (RGBA) for transparency
                    transparent = Image.new('RGBA', base_image.size, (0, 0, 0, 0))
                    transparent.paste(base_image, (0, 0))
                    transparent.paste(watermark, watermark_position, mask=watermark)

                    # Convert back to RGB and save the image
                    final_image = transparent.convert('RGB')
                    file_path = os.path.join('static/mainassets/images/portfolios', new_filename)
                    final_image.save(file_path)

            # Insert record into the database
            with connection.cursor() as cursor:
                cursor.execute(
                    'INSERT INTO portfolios (portfolio_name, portfolio_description, portfolio, created_at) VALUES (%s, %s, %s, NOW())',
                    (portfolio_name, portfolio_description, new_filename)
                )
                connection.commit()

            # Clean up the temporary file
            os.remove(temp_path)

            return jsonify({'success': 'Portfolio Upload Success'})

        except Exception as e:
            return jsonify({'error': f"Request error: {str(e)}"}), 500

    return jsonify({'error': 'Invalid request method.'}), 405


@app.route('/fetch_portfolio', methods=['GET'])
def fetch_portfolio():
    try:
        with connection.cursor() as cursor:
            # SQL query to fetch all data from the portfolio table
            portfolio_sql = "SELECT * FROM portfolios"
            cursor.execute(portfolio_sql)
            portfolio_data = cursor.fetchall()
        
        # Convert the portfolio data to a dictionary format
        portfolio_data = [
            {
                'portfolio_id': row['portfolio_id'],
                'portfolio_name': row['portfolio_name'],
                'portfolio_description': row['portfolio_description'],
                'portfolio': row['portfolio']
                
            }
            for row in portfolio_data
        ]
        
        # Return the portfolio data as JSON
        return jsonify(portfolio_data), 200

    except Exception as e:
        # Log the error and return an error message
        logging.error(f"Error fetching portfolio data: {str(e)}")
        return jsonify({'error': f"Request error: {str(e)}"}), 500
