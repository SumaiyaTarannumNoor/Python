########################################################################################################################################################################################

################################################################ N   E   W        V   E   R   S   I   O   N ############################################################################

############################################################# Integrated In - https://freelancingpathshala.com/ ########################################################################

@app.route('/user_blog', methods=['POST'])
def user_blog():
    if 'logged_in' in session and session['logged_in']:
        try:
            # Get user's email from session
            email = session['user_email']
            
            # Extract form data
            emojiText = request.form.get('emojiText')
            imageFile = request.files.get('imageFile')
            
            # Set image_data to None if not provided
            image_data = None
            if imageFile:
                # Read the file
                file_data = imageFile.read()
                
                # Get MIME type
                mime_type = imageFile.content_type
                print(f"Received MIME type: {mime_type}")
                
                if mime_type not in ['image/jpeg', 'image/png', 'image/jpg', 'image/gif', 'image/svg+xml']:
                    return jsonify({"message": "Unsupported image format. Only JPG, JPEG, PNG, GIF, and SVG formats are allowed."}), 400
                
                if mime_type != 'image/svg+xml':
                    image = Image.open(io.BytesIO(file_data))
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
                        image_data = resized_image_io.getvalue()
                    else:
                        image_data = file_data
                else:
                    image_data = file_data
                
                if not image_data:
                    return jsonify({"message": "Invalid image data."}), 400
            
            # Connect to the database
            connection = pymysql.connect(**db_config)
            
            try:
                with connection.cursor(pymysql.cursors.DictCursor) as cursor:
                    # First, fetch user details from student_signup table
                    sql_fetch_user = """
                    SELECT Full_name, Image
                    FROM student_signup
                    WHERE Email = %s
                    """
                    cursor.execute(sql_fetch_user, (email,))
                    user_data = cursor.fetchone()
                    
                    if not user_data:
                        return jsonify({"message": "User not found"}), 404
                    
                    user_name = user_data['Full_name']
                    user_image = user_data['Image']
                    
                    # Now insert data into user_blog table
                    sql_insert_blog = '''
                    INSERT INTO user_blog (email, emojiText, imageFile, approve, user_name, user_image)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    '''
                    cursor.execute(sql_insert_blog, (email, emojiText, image_data, False, user_name, user_image))
                
                # Commit changes
                connection.commit()
                
                return jsonify({"message": "Post successful"}), 200
            
            finally:
                connection.close()
        
        except Exception as e:
            print(f"Error processing request: {str(e)}")
            return jsonify({"message": "An error occurred. Please try again."}), 500
    
    return jsonify({"message": "User not authenticated or request processing failed."}), 401

########### OLD VERSION ###############
@app.route('/user_blog', methods=['POST'])
def user_blog():
    if 'logged_in' in session and session['logged_in']:
        try:
            # Get user's email from session
            email = session['user_email']
            
            # Extract form data
            emojiText = request.form.get('emojiText')
            imageFile = request.files.get('imageFile')
            
            # Set image_data to None if not provided
            image_data = None
            if imageFile:
                filename = secure_filename(imageFile.filename)
                image_data = imageFile.read()
            
            # Connect to the database
            connection = pymysql.connect(**db_config)
            
            try:
                with connection.cursor(pymysql.cursors.DictCursor) as cursor:
                    # First, fetch user details from student_signup table
                    sql_fetch_user = """
                    SELECT Full_name, Image, Freelancing_Experience
                    FROM student_signup
                    WHERE Email = %s
                    """
                    cursor.execute(sql_fetch_user, (email,))
                    user_data = cursor.fetchone()
                    
                    if not user_data:
                        return jsonify({"message": "User not found"}), 404
                    
                    user_name = user_data['Full_name']
                    user_image = user_data['Image']
                    years_of_experience = user_data['Freelancing_Experience']
                    
                    # Now insert data into user_blog table
                    sql_insert_blog = '''
                    INSERT INTO user_blog (email, emojiText, imageFile, approve, user_name, user_image, years_of_experience)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    '''
                    cursor.execute(sql_insert_blog, (email, emojiText, image_data, False, user_name, user_image, years_of_experience))
                
                # Commit changes
                connection.commit()
                
                return jsonify({"message": "Post successful"}), 200
                
            finally:
                connection.close()
                
        except Exception as e:
            print(f"Error processing request: {str(e)}")
            return jsonify({"message": "An error occurred. Please try again."}), 500
    
    return jsonify({"message": "User not authenticated or request processing failed."}), 401


# For Recurrent Data
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


# For All time new update
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
###################### SIGNUP FORM #####################
################## 4th Version ########################
################# General Form ####################
from PIL import Image
import io

@app.route('/S_Signup', methods=['POST'])
def S_Signup():
    # Extract form data
    full_name = request.form.get('full-name')
    email = request.form.get('email')
    organization = request.form.get('organization') # Renamed on Front-end as Educational Institution
    phone_number = request.form.get('phone-number')
    address = request.form.get('address')
    educational_level = request.form.get('educational-level')
    skills = request.form.get('skills') # Renamed on Front-end as Subject of Study
    freelancing_word_data = request.form.get('freelancing_word_data')
    image_upload = request.files.get('image-upload')
    password = request.form.get('password')

    # Set category, seminer_date, and seminer_name default values
    category = 'General'
    seminer_date = None
    seminer_name = None

    # Handle image upload and resizing
    image_data = None
    default_image_path = 'static/assets/profile_avatar/avatar.jpg'

    try:
        if image_upload:
            # Check if the uploaded file is an image
            if image_upload.content_type not in ['image/jpeg', 'image/png', 'image/jpg']:
                return jsonify({"message": "Unsupported image format. Only JPG, JPEG, and PNG are allowed."}), 400

            # Open the image and resize it
            image = Image.open(image_upload)

            # Function to resize image to be under 60KB
            def resize_image(image, max_size_kib):
                output_io = io.BytesIO()
                quality = 95
                while True:
                    output_io.seek(0)
                    image.save(output_io, format=image.format, quality=quality)
                    size = output_io.tell()
                    if size <= max_size_kib * 1024 or quality <= 5:
                        break
                    quality -= 5
                output_io.seek(0)
                return output_io

            resized_image_io = resize_image(image, 60)
            image_data = resized_image_io.read()

        else:
            # Load default image if none is uploaded
            with open(default_image_path, 'rb') as f:
                image_data = f.read()

        # Connect to the database and perform operations
        connection = pymysql.connect(**db_config)
        with connection.cursor() as cursor:
            # Check if the email is already registered
            check_email_sql = "SELECT COUNT(*) AS count FROM student_signup WHERE Email = %s"
            cursor.execute(check_email_sql, (email,))
            result = cursor.fetchone()
            if result['count'] > 0:
                return jsonify({"message": "Email is already registered"}), 400
            else:
                # Insert the new user into the database with default category, seminer_date, and seminer_name
                sql = """
                    INSERT INTO student_signup (Full_name, Email, Organization, Phone_number, Address, Educational_Level, Skills, Freelancing_Word_Data, Image, Password, category, seminer_date, seminer_name)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                cursor.execute(sql, (
                    full_name, 
                    email, 
                    organization, 
                    phone_number, 
                    address, 
                    educational_level, 
                    skills,
                    freelancing_word_data, 
                    image_data, 
                    password,
                    category,       # Default value 'General'
                    seminer_date,   # Default value NULL
                    seminer_name    # Default value NULL
                ))
            connection.commit()

    except Exception as e:
        # Print the error to console for debugging
        print(e)
        return jsonify({"message": "An error occurred!", "error": str(e)}), 500
    finally:
        connection.close()

    return jsonify({"message": "Signup successful"}), 200

################# Event SignUp #######################
from PIL import Image
import io

@app.route('/S_Signup', methods=['POST'])
def S_Signup():
    # Extract form data
    full_name = request.form.get('full-name')
    email = request.form.get('email')
    organization = request.form.get('organization') # Renamed on Front-end as Educational Institution
    phone_number = request.form.get('phone-number')
    address = request.form.get('address')
    educational_level = request.form.get('educational-level')
    skills = request.form.get('skills') # Renamed on Front-end as Subject of Study
    freelancing_word_data = request.form.get('freelancing_word_data')
    image_upload = request.files.get('image-upload')
    password = request.form.get('password')

    # Set category, seminer_date, and seminer_name default values
    category = 'General'
    seminer_date = None
    seminer_name = None

    # Handle image upload and resizing
    image_data = None
    default_image_path = 'static/assets/profile_avatar/avatar.jpg'

    try:
        if image_upload:
            # Check if the uploaded file is an image
            if image_upload.content_type not in ['image/jpeg', 'image/png', 'image/jpg']:
                return jsonify({"message": "Unsupported image format. Only JPG, JPEG, and PNG are allowed."}), 400

            # Open the image and resize it
            image = Image.open(image_upload)

            # Function to resize image to be under 60KB
            def resize_image(image, max_size_kib):
                output_io = io.BytesIO()
                quality = 95
                while True:
                    output_io.seek(0)
                    image.save(output_io, format=image.format, quality=quality)
                    size = output_io.tell()
                    if size <= max_size_kib * 1024 or quality <= 5:
                        break
                    quality -= 5
                output_io.seek(0)
                return output_io

            resized_image_io = resize_image(image, 60)
            image_data = resized_image_io.read()

        else:
            # Load default image if none is uploaded
            with open(default_image_path, 'rb') as f:
                image_data = f.read()

        # Connect to the database and perform operations
        connection = pymysql.connect(**db_config)
        with connection.cursor() as cursor:
            # Check if the email is already registered
            check_email_sql = "SELECT COUNT(*) AS count FROM student_signup WHERE Email = %s"
            cursor.execute(check_email_sql, (email,))
            result = cursor.fetchone()
            if result['count'] > 0:
                return jsonify({"message": "Email is already registered"}), 400
            else:
                # Insert the new user into the database with default category, seminer_date, and seminer_name
                sql = """
                    INSERT INTO student_signup (Full_name, Email, Organization, Phone_number, Address, Educational_Level, Skills, Freelancing_Word_Data, Image, Password, category, seminer_date, seminer_name)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                cursor.execute(sql, (
                    full_name, 
                    email, 
                    organization, 
                    phone_number, 
                    address, 
                    educational_level, 
                    skills,
                    freelancing_word_data, 
                    image_data, 
                    password,
                    category,       # Default value 'General'
                    seminer_date,   # Default value NULL
                    seminer_name    # Default value NULL
                ))
            connection.commit()

    except Exception as e:
        # Print the error to console for debugging
        print(e)
        return jsonify({"message": "An error occurred!", "error": str(e)}), 500
    finally:
        connection.close()

    return jsonify({"message": "Signup successful"}), 200


@app.route('/S_Signup_Event', methods=['POST'])
def S_Signup_Event():
    # Extract form data
    full_name = request.form.get('full-name')
    email = request.form.get('email')
    organization = request.form.get('organization')  # Renamed on Front-end as Educational Institution
    phone_number = request.form.get('phone-number')
    address = request.form.get('address')
    educational_level = request.form.get('educational-level')
    skills = request.form.get('skills')  # Renamed on Front-end as Subject of Study
    freelancing_word_data = request.form.get('freelancing_word_data')
    image_upload = request.files.get('image-upload')
    password = request.form.get('password')
    seminar_date = request.form.get('seminar-date')  # Corrected to match HTML field names
    seminar_name = request.form.get('seminar-name')  # Corrected to match HTML field names

    # Set category default value
    category = 'Event'

    # Handle image upload and resizing
    image_data = None
    default_image_path = 'static/assets/profile_avatar/avatar.jpg'

    try:
        if image_upload:
            # Check if the uploaded file is an image
            if image_upload.content_type not in ['image/jpeg', 'image/png', 'image/jpg']:
                return jsonify({"message": "Unsupported image format. Only JPG, JPEG, and PNG are allowed."}), 400

            # Open the image and resize it
            image = Image.open(image_upload)

            # Function to resize image to be under 60KB
            def resize_image(image, max_size_kib):
                output_io = io.BytesIO()
                quality = 95
                while True:
                    output_io.seek(0)
                    image.save(output_io, format=image.format, quality=quality)
                    size = output_io.tell()
                    if size <= max_size_kib * 1024 or quality <= 5:
                        break
                    quality -= 5
                output_io.seek(0)
                return output_io

            resized_image_io = resize_image(image, 60)
            image_data = resized_image_io.read()

        else:
            # Load default image if none is uploaded
            with open(default_image_path, 'rb') as f:
                image_data = f.read()

        # Connect to the database and perform operations
        connection = pymysql.connect(**db_config)
        with connection.cursor() as cursor:
            # Check if the email is already registered
            check_email_sql = "SELECT COUNT(*) AS count FROM student_signup WHERE Email = %s"
            cursor.execute(check_email_sql, (email,))
            result = cursor.fetchone()
            if result['count'] > 0:
                return jsonify({"message": "Email is already registered"}), 400
            else:
                # Insert the new user into the database with seminar details
                sql = """
                    INSERT INTO student_signup (Full_name, Email, Organization, Phone_number, Address, Educational_Level, Skills, Freelancing_Word_Data, Image, Password, category, seminer_date, seminer_name)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                cursor.execute(sql, (
                    full_name, 
                    email, 
                    organization, 
                    phone_number, 
                    address, 
                    educational_level, 
                    skills,
                    freelancing_word_data, 
                    image_data, 
                    password,
                    category,       # Default value 'Event'
                    seminar_date,   # Use the passed seminar date
                    seminar_name    # Use the passed seminar name
                ))
            connection.commit()

    except Exception as e:
        # Print the error to console for debugging
        print(e)
        return jsonify({"message": "An error occurred!", "error": str(e)}), 500
    finally:
        connection.close()

    return jsonify({"message": "Signup successful"}), 200



############### 1st version - Ridoy Bhaiya ###########

############# Updated SignUp Form Route ############
############## 2nd & 3rd Version - Sumaiya #########
from PIL import Image
import io
@app.route('/S_Signup', methods=['POST'])
def S_Signup():
    # Extract form data
    full_name = request.form.get('full-name')
    email = request.form.get('email')
    organization = request.form.get('organization') # Renamed on Front-end as Educational Institution
    phone_number = request.form.get('phone-number')
    address = request.form.get('address')
    educational_level = request.form.get('educational-level')
    skills = request.form.get('skills') # Renamed on Front-end as Subject of Study
    freelancing_word_data = request.form.get(' freelancing_word_data') 
    # freelancing_experience = request.form.get('freelancing-experience')
    # portfolio_links = request.form.getlist('portfolio-links[]')
    # language_proficiency = request.form.getlist('language-proficiency[]')
    # training_done = request.form.getlist('training_done[]')
    # training_interest = request.form.getlist('training_interest[]')
    image_upload = request.files.get('image-upload')
    password = request.form.get('password')

    # Handle image upload and resizing
    image_data = None
    default_image_path = 'static/assets/profile_avatar/avatar.jpg'

    try:
        if image_upload:
            # Check if the uploaded file is an image
            if image_upload.content_type not in ['image/jpeg', 'image/png', 'image/jpg']:
                return jsonify({"message": "Unsupported image format. Only JPG, JPEG, and PNG are allowed."}), 400

            # Open the image and resize it
            image = Image.open(image_upload)

            # Function to resize image to be under 60KB
            def resize_image(image, max_size_kib):
                output_io = io.BytesIO()
                quality = 95
                while True:
                    output_io.seek(0)
                    image.save(output_io, format=image.format, quality=quality)
                    size = output_io.tell()
                    if size <= max_size_kib * 1024 or quality <= 5:
                        break
                    quality -= 5
                output_io.seek(0)
                return output_io

            resized_image_io = resize_image(image, 60)
            image_data = resized_image_io.read()

        else:
            # Load default image if none is uploaded
            with open(default_image_path, 'rb') as f:
                image_data = f.read()

        # Connect to the database and perform operations
        connection = pymysql.connect(**db_config)
        with connection.cursor() as cursor:
            # Check if the email is already registered
            check_email_sql = "SELECT COUNT(*) AS count FROM student_signup WHERE Email = %s"
            cursor.execute(check_email_sql, (email,))
            result = cursor.fetchone()
            if result['count'] > 0:
                return jsonify({"message": "Email is already registered"}), 400
            else:
                # Insert the new user into the database
                # sql = """
                #     INSERT INTO student_signup (Full_name, Email, Organization, Phone_number, Address, Educational_Level, Skills, Freelancing_Word_Data, Freelancing_Experience, Portfolio_Links, Language_Proficiency, Training_done, Training_interests, Image, Password)
                #     VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                # """

                sql = """
                    INSERT INTO student_signup (Full_name, Email, Organization, Phone_number, Address, Educational_Level, Skills, Freelancing_Word_Data, Image, Password)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                cursor.execute(sql, (
                    full_name, 
                    email, 
                    organization, 
                    phone_number, 
                    address, 
                    educational_level, 
                    skills,
                    freelancing_word_data, 
                    # freelancing_experience, 
                    # ','.join(portfolio_links), 
                    # ','.join(language_proficiency), 
                    # ','.join(training_done), 
                    # ','.join(training_interest), 
                    image_data, 
                    password
                ))
            connection.commit()

    except Exception as e:
        # Print the error to console for debugging
        print(e)
        return jsonify({"message": "An error occurred!", "error": str(e)}), 500
    finally:
        connection.close()

    return jsonify({"message": "Signup successful"}), 200

@app.route('/fetch-users', methods=['GET'])
def fetch_users():
    try:
        # Get the search query from the request
        search_query = request.args.get('query', '')

        connection = pymysql.connect(**db_config)
        with connection.cursor() as cursor:
            # SQL query with search functionality
            sql = """
            SELECT Full_name, Email, Phone_number, category, seminer_date, seminer_name   
            FROM student_signup 
            WHERE Full_name LIKE %s OR Email LIKE %s OR Phone_number LIKE %s OR category LIKE %s OR seminer_date LIKE %s OR seminer_name LIKE %s 
            ORDER BY created_at DESC
            """
            # The search query will be used in a wildcard search
            wildcard_search = f"%{search_query}%"
            cursor.execute(sql, (wildcard_search, wildcard_search, wildcard_search, wildcard_search, wildcard_search, wildcard_search))
            data = cursor.fetchall()

            return jsonify(data), 200
    except Exception as e:
        return jsonify({"message": "An error occurred!", "error": str(e)}), 500
    finally:
        connection.close()
############## OLD VERSION ##############
# @app.route('/fetch-users', methods=['GET'])
# def fetch_users():
#     try:
#         connection = pymysql.connect(**db_config)
#         with connection.cursor() as cursor:
#             sql = """SELECT Full_name, Email, Phone_number 
#                      FROM student_signup ORDER BY created_at DESC"""  
#             cursor.execute(sql)
#             data = cursor.fetchall()
#             return jsonify(data), 200
#     except Exception as e:
#         return jsonify({"message": "An error occurred!", "error": str(e)}), 500
#     finally:
#         connection.close()   

