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

########################################################################################################################################################################################

################################################################ N   E   W        V   E   R   S   I   O   N ############################################################################


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

////////////////////////////////////////  RENEWED ROUTES FOR IMAGE VALIDATION TO SAVE BEST QUALITY IMAGE AS BLOB IN DATABASE /////////////////////////////////////////////////////////
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

                sql_select_blog = "SELECT comment, emails_commented, user_comment FROM user_blog WHERE blog_id = %s"
                cursor.execute(sql_select_blog, (blog_id,))
                blog = cursor.fetchone()

                if not blog:
                    return jsonify({"message": "Blog post not found"}), 404

                comments_count = blog['comment'] if blog['comment'] is not None else 0
                emails_commented = blog['emails_commented'] or ''
                user_comment = blog['user_comment'] or ''

                comments_count += 1
                updated_emails_commented = f"{emails_commented},{user_email}" if emails_commented else user_email

                import time
                unique_key = f"{full_name}_{int(time.time())}"
                new_comment_entry = f"{unique_key}:{comment}"
                updated_user_comment = f"{user_comment},{new_comment_entry}" if user_comment else new_comment_entry

                sql_update = """
                    UPDATE user_blog
                    SET comment = %s,
                        emails_commented = %s,
                        user_comment = %s
                    WHERE blog_id = %s
                """
                cursor.execute(sql_update, (comments_count, updated_emails_commented, updated_user_comment, blog_id))

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


