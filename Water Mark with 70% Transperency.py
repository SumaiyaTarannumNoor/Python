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


/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
EXPLANATION

Let's break down how the watermark transparency is adjusted in the `Pillow` library (PIL) using the code:

### Understanding the Code

```python
# Get the alpha channel from the watermark image
watermark_alpha = watermark.split()[3]
# Adjust the opacity to 30% (70% transparent)
watermark_alpha = watermark_alpha.point(lambda p: int(p * 0.3))
# Apply the adjusted alpha channel back to the watermark
watermark.putalpha(watermark_alpha)
```

### Detailed Explanation

1. **Extract the Alpha Channel:**

   ```python
   watermark_alpha = watermark.split()[3]
   ```
   
   - **`watermark.split()`**: The `split()` method splits the image into its constituent bands. For an RGBA image, this returns a list with four items: the red, green, blue, and alpha (transparency) channels.
   - **`watermark.split()[3]`**: This accesses the alpha channel, which represents the image's transparency. This channel contains the alpha values (0 to 255) for each pixel.

2. **Adjust the Opacity:**

   ```python
   watermark_alpha = watermark_alpha.point(lambda p: int(p * 0.3))
   ```
   
   - **`watermark_alpha.point(lambda p: int(p * 0.3))`**: The `point()` method applies a function to each pixel value in the alpha channel.
     - **`lambda p: int(p * 0.3)`**: This lambda function takes each pixel value (`p`), multiplies it by `0.3`, and converts it to an integer.
       - **`p * 0.3`**: Adjusts the transparency. If the original alpha value is 255 (fully opaque), it becomes `255 * 0.3 = 76.5`, which is rounded to 76 (partially transparent). This sets the opacity of the watermark to 30% (70% transparent).

3. **Apply the Adjusted Alpha Channel:**

   ```python
   watermark.putalpha(watermark_alpha)
   ```
   
   - **`watermark.putalpha(watermark_alpha)`**: This method applies the adjusted alpha channel back to the watermark image. Now the watermark has the desired level of transparency.

### Summary

- **Extract the Alpha Channel**: You access the alpha (transparency) channel of the watermark image.
- **Adjust Transparency**: Modify the alpha channel values to change the transparency level.
- **Apply Changes**: Set the modified alpha channel back to the watermark image.

This approach allows you to control how visible the watermark is on the base image by adjusting its transparency level. The transparency level can be set according to your needs by changing the multiplication factor (`0.3` in this case) to other values.
