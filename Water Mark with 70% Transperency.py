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
                    watermark_alpha = watermark_alpha.point(lambda p: int(p * 0.3))  # Adjust opacity to 30% (70% transparent)
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
