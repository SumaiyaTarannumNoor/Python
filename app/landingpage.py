#######################################################################
################ LANDING PAGE ####################

@app.route('/Admin_to_LandingPage_CarouselImage')
def Admin_to_LandingPage_Carousel_Image():
    if 'logged_in' not in session or not session.get('allow_dashboard'):
            return redirect(url_for('index'))
    return render_template('Admin_to_LandingPage_Carousel.html')  

@app.route('/Admin_to_LandingPage_AboutUs')
def Admin_to_LandingPage_About_Us():
    if 'logged_in' not in session or not session.get('allow_dashboard'):
            return redirect(url_for('index'))
    return render_template('Admin_to_LandingPage_AboutUs.html') 

@app.route('/Admin_to_LandingPage_Latest')
def Admin_to_LandingPage_Latest():
    if 'logged_in' not in session or not session.get('allow_dashboard'):
            return redirect(url_for('index'))
    return render_template('Admin_to_LandingPage_Latest.html')  

@app.route('/Admin_to_LandingPage_Trending')
def Admin_to_LandingPage_Trending():
    if 'logged_in' not in session or not session.get('allow_dashboard'):
            return redirect(url_for('index'))
    return render_template('Admin_to_LandingPage_Trending.html')  

@app.route('/Admin_to_LandingPage_Seminer')
def Admin_to_LandingPage_Seminer():
    if 'logged_in' not in session or not session.get('allow_dashboard'):
            return redirect(url_for('index'))
    return render_template('Admin_to_LandingPage_Seminer.html')   

@app.route('/Admin_to_LandingPage_SuccessStories')
def Admin_to_LandingPage_SuccesssStories():
    if 'logged_in' not in session or not session.get('allow_dashboard'):
            return redirect(url_for('index'))
    return render_template('Admin_to_LandingPage_SuccessStories.html')

@app.route('/Admin_to_LandingPage_AdminBlog')
def Admin_to_LandingPage_AdminBlog():
    if 'logged_in' not in session or not session.get('allow_dashboard'):
            return redirect(url_for('index'))
    return render_template('Admin_to_LandingPage_AdminBlog.html')   

@app.route('/Admin_Video_Course_Creation')
def Admin_Video_Course_Creation():
    if 'logged_in' not in session or not session.get('allow_dashboard'):
            return redirect(url_for('index'))
    return render_template('Admin_Video_Course_Creation.html')                  

@app.route('/blog_details/<int:admin_blog_id>')
def blog_details(admin_blog_id):
    return render_template('blog_details.html', blog_id=admin_blog_id)

@app.route('/Student_Signup_Event')
def Student_Signup_Event():
    return render_template('Student_Signup_Event.html')

@app.route('/Video_Courses')
def Video_Courses():
    return render_template('Video_Courses.html')

@app.route('/All_Shows')
def All_Shows():
    return render_template('All_Shows.html')

# @app.route('/carousel_image_upload', methods=['POST'])
# def carousel_image_upload():
#     image_name = request.form.get('image_name')
#     carousel_image = request.form.get('carousel_image')  # Now expecting base64 encoded string

#     if image_name and carousel_image:
#         try:
#             # Decode the base64 image
#             image_data = base64.b64decode(carousel_image)
#             filename = secure_filename(image_name)  # Use image_name as filename
            
#             # Connect to the database
#             connection = pymysql.connect(**db_config)

#             try:
#                 with connection.cursor(pymysql.cursors.DictCursor) as cursor:
#                     sql_insert_carousel_image = '''
#                     INSERT INTO carousel_images (image_name, carousel_image, status)
#                     VALUES (%s, %s, %s)
#                     '''
#                     cursor.execute(sql_insert_carousel_image, (image_name, image_data, False))

#                 # Commit changes
#                 connection.commit()

#                 return jsonify({"message": "Post successful"}), 200

#             except Exception as e:
#                 print(f"Error processing request: {str(e)}")
#                 return jsonify({"message": "An error occurred. Please try again."}), 500

#             finally:
#                 connection.close()
        
#         except Exception as e:
#             print(f"Error processing request: {str(e)}")
#             return jsonify({"message": "An error occurred. Please try again."}), 500

#     return jsonify({"message": "User not authenticated or request processing failed."}), 401

@app.route('/carousel_image_upload', methods=['POST'])
def carousel_image_upload():
    data = request.get_json()
    image_name = data.get('image_name')
    carousel_image = data.get('carousel_image')

    if image_name and carousel_image:
        try:
            header, image_data = carousel_image.split(',', 1)
            mime_type = header.split(';')[0].split(':')[1]
            print(f"Received MIME type: {mime_type}")

            if mime_type not in ['image/jpeg', 'image/png', 'image/jpg', 'image/gif', 'image/svg+xml']:
                return jsonify({"message": "Unsupported image format. Only JPG, JPEG, PNG, GIF, and SVG formats are allowed."}), 400

            carousel_image_data = base64.b64decode(image_data)
            
            if mime_type != 'image/svg+xml':
                image = Image.open(io.BytesIO(carousel_image_data))
                image_format = image.format

                def resize_image(image, max_size_kib):
                    output_io = io.BytesIO()
                    quality = 95
                    while True:
                        output_io.seek(0)
                        image.save(output_io, format=image_format, quality=quality)
                        size = output_io.tell()
                        if size <= max_size_kib * 1024 or quality <= 5:
                            break
                        quality -= 5
                    output_io.seek(0)
                    return output_io

                if mime_type != 'image/gif':
                    resized_image_io = resize_image(image, 60)  # Resize image to fit within 60 KB
                    resized_image_data = resized_image_io.read()
                else:
                    resized_image_data = carousel_image_data
            else:
                resized_image_data = carousel_image_data

            if not resized_image_data:
                return jsonify({"message": "Invalid image data."}), 400

            filename = secure_filename(image_name)

            connection = pymysql.connect(**db_config)
            try:
                with connection.cursor(pymysql.cursors.DictCursor) as cursor:
                    sql_insert_carousel_image = '''
                    INSERT INTO carousel_images (image_name, carousel_image, status)
                    VALUES (%s, %s, %s)
                    '''
                    cursor.execute(sql_insert_carousel_image, (filename, resized_image_data, False))

                connection.commit()
                return jsonify({"message": "Post successful"}), 200

            except pymysql.MySQLError as e:
                print(f"Database error: {str(e)}")
                return jsonify({"message": f"An error occurred while saving the image. Details: {str(e)}"}), 500

            finally:
                connection.close()

        except Exception as e:
            print(f"Error processing image: {str(e)}")
            return jsonify({"message": f"An error occurred while processing the image. Details: {str(e)}"}), 500

    return jsonify({"message": "Invalid request data."}), 400


