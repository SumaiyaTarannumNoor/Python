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
            users_gallary_sql = "SELECT * FROM ahm_gallary_partners WHERE category = 'gallary' LIMIT 6"
            cursor.execute(users_gallary_sql)
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

        return render_template('user_gallary.html', gallaries=gallary_data, current_page=1, total_pages=total_pages)
    except Exception as e:
        return jsonify({'error': f"Request error: {str(e)}"})
    

# GET NEXT 10 IMAGES
PER_PAGE = 6  # Number of items per page
START_PAGE = 2  # Starting page number

@app.route('/user_gallary_pagination', methods=['GET'])
def user_gallary_pagination():
    try:
        # Get the page number from the request arguments, default to START_PAGE if not provided
        page = request.args.get('page', START_PAGE, type=int)

        # Calculate the OFFSET based on the page number and number of items per page
        offset = (page - 1) * PER_PAGE

        with connection.cursor() as cursor:
            # SQL query to fetch paginated data from the users table
            users_gallary_sql = f"SELECT * FROM ahm_gallary_partners WHERE category = 'gallary' LIMIT %s OFFSET %s"
            cursor.execute(users_gallary_sql, (PER_PAGE, offset))
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
            
            # Perform database operations
            with connection.cursor() as cursor:
                trainee_create_sql = "INSERT INTO trainees (full_name, organization, email, phone_number, address, educational_level, skills, freelancing_experience, portfolio_link, language_proficiency, done_trainings, wantTo_trainings, password) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                cursor.execute(trainee_create_sql, (full_name, organization, email, phone_number, address, educational_level, skills, freelancing_experience, json_data,language_proficiency, done_trainings, wantTo_trainings, password))
                connection.commit()

            return jsonify({'success': 'Registration successful'}), 200
        
        elif request.method == 'GET':
            return jsonify({'message': 'GET request received'}), 200

    except Exception as e:
        return jsonify({'error': f"Request error: {str(e)}"}), 500

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
                blog_sql = "SELECT * FROM blogs WHERE status = 1 ORDER BY created_at DESC LIMIT 6" 
                cursor.execute(blog_sql)
                blog_data = cursor.fetchall()
                
                count_query = "SELECT COUNT(blog_id) FROM blogs"
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
        
PER_PAGE = 6  # Number of items per page
START_PAGE = 2  # Starting page number        
        
@app.route('/blog_pagination', methods=['GET'])
def blog_pagination():
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
    
PER_PAGE = 6  # Number of items per page
START_PAGE = 2  # Starting page number        
        
@app.route('/user_blog_pagination', methods=['GET'])
def user_blog_pagination():
    if 'loggedin' in session and session['loggedin']:
        try:
            writers_name= session['name']
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
                    blog_sql = f"SELECT * FROM blogs WHERE writers_name=%s LIMIT %s OFFSET %s"
                    cursor.execute(blog_sql, (writers_name, PER_PAGE, offset))
                    blog_data = cursor.fetchall()
                    
                    count_query = "SELECT COUNT(blog_id) FROM blogs WHERE writers_name = %s"
                    cursor.execute(count_query, (writers_name))
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
@app.route('/blogs_admin_panel_pagination', methods=['GET', 'POST'])
def blogs_admin_panel_pagination():
    try:
        # Get the page number and sort order from the request arguments
        page = request.args.get('page', START_PAGE, type=int)
        sort_order = request.args.get('sort_order', 'desc')
        
        # Calculate the OFFSET based on the page number and number of items per page
        offset = (page - 1) * PER_PAGE

        with connection.cursor() as cursor:
            # SQL query to fetch paginated data from the blogs table, sorted by created_at in descending order
            blog_sql = f"SELECT * FROM blogs ORDER BY created_at {sort_order} LIMIT %s OFFSET %s"
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

            return jsonify({'success': 'Blog Creation successful'}), 200

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

            return jsonify({'success': 'Blog Creation successful'}), 200

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
