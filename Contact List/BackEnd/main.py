from flask import request, jsonify
from config import app, db
from models import Contact

@app.route('/contacts', methods=['GET'])
def get_contacts():
    contacts = Contact.query.all()
    json_contacts = [contact.to_json() for contact in contacts]
    return jsonify({"contacts": json_contacts}), 200

@app.route('/create_contact', methods=['POST'])
def create_contact():
    data = request.json
    first_name = data.get("firstName")
    last_name = data.get("lastName")
    email = data.get("email")

    if not first_name or not last_name or not email:
        return jsonify({"message": "You must fill up all the fields."}), 400

    new_contact = Contact(first_name=first_name, last_name=last_name, email=email)
    try:
        db.session.add(new_contact)
        db.session.commit()
        return jsonify({"message": "New Contact is created!"}), 201
    except Exception as e:
        return jsonify({"message": str(e)}), 422

@app.route('/update_contact/<int:contact_id>', methods=['PATCH'])
def update_contact(contact_id):
    contact = Contact.query.get(contact_id)

    if not contact:
        return jsonify({"message": "Contact not found"}), 404

    data = request.json
    contact.first_name = data.get("firstName", contact.first_name)
    contact.last_name = data.get("lastName", contact.last_name)
    contact.email = data.get("email", contact.email)

    try:
        db.session.commit()
        return jsonify({"message": "Contact Updated."}), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 400

@app.route('/delete_contact/<int:contact_id>', methods=['DELETE'])
def delete_contact(contact_id):
    contact = Contact.query.get(contact_id)

    if not contact:
        return jsonify({"message": "Contact not found"}), 404

    db.session.delete(contact)
    db.session.commit()

    return jsonify({"message": "Contact deleted!"}), 200

if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    app.run(debug=True)