@app.route('/delete-user', methods=['DELETE'])
def delete_user():
    try:
        # Get the email from the request
        email = request.args.get('email', '')

        connection = pymysql.connect(**db_config)
        with connection.cursor() as cursor:
            # SQL query to delete a user based on their email
            sql = "DELETE FROM student_signup WHERE Email = %s"
            cursor.execute(sql, (email,))
            connection.commit()

            if cursor.rowcount > 0:
                return jsonify({"message": "User deleted successfully"}), 200
            else:
                return jsonify({"message": "User not found"}), 404
    except Exception as e:
        return jsonify({"message": "An error occurred!", "error": str(e)}), 500
    finally:
        connection.close()


@app.route('/fetch_user_data', methods=['GET'])
def fetch_user_data():
    email =session['user_email']
    # email = session['user_email']
    # if 'email' not in session:
    #     return jsonify({"message": "User not logged in"}), 401

    
    # print(email)
    try:
        connection = pymysql.connect(**db_config)
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        sql = """SELECT 
            Full_name,
            Email,
            Organization,
            Phone_number,
            Address,
            Educational_Level,
            Skills,
            # Freelancing_Experience,
            # Portfolio_Links,
            # Language_Proficiency,
            # Training_done,
            # Training_interests,
            Image,
            Password
        FROM 
            student_signup
        WHERE Email = %s;"""
        
        cursor.execute(sql, (email,))
        data = cursor.fetchall()
        # print(data)
        for row in data:
            if row['Image']:
                row['Image'] = f"/fetch_image_drawer/{row['Email']}"
        # print(data)
        return jsonify(data), 200
    except pymysql.MySQLError as e:
        print(f"MySQL error occurred: {e.args[0]} - {e.args[1]}")
        return jsonify({"message": "A database error occurred!", "error": str(e)}), 500
    except Exception as e:
        # print(f"An error occurred: {str(e)}")
        return jsonify({"message": "An error occurred!", "error": str(e)}), 500
    finally:
        if connection:
            # print("Closing connection...")
            connection.close()