@app.route('/fetch_images_for_carousel', methods=['GET'])
def fetch_images_for_carousel():
    try:
        connection = pymysql.connect(**db_config)
        
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            sql = "SELECT * FROM carousel_images where status=1"
            cursor.execute(sql)
            rows = cursor.fetchall()

            if rows:
                images = []
                for row in rows:
                    image_data = base64.b64encode(row['carousel_image']).decode('utf-8')
                    images.append({
                        'image_id': row['image_id'],
                        'image_name': row['image_name'],
                        'carousel_image': image_data,
                        'status': row['status']
                    })
                return jsonify(images), 200
            else:
                return jsonify({"message": "No images found"}), 404

    except pymysql.MySQLError as e:
        return jsonify({"message": "A database error occurred!", "error": str(e)}), 500
    except Exception as e:
        return jsonify({"message": "An error occurred!", "error": str(e)}), 500
    finally:
        connection.close()    


@app.route('/fetch_carousel_images', methods=['GET'])
def fetch_carousel_images():
    try:
        connection = pymysql.connect(**db_config)
        
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            sql = "SELECT * FROM carousel_images ORDER BY created_at DESC"
            cursor.execute(sql)
            rows = cursor.fetchall()

            if rows:
                images = []
                for row in rows:
                    image_data = base64.b64encode(row['carousel_image']).decode('utf-8')
                    images.append({
                        'image_id': row['image_id'],
                        'image_name': row['image_name'],
                        'carousel_image': image_data,
                        'status': row['status']
                    })
                return jsonify(images), 200
            else:
                return jsonify({"message": "No images found"}), 404

    except pymysql.MySQLError as e:
        return jsonify({"message": "A database error occurred!", "error": str(e)}), 500
    except Exception as e:
        return jsonify({"message": "An error occurred!", "error": str(e)}), 500
    finally:
        connection.close()

@app.route('/update_image_status/<int:image_id>', methods=['POST'])
def update_image_status(image_id):
    try:
        data = request.get_json()
        new_status = data.get('status')

        if new_status is None:
            return jsonify({"message": "Invalid status value"}), 400

        connection = pymysql.connect(**db_config)
        with connection.cursor() as cursor:
            sql_update_status = "UPDATE carousel_images SET status = %s WHERE image_id = %s"
            cursor.execute(sql_update_status, (new_status, image_id))

        connection.commit()
        return jsonify({"message": "Status updated successfully"}), 200

    except pymysql.MySQLError as e:
        return jsonify({"message": "A database error occurred!", "error": str(e)}), 500
    except Exception as e:
        return jsonify({"message": "An error occurred!", "error": str(e)}), 500
    finally:
        connection.close()


@app.route('/delete_carousel_image/<int:image_id>', methods=['DELETE'])
def delete_carousel_image(image_id):
    try:
        # Connect to the database
        connection = pymysql.connect(**db_config)

        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            sql_delete_carousel_image = '''
            DELETE FROM carousel_images WHERE image_id = %s
            '''
            cursor.execute(sql_delete_carousel_image, (image_id,))

        # Commit changes
        connection.commit()
        
        return jsonify({"message": "Image deleted successfully."}), 200

    except pymysql.MySQLError as e:
        return jsonify({"message": "A database error occurred!", "error": str(e)}), 500
    except Exception as e:
        return jsonify({"message": "An error occurred!", "error": str(e)}), 500
    finally:
        connection.close()

@app.route('/landing_page_text_upload', methods=['POST'])
def landing_page_text_upload():
    data = request.get_json()
    heading = data.get('heading')
    second_heading = data.get('second_heading')
    about_us_text = data.get('about_us_text')
    status = False  # Default status

    if heading and second_heading and about_us_text:
        try:
            # Connect to the database
            connection = pymysql.connect(**db_config)

            try:
                with connection.cursor(pymysql.cursors.DictCursor) as cursor:
                    sql_insert_landing_page_text = '''
                    INSERT INTO landing_page_texts (heading, second_heading, about_us_text, status)
                    VALUES (%s, %s, %s, %s)
                    '''
                    cursor.execute(sql_insert_landing_page_text, (heading, second_heading, about_us_text, status))

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

    return jsonify({"message": "Invalid input or request processing failed."}), 400


@app.route('/fetch_landing_page_texts', methods=['GET'])
def fetch_landing_page_texts():
    try:
        connection = pymysql.connect(**db_config)
        
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            sql = "SELECT * FROM landing_page_texts ORDER BY created_at DESC"
            cursor.execute(sql)
            rows = cursor.fetchall()

            if rows:
                texts = []
                for row in rows:
                    texts.append({
                        'text_id': row['text_id'],
                        'heading': row['heading'],
                        'second_heading': row['second_heading'],
                        'about_us_text': row['about_us_text'],
                        'status': row['status'],
                        'created_at': row['created_at'].isoformat()  # Format timestamp
                    })
                return jsonify(texts), 200
            else:
                return jsonify({"message": "No texts found"}), 404

    except pymysql.MySQLError as e:
        return jsonify({"message": "A database error occurred!", "error": str(e)}), 500
    except Exception as e:
        return jsonify({"message": "An error occurred!", "error": str(e)}), 500
    finally:
        connection.close()

@app.route('/update_landing_page_text_status/<int:text_id>', methods=['POST'])
def update_landing_page_text_status(text_id):
    try:
        data = request.get_json()
        new_status = data.get('status')

        connection = pymysql.connect(**db_config)
        with connection.cursor() as cursor:
            sql_update_status = "UPDATE landing_page_texts SET status = %s WHERE text_id = %s"
            cursor.execute(sql_update_status, (new_status, text_id))
        
        connection.commit()
        return jsonify({"message": "Status updated successfully"}), 200

    except pymysql.MySQLError as e:
        return jsonify({"message": "A database error occurred!", "error": str(e)}), 500
    except Exception as e:
        return jsonify({"message": "An error occurred!", "error": str(e)}), 500
    finally:
        connection.close()

@app.route('/fetch_landing_page_about_us_texts', methods=['GET'])
def fetch_landing_page_about_us_texts():
    try:
        connection = pymysql.connect(**db_config)
        
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            sql = "SELECT * FROM landing_page_texts WHERE status = 1"
            cursor.execute(sql)
            rows = cursor.fetchall()

            if rows:
                texts = []
                for row in rows:
                    texts.append({
                        'text_id': row['text_id'],
                        'heading': row['heading'],
                        'second_heading': row['second_heading'],
                        'about_us_text': row['about_us_text'],
                        'status': row['status'],
                        'created_at': row['created_at'].isoformat()  # Format timestamp if needed
                    })
                return jsonify(texts), 200
            else:
                return jsonify({"message": "No texts found"}), 404

    except pymysql.MySQLError as e:
        return jsonify({"message": "A database error occurred!", "error": str(e)}), 500
    except Exception as e:
        return jsonify({"message": "An error occurred!", "error": str(e)}), 500
    finally:
        connection.close()

@app.route('/delete_landing_page_text/<int:text_id>', methods=['DELETE'])
def delete_landing_page_text(text_id):
    try:
        connection = pymysql.connect(**db_config)
        with connection.cursor() as cursor:
            sql_delete_text = "DELETE FROM landing_page_texts WHERE text_id = %s"
            cursor.execute(sql_delete_text, (text_id,))
        
        connection.commit()
        
        if cursor.rowcount == 0:
            return jsonify({"message": "Text not found"}), 404

        return jsonify({"message": "Text deleted successfully"}), 200

    except pymysql.MySQLError as e:
        return jsonify({"message": "A database error occurred!", "error": str(e)}), 500
    except Exception as e:
        return jsonify({"message": "An error occurred!", "error": str(e)}), 500
    finally:
        connection.close()


