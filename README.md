Cinema Website Project

This is a web application project that allows users to search for movies, choose seats in a cinema, purchase tickets online, and receive tickets via email with a QR code. Additionally, the system supports in-person ticket purchases, where cash payments can be recorded. The project utilizes the Stripe API for online payments, the IMDb API for movie details, and SQLite for database management. Flask is used as the web framework, and various Flask extensions such as Flask-Migrate, Flask-Bcrypt, Flask-Mail, and WTForms are integrated into the application. PDFKit is used for printing tickets.
Table of Contents

    Features
    Requirements
    Installation
    Usage
    Database
    APIs
    Contributing
    License

Features

    User Registration and Authentication.
    Movie Search and Selection.
    Seat Reservation.
    Online Payment via Stripe.
    Ticket Generation with QR Code via Email.
    In-Person Ticket Purchase and Cash Payment Recording.
    Admin Functions:
        Movie Database Management (Add/Modify/Delete Movies).
        View Movie Sales Data.
        IMDb Integration for Movie Details.

Requirements

    Python 3.x
    Flask
    SQLite
    Stripe API Key
    IMDb API Key
    Flask-Migrate
    Flask-Bcrypt
    Flask-Mail
    WTForms
    PDFKit

Installation

    Clone the repository:

    bash

git clone https://github.com/yourusername/cinema.git
cd cinema

Create a virtual environment and activate it:

bash

python -m venv venv
source venv/bin/activate

Install the required dependencies:

bash

pip install -r requirements.txt

Set up your environment variables for the Stripe API Key, IMDb API Key, and other necessary configurations.

Initialize and migrate the database:

bash

    flask db init
    flask db migrate
    flask db upgrade

Usage

    Run the Flask development server:

    bash

    flask run

    Access the web application in your browser at http://localhost:5000.

Database

The SQLite database is used to store user data, movie information, ticket records, and more. You can use any SQLite database management tool to explore and manipulate the data.
APIs

    Stripe API: Set up your Stripe API keys to enable online payments.
    IMDb API: Obtain an IMDb API key to fetch movie details.

Contributing

Contributions are welcome! Please follow the Contributing Guidelines for details on how to contribute to this project.
License

This project is licensed under the MIT License - see the LICENSE file for details.

Feel free to customize this README to suit your project's specific needs. Don't forget to create a CONTRIBUTING.md file and a LICENSE file, and include them in your repository for better documentation and collaboration with others.