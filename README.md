# C3 Digital Transformation System - Prototype

This project is a prototype for the C3 Digital Transformation System, designed to streamline operations for Consumer Car Care (C3). The system provides tools for managing claims processing, inventory tracking, sales transactions, and user accounts in an efficient, paperless environment.

## Description

The prototype focuses on demonstrating the user interface (UI), data models, and key workflows, serving as a foundation for future development.

Features:
1. Dashboard
- Provides an overview of system activities, including:
- Recent claims
- Dealership inventory status
- Recent sales transactions

2. Claims Processing
- Allows C3 staff to view and manage claims.

3. Inventory Management
- Displays available inventory for dealerships.

4. Sales Portal
- Logs sales transactions and associates them with products and dealerships.

5. User Authentication & Role-Based Access
- Admin users can manage system data.
- Regular users have restricted access to relevant sections.
- Secure login/logout functionality with session management.

## Getting Started

### Installing

Installation & Setup
1. Clone the Repository
* git clone https://github.com/salmaan1-btm/C3-Digital.git
* cd C3-Digital

2. Create a Virtual Environment
* python -m venv venv
* source venv/bin/activate  # Mac/Linux
* venv\Scripts\activate  # Windows

3. Install Dependencies
* pip install -r requirements.txt

4. Apply Database Migrations
* python manage.py migrate

5. Create a Superuser (Admin)
* python manage.py createsuperuser
* Follow the prompts to set up admin credentials.

6. Run the Development Server
* python manage.py runserver
* Visit http://127.0.0.1:8000/ in your browser.

## Authors

Salmaan Khan
- Email: salmaan1@ualberta.ca

Sophia Kim
- Email: syk@ualberta.ca

Sahibpreet Boyal
- Email: sahibpre@ualberta.ca