@app.route('/latest_video_upload', methods=['POST'])
def latest_video_upload():
    data = request.get_json()
    latest_link = data.get('latest_link')
    latest_title = data.get('latest_title')
    latest_details = data.get('latest_details')

    if latest_link and latest_title and latest_details:
        try:
            # Connect to the database
            connection = pymysql.connect(**db_config)

            try:
                with connection.cursor() as cursor:
                    sql_insert_latest = '''
                    INSERT INTO latest (latest_link, latest_title, latest_details)
                    VALUES (%s, %s, %s)
                    '''
                    cursor.execute(sql_insert_latest, (latest_link, latest_title, latest_details))

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

    return jsonify({"message": "Invalid input or request processing failed."}), 400


# @app.route('/fetch_latest_videos', methods=['GET'])
# def fetch_latest_videos():
#     try:
#         connection = pymysql.connect(**db_config)
#         print("Database connection established.")
        
#         with connection.cursor() as cursor:
#             sql = "SELECT * FROM latest ORDER BY created_at DESC"
#             cursor.execute(sql)
#             rows = cursor.fetchall()
#             print(f"Fetched rows: {rows}")

#             if rows:
#                 latest_data = []
#                 for row in rows:
#                     latest_data.append({
#                         'latest_id': row['latest_id'],
#                         'latest_link': row['latest_link'],
#                         'latest_title': row['latest_title'],
#                         'latest_details': row['latest_details'],
#                         'created_at': row['created_at'].strftime('%Y-%m-%d %H:%M:%S')  # Formatting the timestamp
#                     })
#                 return jsonify(latest_data), 200
#             else:
#                 return jsonify({"message": "No data found"}), 404

#     except pymysql.MySQLError as e:
#         print(f"MySQL error: {str(e)}")
#         return jsonify({"message": "A database error occurred!", "error": str(e)}), 500
#     except Exception as e:
#         print(f"Error: {str(e)}")
#         return jsonify({"message": "An error occurred!", "error": str(e)}), 500
#     finally:
#         connection.close()

@app.route('/fetch_latest_videos', methods=['GET'])
def fetch_latest_videos():
    try:
        # Fetch the search query from request parameters
        search_query = request.args.get('query', '')
        
        # Establish a connection to the database
        connection = pymysql.connect(**db_config)
        print("Database connection established.")
        
        with connection.cursor() as cursor:
            # SQL query with multiple fields using LIKE for searching
            sql = """
                SELECT latest_id, latest_link, latest_title, latest_details, created_at
                FROM latest
                WHERE latest_title LIKE %s 
                OR latest_details LIKE %s 
                ORDER BY created_at DESC
            """
            
            # Prepare the search query with wildcards for LIKE search
            wildcard_search = f"%{search_query}%"
            
            # Execute the query with the same search term applied to title and details
            cursor.execute(sql, (wildcard_search, wildcard_search))
            
            # Fetch all matching rows
            rows = cursor.fetchall()
            print(f"Fetched rows: {rows}")

            if rows:
                latest_data = []
                for row in rows:
                    latest_data.append({
                        'latest_id': row['latest_id'],
                        'latest_link': row['latest_link'],
                        'latest_title': row['latest_title'],
                        'latest_details': row['latest_details'],
                        'created_at': row['created_at'].strftime('%Y-%m-%d %H:%M:%S')  # Formatting the timestamp
                    })
                return jsonify(latest_data), 200
            else:
                return jsonify({"message": "No data found"}), 404

    except pymysql.MySQLError as e:
        print(f"MySQL error: {str(e)}")
        return jsonify({"message": "A database error occurred!", "error": str(e)}), 500
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({"message": "An error occurred!", "error": str(e)}), 500
    finally:
        connection.close()


@app.route('/fetch_latest_videos_latest', methods=['GET'])
def fetch_latest_videos_latest():
    try:
        connection = pymysql.connect(**db_config)
        print("Database connection established.")
        
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            sql = "SELECT * FROM latest ORDER BY created_at DESC LIMIT 3"
            cursor.execute(sql)
            rows = cursor.fetchall()
            print(f"Fetched rows: {rows}")

            if rows:
                latest_data = []
                for row in rows:
                    latest_data.append({
                        'latest_id': row['latest_id'],
                        'latest_link': row['latest_link'],
                        'latest_title': row['latest_title'],
                        'latest_details': row['latest_details'],
                        'created_at': row['created_at'].strftime('%Y-%m-%d %H:%M:%S')  # Formatting the timestamp
                    })
                return jsonify(latest_data), 200
            else:
                return jsonify({"message": "No data found"}), 404

    except pymysql.MySQLError as e:
        print(f"MySQL error: {str(e)}")
        return jsonify({"message": "A database error occurred!", "error": str(e)}), 500
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({"message": "An error occurred!", "error": str(e)}), 500
    finally:
        connection.close()


@app.route('/delete_latest_video/<int:video_id>', methods=['DELETE'])
def delete_latest_video(video_id):
    connection = None
    try:
        connection = pymysql.connect(**db_config)
        
        with connection.cursor() as cursor:
            sql = "DELETE FROM latest WHERE latest_id = %s"
            cursor.execute(sql, (video_id,))
            connection.commit()

            if cursor.rowcount > 0:
                return jsonify({"message": "Video deleted successfully!"}), 200
            else:
                return jsonify({"message": "Video not found!"}), 404

    except pymysql.MySQLError as e:
        print(f"MySQL error: {str(e)}")
        return jsonify({"message": "A database error occurred!", "error": str(e)}), 500
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({"message": "An error occurred!", "error": str(e)}), 500
    finally:
        if connection:
            connection.close()


# @app.route('/copy_to_trending', methods=['POST'])
# def copy_to_trending():
#     try:
#         connection = pymysql.connect(**db_config)
#         print("Database connection established.")
#         with connection.cursor() as cursor:
#             # First, get the IDs of the three most recent records in the latest table
#             cursor.execute("SELECT latest_id FROM latest ORDER BY created_at DESC LIMIT 3")
#             recent_ids = [row['latest_id'] for row in cursor.fetchall()]

#             # Now, select all records from latest except the three most recent
#             cursor.execute("""
#                 SELECT latest_link, latest_title, latest_details, created_at
#                 FROM latest
#                 WHERE latest_id NOT IN (%s, %s, %s)
#             """, tuple(recent_ids))
#             records_to_copy = cursor.fetchall()

#             # Insert these records into the trending table
#             if records_to_copy:
#                 cursor.executemany("""
#                     INSERT INTO trending (trending_link, trending_title, trending_details, created_at)
#                     VALUES (%s, %s, %s, %s)
#                 """, [(row['latest_link'], row['latest_title'], row['latest_details'], row['created_at']) for row in records_to_copy])

#                 connection.commit()
#                 return jsonify({
#                     "message": f"Successfully copied {len(records_to_copy)} records to trending table.",
#                     "copied_count": len(records_to_copy)
#                 }), 200
#             else:
#                 return jsonify({"message": "No records to copy."}), 200

