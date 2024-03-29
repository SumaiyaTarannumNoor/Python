import { useState } from 'react';

const ContactForm = ({existingContact = {}, updateCallback}) => {
    const [firstName, setFirstName] = useState(existingContact.firstName||"");
    const [lastName, setLastName] = useState(existingContact.lastName||"");
    const [email, setEmail] = useState(existingContact.email||""); // Corrected variable name

    const updating = Object.entries(existingContact).length !== 0


    const onSubmit = async (e) => {
        e.preventDefault();

        const data = {
            firstName,
            lastName,
            email
        };

        const url = "http://127.0.0.1:5000/" + (updating ? `update_contact/${existingContact.id}`:"create_contact")
        const options = {
            method: updating ? "PATCH" : 'POST', 
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(data)
        };

        const response = await fetch(url, options)
        
        if (response.status !== 201 && response.status !== 200) {
            const data = await response.json(); // Renamed variable to avoid conflict
            alert(data.message);
            setTimeout(() => {
                window.location.reload();
            }, 2000);
        } else {
            updateCallback()
        }
    };

    return (
        <form onSubmit={onSubmit}>
            <div className="container">
            <div className="field">
                <label htmlFor="firstName" className="label"><p>First Name</p></label>
                <input
                    type="text"
                    id="firstName"
                    value={firstName}
                    className="input"
                    onChange={(e) => setFirstName(e.target.value)} />
            </div>
            <div className="field">
                <label htmlFor="lastName" className="label"><p>Last Name</p></label>
                <input
                    type="text"
                    id="lastName"
                    value={lastName}
                    className="input"
                    onChange={(e) => setLastName(e.target.value)} />
            </div>
            <div className="field">
                <label htmlFor="email" className="label"><p>Email</p></label>
                <input
                    type="text"
                    id="email"
                    value={email}
                    className="input"
                    onChange={(e) => setEmail(e.target.value)} />
            </div>
            <button type="submit">{updating ? "Update" : "Create New Contact"}</button>
           </div>
        </form>
    );
};

export default ContactForm;
