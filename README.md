# Cinema Website Project

This is a web application project that allows users to search for movies, choose seats in a cinema, purchase tickets online, and receive tickets via email with a QR code. Additionally, the system supports in-person ticket purchases, where cash payments can be recorded. The project utilizes the Stripe API for online payments, the IMDb API for movie details, and SQLite for database management. Flask is used as the web framework, and various Flask extensions such as Flask-Migrate, Flask-Bcrypt, Flask-Mail, and WTForms are integrated into the application. PDFKit is used for printing tickets.

## Table of Contents

- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Database](#database)
- [APIs](#apis)
- [Contributors](#contributors)
- [License](#license)

## Features

- User Registration and Authentication.
- Movie Search and Selection.
- Seat Reservation.
- Online Payment via Stripe.
- Ticket Generation with QR Code via Email.
- In-Person Ticket Purchase and Cash Payment Recording.
- Admin Functions:
  - Movie Database Management (Add/Modify/Delete Movies).
  - View Movie Sales Data.
  - IMDb Integration for Movie Details.

## Requirements

- Python 3.12
- Flask
- SQLite
- Stripe API Key
- IMDb API Key
- Flask-Migrate
- Flask-Bcrypt
- Flask-Mail
- WTForms
- PDFKit

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/cinema.git
   cd cinema
2. Create a virtual environment and activate it:

   ```bash
   python -m venv venv
   source venv/bin/activate
3. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
4. Set up your environment variables for the Stripe API Key, IMDb API Key, and other necessary configurations.
5. Initialize and migrate the database:

   ```bash
   flask db init
   flask db migrate
   flask db upgrade

## Usage

1. Run the Flask development server:
   
   ```bash
   flask run
2. Access the web application in your browser at http://localhost:5000

## Database

The SQLite database is used to store user data, movie information, ticket records, and more. You can use any SQLite database management tool to explore and manipulate the data.

## APIs

- Stripe API: Set up your Stripe API keys to enable online payments.
- IMDb API: Obtain an IMDb API key to fetch movie details.

## Contributors

We would like to extend our heartfelt thanks to the following contributors for their valuable contributions to this project:

-[tobiy105](https://github.com/tobiy105)
-[AlecMillward](https://gitlab.com/AlecMillward)
-[BenJOHara](https://github.com/BenJOHara)
-[MattNWaite](https://github.com/MattNWaite)
-[AwkwardBoi1 ](https://github.com/AwkwardBoi1)

Your dedication and hard work have been instrumental in making this project a success. We appreciate your commitment to the development and improvement of this software engineering project during the second semester of year 2. Thank you for your contributions!

## License

This project is licensed under the MIT License - see the LICENSE file for details.