#     except pymysql.MySQLError as e:
#         print(f"MySQL error: {str(e)}")
#         connection.rollback()
#         return jsonify({"message": "A database error occurred!", "error": str(e)}), 500
#     except Exception as e:
#         print(f"Error: {str(e)}")
#         connection.rollback()
#         return jsonify({"message": "An error occurred!", "error": str(e)}), 500
#     finally:
#         connection.close()

@app.route('/copy_to_trending', methods=['POST'])
def copy_to_trending():
    try:
        connection = pymysql.connect(**db_config)
        print("Database connection established.")
        with connection.cursor() as cursor:
            # First, get the IDs of the three most recent records in the latest table
            cursor.execute("SELECT latest_id FROM latest ORDER BY created_at DESC LIMIT 3")
            recent_ids = [row['latest_id'] for row in cursor.fetchall()]

            # Now, select all records from latest except the three most recent
            cursor.execute("""
                SELECT latest_link, latest_title, latest_details, created_at
                FROM latest
                WHERE latest_id NOT IN (%s, %s, %s)
            """, tuple(recent_ids))
            records_to_copy = cursor.fetchall()

            # Clear the trending table
            cursor.execute("DELETE FROM trending")

            # Insert these records into the trending table
            if records_to_copy:
                cursor.executemany("""
                    INSERT INTO trending (trending_link, trending_title, trending_details, created_at)
                    VALUES (%s, %s, %s, %s)
                """, [(row['latest_link'], row['latest_title'], row['latest_details'], row['created_at']) for row in records_to_copy])

                connection.commit()
                return jsonify({
                    "message": f"Successfully copied {len(records_to_copy)} records to trending table.",
                    "copied_count": len(records_to_copy)
                }), 200
            else:
                return jsonify({"message": "No records to copy."}), 200

    except pymysql.MySQLError as e:
        print(f"MySQL error: {str(e)}")
        connection.rollback()
        return jsonify({"message": "A database error occurred!", "error": str(e)}), 500
    except Exception as e:
        print(f"Error: {str(e)}")
        connection.rollback()
        return jsonify({"message": "An error occurred!", "error": str(e)}), 500
    finally:
        connection.close()


@app.route('/fetch_trending_videos_trending', methods=['GET'])
def fetch_trending_videos_trending():
    try:
        connection = pymysql.connect(**db_config)
        print("Database connection established.")
        
        with connection.cursor() as cursor:
            sql = "SELECT * FROM trending ORDER BY created_at DESC"
            cursor.execute(sql)
            rows = cursor.fetchall()
            print(f"Fetched rows: {rows}")

            if rows:
                trending_data = []
                for row in rows:
                    trending_data.append({
                        'trending_id': row['trending_id'],
                        'trending_link': row['trending_link'],
                        'trending_title': row['trending_title'],
                        'trending_details': row['trending_details'],
                        'created_at': row['created_at'].strftime('%Y-%m-%d %H:%M:%S')  # Formatting the timestamp
                    })
                return jsonify(trending_data), 200
            else:
                return jsonify({"message": "No data found"}), 404

    except pymysql.MySQLError as e:
        print(f"MySQL error: {str(e)}")
        return jsonify({"message": "A database error occurred!", "error": str(e)}), 500
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({"message": "An error occurred!", "error": str(e)}), 500
    finally:
        connection.close()

@app.route('/delete_trending_video/<int:trending_id>', methods=['DELETE'])
def delete_trending_video(trending_id):
    try:
        connection = pymysql.connect(**db_config)
        print("Database connection established.")
        
        with connection.cursor() as cursor:
            sql = "DELETE FROM trending WHERE trending_id = %s"
            result = cursor.execute(sql, (trending_id,))
            connection.commit()

            if result:
                print(f"Deleted record with trending_id: {trending_id}")
                return jsonify({"message": "Record deleted successfully"}), 200
            else:
                print(f"No record found with trending_id: {trending_id}")
                return jsonify({"message": "Record not found"}), 404

    except pymysql.MySQLError as e:
        print(f"MySQL error: {str(e)}")
        return jsonify({"message": "A database error occurred!", "error": str(e)}), 500
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({"message": "An error occurred!", "error": str(e)}), 500
    finally:
        try:
            connection.close()
            print("Database connection closed.")
        except Exception as e:
            print(f"Error closing connection: {str(e)}")

@app.route('/fetch_trending_videos', methods=['GET'])
def fetch_trending_videos():
    try:
        connection = pymysql.connect(**db_config)
        print("Database connection established.")
        
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            sql = "SELECT * FROM trending ORDER BY created_at DESC LIMIT 3"
            cursor.execute(sql)
            rows = cursor.fetchall()
            print(f"Fetched rows: {rows}")

            if rows:
                trending_data = []
                for row in rows:
                    trending_data.append({
                        'trending_id': row['trending_id'],
                        'trending_link': row['trending_link'],
                        'trending_title': row['trending_title'],
                        'trending_details': row['trending_details'],
                        'created_at': row['created_at'].strftime('%Y-%m-%d %H:%M:%S')  # Formatting the timestamp
                    })
                return jsonify(trending_data), 200
            else:
                return jsonify({"message": "No data found"}), 404

    except pymysql.MySQLError as e:
        print(f"MySQL error: {str(e)}")
        return jsonify({"message": "A database error occurred!", "error": str(e)}), 500
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({"message": "An error occurred!", "error": str(e)}), 500
    finally:
        connection.close()
          
# @app.route('/seminer_upload', methods=['POST'])
# def seminer_upload():
#     data = request.get_json()
#     seminer_date = data.get('seminer_date')
#     seminer_name = data.get('seminer_name')
#     seminer_details = data.get('seminer_details')
#     seminer_image = data.get('seminer_image')
#     status = False  # Default status
#     created_at = None  # Will be set by the database

#     if seminer_date and seminer_name and seminer_details and seminer_image:
#         try:
#             # Decode base64 image
#             seminer_image_data = base64.b64decode(seminer_image)

#             # Connect to the database
#             connection = pymysql.connect(**db_config)

#             try:
#                 with connection.cursor() as cursor:
#                     sql_insert_seminer = '''
#                     INSERT INTO seminers (seminer_date, seminer_name, seminer_details, seminer_image, status, created_at)
#                     VALUES (%s, %s, %s, %s, %s, CURRENT_TIMESTAMP)
#                     '''
#                     cursor.execute(sql_insert_seminer, (seminer_date, seminer_name, seminer_details, seminer_image_data, status))

#                 # Commit changes
#                 connection.commit()

#                 return jsonify({"message": "Seminar upload successful"}), 200

#             except Exception as e:
#                 print(f"Error processing request: {str(e)}")
#                 return jsonify({"message": "An error occurred. Please try again."}), 500

#             finally:
#                 connection.close()

#         except Exception as e:
#             print(f"Error processing request: {str(e)}")
#             return jsonify({"message": "An error occurred. Please try again."}), 500

#     return jsonify({"message": "Invalid input or request processing failed."}), 400