/////////////////////////////////////////// ADMIN PANEL /////////////////////////////////////////////////////////////////

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

            # Connect to the database
            connection = pymysql.connect(**db_config)

            try:
                with connection.cursor() as cursor:
                    sql_insert_seminer = '''
                    INSERT INTO seminers (seminer_date, seminer_name, seminer_details, seminer_image, status, created_at)
                    VALUES (%s, %s, %s, %s, %s, CURRENT_TIMESTAMP)
                    '''
                    cursor.execute(sql_insert_seminer, (seminer_date, seminer_name, seminer_details, seminer_image_data, status))

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
            sql = "SELECT * FROM seminers ORDER BY seminer_id DESC LIMIT 2"
            cursor.execute(sql)
            rows = cursor.fetchall()

            if rows:
                seminers = []
                for row in rows:
                    seminers.append({
                        'seminer_date': row['seminer_date'],
                        'seminer_name': row['seminer_name'],
                        'seminer_details': row['seminer_details'],
                        'status': row['status'],
                        'created_at': row['created_at'],
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

# @app.route('/course_video_upload', methods=['POST'])
# def course_video_upload():
#     data = request.get_json()
#     course_link = data.get('course_link')
#     course_title = data.get('course_title')
#     course_details = data.get('course_details')
#     course_category = data.get('course_category')

#     if course_link and course_title and course_details and course_category:
#         try:
#             # Connect to the database
#             connection = pymysql.connect(**db_config)

#             try:
#                 with connection.cursor() as cursor:
#                     sql_insert_course = '''
#                     INSERT INTO video_courses (course_link, course_title, course_details, course_category)
#                     VALUES (%s, %s, %s, %s)
#                     '''
#                     cursor.execute(sql_insert_course, (course_link, course_title, course_details, course_category))

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

#     return jsonify({"message": "Invalid input or request processing failed."}), 400

@app.route('/course_video_upload', methods=['POST'])
def course_video_upload():
    data = request.get_json()
    course_link = data.get('course_link')
    course_title = data.get('course_title')
    course_details = data.get('course_details')
    course_category = data.get('course_category')
    teachers_name = data.get('teachers_name')  # Corrected variable name
    teachers_about = data.get('teachers_about')  # Corrected variable name

    if course_link and course_title and course_details and course_category:
        try:
            # Connect to the database
            connection = pymysql.connect(**db_config)

            try:
                with connection.cursor() as cursor:
                    sql_insert_course = '''
                    INSERT INTO video_courses (course_link, course_title, course_details, course_category, teachers_name, teachers_about)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    '''
                    cursor.execute(sql_insert_course, (course_link, course_title, course_details, course_category, teachers_name, teachers_about))

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


# @app.route('/course_video_edit/<int:course_id>', methods=['GET', 'POST'])
# def course_video_edit(course_id):
#     # Connect to the database
#     connection = pymysql.connect(**db_config)

#     if request.method == 'GET':
#         try:
#             with connection.cursor() as cursor:
#                 sql_fetch_course = '''
#                 SELECT course_link, course_title, course_category, course_details
#                 FROM video_courses
#                 WHERE course_id = %s
#                 '''
#                 cursor.execute(sql_fetch_course, (course_id,))
#                 course = cursor.fetchone()

#                 if course:
#                     return jsonify({
#                         "course_link": course[0],
#                         "course_title": course[1],
#                         "course_category": course[2],
#                         "course_details": course[3]
#                     }), 200
#                 else:
#                     return jsonify({"message": "No course found with the given ID."}), 404

#         except Exception as e:
#             print(f"Error fetching course: {str(e)}")
#             return jsonify({"message": "An error occurred while fetching the course."}), 500

#         finally:
#             connection.close()

#     elif request.method == 'POST':
#         data = request.get_json()
#         course_link = data.get('course_link')
#         course_title = data.get('course_title')
#         course_category = data.get('course_category')
#         course_details = data.get('course_details')

#         if course_link and course_title and course_category and course_details:
#             try:
#                 with connection.cursor() as cursor:
#                     sql_update_course = '''
#                     UPDATE video_courses
#                     SET course_link = %s, course_title = %s, course_category = %s, course_details = %s
#                     WHERE course_id = %s
#                     '''
#                     cursor.execute(sql_update_course, (course_link, course_title, course_category, course_details, course_id))

#                 # Commit changes
#                 connection.commit()

#                 if cursor.rowcount == 0:
#                     return jsonify({"message": "No course found with the given ID."}), 404

#                 return jsonify({"message": "Course updated successfully"}), 200

#             except Exception as e:
#                 print(f"Error processing request: {str(e)}")
#                 return jsonify({"message": "An error occurred. Please try again."}), 500

#             finally:
#                 connection.close()

#     return jsonify({"message": "Invalid input or request processing failed."}), 400

@app.route('/course_video_edit/<int:course_id>', methods=['GET', 'POST'])
def course_video_edit(course_id):
    # Connect to the database
    connection = pymysql.connect(**db_config)

    if request.method == 'GET':
        try:
            with connection.cursor() as cursor:
                sql_fetch_course = '''
                SELECT course_link, course_title, course_category, course_details, teachers_name, teachers_about
                FROM video_courses
                WHERE course_id = %s
                '''
                cursor.execute(sql_fetch_course, (course_id,))
                course = cursor.fetchone()

                if course:
                    return jsonify({
                        "course_link": course[0],
                        "course_title": course[1],
                        "course_category": course[2],
                        "course_details": course[3],
                        "teachers_name": course[4],  # Added teachers_name
                        "teachers_about": course[5]   # Added teachers_about
                    }), 200
                else:
                    return jsonify({"message": "No course found with the given ID."}), 404

        except Exception as e:
            print(f"Error fetching course: {str(e)}")
            return jsonify({"message": "An error occurred while fetching the course."}), 500

        finally:
            connection.close()

    elif request.method == 'POST':
        data = request.get_json()
        course_link = data.get('course_link')
        course_title = data.get('course_title')
        course_category = data.get('course_category')
        course_details = data.get('course_details')
        teachers_name = data.get('teachers_name')  # Added teachers_name
        teachers_about = data.get('teachers_about')  # Added teachers_about

        if course_link and course_title and course_category and course_details:
            try:
                with connection.cursor() as cursor:
                    sql_update_course = '''
                    UPDATE video_courses
                    SET course_link = %s, course_title = %s, course_category = %s, 
                        course_details = %s, teachers_name = %s, teachers_about = %s
                    WHERE course_id = %s
                    '''
                    cursor.execute(sql_update_course, (course_link, course_title, course_category, course_details, teachers_name, teachers_about, course_id))

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
                SELECT course_id, course_link, course_title, course_details, course_category, created_at
                FROM video_courses
                WHERE course_link LIKE %s 
                OR course_title LIKE %s 
                OR course_details LIKE %s 
                OR course_category LIKE %s
                OR created_at LIKE %s
                ORDER BY created_at DESC
            """
            
            # Prepare the search query with wildcards for LIKE search
            wildcard_search = f"%{search_query}%"
            
            # Execute the query with the same search term applied to all fields
            cursor.execute(sql, (wildcard_search, wildcard_search, wildcard_search, wildcard_search, wildcard_search))
            
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
        # Fetch the search query from request parameters
        search_query = request.args.get('query', '')
        
        # Establish a connection to the database
        connection = pymysql.connect(**db_config)
        
        with connection.cursor() as cursor:
            # SQL query with multiple fields using LIKE for searching
            sql = """
                SELECT course_id, course_link, course_title, course_details, course_category, created_at
                FROM video_courses
                WHERE course_link LIKE %s 
                OR course_title LIKE %s 
                OR course_details LIKE %s 
                OR course_category LIKE %s
                OR created_at LIKE %s
                ORDER BY created_at DESC
            """
            
            # Prepare the search query with wildcards for LIKE search
            wildcard_search = f"%{search_query}%"
            
            # Execute the query with the same search term applied to all fields
            cursor.execute(sql, (wildcard_search, wildcard_search, wildcard_search, wildcard_search, wildcard_search))
            
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



# @app.route('/delete_course_video/<int:video_id>', methods=['DELETE'])
# def delete_course_video(video_id):
#     connection = None
#     try:
#         connection = pymysql.connect(**db_config)
        
#         with connection.cursor() as cursor:
#             sql = "DELETE FROM video_courses WHERE course_id = %s"
#             cursor.execute(sql, (video_id,))
#             connection.commit()

#             if cursor.rowcount > 0:
#                 return jsonify({"message": "Video deleted successfully!"}), 200
#             else:
#                 return jsonify({"message": "Video not found!"}), 404

#     except pymysql.MySQLError as e:
#         print(f"MySQL error: {str(e)}")
#         return jsonify({"message": "A database error occurred!", "error": str(e)}), 500
#     except Exception as e:
#         print(f"Error: {str(e)}")
#         return jsonify({"message": "An error occurred!", "error": str(e)}), 500
#     finally:
#         if connection:
#             connection.close()

@app.route('/delete_course_video/<int:course_id>', methods=['DELETE'])
def delete_course_video(course_id):
    connection = None
    try:
        connection = pymysql.connect(**db_config)
        
        with connection.cursor() as cursor:
            sql = "DELETE FROM video_courses WHERE course_id = %s"
            cursor.execute(sql, (course_id,))
            connection.commit()

            if cursor.rowcount > 0:
                return jsonify({"message": "Video deleted successfully!"}), 200
            else:
                return jsonify({"message": "Video not found!"}), 404

    except pymysql.MySQLError as e:
        return jsonify({"message": "A database error occurred!", "error": str(e)}), 500
    except Exception as e:
        return jsonify({"message": "An error occurred!", "error": str(e)}), 500
    finally:
        if connection:
            connection.close()

@app.route('/fetch_course_categories', methods=['GET'])
def fetch_course_categories():
    connection = None
   
    try:
        connection = pymysql.connect(**db_config)

        with connection.cursor() as cursor:
            # Query to fetch distinct course categories
            query = "SELECT DISTINCT course_category FROM video_courses"
            cursor.execute(query)
            categories = cursor.fetchall()

            # Return the categories in JSON format
            return jsonify(categories)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        connection.close()


//////////////////////////////////// Latest Videos - Working on Server ////////////////////////////////////////

@app.route('/fetch_latest_videos', methods=['GET'])
def fetch_latest_videos():
    try:
         # Fetch the search query from request parameters
        search_query = request.args.get('query', '')
        
        # Establish a connection to the database
        connection = pymysql.connect(**db_config)
        
        with connection.cursor() as cursor:
            # SQL query with multiple fields using LIKE for searching
            sql = """
                SELECT latest_id, latest_link, latest_title, latest_details, created_at
                FROM latest
                WHERE latest_link LIKE %s 
                OR latest_title LIKE %s 
                OR latest_details LIKE %s 
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



@app.route('/fetch_latest_videos_latest', methods=['GET'])
def fetch_latest_videos_latest():
    try:
         # Fetch the search query from request parameters
        search_query = request.args.get('query', '')
        
        # Establish a connection to the database
        connection = pymysql.connect(**db_config)
        
        with connection.cursor() as cursor:
            # SQL query with multiple fields using LIKE for searching
            sql = """
                SELECT latest_id, latest_link, latest_title, latest_details, created_at
                FROM latest
                WHERE latest_link LIKE %s 
                OR latest_title LIKE %s 
                OR latest_details LIKE %s 
                OR created_at LIKE %s
                ORDER BY created_at DESC LIMIT 3
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



////////////////////////////////////////  RENEWED ROUTES FOR IMAGE VALIDATION TO SAVE BEST QUALITY IMAGE AS BLOB IN DATABASE /////////////////////////////////////////////////////////
################################ GIF/ JPG/ PNG/ SVG Upload For Carousel ############################################
@app.route('/carousel_image_upload', methods=['POST'])
def carousel_image_upload():
    data = request.get_json()  # Extract JSON data from the request
    image_name = data.get('image_name')
    carousel_image = data.get('carousel_image')  # Now expecting base64 encoded string

    if image_name and carousel_image:
        try:
            # Decode the base64 image
            header, image_data = carousel_image.split(',', 1)
            mime_type = header.split(';')[0].split(':')[1]

            if mime_type not in ['image/jpeg', 'image/png', 'image/jpg', 'image/gif', 'image/svg+xml']:
                return jsonify({"message": "Unsupported image format. Only JPG, JPEG, PNG, GIF, and SVG formats are allowed."}), 400

            if mime_type == 'image/svg+xml':
                # For SVG, just store the base64 string as it is, no resizing needed
                carousel_image_data = base64.b64decode(image_data)

            else:
                # For raster images (JPG, PNG, GIF), decode and process further
                carousel_image_data = base64.b64decode(image_data)
                
                image = Image.open(io.BytesIO(carousel_image_data))
                image_format = image.format  # Get original image format

                # Resize function, skip resizing if it's a GIF
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

                # Only resize non-GIF images
                if mime_type != 'image/gif':
                    resized_image_io = resize_image(image, 60)
                    resized_image_data = resized_image_io.read()
                else:
                    resized_image_data = carousel_image_data

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


#################### GIF/SVG/ MP4 Upload For Carousel (Doesn't Work) ######################
# from flask import request, jsonify
# from werkzeug.utils import secure_filename
# import pymysql
# import base64
# import io
# from PIL import Image
# from moviepy.editor import VideoFileClip
# @app.route('/carousel_image_upload', methods=['POST'])
# def carousel_image_upload():
#     def save_file_to_db(image_name, filedata, mime_type):
#         connection = pymysql.connect(**db_config)
#         try:
#             with connection.cursor(pymysql.cursors.DictCursor) as cursor:
#                 sql_insert_file = '''
#                     INSERT INTO carousel_images (image_name, carousel_image, mime_type, status)
#                     VALUES (%s, %s, %s, %s)
#                 '''
#                 cursor.execute(sql_insert_file, (image_name, filedata, mime_type, False))
#             connection.commit()
#         finally:
#             connection.close()

#     try:
#         image_name = request.form.get('image_name')
#         carousel_file = request.files.get('carousel_file')  # Expecting file upload

#         if not image_name or not carousel_file:
#             return jsonify({"message": "File or image name missing."}), 400

#         filetype = carousel_file.content_type
#         filedata = carousel_file.read()

#         # Handle different file types
#         if filetype.startswith('image/') or filetype == 'video/mp4':
#             if filetype == 'video/mp4':
#                 # Check video duration
#                 video = VideoFileClip(io.BytesIO(filedata))
#                 if video.duration > 5:
#                     return jsonify({"message": "MP4 file duration exceeds 5 seconds."}), 400
#                 filedata = base64.b64encode(filedata).decode('utf-8')
#             else:
#                 # Process images
#                 valid_image_types = ['image/jpeg', 'image/png', 'image/jpg', 'image/gif', 'image/svg+xml']
#                 if filetype not in valid_image_types:
#                     return jsonify({"message": "Unsupported image format."}), 400
#                 filedata = base64.b64encode(filedata).decode('utf-8')

#             # Save to database
#             save_file_to_db(image_name, filedata, filetype)
#             return jsonify({"message": "File successfully uploaded"}), 200
#         else:
#             return jsonify({"message": "Unsupported file type."}), 400

#     except Exception as e:
#         print(f"Error processing request: {str(e)}")
#         return jsonify({"message": f"An error occurred: {str(e)}"}), 500

////////////////////////////////////////////////////
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


###################################################################################################################################################################################

########################################################################### L I K E   A   P O S T #################################################################################


@app.route('/toggle_like/<int:blog_id>', methods=['POST'])
def toggle_like(blog_id):
    if 'user_email' not in session:
        return jsonify({"message": "User not logged in"}), 401

    user_email = session.get('user_email')
    if not user_email:
        return jsonify({"message": "User email not found in session"}), 401

    try:
        connection = pymysql.connect(**db_config)
        with connection.cursor() as cursor:
            # Check if the blog post exists and get current like count
            sql_select = "SELECT `like`, `emails_liked` FROM user_blog WHERE blog_id = %s"
            cursor.execute(sql_select, (blog_id,))
            blog = cursor.fetchone()

            if not blog:
                return jsonify({"message": "Blog post not found"}), 404

            like_count = blog['like'] if blog['like'] is not None else 0
            emails_liked = blog['emails_liked'] or ''
            emails_liked_list = emails_liked.split(',') if emails_liked else []

            if user_email in emails_liked_list:
                like_count = max(0, like_count - 1)  # Ensure like_count doesn't go below 0
                emails_liked_list.remove(user_email)
                action = 'unliked'
            else:
                like_count += 1
                emails_liked_list.append(user_email)
                action = 'liked'

            updated_emails_liked = ','.join(filter(None, emails_liked_list))

            # Update the blog post with new like count and emails_liked
            sql_update = "UPDATE user_blog SET `like` = %s, `emails_liked` = %s WHERE blog_id = %s"
            cursor.execute(sql_update, (like_count, updated_emails_liked, blog_id))

        connection.commit()
        return jsonify({
            "message": "Like toggled successfully",
            "like_count": like_count,
            "action": action
        }), 200
    except Exception as e:
        return jsonify({"message": f"An error occurred: {str(e)}"}), 500
    finally:
        if connection:
            connection.close()

################################################################
@app.route('/check_like_status/<int:blog_id>', methods=['GET'])
def check_like_status(blog_id):
    email = session.get('user_email')
    
    if not email:
        return jsonify({'error': 'User not logged in'}), 401

    try:
        connection = pymysql.connect(**db_config)
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            query = '''
                SELECT 1 AS liked
                FROM user_blog
                WHERE blog_id = %s AND FIND_IN_SET(%s, emails_liked) > 0
            '''
            cursor.execute(query, (blog_id, email))
            result = cursor.fetchone()
            return jsonify({'liked': bool(result)})
    
    finally:
        connection.close()


@socketio.on('check_like_status')
def handle_check_like_status(data):
    blog_id = data['blog_id']
    email = session.get('email')
    
    if not email:
        emit('like_status', {'error': 'User not logged in'})
        return

    try:
        connection = pymysql.connect(**db_config)
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            query = '''
                SELECT 1 AS liked
                FROM user_blog
                WHERE blog_id = %s AND FIND_IN_SET(%s, emails_liked) > 0
            '''
            cursor.execute(query, (blog_id, email))
            result = cursor.fetchone()
            emit('like_status', {'liked': bool(result)})
    
    finally:
        connection.close()



////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

///////////////////////////////////////// A D D I N G   C O M M E N T S ///////////////////////////////////////////////////////////////////////////////////////////////

@app.route('/add_comment/<int:blog_id>', methods=['POST', 'GET'])
def add_comment(blog_id):
    if 'user_email' not in session:
        return jsonify({"message": "User not logged in"}), 401 

    user_email = session.get('user_email')

    if request.method == 'POST':
        data = request.get_json()
        comment = data.get('comment')

        if not user_email or not comment:
            return jsonify({"message": "User email or comment not found in request"}), 400

        try:
            connection = pymysql.connect(**db_config)
            with connection.cursor() as cursor:
                sql_select_user = "SELECT Full_name FROM student_signup WHERE Email = %s"
                cursor.execute(sql_select_user, (user_email,))
                user = cursor.fetchone()

                if not user:
                    return jsonify({"message": "User not found"}), 404

                full_name = user['Full_name']

                sql_select_blog = "SELECT comment, emails_commented, user_comments FROM user_blog WHERE blog_id = %s"
                cursor.execute(sql_select_blog, (blog_id,))
                blog = cursor.fetchone()

                if not blog:
                    return jsonify({"message": "Blog post not found"}), 404

                comments_count = blog['comment'] if blog['comment'] is not None else 0
                emails_commented = blog['emails_commented'] or ''
                user_comments = blog['user_comments'] or ''

                comments_count += 1
                updated_emails_commented = f"{emails_commented},{user_email}" if emails_commented else user_email

                import time
                # unique_key = f"{full_name}_{int(time.time())}"
                unique_key = f"{user_email}"
                new_comment_entry = f"{unique_key}:{comment}"
                updated_user_comments = f"{user_comments},{new_comment_entry}" if user_comments else new_comment_entry

                sql_update = """
                    UPDATE user_blog
                    SET comment = %s,
                        emails_commented = %s,
                        user_comments = %s
                    WHERE blog_id = %s
                """
                cursor.execute(sql_update, (comments_count, updated_emails_commented, updated_user_comments, blog_id))

            connection.commit()
            return jsonify({
                "message": "Comment added successfully",
                "comment_count": comments_count
            }), 200
        except Exception as e:
            return jsonify({"message": f"An error occurred: {str(e)}"}), 500
        finally:
            if connection:
                connection.close()

    elif request.method == 'GET':
        try:
            connection = pymysql.connect(**db_config)
            with connection.cursor() as cursor:
                sql_select_blog = "SELECT comment FROM user_blog WHERE blog_id = %s"
                cursor.execute(sql_select_blog, (blog_id,))
                blog = cursor.fetchone()

                if not blog:
                    return jsonify({"message": "Blog post not found"}), 404

                comments_count = blog['comment'] if blog['comment'] is not None else 0

            connection.commit()
            return jsonify({
                "comments_count": comments_count
            }), 200
        except Exception as e:
            return jsonify({"message": f"An error occurred: {str(e)}"}), 500
        finally:
            if connection:
                connection.close()



@app.route('/all_comments/<int:blog_id>', methods=['GET'])
def all_comments(blog_id):
    try:
        connection = pymysql.connect(**db_config)
        
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute("SELECT user_comments FROM user_blog WHERE blog_id = %s", (blog_id,))
            user_comments = cursor.fetchall()
            
            print(f"Fetched comments for blog_id {blog_id}: {user_comments}")  # Log fetched comments
            
            # Check if there are no comments or if the 'user_comments' field is empty
            if not user_comments or not user_comments[0]['user_comments']:
                print(f"No comments found for blog_id {blog_id}")  # Log when no comments are found
                return jsonify({"comments": []}), 200

            all_comments_data = []

            # Process each row in the fetched data
            for comment in user_comments:
                comments = comment['user_comments'].split(',')

                for each_comment in comments:
                    if ':' in each_comment:
                        email, user_comment = each_comment.split(':', 1)

                        cursor.execute("SELECT Full_name, Image FROM student_signup WHERE Email = %s", (email,))
                        user_data = cursor.fetchone()

                        if user_data:
                            user_data['Image'] = base64.b64encode(user_data['Image']).decode('utf-8') if user_data['Image'] else None

                            comment_data = {
                                'Email': email,
                                'Full_name': user_data['Full_name'],
                                'Image': user_data['Image'],
                                'Comment': user_comment.strip()
                            }
                            all_comments_data.append(comment_data)

            print(f"Processed comments: {all_comments_data}")  # Log processed comments
            return jsonify({"comments": all_comments_data})

    except Exception as e:
        print(f"Error in all_comments: {str(e)}")  # Log any errors
        return jsonify({"error": "Internal server error", "message": str(e)}), 500

    finally:
        if connection:
            connection.close()








/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////// O L D    V E R S I O N ////////////////////////////////////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

############################################################# A L L  B Y  S U M A I Y A ###################################################################################

@app.route('/home')
def home():
    if 'loggedin' in session and session['loggedin']:
        return render_template('home.html')
    else:
        return redirect(url_for('trainee_login'))

from werkzeug.security import generate_password_hash, check_password_hash
@app.route('/login_trainee', methods=['POST'])
def login_trainee():
    if request.method == 'POST':
        usermail = request.form.get('usermail')
        password = request.form.get('pass')  # Encode password to bytes

        with connection.cursor() as cursor:
            # Retrieve user based on usermail
            sql = "SELECT * FROM trainees WHERE email = %s"
            cursor.execute(sql, (usermail,))
            user = cursor.fetchone()

            if user and check_password_hash(user['password'], password):
                session['loggedin'] = True
                session['id'] = user['trainee_id']
                session['email'] = user['email']
                session['name'] = user['full_name']
                # Redirect to profile_dashboard route
                # return redirect(url_for('profile_dashboard'))
                return jsonify({'redirect': url_for('profile_dashboard')})
            else:
                error = "Invalid credentials. Please try again."
                return jsonify({'error': error})
    else:
        return jsonify({'error': 'Method not allowed'})

@app.route('/approve', methods=['POST'])
def approve_trainee():
    if request.method == 'POST':
        # Get trainee_id and status from the request JSON body
        data = request.get_json()
        trainee_id = data.get('trainee_id')
        status = data.get('status')

        if trainee_id is None or status is None:
            return jsonify({'error': "trainee_id or status not provided"})

        try:
            # Convert status to string ('true' or 'false')
            status_str = 'true' if status else 'false'

            # Update trainee status in the database
            with connection.cursor() as cursor:
                cursor.execute("UPDATE trainees SET status = CASE WHEN %s = 'true' THEN 1 WHEN %s = 'false' THEN 0 ELSE status END WHERE trainee_id = %s;", (status_str, status_str, int(trainee_id)))
                connection.commit()
                return jsonify({'success': True})
        except Exception as e:
            return jsonify({'error': f"Database error: {str(e)}"})
    else:
        return jsonify({'error': "Only POST requests are allowed for this endpoint"})


@app.route('/profile', methods=['GET', 'POST'])
def get_trainee():
    if 'loggedin' in session and session['loggedin']:
        try:
            with connection.cursor() as cursor:
                # Retrieve trainee data based on trainee_id
                trainee_id= session['id']
                trainee_sql = "SELECT * FROM trainees WHERE trainee_id = %s"
                cursor.execute(trainee_sql, (trainee_id,))
                trainee_data = cursor.fetchone()
                if trainee_data:
                    # return render_template('profile_dashboard.html', trainee=trainee_data)
                    return jsonify(trainee_data)
                else:
                    return "Trainee not found"
        except Exception as e:
            return jsonify({'error': f"Request error: {str(e)}"})
    else:
        return redirect(url_for('index'))

@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form.get('email')
        password = generate_password_hash(request.form.get('password'))
        
        try:
            with connection.cursor() as cursor:
                trainee_update_sql = "UPDATE trainees SET password = %s WHERE email = %s"
                cursor.execute(trainee_update_sql, (password,email))
                connection.commit()
             
            return jsonify({'success': 'Password updated successfully'}), 200
        except Exception as e:
            return jsonify({'error': f"Request error: {str(e)}"}), 500

@app.route('/user_forgot_password')
def user_forgot_password():
    return render_template('forgot_password.html') 

@app.route('/user_gallery', methods=['GET','POST'])
def get_user_gallary():
    try:
        with connection.cursor() as cursor:
            # SQL query to fetch data from the users table
            # users_gallary_sql = "SELECT * FROM ahm_gallary_partners LIMIT 6"
            users_gallary_sql = "SELECT * FROM ahm_gallary_partners WHERE category = 'gallary' ORDER BY create_at DESC LIMIT 6"
            cursor.execute(users_gallary_sql)
            gallary_data = cursor.fetchall()
            
           
            count_query = "SELECT COUNT(g_p_id) FROM ahm_gallary_partners WHERE category = 'gallary'"
            cursor.execute(count_query)
            total_records = cursor.fetchone()
            count_value = total_records['COUNT(g_p_id)']
            
        
        limit_per_page = 6
        total_pages = (count_value + limit_per_page)
        
        
        total_pages = math.ceil(total_pages / limit_per_page)-1

        return render_template('user_gallary.html', gallaries=gallary_data, current_page=1, total_pages=total_pages)
    except Exception as e:
        return jsonify({'error': f"Request error: {str(e)}"})
    
    

# GET NEXT 10 IMAGES
gallery_PER_PAGE = 6  # Number of items per page
gallery_START_PAGE = 2  # Starting page number

@app.route('/user_gallary_pagination', methods=['GET'])
def user_gallary_pagination():
    try:
        # Get the page number from the request arguments, default to START_PAGE if not provided
        # page = request.args.get('page', START_PAGE, type=int)
        page = request.args.get('page', gallery_START_PAGE, type=int)
        
        selected_year = request.args.get('selected_year')

        # Calculate the OFFSET based on the page number and number of items per page
        offset = (page - 1) * gallery_PER_PAGE

        with connection.cursor() as cursor:
            
            if selected_year:
                # SQL query to fetch paginated data from the users table
                users_gallary_sql = f"SELECT * FROM ahm_gallary_partners WHERE category = 'gallary' and year=%s LIMIT %s OFFSET %s"
                cursor.execute(users_gallary_sql, (selected_year, gallery_PER_PAGE, offset))
                gallary_data = cursor.fetchall()
                
                count_query = f"SELECT COUNT(g_p_id) FROM ahm_gallary_partners WHERE category = 'gallary' and year=%s"
                cursor.execute(count_query, (selected_year))
                total_records = cursor.fetchone()
                count_value = total_records['COUNT(g_p_id)']
            else:
                 # SQL query to fetch paginated data from the users table
                users_gallary_sql = f"SELECT * FROM ahm_gallary_partners WHERE category = 'gallary' LIMIT %s OFFSET %s"
                cursor.execute(users_gallary_sql, (gallery_PER_PAGE, offset))
                gallary_data = cursor.fetchall()
                
                count_query = "SELECT COUNT(g_p_id) FROM ahm_gallary_partners WHERE category = 'gallary'"
                cursor.execute(count_query)
                total_records = cursor.fetchone()
                count_value = total_records['COUNT(g_p_id)']
            
            
           
            
        limit_per_page = 6
        total_pages = (count_value + limit_per_page)
        
        # print(gallary_data)
        # sys.exit(1)
        
        total_pages = math.ceil(total_pages / limit_per_page)-1

        return jsonify({'galleries': gallary_data, 'page': page, 'total_pages': total_pages})

    except Exception as e:
        return jsonify({'error': f"Request error: {str(e)}"})
    

@app.route('/user_gallery_by_year', methods=['GET', 'POST'])
def get_user_gallery_by_year():
    
    if request.method == 'POST':
    
        try:
            data = request.json
            selected_year = data['year']
            
            
            with connection.cursor() as cursor:
                # SQL query to fetch data from the ahm_gallary_partners table based on selected year
                users_gallary_sql = "SELECT * FROM ahm_gallary_partners WHERE category = 'gallary' AND year = %s"
                cursor.execute(users_gallary_sql, (selected_year,))
                gallary_data = cursor.fetchall()
                
                count_query = "SELECT COUNT(g_p_id) FROM ahm_gallary_partners WHERE category = 'gallary' AND year = %s"
                cursor.execute(count_query, (selected_year,))
                total_records = cursor.fetchone()
                count_value = total_records['COUNT(g_p_id)']
                
            limit_per_page = 6
            total_pages = math.ceil(count_value / limit_per_page)
            
            # return render_template('user_gallary.html', gallaries=gallary_data, current_page=1, total_pages=total_pages)
            return jsonify({'galleries': gallary_data, 'current_page': 1, 'total_pages': total_pages})
        except Exception as e:
            return jsonify({'error': f"Request error: {str(e)}"})

from werkzeug.security import generate_password_hash, check_password_hash
@app.route('/registration', methods=['GET', 'POST'])
def registration():
    try:
        if request.method == 'POST':
            full_name = request.form.get('full_name')
            email = request.form.get('email')
            organization = request.form.get('organization')
            phone_number = request.form.get('phone_number')
            address = request.form.get('address')
            educational_level = request.form.get('educational_level')
            skills = request.form.get('skills')
            freelancing_experience = request.form.get('freelancing_experience')
            # portfolio_link = request.form.get('portfolio_link')
            # language_proficiency = request.form.get('language_proficiency')
            # institution = request.form.get('institution')
            # educational_certificates = request.form.get('educational_certificates
            # availability = request.form.get('availability')
            # preferred_work_type = request.form.get('preferred_work_type')
            # hourly_rate = request.form.get('hourly_rate')
            # certifications = request.form.get('certifications')
            # linkedIn_profile = request.form.get('linkedIn_profile')
            # github_profile = request.form.get('github_profile')
            # course_joining_date = request.form.get('course_joining_date')
            # Handling language proficiency
            portfolio_links = {}

            # Extract portfolio links for selected platforms
            if 'fiverr' in request.form:
                portfolio_links['fiverr'] = request.form.get('fiverr_link')
            if 'upwork' in request.form:
                portfolio_links['upwork'] = request.form.get('upwork_link')
            if 'freelancer' in request.form:
                portfolio_links['freelancer'] = request.form.get('freelancer_link')
            if 'toptal' in request.form:
                portfolio_links['toptal'] = request.form.get('toptal_link')
            if 'guru' in request.form:
                portfolio_links['guru'] = request.form.get('guru_link')
            if 'other' in request.form:
                portfolio_links['other'] = request.form.get('other_link')

            # Convert the dictionary to a JSON string
            json_data = json.dumps(portfolio_links)
        

            languages = []
            if 'bangla' in request.form:
                languages.append('Bangla')
            if 'english' in request.form:
                languages.append('English')
            if 'other_language' in request.form:
                other_language = request.form.get('other_language')
                if other_language:
                    languages.append(other_language)
            # print(languages)
            # exit()
            language_proficiency = ', '.join(languages)
            
            done_trainings = []
            if 'copywriting' in request.form:
                done_trainings.append('Copywriting')
            if 'digital_marketing' in request.form:
                done_trainings.append('Digital Marketing')
            if 'graphic_design' in request.form:
                done_trainings.append('Graphic Design')  
            if 'data_entry' in request.form:
                done_trainings.append('Data Entry')    
            if 'seo' in request.form:
                done_trainings.append('SEO')    
            if 'uxui' in request.form:
                done_trainings.append('UX/UI Design') 
            if 'other_done_training' in request.form:
                other_done_training = request.form.get('other_done_training')
                if other_done_training:
                    done_trainings.append(other_done_training)        
                       
            done_trainings = ', '.join(done_trainings)
            
            wantTo_trainings = []
            if 'copywriting' in request.form:
                wantTo_trainings.append('Copywriting')
            if 'digital_marketing' in request.form:
                wantTo_trainings.append('Digital Marketing')
            if 'graphic_design' in request.form:
                wantTo_trainings.append('Graphic Design')  
            if 'data_entry' in request.form:
                wantTo_trainings.append('Data Entry')    
            if 'seo' in request.form:
                wantTo_trainings.append('SEO')    
            if 'uxui' in request.form:
                wantTo_trainings.append('UX/UI Design') 
            if 'other_wantTo_training' in request.form:
                other_wantTo_training = request.form.get('other_wantTo_training')
                if other_wantTo_training:
                    wantTo_trainings.append(other_wantTo_training)        
                       
            wantTo_trainings = ', '.join(wantTo_trainings) 
            
            password = generate_password_hash(request.form.get('password'))

            # Check for required fields
            if not ([full_name, email, phone_number, address, educational_level, password]):
                return jsonify({"message": "You must fill up these required fields."}), 400
            
            file_photo = request.files['file_photo']
            if file_photo.filename != '':
                # Generate a unique filename
                unique_filename = str(uuid.uuid4()) + "_" + secure_filename(file_photo.filename)
                file_path = os.path.join('static/mainassets/images/trainees_images', unique_filename)
                file_photo.save(file_path)
            
            # Perform database operations
            with connection.cursor() as cursor:
                trainee_create_sql = "INSERT INTO trainees (trainee_image,full_name, organization, email, phone_number, address, educational_level, skills, freelancing_experience, portfolio_link, language_proficiency, done_trainings, wantTo_trainings, password) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                cursor.execute(trainee_create_sql, (unique_filename, full_name, organization, email, phone_number, address, educational_level, skills, freelancing_experience, json_data,language_proficiency, done_trainings, wantTo_trainings, password))
                connection.commit()    
                
            # send_registration_email(email, full_name)     
            msg = Message('Welcome !', recipients=[email])
            
            # filename = "FreelancingPathshalaWelcome.jpg"
            # # url_for('static', filename='mainassets/images/welcome_message/FreelancingPathshalaWelcome.jpg', _external=True)
            # path = os.path.join("static/mainassets/images/welcome_message", filename)
            # with open(path, "rb") as f:
            #     data = f.read()
            # type = os.path.splitext(path)[1][1:]
            # base64_data = base64.b64encode(data).decode("utf-8")
            # base64_image = "data:image/" + type + ";base64," + base64_data


            # Render the HTML template with the image file name passed as a keyword argument
            msg.html = render_template("welcome_mail.html", full_name=full_name, msg=msg)

            # Send the email
            mail.send(msg)

            return jsonify({'success': 'Registration successful'}), 200
                
        elif request.method == 'GET':
            return jsonify({'message': 'GET request received'}), 200

    except Exception as e:
        return jsonify({'error': f"Request error: {str(e)}"}), 500

///////////////////////////////////////////////////Google Sheet API Intrigation////////////////////////////////////////////////////////
import base64
import math
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from google.oauth2 import service_account
from googleapiclient.discovery import build

SERVICE_ACCOUNT_FILE = 'path_to_json_file.json'
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)

service = build('sheets', 'v4', credentials=credentials)

SPREADSHEET_ID = '#################'  # Replace with your actual spreadsheet ID
RANGE_NAME = 'Sheet1!A3'  # Adjust this based on where you want to start inserting data

@app.route('/registration', methods=['GET', 'POST'])
def registration():
    try:
        if request.method == 'POST':
            full_name = request.form.get('full_name')
            email = request.form.get('email')
            organization = request.form.get('organization')
            phone_number = request.form.get('phone_number')
            address = request.form.get('address')
            educational_level = request.form.get('educational_level')
            skills = request.form.get('skills')
            freelancing_experience = request.form.get('freelancing_experience')

            portfolio_links = {}
            if 'fiverr' in request.form:
                portfolio_links['fiverr'] = request.form.get('fiverr_link')
            if 'upwork' in request.form:
                portfolio_links['upwork'] = request.form.get('upwork_link')
            if 'freelancer' in request.form:
                portfolio_links['freelancer'] = request.form.get('freelancer_link')
            if 'toptal' in request.form:
                portfolio_links['toptal'] = request.form.get('toptal_link')
            if 'guru' in request.form:
                portfolio_links['guru'] = request.form.get('guru_link')
            if 'other' in request.form:
                portfolio_links['other'] = request.form.get('other_link')

            json_data = json.dumps(portfolio_links)

            languages = []
            if 'bangla' in request.form:
                languages.append('Bangla')
            if 'english' in request.form:
                languages.append('English')
            if 'other_language' in request.form:
                other_language = request.form.get('other_language')
                if other_language:
                    languages.append(other_language)
            language_proficiency = ', '.join(languages)

            done_trainings = []
            if 'copywriting' in request.form:
                done_trainings.append('Copywriting')
            if 'digital_marketing' in request.form:
                done_trainings.append('Digital Marketing')
            if 'graphic_design' in request.form:
                done_trainings.append('Graphic Design')
            if 'data_entry' in request.form:
                done_trainings.append('Data Entry')
            if 'seo' in request.form:
                done_trainings.append('SEO')
            if 'uxui' in request.form:
                done_trainings.append('UX/UI Design')
            if 'other_done_training' in request.form:
                other_done_training = request.form.get('other_done_training')
                if other_done_training:
                    done_trainings.append(other_done_training)
            done_trainings = ', '.join(done_trainings)

            wantTo_trainings = []
            if 'copywriting' in request.form:
                wantTo_trainings.append('Copywriting')
            if 'digital_marketing' in request.form:
                wantTo_trainings.append('Digital Marketing')
            if 'graphic_design' in request.form:
                wantTo_trainings.append('Graphic Design')
            if 'data_entry' in request.form:
                wantTo_trainings.append('Data Entry')
            if 'seo' in request.form:
                wantTo_trainings.append('SEO')
            if 'uxui' in request.form:
                wantTo_trainings.append('UX/UI Design')
            if 'other_wantTo_training' in request.form:
                other_wantTo_training = request.form.get('other_wantTo_training')
                if other_wantTo_training:
                    wantTo_trainings.append(other_wantTo_training)
            wantTo_trainings = ', '.join(wantTo_trainings)

            password = generate_password_hash(request.form.get('password'))

            if not all([full_name, email, phone_number, address, educational_level, password]):
                return jsonify({"message": "You must fill up these required fields."}), 400

            file_photo = request.files['file_photo']
            if file_photo.filename != '':
                unique_filename = str(uuid.uuid4()) + "_" + secure_filename(file_photo.filename)
                file_path = os.path.join('static/mainassets/images/trainees_images', unique_filename)
                file_photo.save(file_path)

            # Perform database operations here

            # Google Sheets API integration
            values = [
                [
                    full_name, email, organization, phone_number, address, educational_level,
                    skills, freelancing_experience, json_data, language_proficiency,
                    done_trainings, wantTo_trainings
                ]
            ]
            body = {
                'values': values
            }

            result = service.spreadsheets().values().append(
                spreadsheetId=SPREADSHEET_ID,
                range=RANGE_NAME,
                valueInputOption="RAW",
                body=body
            ).execute()

            msg = Message('Welcome!', recipients=[email])
            msg.html = render_template("welcome_mail.html", full_name=full_name, msg=msg)
            mail.send(msg)

            return jsonify({'success': 'Registration successful', 'result': result}), 200

        elif request.method == 'GET':
            return jsonify({'message': 'GET request received'}), 200

    except Exception as e:
        return jsonify({'error': f"Request error: {str(e)}"}), 500

////////////////////////////////////////////////////////////////////////////////////////////////////////////////

@app.route('/trainee_list', methods=['GET', 'POST'])
def trainee_list():
    if 'loggedin' in session and session['loggedin']:
        try:
            with connection.cursor() as cursor:
                trainee_sql = "SELECT * FROM trainees ORDER BY joined_on  DESC LIMIT 20"
                cursor.execute(trainee_sql)
                trainee_data = cursor.fetchall()

                count_query = "SELECT COUNT(trainee_id ) FROM trainees"
                cursor.execute(count_query)
                total_records = cursor.fetchone()
                count_value = total_records['COUNT(trainee_id )']

            limit_per_page = 20
            total_pages = (count_value + limit_per_page)    

            total_pages = math.ceil(total_pages / limit_per_page)-1 

            return render_template('trainee_list.html', trainees=trainee_data, current_page=1, total_pages=total_pages)
        except Exception as e:
            return jsonify({'error': f"Request error: {str(e)}"})
    else:
        return redirect(url_for('admin'))
    

PER_PAGE = 20  # Number of items per page
START_PAGE = 2  # Starting page number        
        
@app.route('/trainee_list_pagination', methods=['GET'])
def trainee_list_pagination():
    try:
        # Get the page number from the request arguments, default to START_PAGE if not provided
        page = request.args.get('page', START_PAGE, type=int)
        
        # selected_year = request.args.get('selected_year')

        # Calculate the OFFSET based on the page number and number of items per page
        offset = (page - 1) * PER_PAGE

        with connection.cursor() as cursor:
            
          
            # SQL query to fetch paginated data from the users table
            trainee_sql = f"SELECT * FROM trainees LIMIT %s OFFSET %s"
            cursor.execute(trainee_sql, (PER_PAGE, offset))
            trainee_data = cursor.fetchall()
            
            count_query = "SELECT COUNT(trainee_id) FROM trainees"
            cursor.execute(count_query)
            total_records = cursor.fetchone()
            count_value = total_records['COUNT(trainee_id)']
            
            
           
            
        limit_per_page = 20
        total_pages = (count_value + limit_per_page)
        
        # print(gallary_data)
        # sys.exit(1)
        
        total_pages = math.ceil(total_pages / limit_per_page)-1

        return jsonify({'trainees': trainee_data, 'page': page, 'total_pages': total_pages})

    except Exception as e:
        return jsonify({'error': f"Request error: {str(e)}"})   
    

@app.route('/trainee_list_edit/<int:trainee_id>', methods=['GET','POST'])
def trainee_list_edit(trainee_id):
    if request.method == 'POST':
        trainee_id = request.form.get('trainee_id')
        full_name = request.form.get('full_name')
        email = request.form.get('email')
        organization = request.form.get('organization')
        phone_number = request.form.get('phone_number')
        address = request.form.get('address')
        educational_level = request.form.get('educational_level')
        skills = request.form.get('skills')
        freelancing_experience = request.form.get('freelancing_experience')
        portfolio_link = request.form.get('portfolio_link')
        language_proficiency = request.form.get('language_proficiency')

        # Perform database operations
        try:
            with connection.cursor() as cursor:
                trainee_update_sql = "UPDATE trainees SET full_name=%s, organization=%s, email=%s, phone_number=%s, address=%s, educational_level=%s, skills=%s, freelancing_experience=%s, portfolio_link=%s, language_proficiency=%s WHERE trainee_id = %s"
                cursor.execute(trainee_update_sql, (full_name, organization, email, phone_number, address, educational_level, skills, freelancing_experience, portfolio_link, language_proficiency, trainee_id))
                connection.commit()

            return jsonify({'success': 'Trainee info updated successfully'}), 200
        except Exception as e:
            return jsonify({'error': f"Request error: {str(e)}"}), 500


@app.route('/trainee_delete/<int:trainee_id>', methods=['GET','POST'])
def trainee_delete(trainee_id):
    try:
        if request.method == 'POST':
            # trainee_id = request.form.get('trainee_id ')
            # print(trainee_id )
            cursor = connection.cursor()
            event_delete_query = "DELETE FROM trainees  WHERE trainee_id  = %s"
            cursor.execute(event_delete_query, (trainee_id,))
            connection.commit()
            return jsonify({'success': 'Delete Success'})
        return jsonify({'error': 'Invalid request'})
    except Exception as e:
        return jsonify({'error': f"Request error: {str(e)}"})


@app.route('/blogs', methods=['GET', 'POST'])
def get_blogs():
        try:
            with connection.cursor() as cursor:
                blog_sql = "SELECT * FROM blogs WHERE status=1 ORDER BY created_at DESC LIMIT 6" 
                cursor.execute(blog_sql)
                blog_data = cursor.fetchall()
                
                count_query = "SELECT COUNT(blog_id) FROM blogs WHERE status=1"
                cursor.execute(count_query)
                total_records = cursor.fetchone()
                count_value = total_records['COUNT(blog_id)']
            
              
            limit_per_page = 6
            total_pages = (count_value + limit_per_page)
            
            # print(gallary_data)
            # sys.exit(1)
            
            total_pages = math.ceil(total_pages / limit_per_page)-1    
                
            return render_template('blogs.html', blogs=blog_data, current_page=1, total_pages=total_pages)
        except Exception as e:
            return jsonify({'error': f"Request error: {str(e)}"})   
        
blog_PER_PAGE = 6  # Number of items per page
blog_START_PAGE = 2  # Starting page number        
        
@app.route('/blog_pagination', methods=['GET'])
def blog_pagination():
    try:
        # Get the page number from the request arguments, default to START_PAGE if not provided
        page = request.args.get('page', blog_START_PAGE, type=int)
        
        # selected_year = request.args.get('selected_year')

        # Calculate the OFFSET based on the page number and number of items per page
        offset = (page - 1) * blog_PER_PAGE

        with connection.cursor() as cursor:
            
            # if selected_year:
            #     # SQL query to fetch paginated data from the users table
            #     users_gallary_sql = f"SELECT * FROM ahm_gallary_partners WHERE category = 'gallary' and year=%s LIMIT %s OFFSET %s"
            #     cursor.execute(users_gallary_sql, (selected_year, PER_PAGE, offset))
            #     gallary_data = cursor.fetchall()
                
            #     count_query = f"SELECT COUNT(g_p_id) FROM ahm_gallary_partners WHERE category = 'gallary' and year=%s"
            #     cursor.execute(count_query, (selected_year))
            #     total_records = cursor.fetchone()
            #     count_value = total_records['COUNT(g_p_id)']
            # else:
                 # SQL query to fetch paginated data from the users table
                blog_sql = f"SELECT * FROM blogs WHERE status=1 ORDER BY created_at DESC LIMIT %s OFFSET %s"
                cursor.execute(blog_sql, (blog_PER_PAGE, offset))
                blog_data = cursor.fetchall()
                
                count_query = "SELECT COUNT(blog_id) FROM blogs WHERE status=1"
                cursor.execute(count_query)
                total_records = cursor.fetchone()
                count_value = total_records['COUNT(blog_id)']
            
            
           
            
        limit_per_page = 6
        total_pages = (count_value + limit_per_page)
        
        # print(gallary_data)
        # sys.exit(1)
        
        total_pages = math.ceil(total_pages / limit_per_page)-1

        return jsonify({'blogs': blog_data, 'page': page, 'total_pages': total_pages})

    except Exception as e:
        return jsonify({'error': f"Request error: {str(e)}"})          

@app.route('/user_blogs', methods=['GET', 'POST'])
def user_blogs():
     if 'loggedin' in session and session['loggedin']:
        try:
            writers_name= session['name']
            with connection.cursor() as cursor:
                blog_sql = f"SELECT * FROM blogs WHERE writers_name = %s ORDER BY created_at DESC LIMIT 6" 
                cursor.execute(blog_sql, writers_name)
                blog_data = cursor.fetchall()
                
                count_query = f"SELECT COUNT(blog_id) FROM blogs WHERE writers_name = %s"
                cursor.execute(count_query, writers_name)
                total_records = cursor.fetchone()
                count_value = total_records['COUNT(blog_id)']
            
              
            limit_per_page = 6
            total_pages = (count_value + limit_per_page)
            
            # print(gallary_data)
            # sys.exit(1)
            
            total_pages = math.ceil(total_pages / limit_per_page)-1    
                
            return render_template('user_blogs.html', blogs=blog_data, current_page=1, total_pages=total_pages)
        except Exception as e:
            return jsonify({'error': f"Request error: {str(e)}"})  
     else:
        return redirect(url_for('trainee_login'))
    
user_blog_PER_PAGE = 6  # Number of items per page
user_blog_START_PAGE = 2  # Starting page number        
        
@app.route('/user_blog_pagination', methods=['GET'])
def user_blog_pagination():
    if 'loggedin' in session and session['loggedin']:
        try:
            writers_name= session['name']
            # Get the page number from the request arguments, default to START_PAGE if not provided
            page = request.args.get('page', user_blog_START_PAGE, type=int)
            
            # selected_year = request.args.get('selected_year')

            # Calculate the OFFSET based on the page number and number of items per page
            offset = (page - 1) * user_blog_PER_PAGE

            with connection.cursor() as cursor:
                
                # if selected_year:
                #     # SQL query to fetch paginated data from the users table
                #     users_gallary_sql = f"SELECT * FROM ahm_gallary_partners WHERE category = 'gallary' and year=%s LIMIT %s OFFSET %s"
                #     cursor.execute(users_gallary_sql, (selected_year, PER_PAGE, offset))
                #     gallary_data = cursor.fetchall()
                    
                #     count_query = f"SELECT COUNT(g_p_id) FROM ahm_gallary_partners WHERE category = 'gallary' and year=%s"
                #     cursor.execute(count_query, (selected_year))
                #     total_records = cursor.fetchone()
                #     count_value = total_records['COUNT(g_p_id)']
                # else:
                    # SQL query to fetch paginated data from the users table
                    blog_sql = f"SELECT * FROM blogs WHERE writers_name=%s ORDER BY created_at DESC LIMIT %s OFFSET %s"
                    cursor.execute(blog_sql, (writers_name, user_blog_PER_PAGE, offset))
                    blog_data = cursor.fetchall()
                    
                    count_query = "SELECT COUNT(blog_id) FROM blogs WHERE writers_name = %s"
                    cursor.execute(count_query, (writers_name))
                    total_records = cursor.fetchone()
                    count_value = total_records['COUNT(blog_id)']
                
                
            
                
            limit_per_page = 6
            total_pages = (count_value + limit_per_page)
            total_pages = math.ceil(total_pages / limit_per_page)-1

            return jsonify({'blogs': blog_data, 'page': page, 'total_pages': total_pages})

        except Exception as e:
            return jsonify({'error': f"Request error: {str(e)}"}) 

@app.route('/blogs_admin_panel', methods=['GET', 'POST'])
def get_blogs_admin_panel():
    if 'loggedin' in session and session['loggedin']:
        try:
            with connection.cursor() as cursor:
                blog_sql = "SELECT * FROM blogs ORDER BY created_at DESC LIMIT 20"
                cursor.execute(blog_sql)
                blog_data = cursor.fetchall()

                count_query = "SELECT COUNT(blog_id) FROM blogs"
                cursor.execute(count_query)
                total_records = cursor.fetchone()
                count_value = total_records['COUNT(blog_id)']

            limit_per_page = 20
            total_pages = (count_value + limit_per_page)    

            total_pages = math.ceil(total_pages / limit_per_page)-1 

            return render_template('blogs_admin_panel.html', blogs=blog_data, current_page=1, total_pages=total_pages)
        except Exception as e:
            return jsonify({'error': f"Request error: {str(e)}"})   
    else:
        return redirect(url_for('admin'))       

//////////////// Previous One ////////////////

PER_PAGE = 20  # Number of items per page
START_PAGE = 2  # Starting page number        
        
@app.route('/blogs_admin_panel_pagination', methods=['GET'])
def blogs_admin_panel_pagination():
    try:
        # Get the page number from the request arguments, default to START_PAGE if not provided
        page = request.args.get('page', START_PAGE, type=int)
        
        # selected_year = request.args.get('selected_year')

        # Calculate the OFFSET based on the page number and number of items per page
        offset = (page - 1) * PER_PAGE

        with connection.cursor() as cursor:
            
            # if selected_year:
            #     # SQL query to fetch paginated data from the users table
            #     users_gallary_sql = f"SELECT * FROM ahm_gallary_partners WHERE category = 'gallary' and year=%s LIMIT %s OFFSET %s"
            #     cursor.execute(users_gallary_sql, (selected_year, PER_PAGE, offset))
            #     gallary_data = cursor.fetchall()
                
            #     count_query = f"SELECT COUNT(g_p_id) FROM ahm_gallary_partners WHERE category = 'gallary' and year=%s"
            #     cursor.execute(count_query, (selected_year))
            #     total_records = cursor.fetchone()
            #     count_value = total_records['COUNT(g_p_id)']
            # else:
                 # SQL query to fetch paginated data from the users table
                blog_sql = f"SELECT * FROM blogs LIMIT %s OFFSET %s"
                cursor.execute(blog_sql, (PER_PAGE, offset))
                blog_data = cursor.fetchall()
                
                count_query = "SELECT COUNT(blog_id) FROM blogs"
                cursor.execute(count_query)
                total_records = cursor.fetchone()
                count_value = total_records['COUNT(blog_id  )']
            
            
           
            
        limit_per_page = 20
        total_pages = (count_value + limit_per_page)
        
        # print(gallary_data)
        # sys.exit(1)
        
        total_pages = math.ceil(total_pages / limit_per_page)-1

        return jsonify({'blogs': blog_data, 'page': page, 'total_pages': total_pages})

    except Exception as e:
        return jsonify({'error': f"Request error: {str(e)}"})   

//////////////// Previous One ////////////////

//////////////// New One ////////////////
PER_PAGE = 10  # Number of items per page
START_PAGE = 2  # Starting page number        
        
@app.route('/blogs_admin_panel_pagination', methods=['GET'])
def blogs_admin_panel_pagination():
    try:
        # Get the page number from the request arguments, default to START_PAGE if not provided
        page = request.args.get('page', START_PAGE, type=int)
        
        # Calculate the OFFSET based on the page number and number of items per page
        offset = (page - 1) * PER_PAGE

        with connection.cursor() as cursor:
            # SQL query to fetch paginated data from the blogs table
            blog_sql = "SELECT * FROM blogs ORDER BY created_at DESC LIMIT %s OFFSET %s"
            cursor.execute(blog_sql, (PER_PAGE, offset))
            blog_data = cursor.fetchall()
            
            # Query to get the total number of records in the blogs table
            count_query = "SELECT COUNT(blog_id) FROM blogs"
            cursor.execute(count_query)
            total_records = cursor.fetchone()
            count_value = total_records['COUNT(blog_id)']
            
            # Calculate the total number of pages based on the total number of records and items per page
            total_pages = math.ceil(count_value / PER_PAGE)

        return jsonify({'blogs': blog_data, 'page': page, 'total_pages': total_pages})

    except Exception as e:
        return jsonify({'error': f"Request error: {str(e)}"})   
//////////////// New One ////////////////
        


@app.route('/blog_creation', methods=['POST'])
def create_blogs():
    try:
        if request.method == 'POST':
            # image = request.form['image']
            writers_name = request.form.get('writers_name')
            topic = request.form.get('topic')
            blog_headline = request.form.get('blog_headline')
            blog_details = request.form.get('blog_details')

            # Check for required fields
            if not all([writers_name, topic, blog_headline, blog_details]):
                return jsonify({"message": "You must fill up all required fields."}), 400
            
            # Save the image file
            file_photo = request.files['file_photo']
            if file_photo.filename != '':
                image = secure_filename(file_photo.filename)
                file_path = os.path.join('static/mainassets/images/blog_images', image)
                file_photo.save(file_path)
                
            # Perform database operations
            with connection.cursor() as cursor:
                blog_create_sql = "INSERT INTO blogs  (image, writers_name, topic, blog_headline, blog_details) VALUES (%s, %s, %s, %s, %s)"
                cursor.execute(blog_create_sql, (image, writers_name, topic, blog_headline, blog_details))
                connection.commit()

            return jsonify({'success': 'Blog Creation successful; Wait for Admins Approval.'}), 200

    except Exception as e:
        return jsonify({'error': f"Request error: {str(e)}"}), 500


////////////////// Blog Creation using different image name //////////////////
import uuid
from datetime import datetime
@app.route('/blog_creation', methods=['POST'])
def create_blogs():
    try:
        if request.method == 'POST':
            # image = request.form['image']
            writers_name = request.form.get('writers_name')
            topic = request.form.get('topic')
            blog_headline = request.form.get('blog_headline')
            blog_details = request.form.get('blog_details')

            # Check for required fields
            if not all([writers_name, topic, blog_headline, blog_details]):
                return jsonify({"message": "You must fill up all required fields."}), 400
            
            # Save the image file with a unique filename
            file_photo = request.files['file_photo']
            if file_photo.filename != '':
                # Generate a unique filename
                unique_filename = str(uuid.uuid4()) + "_" + secure_filename(file_photo.filename)
                file_path = os.path.join('static/mainassets/images/blog_images', unique_filename)
                file_photo.save(file_path)
                
            # Perform database operations
            with connection.cursor() as cursor:
                blog_create_sql = "INSERT INTO blogs  (image, writers_name, topic, blog_headline, blog_details) VALUES (%s, %s, %s, %s, %s)"
                cursor.execute(blog_create_sql, (unique_filename, writers_name, topic, blog_headline, blog_details))
                connection.commit()

            return jsonify({'success': 'Blog Creation successful; Wait for Admins Approval.'}), 200

    except Exception as e:
        return jsonify({'error': f"Request error: {str(e)}"}), 500
////////////////// Blog Creation using different image name //////////////////

@app.route('/blog_approve', methods=['POST'])
def approve_blog():
    if request.method == 'POST':
        # Get trainee_id and status from the request JSON body
        data = request.get_json()
        blog_id = data.get('blog_id')
        status = data.get('status')

        if blog_id is None or status is None:
            return jsonify({'error': "blog_id or status not provided"})

        try:
            # Convert status to string ('true' or 'false')
            status_str = 'true' if status else 'false'

            # Update trainee status in the database
            with connection.cursor() as cursor:
                cursor.execute("UPDATE blogs SET status = CASE WHEN %s = 'true' THEN 1 WHEN %s = 'false' THEN 0 ELSE status END WHERE blog_id = %s;", (status_str, status_str, int(blog_id)))
                connection.commit()
                return jsonify({'success': True})
        except Exception as e:
            return jsonify({'error': f"Database error: {str(e)}"})
    else:
        return jsonify({'error': "Only POST requests are allowed for this endpoint"})

@app.route('/blog_delete/<int:blog_id>', methods=['GET','POST'])
def blog_delete(blog_id):
    try:
        if request.method == 'POST':
            cursor = connection.cursor()
            event_delete_query = "DELETE FROM trainees  WHERE blog_id  = %s"
            cursor.execute(event_delete_query, (blog_id))
            connection.commit()
            return jsonify({'success': 'Delete Success'})
        return jsonify({'error': 'Invalid request'})
    except Exception as e:
        return jsonify({'error': f"Request error: {str(e)}"})

@app.route('/trainee_logout')
def trainee_logout():
    session.clear()
    return redirect(url_for('trainee_login')) 

@app.route('/trainee_password_edit/<int:trainee_id>', methods=['GET','POST'])
def trainee_password_edit(trainee_id):
    if request.method == 'POST':
        
        password = generate_password_hash(request.form.get('password'))

        # Perform database operations
        try:
            with connection.cursor() as cursor:
                trainee_update_sql = "UPDATE trainees SET password = %s WHERE trainee_id = %s"
                cursor.execute(trainee_update_sql, (password, trainee_id))
                connection.commit()

            return jsonify({'success': 'Trainee password updated successfully'}), 200
        except Exception as e:
            return jsonify({'error': f"Request error: {str(e)}"}), 500    

# @app.route('/create_playlist', methods=['POST'])
# def create_playlist():
#     data = request.get_json()
#     playlist_name = data.get('playlist_name')  # Update to match the key from JavaScript
#     video_ids = data.get('video_ids')
#     teachers_name = data.get('teachers_name')  # Fetch teachers_name from data
#     teachers_about = data.get('teachers_about')  # Fetch teachers_about from data

#     if not playlist_name or not video_ids:
#         return jsonify({"message": "Invalid data"}), 400

#     try:
#         connection = pymysql.connect(**db_config)
#         with connection.cursor() as cursor:
#             # Insert playlist into playlists table
#             cursor.execute("INSERT INTO playlists (name, teachers_name, teachers_about) VALUES (%s, %s, %s)", 
#                            (playlist_name, teachers_name, teachers_about))
#             playlist_id = cursor.lastrowid  # Get the last inserted playlist ID

#             # Insert each video into the playlist_videos table
#             for video_id in video_ids:
#                 cursor.execute("INSERT INTO playlist_videos (playlist_id, video_id, teachers_name, teachers_about) VALUES (%s, %s, %s, %s)", 
#                                (playlist_id, video_id, teachers_name, teachers_about))
            
#             connection.commit()

#         return jsonify({"message": "Playlist created successfully!"}), 201
#     except Exception as e:
#         print("Error creating playlist:", e)
#         return jsonify({"message": "Error creating playlist"}), 500
#     finally:
#         connection.close()


###### New Route For Playlist Creation #########
@app.route('/create_playlist', methods=['POST'])
def create_playlist():
    try:
        data = request.get_json()
        playlist_name = data.get('playlist_name')
        video_ids = data.get('video_ids')
        teachers_name = data.get('teachers_name')
        teachers_about = data.get('teachers_about')
        category = data.get('category')
        playlist_about = data.get('playlist_about')
        playlist_thumbnail = data.get('playlist_thumbnail')

        if not playlist_name or not video_ids:
            return jsonify({"message": "Invalid data: playlist_name or video_ids missing"}), 400

        # Handle playlist thumbnail
        resized_thumbnail_data = None
        if playlist_thumbnail and playlist_thumbnail.startswith('data:image/'):
            header, image_data = playlist_thumbnail.split(',', 1)
            mime_type = header.split(';')[0].split(':')[1]
            if mime_type not in ['image/jpeg', 'image/png', 'image/jpg']:
                return jsonify({"message": "Unsupported image format. Only JPG, JPEG, and PNG are allowed."}), 400

            # Decode base64 image
            thumbnail_data = base64.b64decode(image_data)

            # Resize image
            image = Image.open(io.BytesIO(thumbnail_data))
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

            resized_thumbnail_io = resize_image(image, 60)
            resized_thumbnail_data = resized_thumbnail_io.read()

        connection = pymysql.connect(**db_config)
        try:
            with connection.cursor() as cursor:
                # Insert playlist into playlists table
                cursor.execute(
                    """INSERT INTO playlists 
                       (name, teachers_name, teachers_about, category, playlist_about, playlist_thumbnail) 
                       VALUES (%s, %s, %s, %s, %s, %s)""",
                    (playlist_name, teachers_name, teachers_about, category, playlist_about, resized_thumbnail_data)
                )
                playlist_id = cursor.lastrowid

                # Insert each video into the playlist_videos table
                for video_id in video_ids:
                    cursor.execute(
                        """INSERT INTO playlist_videos 
                           (playlist_id, video_id, teachers_name, teachers_about, playlist_name) 
                           VALUES (%s, %s, %s, %s, %s)""",
                        (playlist_id, video_id, teachers_name, teachers_about, playlist_name)
                    )
            
            connection.commit()
        except Exception as e:
            connection.rollback()
            raise e
        finally:
            connection.close()

        return jsonify({"message": "Playlist created successfully!"}), 201

    except pymysql.Error as e:
        print(f"Database error: {e}")
        return jsonify({"message": f"Database error: {str(e)}"}), 500
    except Exception as e:
        print(f"Error creating playlist: {e}")
        return jsonify({"message": f"Error creating playlist: {str(e)}"}), 500


# @app.route('/fetch_playlist/<int:playlist_id>', methods=['GET'])
# def fetch_playlist(playlist_id):
#     try:
#         connection = pymysql.connect(**db_config)
#         with connection.cursor() as cursor:
#             # Fetch playlist information
#             cursor.execute("""
#                 SELECT * FROM playlists
#                 WHERE playlist_id = %s
#             """, (playlist_id,))
#             playlist = cursor.fetchone()

#             if not playlist:
#                 return jsonify({"message": "Playlist not found"}), 404

#             # Fetch videos in the playlist
#             cursor.execute("""
#                 SELECT pv.playlist_id, pv.video_id, pv.teachers_name, pv.teachers_about,
#                        vc.course_link, vc.course_title, vc.course_details, vc.course_category, vc.created_at
#                 FROM playlist_videos pv
#                 JOIN video_courses vc ON pv.video_id = vc.course_id
#                 WHERE pv.playlist_id = %s
#             """, (playlist_id,))
#             videos = cursor.fetchall()

#             # Prepare the response
#             response = {
#                 "playlist_id": playlist['playlist_id'],
#                 "playlist_name": playlist['name'],
#                 "created_at": playlist['created_at'].isoformat(),
#                 "teachers_name": playlist['teachers_name'],
#                 "teachers_about": playlist['teachers_about'],
#                 "videos": videos
#             }

#             return jsonify(response), 200

#     except Exception as e:
#         print("Error fetching playlist:", e)
#         return jsonify({"message": "Error fetching playlist"}), 500

#     finally:
#         connection.close()


# @app.route('/fetch_all_playlists', methods=['GET'])
# def fetch_all_playlists():
#     try:
#         connection = pymysql.connect(**db_config)
#         with connection.cursor() as cursor:
#             # Fetch all playlists
#             cursor.execute("SELECT playlist_id, name AS playlist_name, teachers_name FROM playlists")
#             playlists = cursor.fetchall()

#             # Prepare the response
#             response = []
#             for playlist in playlists:
#                 response.append({
#                     "playlist_id": playlist['playlist_id'],
#                     "playlist_name": playlist['playlist_name'],
#                     "teachers_name": playlist['teachers_name']
#                 })

#             return jsonify(response), 200

#     except Exception as e:
#         print("Error fetching playlists:", e)
#         return jsonify({"message": "Error fetching playlists"}), 500

#     finally:
#         connection.close()


@app.route('/fetch_playlist/<int:playlist_id>', methods=['GET'])
def fetch_playlist(playlist_id):
    try:
        connection = pymysql.connect(**db_config)
        with connection.cursor() as cursor:
            # Fetch playlist information
            cursor.execute("""
                SELECT playlist_id, name AS playlist_name, teachers_name, teachers_about, 
                       category, playlist_about, playlist_thumbnail, created_at 
                FROM playlists 
                WHERE playlist_id = %s
            """, (playlist_id,))
            playlist = cursor.fetchone()

            if not playlist:
                return jsonify({"message": "Playlist not found"}), 404

            # Fetch videos in the playlist
            cursor.execute("""
                SELECT pv.playlist_id, pv.video_id, pv.teachers_name, pv.teachers_about,
                       vc.course_link, vc.course_title, vc.course_details, vc.course_category, vc.created_at
                FROM playlist_videos pv
                JOIN video_courses vc ON pv.video_id = vc.course_id
                WHERE pv.playlist_id = %s
            """, (playlist_id,))
            videos = cursor.fetchall()

            # Handle thumbnail if available
            thumbnail = None
            if playlist['playlist_thumbnail']:
                thumbnail = f"data:image/jpeg;base64,{base64.b64encode(playlist['playlist_thumbnail']).decode()}"

            # Prepare the response
            response = {
                "playlist_id": playlist['playlist_id'],
                "playlist_name": playlist['playlist_name'],
                "teachers_name": playlist['teachers_name'],
                "teachers_about": playlist['teachers_about'],
                "category": playlist['category'],
                "playlist_about": playlist['playlist_about'],
                "created_at": playlist['created_at'].isoformat(),
                "playlist_thumbnail": thumbnail,
                "videos": videos
            }

            return jsonify(response), 200

    except Exception as e:
        print("Error fetching playlist:", e)
        return jsonify({"message": "Error fetching playlist"}), 500

    finally:
        connection.close()


# @app.route('/fetch_all_playlists', methods=['GET'])
# def fetch_all_playlists():
#     try:
#         connection = pymysql.connect(**db_config)
#         with connection.cursor() as cursor:
#             # Fetch all playlists with their first video URL and thumbnail
#             cursor.execute("""
#                 SELECT p.playlist_id, p.name AS playlist_name, p.teachers_name, p.teachers_about,
#                        p.category, p.playlist_about, p.playlist_thumbnail, MIN(vc.course_link) AS first_video_url
#                 FROM playlists p
#                 LEFT JOIN playlist_videos pv ON p.playlist_id = pv.playlist_id
#                 LEFT JOIN video_courses vc ON pv.video_id = vc.course_id
#                 GROUP BY p.playlist_id
#             """)
#             playlists = cursor.fetchall()

#             # Prepare the response
#             response = []
#             for playlist in playlists:
#                 thumbnail = None
#                 if playlist['playlist_thumbnail']:
#                     thumbnail = f"data:image/jpeg;base64,{base64.b64encode(playlist['playlist_thumbnail']).decode()}"

#                 response.append({
#                     "playlist_id": playlist['playlist_id'],
#                     "playlist_name": playlist['playlist_name'],
#                     "teachers_name": playlist['teachers_name'],
#                     "teachers_about": playlist['teachers_about'],
#                     "category": playlist['category'],
#                     "playlist_about": playlist['playlist_about'],
#                     "first_video_url": playlist['first_video_url'],
#                     "playlist_thumbnail": thumbnail
#                 })

#             return jsonify(response), 200

#     except Exception as e:
#         print("Error fetching playlists:", e)
#         return jsonify({"message": "Error fetching playlists"}), 500

#     finally:
#         connection.close()

@app.route('/fetch_all_playlists', methods=['GET'])
def fetch_all_playlists():
    try:
        # Get the search query from the request parameters
        search_query = request.args.get('query', '')

        connection = pymysql.connect(**db_config)
        with connection.cursor() as cursor:
            # Prepare the search term for playlists
            wildcard_search = f"%{search_query}%"

            # Fetch all playlists with their first video URL and thumbnail, filtered by search query
            cursor.execute("""
                SELECT p.playlist_id, p.name AS playlist_name, p.teachers_name, p.teachers_about,
                       p.category, p.playlist_about, p.playlist_thumbnail, MIN(vc.course_link) AS first_video_url
                FROM playlists p
                LEFT JOIN playlist_videos pv ON p.playlist_id = pv.playlist_id
                LEFT JOIN video_courses vc ON pv.video_id = vc.course_id
                WHERE p.name LIKE %s
                   OR p.teachers_name LIKE %s
                   OR p.teachers_about LIKE %s
                   OR p.category LIKE %s
                   OR p.playlist_about LIKE %s
                GROUP BY p.playlist_id
            """, (wildcard_search, wildcard_search, wildcard_search, wildcard_search, wildcard_search))
            playlists = cursor.fetchall()

            # Prepare the response
            response = []
            for playlist in playlists:
                thumbnail = None
                if playlist['playlist_thumbnail']:
                    thumbnail = f"data:image/jpeg;base64,{base64.b64encode(playlist['playlist_thumbnail']).decode()}"

                response.append({
                    "playlist_id": playlist['playlist_id'],
                    "playlist_name": playlist['playlist_name'],
                    "teachers_name": playlist['teachers_name'],
                    "teachers_about": playlist['teachers_about'],
                    "category": playlist['category'],
                    "playlist_about": playlist['playlist_about'],
                    "first_video_url": playlist['first_video_url'],
                    "playlist_thumbnail": thumbnail
                })

            return jsonify(response), 200

    except Exception as e:
        print("Error fetching playlists:", e)
        return jsonify({"message": "Error fetching playlists", "error": str(e)}), 500

    finally:
        if 'connection' in locals():
            connection.close()


@app.route('/remove_video/<int:playlist_id>/<int:video_id>', methods=['DELETE'])
def remove_video(playlist_id, video_id):
    connection = None
    try:
        connection = pymysql.connect(**db_config)
        with connection.cursor() as cursor:
            # Check if the video exists in the playlist
            cursor.execute("""
                SELECT * FROM playlist_videos
                WHERE playlist_id = %s AND video_id = %s
            """, (playlist_id, video_id))
            video_in_playlist = cursor.fetchone()
            
            if not video_in_playlist:
                return jsonify({"message": "Video not found in the playlist"}), 404
            
            # Delete the video from the playlist
            cursor.execute("""
                DELETE FROM playlist_videos
                WHERE playlist_id = %s AND video_id = %s
            """, (playlist_id, video_id))
            connection.commit()
            
            return jsonify({"message": "Video removed from the playlist"}), 200
    except Exception as e:
        # Log the error and return a generic error message
        print(f"Error: {e}")
        return jsonify({"message": "An error occurred while removing the video"}), 500
    finally:
        if connection:
            connection.close()

@app.route('/delete_playlist/<int:playlist_id>', methods=['DELETE'])
def delete_playlist(playlist_id):
    connection = None
    try:
        # Establish a connection to the database
        connection = pymysql.connect(**db_config)

        with connection.cursor() as cursor:
            # Check if the playlist exists
            cursor.execute("""
                SELECT * FROM playlists
                WHERE playlist_id = %s
            """, (playlist_id,))
            playlist = cursor.fetchone()

            if not playlist:
                return jsonify({"message": "Playlist not found"}), 404

            # Delete videos associated with the playlist
            cursor.execute("""
                DELETE FROM playlist_videos
                WHERE playlist_id = %s
            """, (playlist_id,))
            connection.commit()

            # Delete the playlist itself
            cursor.execute("""
                DELETE FROM playlists
                WHERE playlist_id = %s
            """, (playlist_id,))
            connection.commit()

            return jsonify({"message": "Playlist and associated videos deleted successfully."}), 200

    except Exception as e:
        # Handle any errors that occur during the process
        print("Error deleting playlist:", e)
        return jsonify({"message": "An error occurred while deleting the playlist.", "error": str(e)}), 500

    finally:
        # Ensure the connection is closed even if an error occurs
        if connection:
            connection.close()


# @app.route('/edit_playlist/<int:playlist_id>', methods=['PUT'])
# def edit_playlist(playlist_id):
#     data = request.get_json()
#     playlist_name = data.get('playlist_name')
#     teachers_name = data.get('teachers_name')
#     teachers_about = data.get('teachers_about')

#     if not playlist_name:
#         return jsonify({"message": "Invalid data"}), 400

#     try:
#         connection = pymysql.connect(**db_config)
#         with connection.cursor() as cursor:
#             # Update playlist information
#             cursor.execute("""
#                 UPDATE playlists
#                 SET name = %s, teachers_name = %s, teachers_about = %s
#                 WHERE playlist_id = %s
#             """, (playlist_name, teachers_name, teachers_about, playlist_id))
            
#             connection.commit()

#         return jsonify({"message": "Playlist updated successfully!"}), 200
#     except Exception as e:
#         print("Error updating playlist:", e)
#         return jsonify({"message": "Error updating playlist"}), 500
#     finally:
#         connection.close()


@app.route('/edit_playlist/<int:playlist_id>', methods=['GET', 'POST'])
def edit_playlist(playlist_id):
    # Connect to the database
    connection = pymysql.connect(**db_config)
    
    if request.method == 'GET':
        try:
            with connection.cursor() as cursor:
                sql_fetch_playlist = '''
                SELECT name, teachers_name, teachers_about, category, playlist_about, playlist_thumbnail
                FROM playlists
                WHERE playlist_id = %s
                '''
                cursor.execute(sql_fetch_playlist, (playlist_id,))
                playlist = cursor.fetchone()
                if playlist:
                    return jsonify({
                        'playlist_id': playlist_id,
                        'playlist_name': playlist[0],
                        'teachers_name': playlist[1],
                        'teachers_about': playlist[2],
                        'category': playlist[3],
                        'playlist_about': playlist[4],
                        'playlist_thumbnail': base64.b64encode(playlist[5]).decode() if playlist[5] else None,
                    })
                else:
                    return jsonify({'message': 'Playlist not found'}), 404
        except Exception as e:
            return jsonify({'message': str(e)}), 500
        finally:
            connection.close()
    
    elif request.method == 'POST':
        data = request.json
        try:
            with connection.cursor() as cursor:
                # Prepare data for updating
                name = data['playlist_name']
                about = data['playlist_about']
                teachers_name = data['teachers_name']
                teachers_about = data['teachers_about']
                category = data['category']
                thumbnail_data = data.get('playlist_thumbnail')
                
                if thumbnail_data:
                    # Decode base64 string to bytes
                    image_data = base64.b64decode(thumbnail_data)
                    image = Image.open(io.BytesIO(image_data))
                    
                    # Convert image to RGB mode if it's RGBA
                    if image.mode == 'RGBA':
                        image = image.convert('RGB')
                    
                    image = image.resize((300, 300))  # Resize image to desired dimensions
                    img_io = io.BytesIO()
                    image.save(img_io, format='JPEG', quality=85)  # Save image as JPEG
                    img_io.seek(0)
                    thumbnail_data = img_io.getvalue()
                else:
                    thumbnail_data = None  # No new thumbnail uploaded
                
                # SQL query to update playlist
                sql_update_playlist = '''
                UPDATE playlists
                SET name = %s, teachers_name = %s, teachers_about = %s, category = %s, playlist_about = %s, 
                    playlist_thumbnail = IF(%s IS NULL, playlist_thumbnail, %s)
                WHERE playlist_id = %s
                '''
                cursor.execute(sql_update_playlist, (name, teachers_name, teachers_about, category, about, 
                                                     thumbnail_data, thumbnail_data, playlist_id))
                connection.commit()
                
                return jsonify({'message': 'Playlist updated successfully'})
        except Exception as e:
            connection.rollback()
            return jsonify({'message': str(e)}), 500
        finally:
            connection.close()


########################################################################################################
########################################################################################################
##################### T E A C H E R S  P A N E L #######################################################
            
@app.route('/T_Signup', methods=['POST'])
def T_Signup():
    # Extract form data
    name = request.form.get('name')
    email = request.form.get('email')
    phone_number = request.form.get('phone-number')
    educational_institution_level_passing_year = request.form.get('educational-institution-level-passing-year')
    skills = request.form.get('skills')
    experiences = request.form.get('experiences')
    image_upload = request.files.get('image-upload')
    password = request.form.get('password')

    # Handle image upload and resizing
    image_data = None
    default_image_path = 'static/assets/profile_avatar/avatar.jpg'

    try:
        if image_upload:
            # Check if the uploaded file is an image
            if image_upload.content_type not in ['image/jpeg', 'image/png', 'image/jpg']:
                return jsonify({"message": "Unsupported image format. Only JPG, JPEG, and PNG are allowed."}), 400

            # Open the image and resize it
            image = Image.open(image_upload)

            # Function to resize image to be under 60KB
            def resize_image(image, max_size_kib):
                output_io = io.BytesIO()
                quality = 95
                while True:
                    output_io.seek(0)
                    image.save(output_io, format=image.format, quality=quality)
                    size = output_io.tell()
                    if size <= max_size_kib * 1024 or quality <= 5:
                        break
                    quality -= 5
                output_io.seek(0)
                return output_io

            resized_image_io = resize_image(image, 60)
            image_data = resized_image_io.read()

        else:
            # Load default image if none is uploaded
            with open(default_image_path, 'rb') as f:
                image_data = f.read()

        # Connect to the database and perform operations
        connection = pymysql.connect(**db_config)
        with connection.cursor() as cursor:
            # Check if the email is already registered
            check_email_sql = "SELECT COUNT(*) AS count FROM teachers WHERE email = %s"
            cursor.execute(check_email_sql, (email,))
            result = cursor.fetchone()
            if result['count'] > 0:
                return jsonify({"message": "Email is already registered"}), 400
            else:
                # Insert the new teacher into the database
                sql = """
                    INSERT INTO teachers (name, email, phone_number, educational_institution_level_passing_year, skills, experiences, profile_picture, password)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """
                cursor.execute(sql, (
                    name,
                    email,
                    phone_number,
                    educational_institution_level_passing_year,
                    skills,
                    experiences,
                    image_data,
                    password
                ))
            connection.commit()

    except Exception as e:
        # Print the error to console for debugging
        print(e)
        return jsonify({"message": "An error occurred!", "error": str(e)}), 500
    finally:
        connection.close()

    return jsonify({"message": "Signup successful"}), 200


####################################################################################
############################## Purchase Course ##########################################

@app.route('/purchase_course', methods=['POST'])
@login_required
def purchase_course():
    print("Session Data:", session)  # Log session data
    
    # Ensure the user is logged in
    if 'logged_in' not in session or not session['logged_in']:
        return jsonify({'error': 'Unauthorized access'}), 403
    
    # Get the user email from the session
    user_email = session.get('user_email')  # Change 'email' to 'user_email'
    if not user_email:
        return jsonify({'error': 'User email not found in session'}), 403
    
    # Get the playlist_id from the request data
    data = request.json
    playlist_id = data.get('playlist_id')  # Expecting a single playlist ID
    
    if not playlist_id:
        return jsonify({'error': 'Playlist ID is required'}), 400
    
    try:
        # Database connection setup
        connection = pymysql.connect(**db_config)
        
        with connection.cursor() as cursor:
            # Fetch the student_id using the email from the session
            cursor.execute("SELECT student_id FROM student_signup WHERE Email = %s", (user_email,))
            student_record = cursor.fetchone()
            
            if not student_record:
                return jsonify({'error': 'Student not found'}), 404
            
            student_id = student_record['student_id']
            
            # Check if the course has already been purchased by the student
            cursor.execute("""SELECT purchase_id FROM course_purchases 
                              WHERE student_id = %s AND playlist_id = %s""", 
                           (student_id, playlist_id))
            
            if cursor.fetchone():
                return jsonify({'message': 'Course already purchased'}), 200
            
            # Insert a new record into course_purchases
            cursor.execute("""INSERT INTO course_purchases (student_id, playlist_id) 
                              VALUES (%s, %s)""", 
                           (student_id, playlist_id))
            
            # Fetch all buyers of this playlist to update the user_bought field in playlists
            cursor.execute("""SELECT GROUP_CONCAT(student_id) as buyers 
                              FROM course_purchases 
                              WHERE playlist_id = %s 
                              GROUP BY playlist_id""", 
                           (playlist_id,))
            buyers_record = cursor.fetchone()
            buyers = buyers_record['buyers'] if buyers_record else ''
            
            # Update the playlists table with the list of buyers
            cursor.execute("""UPDATE playlists 
                              SET user_bought = %s 
                              WHERE playlist_id = %s""", 
                           (buyers, playlist_id))
            
            # Update playlist_id column in student_signup table
            # Fetch the existing playlist_ids
            cursor.execute("""SELECT playlist_id FROM student_signup 
                              WHERE student_id = %s""", 
                           (student_id,))
            existing_playlist_ids_record = cursor.fetchone()
            existing_playlist_ids = existing_playlist_ids_record['playlist_id'] if existing_playlist_ids_record else ''
            
            # If there are existing playlist_ids, append the new one
            if existing_playlist_ids:
                new_playlist_ids = f"{existing_playlist_ids},{playlist_id}"
            else:
                new_playlist_ids = str(playlist_id)
            
            # Update the playlist_id in student_signup
            cursor.execute("""UPDATE student_signup 
                              SET playlist_id = %s 
                              WHERE student_id = %s""", 
                           (new_playlist_ids, student_id))
            
            # Commit all changes to the database
            connection.commit()
            
            return jsonify({
                'success': 'Course purchased successfully!',
                'student_id': student_id,
                'purchased_playlist_id': new_playlist_ids,
                'course_buyers': buyers
            }), 200
    
    except pymysql.MySQLError as e:
        print(f"Database error: {str(e)}")
        return jsonify({'error': 'Database operation failed'}), 500
    
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        return jsonify({'error': 'An unexpected error occurred'}), 500
    
    finally:
        # Ensure the connection is properly closed
        if 'connection' in locals() and connection:
            connection.close()


@app.route('/is_purchased', methods=['GET'])
@login_required
def is_purchased():
    # Ensure the user is logged in and has a user_email in session
    if 'logged_in' not in session or not session['logged_in']:
        return jsonify({'error': 'Unauthorized access'}), 403
    
    # Get the user email from the session
    user_email = session.get('user_email')
    if not user_email:
        return jsonify({'error': 'User email not found in session'}), 403
    
    # Get the playlist_id from the request arguments
    playlist_id = request.args.get('playlist_id')
    
    if not playlist_id:
        return jsonify({'error': 'Playlist ID is required'}), 400
    
    try:
        # Database connection setup
        connection = pymysql.connect(**db_config)
        
        with connection.cursor() as cursor:
            # Fetch the student_id using the email from the session
            cursor.execute("SELECT student_id FROM student_signup WHERE Email = %s", (user_email,))
            student_record = cursor.fetchone()
            
            if not student_record:
                return jsonify({'error': 'Student not found'}), 404
            
            student_id = student_record['student_id']
            
            # Check if the course has been purchased by the student
            cursor.execute("""SELECT 1 FROM course_purchases 
                              WHERE student_id = %s AND playlist_id = %s""", 
                           (student_id, playlist_id))
            
            # If a record is found, send "yes" indicating the course is purchased
            if cursor.fetchone():
                return jsonify({'message': 'yes'}), 200
            
            # If no record is found, send "no" indicating the course is not purchased
            return jsonify({'message': 'no'}), 200
    
    except pymysql.MySQLError as e:
        print(f"Database error: {str(e)}")
        return jsonify({'error': 'Database operation failed'}), 500
    
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        return jsonify({'error': 'An unexpected error occurred'}), 500
    
    finally:
        # Ensure the connection is properly closed
        if 'connection' in locals() and connection:
            connection.close()



#################################################################################
######################### Fetching Individuals Courses ##########################
@app.route('/fetch_users_playlist', methods=['GET'])
@login_required
def fetch_users_playlist():
    try:
        # Ensure user is logged in and has email in session
        if 'logged_in' not in session or not session['logged_in'] or 'user_email' not in session:
            return jsonify({'error': 'Unauthorized access'}), 403

        user_email = session['user_email']
        search_query = request.args.get('query', '')
        
        connection = pymysql.connect(**db_config)
        with connection.cursor() as cursor:
            # First, get the user's playlist_ids from student_signup
            cursor.execute("""
                SELECT playlist_id 
                FROM student_signup 
                WHERE Email = %s 
                AND playlist_id IS NOT NULL
            """, (user_email,))
            
            result = cursor.fetchone()
            if not result or not result['playlist_id']:
                return jsonify([]), 200
                
            # Split the playlist_ids string into a list
            user_playlist_ids = result['playlist_id'].split(',')
            
            # Create placeholders for SQL IN clause
            placeholders = ', '.join(['%s'] * len(user_playlist_ids))
            
            # Prepare the search term
            wildcard_search = f"%{search_query}%"
            
            # Fetch only the playlists that the user has purchased
            query = f"""
                SELECT p.playlist_id, p.name AS playlist_name, p.teachers_name, 
                       p.teachers_about, p.category, p.playlist_about, 
                       p.playlist_thumbnail, MIN(vc.course_link) AS first_video_url
                FROM playlists p
                LEFT JOIN playlist_videos pv ON p.playlist_id = pv.playlist_id
                LEFT JOIN video_courses vc ON pv.video_id = vc.course_id
                WHERE p.playlist_id IN ({placeholders})
                AND (
                    p.name LIKE %s
                    OR p.teachers_name LIKE %s
                    OR p.teachers_about LIKE %s
                    OR p.category LIKE %s
                    OR p.playlist_about LIKE %s
                )
                GROUP BY p.playlist_id
            """
            
            # Create parameters list for the query
            params = user_playlist_ids + [wildcard_search] * 5
            
            # Execute the query
            cursor.execute(query, params)
            playlists = cursor.fetchall()
            
            # Prepare the response
            response = []
            for playlist in playlists:
                thumbnail = None
                if playlist['playlist_thumbnail']:
                    thumbnail = f"data:image/jpeg;base64,{base64.b64encode(playlist['playlist_thumbnail']).decode()}"
                
                response.append({
                    "playlist_id": playlist['playlist_id'],
                    "playlist_name": playlist['playlist_name'],
                    "teachers_name": playlist['teachers_name'],
                    "teachers_about": playlist['teachers_about'],
                    "category": playlist['category'],
                    "playlist_about": playlist['playlist_about'],
                    "first_video_url": playlist['first_video_url'],
                    "playlist_thumbnail": thumbnail
                })
            
            return jsonify(response), 200
            
    except Exception as e:
        print("Error fetching user's playlists:", e)
        return jsonify({
            "message": "Error fetching user's playlists", 
            "error": str(e)
        }), 500
        
    finally:
        if 'connection' in locals():
            connection.close()


@app.route('/fetch_user_total_playlist_count', methods=['GET'])
@login_required
def fetch_user_total_playlist_count():
    # Ensure the user is logged in
    if 'logged_in' not in session or not session['logged_in']:
        return jsonify({'error': 'Unauthorized access'}), 403
    
    # Get the user email from the session
    user_email = session.get('user_email')
    if not user_email:
        return jsonify({'error': 'User email not found in session'}), 403
    
    try:
        # Database connection setup
        connection = pymysql.connect(**db_config)
        
        with connection.cursor() as cursor:
            # First get the student_id
            cursor.execute("SELECT student_id FROM student_signup WHERE Email = %s", (user_email,))
            student_record = cursor.fetchone()
            
            if not student_record:
                return jsonify({'error': 'Student not found'}), 404
            
            student_id = student_record['student_id']
            
            # Now count the playlists for this student
            cursor.execute("""
                SELECT COUNT(DISTINCT playlist_id) 
                FROM course_purchases 
                WHERE student_id = %s
            """, (student_id,))
            
            result = cursor.fetchone()
            count = result['COUNT(DISTINCT playlist_id)'] if result else 0
            
            return jsonify({'total_playlist_count': count}), 200
            
    except pymysql.MySQLError as e:
        print(f"Database error: {str(e)}")
        return jsonify({'error': 'Database operation failed'}), 500
        
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        return jsonify({'error': 'An unexpected error occurred'}), 500
        
    finally:
        # Ensure the connection is properly closed
        if 'connection' in locals() and connection:
            connection.close()


###################################################################################
############################ Course Progress ######################################

# @app.route('/save_course_progress', methods=['GET', 'POST'])
# @login_required
# def save_course_progress():
#     # Verify user login status
#     if 'logged_in' not in session or not session['logged_in']:
#         return jsonify({'error': 'Unauthorized access'}), 403

#     # Get the user email from the session
#     user_email = session.get('user_email')
#     if not user_email:
#         return jsonify({'error': 'User email not found in session'}), 403

#     try:
#         # Database connection
#         connection = pymysql.connect(**db_config)
#         with connection.cursor() as cursor:
#             if request.method == 'GET':
#                 # Get playlist_id from query parameters
#                 playlist_id = request.args.get('playlist_id')
#                 if not playlist_id:
#                     return jsonify({'error': 'playlist_id is required'}), 400

#                 # First check if the course is in finished_courses
#                 cursor.execute("SELECT finished_courses, course_progress FROM student_signup WHERE Email = %s", (user_email,))
#                 record = cursor.fetchone()
                
#                 if record:
#                     finished_courses = record['finished_courses'].split(',') if record['finished_courses'] else []
                    
#                     # If course is finished, return special status
#                     if playlist_id in finished_courses:
#                         return jsonify({
#                             'status': 'completed',
#                             'message': 'Course already completed',
#                             'course_progress': None
#                         }), 200
                    
#                     # If not finished, return current progress
#                     current_progress = record['course_progress'] if record['course_progress'] else None
#                     return jsonify({
#                         'status': 'in_progress',
#                         'course_progress': current_progress
#                     }), 200
                
#                 return jsonify({'error': 'User record not found'}), 404

#             elif request.method == 'POST':
#                 # Collect data from the JSON request payload
#                 data = request.json
#                 playlist_id = data.get('playlist_id')
#                 total_videos = data.get('total_videos')
#                 current_video = data.get('video_no')

#                 if not all([playlist_id, total_videos, current_video]):
#                     return jsonify({'error': 'playlist_id, total_videos, video_no are required fields'}), 400

#                 # First check if course is already finished
#                 cursor.execute("SELECT finished_courses, course_progress FROM student_signup WHERE Email = %s", (user_email,))
#                 record = cursor.fetchone()

#                 if not record:
#                     return jsonify({'error': 'User record not found'}), 404

#                 finished_courses = set(record['finished_courses'].split(',')) if record['finished_courses'] and record['finished_courses'].strip() else set()

#                 # If course is already finished, return early
#                 if str(playlist_id) in finished_courses:
#                     return jsonify({
#                         'status': 'completed',
#                         'message': 'Course already completed',
#                         'data': {
#                             'course_progress': record['course_progress'],
#                             'finished_courses': record['finished_courses']
#                         }
#                     }), 200

#                 # Initialize progress tracking
#                 current_progress = record['course_progress'] if record['course_progress'] else ''
                
#                 # Convert the existing course progress data to a list of tuples
#                 progress_list = []
#                 if current_progress:
#                     progress_list = [
#                         tuple(map(int, item.strip('()').split(',')))
#                         for item in current_progress.split(';')
#                         if item.strip()
#                     ]

#                 # Create new progress tuple
#                 new_progress = (int(playlist_id), int(total_videos), int(current_video))

#                 # Update progress list: remove old entry if exists, add new one
#                 progress_list = [prog for prog in progress_list if prog[0] != new_progress[0]]
                
#                 # Check if course is finished
#                 if int(current_video) == int(total_videos):
#                     # Add to finished courses
#                     finished_courses.add(str(playlist_id))
#                 else:
#                     # Add to progress list only if not finished
#                     progress_list.append(new_progress)

#                 # Convert progress list back to string format
#                 new_progress_str = ';'.join(f"({','.join(map(str, prog))})" for prog in progress_list)
#                 new_finished_courses = ','.join(sorted(finished_courses)) if finished_courses else ''

#                 # Update the database
#                 cursor.execute("""
#                     UPDATE student_signup
#                     SET course_progress = %s, finished_courses = %s
#                     WHERE Email = %s
#                 """, (new_progress_str, new_finished_courses, user_email))

#                 # Commit the transaction
#                 connection.commit()

#                 return jsonify({
#                     'success': 'Course progress updated successfully!',
#                     'status': 'completed' if int(current_video) == int(total_videos) else 'in_progress',
#                     'data': {
#                         'course_progress': new_progress_str,
#                         'finished_courses': new_finished_courses
#                     }
#                 }), 200

#     except pymysql.MySQLError as e:
#         print(f"Database error: {str(e)}")
#         return jsonify({'error': 'Database operation failed'}), 500

#     except Exception as e:
#         print(f"Unexpected error: {str(e)}")
#         return jsonify({'error': 'An unexpected error occurred'}), 500

#     finally:
#         # Ensure the connection is closed
#         if 'connection' in locals() and connection:
#             connection.close()

@app.route('/save_course_progress', methods=['GET', 'POST'])
@login_required
def save_course_progress():
    if 'logged_in' not in session or not session['logged_in']:
        return jsonify({'error': 'Unauthorized access'}), 403

    user_email = session.get('user_email')
    if not user_email:
        return jsonify({'error': 'User email not found in session'}), 403

    try:
        connection = pymysql.connect(**db_config)
        with connection.cursor() as cursor:
            if request.method == 'GET':
                playlist_id = request.args.get('playlist_id')
                if not playlist_id:
                    return jsonify({'error': 'playlist_id is required'}), 400

                cursor.execute("SELECT finished_courses, course_progress FROM student_signup WHERE Email = %s", (user_email,))
                record = cursor.fetchone()
                
                if record:
                    finished_courses = record['finished_courses'].split(',') if record['finished_courses'] else []
                    
                    if playlist_id in finished_courses:
                        return jsonify({
                            'status': 'completed',
                            'message': 'Course already completed',
                            'course_progress': None
                        }), 200
                    
                    current_progress = record['course_progress'] if record['course_progress'] else None
                    return jsonify({
                        'status': 'in_progress',
                        'course_progress': current_progress
                    }), 200
                
                return jsonify({'error': 'User record not found'}), 404

            elif request.method == 'POST':
                data = request.json
                playlist_id = data.get('playlist_id')
                total_videos = data.get('total_videos')
                current_video = data.get('video_no')

                if not all([playlist_id, total_videos, current_video]):
                    return jsonify({'error': 'playlist_id, total_videos, video_no are required fields'}), 400

                cursor.execute("SELECT finished_courses, course_progress FROM student_signup WHERE Email = %s", (user_email,))
                record = cursor.fetchone()

                if not record:
                    return jsonify({'error': 'User record not found'}), 404

                finished_courses = set(record['finished_courses'].split(',')) if record['finished_courses'] and record['finished_courses'].strip() else set()

                if str(playlist_id) in finished_courses:
                    return jsonify({
                        'status': 'completed',
                        'message': 'Course already completed',
                        'data': {
                            'course_progress': record['course_progress'],
                            'finished_courses': record['finished_courses']
                        }
                    }), 200

                current_progress = record['course_progress'] if record['course_progress'] else ''
                
                # Parse existing progress
                progress_list = []
                if current_progress:
                    progress_list = [
                        tuple(map(int, item.strip('()').split(',')))
                        for item in current_progress.split(';')
                        if item.strip()
                    ]

                # Special handling for (2,9,1)
                new_progress = (int(playlist_id), int(total_videos), int(current_video))
                
                # Remove any existing progress for this playlist except (2,9,1)
                progress_list = [prog for prog in progress_list if 
                               prog[0] != new_progress[0] or 
                               (prog[0] == 2 and prog[1] == 9 and prog[2] == 1)]

                # Check if we should add the new progress
                should_add_progress = True
                if new_progress[0] == 2:  # If this is playlist 2
                    # Only update if it's not the (2,9,1) record or if we're completing the course
                    if new_progress[1] == 9 and new_progress[2] == 1:
                        should_add_progress = False  # Keep existing (2,9,1)
                    elif new_progress[2] == new_progress[1]:  # Course completion
                        should_add_progress = True  # Allow completion update
                    else:
                        # Check if (2,9,1) exists
                        has_special_record = any(p[0] == 2 and p[1] == 9 and p[2] == 1 for p in progress_list)
                        if has_special_record:
                            should_add_progress = False  # Keep (2,9,1)

                if should_add_progress:
                    progress_list.append(new_progress)

                # Check for course completion
                if int(current_video) == int(total_videos):
                    finished_courses.add(str(playlist_id))

                new_progress_str = ';'.join(f"({','.join(map(str, prog))})" for prog in progress_list)
                new_finished_courses = ','.join(sorted(finished_courses)) if finished_courses else ''

                cursor.execute("""
                    UPDATE student_signup
                    SET course_progress = %s, finished_courses = %s
                    WHERE Email = %s
                """, (new_progress_str, new_finished_courses, user_email))

                connection.commit()

                return jsonify({
                    'success': 'Course progress updated successfully!',
                    'status': 'completed' if int(current_video) == int(total_videos) else 'in_progress',
                    'data': {
                        'course_progress': new_progress_str,
                        'finished_courses': new_finished_courses
                    }
                }), 200

    except pymysql.MySQLError as e:
        print(f"Database error: {str(e)}")
        return jsonify({'error': 'Database operation failed'}), 500

    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        return jsonify({'error': 'An unexpected error occurred'}), 500

    finally:
        if 'connection' in locals() and connection:
            connection.close()

####################### USELESS ##########################

@app.route('/mark_course_finished', methods=['POST'])
@login_required
def mark_course_finished():
    # Check if the user is logged in
    if 'logged_in' not in session or not session['logged_in']:
        return jsonify({'error': 'Unauthorized access'}), 403

    # Get the user email from the session
    user_email = session.get('user_email')
    if not user_email:
        return jsonify({'error': 'User email not found in session'}), 403

    # Get the playlist_id from the request data (expecting a single playlist ID)
    data = request.json
    playlist_id = data.get('playlist_id')  # Expecting a single playlist ID
    
    if not playlist_id:
        return jsonify({'error': 'Playlist ID is required'}), 400

    try:
        # Database connection setup
        connection = pymysql.connect(**db_config)
        
        with connection.cursor() as cursor:
            # Check if user exists in the student_signup table
            cursor.execute("SELECT finished_courses FROM student_signup WHERE Email = %s", (user_email,))
            record = cursor.fetchone()
            if not record:
                return jsonify({'error': 'Student not found'}), 404

            # Get existing finished_courses and append the new playlist_id if needed
            existing_courses = record['finished_courses'] if record['finished_courses'] else ''
            if existing_courses:
                # Split the existing courses into a list
                finished_courses_list = existing_courses.split(',')
                # Add the new playlist_id if it's not already in the list
                if str(playlist_id) not in finished_courses_list:
                    finished_courses_list.append(str(playlist_id))
            else:
                finished_courses_list = [str(playlist_id)]

            # Convert the list back to a comma-separated string
            new_finished_courses = ','.join(finished_courses_list)
            
            # Update the finished_courses column
            cursor.execute("UPDATE student_signup SET finished_courses = %s WHERE Email = %s", (new_finished_courses, user_email))
            
            # Commit changes to the database
            connection.commit()

            return jsonify({
                'success': 'Course marked as finished!',
                'finished_courses': new_finished_courses
            }), 200

    except pymysql.MySQLError as e:
        print(f"Database error: {str(e)}")
        return jsonify({'error': 'Database operation failed'}), 500

    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        return jsonify({'error': 'An unexpected error occurred'}), 500

    finally:
        # Ensure the connection is properly closed
        if 'connection' in locals() and connection:
            connection.close()


####################### USELESS ##########################

###################  Fetching Finished Courses ##############

@app.route('/fetch_users_finished_courses', methods=['GET'])
@login_required
def fetch_users_finished_courses():
    try:
        # Ensure user is logged in and has email in session
        if 'logged_in' not in session or not session['logged_in'] or 'user_email' not in session:
            return jsonify({'error': 'Unauthorized access'}), 403

        user_email = session['user_email']
        search_query = request.args.get('query', '')
        
        connection = pymysql.connect(**db_config)
        with connection.cursor() as cursor:
            # First, get the user's finished_courses from student_signup
            cursor.execute("""
                SELECT finished_courses 
                FROM student_signup 
                WHERE Email = %s 
                AND finished_courses IS NOT NULL
            """, (user_email,))
            
            result = cursor.fetchone()
            if not result or not result['finished_courses']:
                return jsonify([]), 200
                
            # Split the finished_courses string into a list
            finished_course_ids = result['finished_courses'].split(',')
            
            # Create placeholders for SQL IN clause
            placeholders = ', '.join(['%s'] * len(finished_course_ids))
            
            # Prepare the search term
            wildcard_search = f"%{search_query}%"
            
            # Fetch only the playlists that the user has finished
            query = f"""
                SELECT p.playlist_id, p.name AS playlist_name, p.teachers_name, 
                       p.teachers_about, p.category, p.playlist_about, 
                       p.playlist_thumbnail, MIN(vc.course_link) AS first_video_url
                FROM playlists p
                LEFT JOIN playlist_videos pv ON p.playlist_id = pv.playlist_id
                LEFT JOIN video_courses vc ON pv.video_id = vc.course_id
                WHERE p.playlist_id IN ({placeholders})
                AND (
                    p.name LIKE %s
                    OR p.teachers_name LIKE %s
                    OR p.teachers_about LIKE %s
                    OR p.category LIKE %s
                    OR p.playlist_about LIKE %s
                )
                GROUP BY p.playlist_id
            """
            
            # Create parameters list for the query
            params = finished_course_ids + [wildcard_search] * 5
            
            # Execute the query
            cursor.execute(query, params)
            playlists = cursor.fetchall()
            
            # Prepare the response
            response = []
            for playlist in playlists:
                thumbnail = None
                if playlist['playlist_thumbnail']:
                    thumbnail = f"data:image/jpeg;base64,{base64.b64encode(playlist['playlist_thumbnail']).decode()}"
                
                response.append({
                    "playlist_id": playlist['playlist_id'],
                    "playlist_name": playlist['playlist_name'],
                    "teachers_name": playlist['teachers_name'],
                    "teachers_about": playlist['teachers_about'],
                    "category": playlist['category'],
                    "playlist_about": playlist['playlist_about'],
                    "first_video_url": playlist['first_video_url'],
                    "playlist_thumbnail": thumbnail,
                    "status": "completed"  # Adding status to indicate these are completed courses
                })
            
            return jsonify(response), 200
            
    except Exception as e:
        print("Error fetching user's finished courses:", e)
        return jsonify({
            "message": "Error fetching user's finished courses", 
            "error": str(e)
        }), 500
        
    finally:
        if 'connection' in locals():
            connection.close()

############### Track Progress Bar ################
# @app.route('/progress_bar', methods=['GET'])
# @login_required
# def get_user_progress():
#     try:
#         # Ensure user is logged in and has email in session
#         if 'logged_in' not in session or not session['logged_in'] or 'user_email' not in session:
#             return jsonify({'error': 'Unauthorized access'}), 403

#         user_email = session['user_email']
        
#         connection = pymysql.connect(**db_config)
#         with connection.cursor() as cursor:
#             # Get user's playlist_id and finished_courses
#             cursor.execute("""
#                 SELECT playlist_id, finished_courses 
#                 FROM student_signup 
#                 WHERE Email = %s
#             """, (user_email,))
            
#             result = cursor.fetchone()
            
#             # Initialize response
#             response = {
#                 "total_courses": 0,
#                 "completed_courses": 0,
#                 "progress_percentage": 0,
#                 "remaining_courses": 0
#             }
            
#             # If no result or both columns are NULL, return 0 progress
#             if not result or (not result['playlist_id'] and not result['finished_courses']):
#                 return jsonify(response), 200
            
#             # Calculate total courses from playlist_id
#             total_courses = 0
#             if result['playlist_id']:
#                 playlist_ids = [x for x in result['playlist_id'].split(',') if x]
#                 total_courses = len(playlist_ids)
            
#             # Calculate completed courses from finished_courses
#             completed_courses = 0
#             if result['finished_courses']:
#                 finished_ids = [x for x in result['finished_courses'].split(',') if x]
#                 completed_courses = len(finished_ids)
            
#             # Calculate progress percentage
#             progress_percentage = 0
#             if total_courses > 0:
#                 progress_percentage = (completed_courses / total_courses) * 100
#                 progress_percentage = round(progress_percentage, 2)  # Round to 2 decimal places
            
#             # Prepare response
#             response = {
#                 "total_courses": total_courses,
#                 "completed_courses": completed_courses,
#                 "progress_percentage": progress_percentage,
#                 "remaining_courses": total_courses - completed_courses,
#                 "status": "on_track" if progress_percentage < 100 else "completed"
#             }
            
#             # Update course_progress in database
#             try:
#                 cursor.execute("""
#                     UPDATE student_signup 
#                     SET course_progress = %s 
#                     WHERE Email = %s
#                 """, (progress_percentage, user_email))
#                 connection.commit()
#             except Exception as e:
#                 print("Error updating course progress:", e)
#                 # Continue execution even if update fails
#                 pass
            
#             return jsonify(response), 200
            
#     except Exception as e:
#         print("Error calculating progress:", e)
#         return jsonify({
#             "message": "Error calculating progress", 
#             "error": str(e)
#         }), 500
        
#     finally:
#         if 'connection' in locals():
#             connection.close()


@app.route('/progress_bar', methods=['GET'])
@login_required
def get_user_progress():
    try:
        # Ensure user is logged in and has email in session
        if 'logged_in' not in session or not session['logged_in'] or 'user_email' not in session:
            return jsonify({'error': 'Unauthorized access'}), 403
        user_email = session['user_email']
       
        connection = pymysql.connect(**db_config)
        with connection.cursor() as cursor:
            # Get user's playlist_id, finished_courses, and course_progress
            cursor.execute("""
                SELECT playlist_id, finished_courses, course_progress
                FROM student_signup
                WHERE Email = %s
            """, (user_email,))
           
            result = cursor.fetchone()
           
            # Initialize response
            response = {
                "total_courses": 0,
                "completed_courses": 0,
                "progress_percentage": 0,
                "remaining_courses": 0
            }
           
            # If no result or both columns are NULL, return 0 progress
            if not result or (not result['playlist_id'] and not result['finished_courses']):
                return jsonify(response), 200
           
            # Calculate total courses from playlist_id
            total_courses = 0
            if result['playlist_id']:
                playlist_ids = [x for x in result['playlist_id'].split(',') if x]
                total_courses = len(playlist_ids)
           
            # Calculate completed courses from finished_courses
            completed_courses = 0
            if result['finished_courses']:
                finished_ids = [x for x in result['finished_courses'].split(',') if x]
                completed_courses = len(finished_ids)
           
            # Calculate progress percentage
            progress_percentage = 0
            if total_courses > 0:
                progress_percentage = (completed_courses / total_courses) * 100
                progress_percentage = round(progress_percentage, 2)  # Round to 2 decimal places

            # Preserve existing course_progress data
            existing_progress = result['course_progress'] if result['course_progress'] else ''
           
            
            # Prepare response
            response = {
                "total_courses": total_courses,
                "completed_courses": completed_courses,
                "progress_percentage": progress_percentage,
                "remaining_courses": total_courses - completed_courses,
                "status": "on_track" if progress_percentage < 100 else "completed",
                "course_progress_data": existing_progress  # Include the progress data in response
            }
            
            # Only update the progress percentage in a separate field, keeping course_progress intact
            try:
                cursor.execute("""
                    UPDATE student_signup
                    SET progress_percentage = %s
                    WHERE Email = %s
                """, (progress_percentage, user_email))
                connection.commit()
            except Exception as e:
                print("Error updating progress percentage:", e)
                # Continue execution even if update fails
                pass
           
            return jsonify(response), 200
           
    except Exception as e:
        print("Error calculating progress:", e)
        return jsonify({
            "message": "Error calculating progress",
            "error": str(e)
        }), 500
       
    finally:
        if 'connection' in locals():
            connection.close()

########### Fetching Users Total Finished Playlist Count  ###########
  
@app.route('/fetch_user_total_finished_playlist_count', methods=['GET'])
@login_required
def fetch_user_total_finished_playlist_count():
    try:
        # Ensure the user is logged in
        if 'logged_in' not in session or not session['logged_in']:
            return jsonify({'error': 'Unauthorized access'}), 403
        
        # Get the user email from the session
        user_email = session.get('user_email')
        if not user_email:
            return jsonify({'error': 'User email not found in session'}), 403
        
        connection = pymysql.connect(**db_config)
        with connection.cursor() as cursor:
            # Get the finished_courses directly from student_signup
            cursor.execute("""
                SELECT finished_courses 
                FROM student_signup 
                WHERE Email = %s
            """, (user_email,))
            
            result = cursor.fetchone()
            
            if not result:
                return jsonify({'error': 'Student not found'}), 404
            
            # Calculate count from finished_courses
            count = 0
            if result['finished_courses']:
                # Split the string and count non-empty items
                finished_courses = [x for x in result['finished_courses'].split(',') if x]
                count = len(finished_courses)
            
            return jsonify({
                'total_playlist_count': count,
                'status': 'success'
            }), 200
            
    except Exception as e:
        print(f"Error in fetch_user_total_finished_playlist_count: {str(e)}")
        return jsonify({'error': str(e)}), 500
        
    finally:
        if 'connection' in locals():
            connection.close()      



######### Individual Course Progress Tracking ########
@app.route('/course_progress_tracking', methods=['GET'])
@login_required
def track_course_progress():
    try:
        if 'logged_in' not in session or not session['logged_in'] or 'user_email' not in session:
            return jsonify({'error': 'Unauthorized access'}), 403
        
        user_email = session['user_email']
        
        connection = pymysql.connect(**db_config)
        with connection.cursor() as cursor:
            # Get user's course_progress and finished_courses
            cursor.execute("""
                SELECT course_progress, finished_courses, playlist_id 
                FROM student_signup 
                WHERE Email = %s
            """, (user_email,))
            
            result = cursor.fetchone()
            
            if not result:
                return jsonify({'error': 'User record not found'}), 404
                
            course_progress = result['course_progress']
            finished_courses = result['finished_courses']
            all_playlist_ids = result['playlist_id']
            
            # Initialize response structure
            progress_data = {
                'individual_progress': [],
                'completed_courses': [],
                'total_courses': [],
                'summary': {
                    'average_progress': 0,
                    'courses_in_progress': 0,
                    'courses_completed': 0
                }
            }
            
            # Process finished courses
            finished_course_list = finished_courses.split(',') if finished_courses else []
            progress_data['completed_courses'] = [int(course) for course in finished_course_list if course]
            
            # Process total courses
            total_course_list = all_playlist_ids.split(',') if all_playlist_ids else []
            progress_data['total_courses'] = [int(course) for course in total_course_list if course]
            
            # Process course progress data
            if course_progress:
                # Split the progress string into individual records
                progress_entries = []
                if ';' in course_progress:
                    progress_entries = [
                        entry.strip('()').split(',')
                        for entry in course_progress.split(';')
                        if entry.strip()
                    ]
                else:
                    # Handle single entry case
                    single_entry = course_progress.strip('()').split(',')
                    if len(single_entry) == 3:
                        progress_entries = [single_entry]
                
                # Calculate progress for each course
                for entry in progress_entries:
                    if len(entry) == 3:
                        try:
                            playlist_id = int(entry[0])
                            total_videos = int(entry[1])
                            current_video = int(entry[2])
                            
                            # Calculate completion percentage
                            if total_videos > 0:
                                percentage = (current_video / total_videos) * 100
                                # If current_video equals total_videos, mark as 100%
                                if current_video == total_videos:
                                    percentage = 100
                            else:
                                percentage = 0
                            
                            # Determine status
                            status = 'in_progress'
                            if current_video == total_videos or playlist_id in progress_data['completed_courses']:
                                status = 'completed'
                            elif current_video == 0:
                                status = 'not_started'
                            
                            course_data = {
                                'playlist_id': playlist_id,
                                'total_videos': total_videos,
                                'current_video': current_video,
                                'progress_percentage': round(percentage, 1),
                                'remaining_videos': total_videos - current_video,
                                'status': status
                            }
                            
                            progress_data['individual_progress'].append(course_data)
                            
                            # Update completed courses if 100% progress
                            if percentage == 100 and playlist_id not in progress_data['completed_courses']:
                                progress_data['completed_courses'].append(playlist_id)
                            
                        except (ValueError, IndexError) as e:
                            print(f"Error processing entry {entry}: {str(e)}")
                            continue
            
            # Add any completed courses that aren't in progress data
            for course_id in progress_data['completed_courses']:
                if not any(p['playlist_id'] == course_id for p in progress_data['individual_progress']):
                    progress_data['individual_progress'].append({
                        'playlist_id': course_id,
                        'total_videos': None,
                        'current_video': None,
                        'progress_percentage': 100,
                        'remaining_videos': 0,
                        'status': 'completed'
                    })
            
            # Calculate summary statistics
            if progress_data['individual_progress']:
                total_percentage = sum(course['progress_percentage'] for course in progress_data['individual_progress'])
                progress_data['summary'].update({
                    'average_progress': round(total_percentage / len(progress_data['individual_progress']), 1),
                    'courses_in_progress': len([c for c in progress_data['individual_progress'] if c['status'] == 'in_progress']),
                    'courses_completed': len(progress_data['completed_courses'])
                })
            
            # Store the calculated progress data
            try:
                progress_json = json.dumps(progress_data)
                cursor.execute("""
                    UPDATE student_signup 
                    SET individual_course_progress = %s 
                    WHERE Email = %s
                """, (progress_json, user_email))
                connection.commit()
            except Exception as e:
                print(f"Error updating individual course progress: {e}")
            
            return jsonify(progress_data), 200
            
    except Exception as e:
        print(f"Error tracking course progress: {e}")
        return jsonify({
            'message': 'Error tracking course progress',
            'error': str(e)
        }), 500
        
    finally:
        if 'connection' in locals():
            connection.close()            

#### Route For User Based Navbar ####
@app.route('/check_session')
def check_session():
    logged_in = 'user_email' in session
    print(f"Session contents: {session}")  # Debug print
    print(f"Is logged in: {logged_in}")   # Debug print
    return jsonify({
        'loggedIn': logged_in,
        'sessionData': dict(session)  # This helps us see what's in the session
    })
