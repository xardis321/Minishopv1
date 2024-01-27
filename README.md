# minishop
Welcome to the Minishop Computer System, your solution for efficient inventory management and sales processing. This README will guide you through the installation process and help you get started with the system.

Prerequisites:

Python 3.11.4: Ensure you have Python 3.11.4 installed on your system. You can download it from the official Python website: https://www.python.org/downloads/
Installation Steps:

Set Up Your Environment: Clone this repository and navigate to the project directory.

Check Python Version:

Open a terminal.
Run the command: python --version
Ensure it displays Python 3.11.4.
Install pip (if not installed):

If pip is not installed, run the following command to install it:
arduino
Copy code
python -m ensurepip --default-pip
Install Django:

Run the following command to install Django 4.2.4:
Copy code
pip install Django==4.2.4
Install django-import-export:

Run the following command to install the import-export module:
arduino
Copy code
pip install django-import-export
Database Migration:

Run the following commands to perform database migrations:
Copy code
python manage.py makemigrations
python manage.py migrate
Create Superuser:

Create a superuser to access the admin panel:
Copy code
python manage.py createsuperuser
Run the Server:

Start the development server with the following command:
Copy code
python manage.py runserver
Access the system by opening your web browser and navigating to http://localhost:8000/
Troubleshooting:

If you encounter any issues during installation or usage, please refer to the system's documentation or contact our support team for assistance.
Contact Support:

If you require further assistance, encounter errors, or have any questions, please don't hesitate to contact our support team at support@craftbiz.com.
Thank you for choosing the CraftBiz Computer System. We hope this system enhances your business operations and makes managing your inventory and sales a breeze