# @app.route('/seminer_upload', methods=['POST'])
# def seminer_upload():
#     data = request.get_json()
#     seminer_date = data.get('seminer_date')
#     seminer_name = data.get('seminer_name')
#     seminer_details = data.get('seminer_details')
#     seminer_image = data.get('seminer_image')
#     status = False  # Default status

#     if seminer_date and seminer_name and seminer_details and seminer_image:
#         try:
#             # Check if the base64 string starts with the data URL scheme
#             if not seminer_image.startswith('data:image/'):
#                 return jsonify({"message": "Invalid image format."}), 400

#             # Extract the MIME type and base64 data
#             header, image_data = seminer_image.split(',', 1)
#             mime_type = header.split(';')[0].split(':')[1]
#             if mime_type not in ['image/jpeg', 'image/png', 'image/jpg']:
#                 return jsonify({"message": "Unsupported image format. Only JPG, JPEG, and PNG are allowed."}), 400

#             # Decode base64 image
#             seminer_image_data = base64.b64decode(image_data)

#             # Connect to the database
#             connection = pymysql.connect(**db_config)

#             try:
#                 with connection.cursor() as cursor:
#                     sql_insert_seminer = '''
#                     INSERT INTO seminers (seminer_date, seminer_name, seminer_details, seminer_image, status, created_at)
#                     VALUES (%s, %s, %s, %s, %s, CURRENT_TIMESTAMP)
#                     '''
#                     cursor.execute(sql_insert_seminer, (seminer_date, seminer_name, seminer_details, seminer_image_data, status))

#                 # Commit changes
#                 connection.commit()

#                 return jsonify({"message": "Seminar upload successful"}), 200

#             except pymysql.MySQLError as e:
#                 print(f"Database error: {e}")
#                 return jsonify({"message": "A database error occurred!", "error": str(e)}), 500

#             except Exception as e:
#                 print(f"Error processing request: {str(e)}")
#                 return jsonify({"message": "An error occurred. Please try again."}), 500

#             finally:
#                 connection.close()

#         except Exception as e:
#             print(f"Error processing request: {str(e)}")
#             return jsonify({"message": "An error occurred. Please try again."}), 500

#     return jsonify({"message": "Invalid input or request processing failed."}), 400

@app.route('/seminer_upload', methods=['POST'])
def seminer_upload():
    data = request.get_json()
    seminer_date = data.get('seminer_date')
    seminer_name = data.get('seminer_name')
    seminer_details = data.get('seminer_details')
    seminer_image = data.get('seminer_image')
    status = False  # Default status

    if seminer_date and seminer_name and seminer_details and seminer_image:
        try:
            # Check if the base64 string starts with the data URL scheme
            if not seminer_image.startswith('data:image/'):
                return jsonify({"message": "Invalid image format."}), 400

            # Extract the MIME type and base64 data
            header, image_data = seminer_image.split(',', 1)
            mime_type = header.split(';')[0].split(':')[1]
            if mime_type not in ['image/jpeg', 'image/png', 'image/jpg']:
                return jsonify({"message": "Unsupported image format. Only JPG, JPEG, and PNG are allowed."}), 400

            # Decode base64 image
            seminer_image_data = base64.b64decode(image_data)

            # Resize image to be under 60KB
            image = Image.open(io.BytesIO(seminer_image_data))
            image_format = image.format

            def resize_image(image, max_size_kib):
                output_io = io.BytesIO()
                quality = 95
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

            # Connect to the database
            connection = pymysql.connect(**db_config)

            try:
                with connection.cursor() as cursor:
                    sql_insert_seminer = '''
                    INSERT INTO seminers (seminer_date, seminer_name, seminer_details, seminer_image, status, created_at)
                    VALUES (%s, %s, %s, %s, %s, CURRENT_TIMESTAMP)
                    '''
                    cursor.execute(sql_insert_seminer, (seminer_date, seminer_name, seminer_details, resized_image_data, status))

                # Commit changes
                connection.commit()
                return jsonify({"message": "Seminar upload successful"}), 200

            except pymysql.MySQLError as e:
                print(f"Database error: {e}")
                return jsonify({"message": "A database error occurred!", "error": str(e)}), 500

            except Exception as e:
                print(f"Error processing request: {str(e)}")
                return jsonify({"message": "An error occurred. Please try again."}), 500

            finally:
                connection.close()

        except Exception as e:
            print(f"Error processing request: {str(e)}")
            return jsonify({"message": "An error occurred. Please try again."}), 500

    return jsonify({"message": "Invalid input or request processing failed."}), 400



@app.route('/fetch_seminers', methods=['GET'])
def fetch_seminers():
    try:
        connection = pymysql.connect(**db_config)
        
        with connection.cursor() as cursor:
            sql = "SELECT * FROM seminers ORDER BY created_at DESC"
            cursor.execute(sql)
            rows = cursor.fetchall()

            if rows:
                seminers = []
                for row in rows:
                    # Encode image data as base64
                    image_data = base64.b64encode(row['seminer_image']).decode('utf-8') if row['seminer_image'] else None
                    seminers.append({
                        'seminer_id': row['seminer_id'],
                        'seminer_date': row['seminer_date'],
                        'seminer_name': row['seminer_name'],
                        'seminer_details': row['seminer_details'],
                        'status': row['status'],
                        'created_at': row['created_at'],
                        'seminer_image': image_data
                    })
                return jsonify(seminers), 200
            else:
                return jsonify({"message": "No seminar records found"}), 404

    except pymysql.MySQLError as e:
        # Detailed error message
        return jsonify({"message": "A database error occurred!", "error": str(e)}), 500
    except Exception as e:
        # Detailed error message
        return jsonify({"message": "An error occurred!", "error": str(e)}), 500
    finally:
        connection.close()



@app.route('/fetch_seminer_image', methods=['GET'])
def fetch_seminer_image():
    try:
        connection = pymysql.connect(**db_config)
        
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            sql = "SELECT seminer_image FROM seminers WHERE status = 1"
            cursor.execute(sql)
            rows = cursor.fetchall()

            if rows:
                seminers = []
                for row in rows:
                    # Encode image data as base64
                    image_data = base64.b64encode(row['seminer_image']).decode('utf-8') if row['seminer_image'] else None
                    seminers.append({
                        'seminer_image': image_data
                    })
                return jsonify(seminers), 200
            else:
                return jsonify({"message": "No seminar records found"}), 404

    except pymysql.MySQLError as e:
        return jsonify({"message": "A database error occurred!", "error": str(e)}), 500
    except Exception as e:
        return jsonify({"message": "An error occurred!", "error": str(e)}), 500
    finally:
        connection.close()  

@app.route('/update_seminar_status/<int:seminer_id>', methods=['POST'])
def update_seminar_status(seminer_id):
    print(f"Received request to update seminar with ID: {seminer_id}")
    try:
        data = request.get_json()
        print(f"Request data: {data}")

        new_status = data.get('status')
        if new_status not in [0, 1]:
            return jsonify({"message": "Invalid status value. Must be 0 or 1."}), 400

        connection = pymysql.connect(**db_config)
        with connection.cursor() as cursor:
            sql_update_status = "UPDATE seminers SET status = %s WHERE seminer_id = %s"
            cursor.execute(sql_update_status, (new_status, seminer_id))
        
        connection.commit()
        return jsonify({"message": "Status updated successfully"}), 200

    except pymysql.MySQLError as e:
        print(f"Database error: {e}")
        return jsonify({"message": "A database error occurred!", "error": str(e)}), 500
    except Exception as e:
        print(f"General error: {e}")
        return jsonify({"message": "An error occurred!", "error": str(e)}), 500
    finally:
        connection.close()

