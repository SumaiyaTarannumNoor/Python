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
