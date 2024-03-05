@app.route('/registration', methods=['GET', 'POST'])
def registration():
    try:
        if request.method == 'POST':
            full_name = request.form.get('full_name')
            email = request.form.get('email')
            phone_number = request.form.get('phone_number')
            address = request.form.get('address')
            educational_level = request.form.get('educational_level')
            institution = request.form.get('institution')
            educational_certificates = request.form.get('educational_certificates')
            freelancing_experience = request.form.get('freelancing_experience')
            portfolio_link = request.form.get('portfolio_link')
            availability = request.form.get('availability')
            preferred_work_type = request.form.get('preferred_work_type')
            hourly_rate = request.form.get('hourly_rate')
            language_proficiency = request.form.get('language_proficiency')
            certifications = request.form.get('certifications')
            linkedIn_profile = request.form.get('linkedIn_profile')
            github_profile = request.form.get('github_profile')
            course_joining_date = request.form.get('course_joining_date')

        # Check for required fields
            if not ([full_name, email, phone_number, address, educational_level, institution, educational_certificates, availability, course_joining_date]):
                return jsonify({"message": "You must fill up these required fields."}), 400
            
            # Perform database operations
            with connection.cursor() as cursor:
                trainee_create_sql = "INSERT INTO trainees (full_name, email, phone_number, address, educational_level, institution, educational_certificates, freelancing_experience, portfolio_link, availability, preferred_work_type, hourly_rate, language_proficiency, certifications, linkedIn_profile, github_profile, course_joining_date) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                cursor.execute(trainee_create_sql, (full_name, email, phone_number, address, educational_level, institution, educational_certificates, freelancing_experience, portfolio_link, availability, preferred_work_type, hourly_rate, language_proficiency, certifications, linkedIn_profile, github_profile, course_joining_date))
                connection.commit()

            return jsonify({'success': 'Registration successful'}), 200
        
        elif request.method == 'GET':
            return jsonify({'message': 'GET request received'}), 200

    except Exception as e:
        return jsonify({'error': f"Request error: {str(e)}"}), 500