@app.route('/delete_seminar/<int:seminer_id>', methods=['DELETE'])
def delete_seminar(seminer_id):
    print(f"Received request to delete seminar with ID: {seminer_id}")
    try:
        connection = pymysql.connect(**db_config)
        with connection.cursor() as cursor:
            # First, check if the seminar exists
            sql_check_existence = "SELECT * FROM seminers WHERE seminer_id = %s"
            cursor.execute(sql_check_existence, (seminer_id,))
            result = cursor.fetchone()

            if not result:
                return jsonify({"message": "Seminar not found"}), 404

            # If seminar exists, delete it
            sql_delete = "DELETE FROM seminers WHERE seminer_id = %s"
            cursor.execute(sql_delete, (seminer_id,))
            connection.commit()
            return jsonify({"message": "Seminar deleted successfully"}), 200

    except pymysql.MySQLError as e:
        print(f"Database error: {e}")
        return jsonify({"message": "A database error occurred!", "error": str(e)}), 500
    except Exception as e:
        print(f"General error: {e}")
        return jsonify({"message": "An error occurred!", "error": str(e)}), 500
    finally:
        connection.close()

@app.route('/fetch_seminers_last_two', methods=['GET'])
def fetch_seminers_last_two():
    try:
        connection = pymysql.connect(**db_config)
        
        with connection.cursor() as cursor:
            sql = "SELECT * FROM seminers ORDER BY created_at DESC LIMIT 2"
            cursor.execute(sql)
            rows = cursor.fetchall()

            if rows:
                seminers = []
                for row in rows:
                    # Convert the image BLOB to a base64 string
                    seminer_image_base64 = base64.b64encode(row['seminer_image']).decode('utf-8')
                    
                    seminers.append({
                        'seminer_id': row['seminer_id'],
                        'seminer_date': row['seminer_date'],
                        'seminer_name': row['seminer_name'],
                        'seminer_details': row['seminer_details'],
                        'status': row['status'],
                        'seminer_image': seminer_image_base64  # Add the base64-encoded image
                    })
                return jsonify(seminers), 200
            else:
                return jsonify({"message": "No seminar records found"}), 404

    except pymysql.MySQLError as e:
        return jsonify({"message": "A database error occurred!", "error": str(e)}), 500
    except Exception as e:
        return jsonify({"message": "An error occurred!", "error": str(e)}), 500
    finally:
        connection.close()      

@app.route('/success_story_upload', methods=['POST'])
def success_story_upload():
    data = request.get_json()
    success_link = data.get('success_link')
    success_title = data.get('success_title')
    success_details = data.get('success_details')
    success_image = data.get('success_image')
    
    if success_link and success_title and success_details and success_image:
        try:
            # Check if the base64 string starts with the data URL scheme
            if not success_image.startswith('data:image/'):
                return jsonify({"message": "Invalid image format."}), 400

            # Extract the MIME type and base64 data
            header, image_data = success_image.split(',', 1)
            mime_type = header.split(';')[0].split(':')[1]
            if mime_type not in ['image/jpeg', 'image/png', 'image/jpg']:
                return jsonify({"message": "Unsupported image format. Only JPG, JPEG, and PNG are allowed."}), 400

            # Decode base64 image
            success_image_data = base64.b64decode(image_data)

            # Resize image to be under 60KB
            image = Image.open(io.BytesIO(success_image_data))
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

            # Connect to the database
            connection = pymysql.connect(**db_config)

            try:
                with connection.cursor() as cursor:
                    sql_insert_success_story = '''
                    INSERT INTO success_stories (success_link, success_title, success_details, success_image, created_at)
                    VALUES (%s, %s, %s, %s, CURRENT_TIMESTAMP)
                    '''
                    cursor.execute(sql_insert_success_story, (success_link, success_title, success_details, resized_image_data))

                # Commit changes
                connection.commit()

                return jsonify({"message": "Success story upload successful"}), 200

            except pymysql.MySQLError as e:
                print(f"Database error: {e}")
                return jsonify({"message": "A database error occurred!", "error": str(e)}), 500

            except Exception as e:
                print(f"Error processing request: {str(e)}")
                return jsonify({"message": "An error occurred. Please try again."}), 500

            finally:
                connection.close()

        except Exception as e:
            print(f"Error processing request: {str(e)}")
            return jsonify({"message": "An error occurred. Please try again."}), 500

    return jsonify({"message": "Invalid input or request processing failed."}), 400


@app.route('/fetch_success_stories', methods=['GET'])
def fetch_success_stories():
    try:
        connection = pymysql.connect(**db_config)
        
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            sql = "SELECT * FROM success_stories ORDER BY created_at DESC"
            cursor.execute(sql)
            rows = cursor.fetchall()

            if rows:
                success_stories = []
                for row in rows:
                    # Encode image data as base64
                    image_data = base64.b64encode(row['success_image']).decode('utf-8') if row['success_image'] else None
                    success_stories.append({
                        'success_id': row['success_id'],
                        'success_link': row['success_link'],
                        'success_title': row['success_title'],
                        'success_details': row['success_details'],
                        'success_image': image_data
                    })
                return jsonify(success_stories), 200
            else:
                return jsonify({"message": "No success stories found"}), 404

    except pymysql.MySQLError as e:
        # Detailed error message
        return jsonify({"message": "A database error occurred!", "error": str(e)}), 500
    except Exception as e:
        # Detailed error message
        return jsonify({"message": "An error occurred!", "error": str(e)}), 500
    finally:
        connection.close()

@app.route('/fetch_latest_success_stories', methods=['GET'])
def fetch_latest_success_stories():
    try:
        connection = pymysql.connect(**db_config)
        
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            sql = "SELECT * FROM success_stories ORDER BY created_at DESC LIMIT 4"
            cursor.execute(sql)
            rows = cursor.fetchall()
            
            if rows:
                success_stories = []
                for row in rows:
                    image_data = base64.b64encode(row['success_image']).decode('utf-8') if row['success_image'] else None
                    success_stories.append({
                        'success_id': row['success_id'],
                        'success_link': row['success_link'],
                        'success_title': row['success_title'],
                        'success_details': row['success_details'],
                        'success_image': image_data
                    })
                return jsonify(success_stories), 200
            else:
                return jsonify({"message": "No success stories found"}), 404
    
    except pymysql.MySQLError as e:
        return jsonify({"message": "A database error occurred!", "error": str(e)}), 500
    except Exception as e:
        return jsonify({"message": "An error occurred!", "error": str(e)}), 500
    finally:
        connection.close()      


