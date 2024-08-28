# image will be deleted from root folder when edited or deleted

@app.route('/delete_portfolio/<int:portfolio_id>', methods=['DELETE'])
def delete_portfolio(portfolio_id):
    try:
        with connection.cursor() as cursor:
            # Fetch the portfolio entry to get the image filename
            portfolio_sql = "SELECT portfolio FROM portfolios WHERE portfolio_id = %s"
            cursor.execute(portfolio_sql, (portfolio_id,))
            portfolio_data = cursor.fetchone()
            
            if not portfolio_data:
                return jsonify({'error': 'Portfolio not found'}), 404
            
            image_filename = portfolio_data['portfolio']
            
            # Delete the portfolio entry from the database
            delete_sql = "DELETE FROM portfolios WHERE portfolio_id = %s"
            cursor.execute(delete_sql, (portfolio_id,))
            connection.commit()
            
            # Delete the image file from the filesystem
            if image_filename:
                image_path = os.path.join('static', 'mainassets', 'images', 'portfolios', image_filename)
                if os.path.exists(image_path):
                    os.remove(image_path)
            
        return jsonify({'success': 'Portfolio deleted successfully'}), 200

    except Exception as e:
        logging.error(f"Error deleting portfolio: {str(e)}")
        return jsonify({'error': f"Request error: {str(e)}"}), 500


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
                file_path = os.path.join('static/mainassets/images/portfolios', new_filename)

                # Save the new file
                file_photo.save(file_path)

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

                return jsonify({'success': 'Portfolio Edited Successfully'})

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
