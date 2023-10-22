# FlaskChat
Author: Vedic Dutta
Roll No.: 21CH10077
University: Indian Institute of Technology Kharagpur
Department: Chemical Engineering

This is a README file for FlaskChat, a Flask-based real-time messaging application.

## Table of Contents

- [Project Overview](#project-overview)
- [Installation](#installation)
- [Dependencies](#dependencies)
- [Usage](#usage)
- [Contact](#contact)

## Project Overview

FlaskChat is a Flask-based real-time messaging application designed to facilitate quick and efficient chat conversations. It offers a user-friendly interface for real-time communication and empowers users to engage in instant messaging.

Powered by Flask, FlaskChat provides a strong foundation for real-time chat applications, enabling users to focus on real-time conversations with friends, colleagues, or anyone they want to chat with.

Key Features:

**User-Friendly Interface**: FlaskChat offers an intuitive interface that makes it easy to engage in real-time chat conversations.\
**Secure Account Management**: User accounts and chat messages are securely handled and protected.\
**Real-Time Messaging**: Experience instant messaging with friends and colleagues in a real-time chat environment.

FlaskChat is built for real-time communication and simplifies the process of chatting with others.

## Installation

To get started with FlaskChat, follow these steps to install and set up the project on your local development environment:

1. **Clone the Repository**: 
   - Clone the FlaskChat repository from GitHub using the following command:
     ```
     git clone https://github.com/your-username/flaskchat.git
     ```

2. **Navigate to the Project Directory**: 
   - Move into the project directory using the following command:
     ```
     cd flaskchat
     ```

3. **Create and Activate a Virtual Environment (Optional but Recommended)**: 
   - To manage dependencies effectively, consider using a virtual environment. Use the following commands to create and activate one:

For Windows:
python -m venv venv
venv\Scripts\activate


For macOS/Linux:
python3 -m venv venv
source venv/bin/activate


4. **Initialize the Database**: 
- FlaskChat uses a database to store chat messages and user information. Initialize the database by running these commands:
  ```
  flask db init
  flask db migrate
  flask db upgrade
  ```

5. **Start the Flask Development Server**: 
- Launch the Flask development server with the following command:
  ```
  flask run
  ```

6. **Access FlaskChat**: 
- Open your web browser and visit http://localhost:8030 to access FlaskChat locally. You'll see the FlaskChat chat interface.

These instructions assume you have Python and pip installed on your system.

## Usage

To use FlaskChat effectively, follow these guidelines:

1. **Registration**: Start by registering for a new account on FlaskChat. Provide the necessary details to create your account.

2. **Login**: After registering, log in to your account using your credentials. FlaskChat will authenticate your credentials and grant you access to the chat interface.

3. **Chat Conversations**: Use the chat interface to engage in real-time conversations with other users. Select a user from the list, type your message, and click "Send" to initiate a chat.

4. **Receive Messages**: Messages sent to you will appear in the chat interface.

5. **Log Out**: Log out of your FlaskChat account when you're done with your chat session to keep your account secure.

## Dependencies

FlaskChat relies on several dependencies to provide its real-time chat functionality. The key dependencies include:

- Flask
- Flask-SocketIO
- Flask-SQLAlchemy

Make sure to keep your dependencies up to date and consider using a virtual environment to manage your project's dependencies effectively.

## Contact

Feel free to drop suggestions at: vedicdutta86@gmail.com