@app.route('/delete_success_story/<int:success_id>', methods=['DELETE'])
def delete_success_story(success_id):
    print(f"Received request to delete success story with ID: {success_id}")
    try:
        connection = pymysql.connect(**db_config)
        with connection.cursor() as cursor:
            # First, check if the success story exists
            sql_check_existence = "SELECT * FROM success_stories WHERE success_id = %s"
            cursor.execute(sql_check_existence, (success_id,))
            result = cursor.fetchone()

            if not result:
                return jsonify({"message": "Success story not found"}), 404

            # If success story exists, delete it
            sql_delete = "DELETE FROM success_stories WHERE success_id = %s"
            cursor.execute(sql_delete, (success_id,))
            connection.commit()
            return jsonify({"message": "Success story deleted successfully"}), 200

    except pymysql.MySQLError as e:
        print(f"Database error: {e}")
        return jsonify({"message": "A database error occurred!", "error": str(e)}), 500
    except Exception as e:
        print(f"General error: {e}")
        return jsonify({"message": "An error occurred!", "error": str(e)}), 500
    finally:
        connection.close()
        

@app.route('/admin_blog_upload', methods=['POST'])
def admin_blog_upload():
    data = request.get_json()
    
    # Debugging print statements
    print("Received data:", data)

    admin_blog_writer = data.get('admin_blog_writer')
    admin_blog_headline = data.get('admin_blog_headline')
    admin_blog_details = data.get('admin_blog_details')
    admin_blog_image = data.get('admin_blog_image')
    
    if admin_blog_writer and admin_blog_headline and admin_blog_details and admin_blog_image:
        try:
            if not admin_blog_image.startswith('data:image/'):
                return jsonify({"message": "Invalid image format."}), 400

            header, image_data = admin_blog_image.split(',', 1)
            mime_type = header.split(';')[0].split(':')[1]
            if mime_type not in ['image/jpeg', 'image/png', 'image/jpg']:
                return jsonify({"message": "Unsupported image format. Only JPG, JPEG, and PNG are allowed."}), 400

            admin_blog_image_data = base64.b64decode(image_data)

            image = Image.open(io.BytesIO(admin_blog_image_data))
            image_format = image.format

            def resize_image(image, max_size_kib):
                output_io = io.BytesIO()
                quality = 95
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

            connection = pymysql.connect(**db_config)

            try:
                with connection.cursor() as cursor:
                    sql_insert_blog = '''
                    INSERT INTO admin_blog (admin_blog_writer, admin_blog_headline, admin_blog_details, admin_blog_image, created_at)
                    VALUES (%s, %s, %s, %s, CURRENT_TIMESTAMP)
                    '''
                    cursor.execute(sql_insert_blog, (admin_blog_writer, admin_blog_headline, admin_blog_details, resized_image_data))

                connection.commit()

                return jsonify({"message": "Admin blog upload successful"}), 200

            except pymysql.MySQLError as e:
                print(f"Database error: {e}")
                return jsonify({"message": "A database error occurred!", "error": str(e)}), 500

            except Exception as e:
                print(f"Error processing request: {str(e)}")
                return jsonify({"message": "An error occurred. Please try again."}), 500

            finally:
                connection.close()

        except Exception as e:
            print(f"Error processing request: {str(e)}")
            return jsonify({"message": "An error occurred. Please try again."}), 500

    return jsonify({"message": "Invalid input or request processing failed."}), 400



@app.route('/fetch_admin_blog', methods=['GET'])
def fetch_admin_blog():
    try:
        connection = pymysql.connect(**db_config)
        
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            sql = "SELECT * FROM admin_blog ORDER BY created_at DESC"
            cursor.execute(sql)
            rows = cursor.fetchall()

            if rows:
                admin_blogs = []
                for row in rows:
                    # Encode image data as base64
                    image_data = base64.b64encode(row['admin_blog_image']).decode('utf-8') if row['admin_blog_image'] else None
                    admin_blogs.append({
                        'admin_blog_id': row['admin_blog_id'],
                        'admin_blog_writer': row['admin_blog_writer'],
                        'admin_blog_headline': row['admin_blog_headline'],
                        'admin_blog_details': row['admin_blog_details'],
                        'admin_blog_image': image_data,
                    })
                return jsonify(admin_blogs), 200
            else:
                return jsonify({"message": "No admin blogs found"}), 404

    except pymysql.MySQLError as e:
        # Detailed error message
        return jsonify({"message": "A database error occurred!", "error": str(e)}), 500
    except Exception as e:
        # Detailed error message
        return jsonify({"message": "An error occurred!", "error": str(e)}), 500
    finally:
        connection.close()

@app.route('/delete_admin_blog/<int:admin_blog_id>', methods=['DELETE'])
def delete_admin_blog(admin_blog_id):
    print(f"Received request to delete admin blog with ID: {admin_blog_id}")
    try:
        connection = pymysql.connect(**db_config)
        with connection.cursor() as cursor:
            # First, check if the admin blog exists
            sql_check_existence = "SELECT * FROM admin_blog WHERE admin_blog_id = %s"
            cursor.execute(sql_check_existence, (admin_blog_id,))
            result = cursor.fetchone()

            if not result:
                return jsonify({"message": "Admin blog not found"}), 404

            # If admin blog exists, delete it
            sql_delete = "DELETE FROM admin_blog WHERE admin_blog_id = %s"
            cursor.execute(sql_delete, (admin_blog_id,))
            connection.commit()
            return jsonify({"message": "Admin blog deleted successfully"}), 200

    except pymysql.MySQLError as e:
        print(f"Database error: {e}")
        return jsonify({"message": "A database error occurred!", "error": str(e)}), 500
    except Exception as e:
        print(f"General error: {e}")
        return jsonify({"message": "An error occurred!", "error": str(e)}), 500
    finally:
        connection.close()

@app.route('/fetch_admin_blog_three')
def fetch_admin_blog_three():
    try:
        connection = pymysql.connect(**db_config)
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            sql = "SELECT * FROM admin_blog ORDER BY created_at DESC LIMIT 3"
            cursor.execute(sql)
            rows = cursor.fetchall()

            blogs = []
            for row in rows:
                image_data = base64.b64encode(row['admin_blog_image']).decode('utf-8') if row['admin_blog_image'] else None
                blog = {
                    'admin_blog_id': row['admin_blog_id'],  
                    'admin_blog_writer': row['admin_blog_writer'],
                    'admin_blog_headline': row['admin_blog_headline'],
                    'admin_blog_details': row['admin_blog_details'],
                    'admin_blog_image': image_data,
                    'created_at': row['created_at'].isoformat()
                }
                blogs.append(blog)

            return jsonify(blogs), 200
    except pymysql.MySQLError as e:
        return jsonify({"message": "A database error occurred!", "error": str(e)}), 500
    except Exception as e:
        return jsonify({"message": "An error occurred!", "error": str(e)}), 500
    finally:
        connection.close()

