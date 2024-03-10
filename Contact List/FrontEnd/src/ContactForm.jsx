import { useState } from 'react';

const ContactForm = () => {
    const [firstName, setFirstName] = useState("");
    const [lastName, setLastName] = useState("");
    const [email, setEmail] = useState(""); // Corrected variable name

    const onSubmit = async (e) => {
        e.preventDefault();

        const data = {
            firstName,
            lastName, // Corrected variable name
            email
        };

        const url = "http://127.0.0.1:5000/create_contact"; // Corrected URL
        const options = {
            method: 'POST', // Corrected HTTP method
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(data)
        };

        const response = await fetch(url, options);

        if (response.status !== 201 && response.status !== 200) {
            const responseData = await response.json(); // Renamed variable to avoid conflict
            alert(responseData.message);
        } else {
            // Handle success case if needed
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
            <button type="submit">Create Contact</button>
           </div>
        </form>
    );
};

export default ContactForm;