@app.route('/fetch_blog/<int:admin_blog_id>', methods=['GET'])
def fetch_blog(admin_blog_id):
    try:
        connection = pymysql.connect(**db_config)
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            sql = "SELECT * FROM admin_blog WHERE admin_blog_id = %s"
            cursor.execute(sql, (admin_blog_id,))
            row = cursor.fetchone()

            if row:
                image_data = base64.b64encode(row['admin_blog_image']).decode('utf-8') if row['admin_blog_image'] else None
                blog = {
                    'admin_blog_id': row['admin_blog_id'],
                    'admin_blog_writer': row['admin_blog_writer'],
                    'admin_blog_headline': row['admin_blog_headline'],
                    'admin_blog_details': row['admin_blog_details'],
                    'admin_blog_image': image_data,
                    'created_at': row['created_at'].isoformat()
                }
                return jsonify(blog), 200
            else:
                return jsonify({"message": "Blog not found"}), 404

    except pymysql.MySQLError as e:
        return jsonify({"message": "A database error occurred!", "error": str(e)}), 500
    except Exception as e:
        return jsonify({"message": "An error occurred!", "error": str(e)}), 500
    finally:
        connection.close()


@app.route('/course_video_upload', methods=['POST'])
def course_video_upload():
    data = request.get_json()
    course_link = data.get('course_link')
    course_title = data.get('course_title')
    course_details = data.get('course_details')

    if course_link and course_title and course_details:
        try:
            # Connect to the database
            connection = pymysql.connect(**db_config)

            try:
                with connection.cursor() as cursor:
                    sql_insert_course = '''
                    INSERT INTO video_courses (course_link, course_title, course_details)
                    VALUES (%s, %s, %s)
                    '''
                    cursor.execute(sql_insert_course, (course_link, course_title, course_details))

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

    return jsonify({"message": "Invalid input or request processing failed."}), 400


@app.route('/course_video_edit/<int:course_id>', methods=['POST'])
def course_video_edit(course_id):
    data = request.get_json()
    course_link = data.get('course_link')
    course_title = data.get('course_title')
    course_details = data.get('course_details')

    if course_link and course_title and course_details:
        try:
            # Connect to the database
            connection = pymysql.connect(**db_config)

            try:
                with connection.cursor() as cursor:
                    sql_update_course = '''
                    UPDATE video_courses
                    SET course_link = %s, course_title = %s, course_details = %s
                    WHERE id = %s
                    '''
                    cursor.execute(sql_update_course, (course_link, course_title, course_details, course_id))

                # Commit changes
                connection.commit()

                if cursor.rowcount == 0:
                    return jsonify({"message": "No course found with the given ID."}), 404

                return jsonify({"message": "Course updated successfully"}), 200

            except Exception as e:
                print(f"Error processing request: {str(e)}")
                return jsonify({"message": "An error occurred. Please try again."}), 500

            finally:
                connection.close()

        except Exception as e:
            print(f"Error processing request: {str(e)}")
            return jsonify({"message": "An error occurred. Please try again."}), 500

    return jsonify({"message": "Invalid input or request processing failed."}), 400



# @app.route('/fetch_course_videos', methods=['GET'])
# def fetch_course_videos():
#     try:
#         connection = pymysql.connect(**db_config)
#         print("Database connection established.")
        
#         with connection.cursor() as cursor:
#             sql = "SELECT * FROM video_courses ORDER BY created_at DESC"
#             cursor.execute(sql)
#             rows = cursor.fetchall()
#             print(f"Fetched rows: {rows}")

#             if rows:
#                 course_data = []
#                 for row in rows:
#                     course_data.append({
#                         'course_id': row['course_id'],
#                         'course_link': row['course_link'],
#                         'course_title': row['course_title'],
#                         'course_details': row['course_details'],
#                         'created_at': row['created_at'].strftime('%Y-%m-%d %H:%M:%S')  # Formatting the timestamp
#                     })
#                 return jsonify(course_data), 200
#             else:
#                 return jsonify({"message": "No data found"}), 404

#     except pymysql.MySQLError as e:
#         print(f"MySQL error: {str(e)}")
#         return jsonify({"message": "A database error occurred!", "error": str(e)}), 500
#     except Exception as e:
#         print(f"Error: {str(e)}")
#         return jsonify({"message": "An error occurred!", "error": str(e)}), 500
#     finally:
#         connection.close()

@app.route('/fetch_course_videos', methods=['GET'])
def fetch_course_videos():
    try:
        # Fetch the search query from request parameters
        search_query = request.args.get('query', '')
        
        # Establish a connection to the database
        connection = pymysql.connect(**db_config)
        
        with connection.cursor() as cursor:
            # SQL query with multiple fields using LIKE for searching
            sql = """
                SELECT course_id, course_link, course_title, course_details, created_at
                FROM video_courses
                WHERE course_link LIKE %s 
                OR course_title LIKE %s 
                OR course_details LIKE %s 
                OR created_at LIKE %s
                ORDER BY created_at DESC
            """
            
            # Prepare the search query with wildcards for LIKE search
            wildcard_search = f"%{search_query}%"
            
            # Execute the query with the same search term applied to all fields
            cursor.execute(sql, (wildcard_search, wildcard_search, wildcard_search, wildcard_search))
            
            # Fetch all matching rows
            data = cursor.fetchall()
            
            # Return the fetched data as a JSON response
            return jsonify(data), 200

    except Exception as e:
        # Handle any errors that occur during the process
        return jsonify({"message": "An error occurred!", "error": str(e)}), 500
    finally:
        # Ensure the connection is closed even if an error occurs
        connection.close()


@app.route('/fetch_course_videos_latest', methods=['GET'])
def fetch_course_videos_latest():
    try:
        connection = pymysql.connect(**db_config)
        print("Database connection established.")
        
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            sql = "SELECT * FROM video_courses ORDER BY created_at DESC LIMIT 3"
            cursor.execute(sql)
            rows = cursor.fetchall()
            print(f"Fetched rows: {rows}")

            if rows:
                course_data = []
                for row in rows:
                    course_data.append({
                        'course_id': row['course_id'],
                        'course_link': row['course_link'],
                        'course_title': row['course_title'],
                        'course_details': row['course_details'],
                        'created_at': row['created_at'].strftime('%Y-%m-%d %H:%M:%S')  # Formatting the timestamp
                    })
                return jsonify(course_data), 200
            else:
                return jsonify({"message": "No data found"}), 404

    except pymysql.MySQLError as e:
        print(f"MySQL error: {str(e)}")
        return jsonify({"message": "A database error occurred!", "error": str(e)}), 500
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({"message": "An error occurred!", "error": str(e)}), 500
    finally:
        connection.close()


@app.route('/delete_course_video/<int:video_id>', methods=['DELETE'])
def delete_course_video(video_id):
    connection = None
    try:
        connection = pymysql.connect(**db_config)
        
        with connection.cursor() as cursor:
            sql = "DELETE FROM video_courses WHERE course_id = %s"
            cursor.execute(sql, (video_id,))
            connection.commit()

            if cursor.rowcount > 0:
                return jsonify({"message": "Video deleted successfully!"}), 200
            else:
                return jsonify({"message": "Video not found!"}), 404

    except pymysql.MySQLError as e:
        print(f"MySQL error: {str(e)}")
        return jsonify({"message": "A database error occurred!", "error": str(e)}), 500
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({"message": "An error occurred!", "error": str(e)}), 500
    finally:
        if connection:
            connection.close()
