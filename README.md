# Asociación Cultural Peña el Revoque

A comprehensive Django-based web application for managing memberships, events, payments, and merchandising for "Asociación Cultural Peña el Revoque".

## Overview

This project is a full-featured membership management system built with Django that enables our organization to:
- Manage member registrations and profiles
- Organize and track event attendance
- Handle membership fees and payments
- Manage merchandising inventory
- Process contact inquiries
- Control access with role-based permissions (Moderator/Manager)

## Features

### Member Management
- **Member Registration**: Complete registration system with secure password hashing
- **Member Profiles**: Detailed profiles with personal information, membership type, and payment history
- **Member Directory**: Searchable and paginated list of all members (restricted access)
- **Profile Editing**: Members and administrators can update profile information

### Event Management
- **Event Creation**: Add new events with details (name, date, location, description, images)
- **Event Attendance**: Members can register for events with email/password authentication
- **Attendance Tracking**: View and manage event participant lists
- **Event Calendar**: Browse upcoming and past events

### Membership & Payments
- **Membership Tiers**: Different membership types with varying prices and benefits
- **Payment Tracking**: Record and monitor membership fee payments
- **Payment History**: View payment records for each member
- **Flexible Pricing**: Configure custom membership tiers and pricing

### Merchandising
- **Product Catalog**: Browse available merchandise with images and descriptions
- **Product Management**: Add, edit, and manage merchandise inventory
- **Product Details**: Detailed product pages with multiple images

### Communication
- **Contact Form**: Allow visitors and members to send inquiries
- **Message Management**: Administrators can view and manage contact messages
- **Email Integration**: Email-based contact system

### Access Control
- **Role-Based Permissions**: Moderator and Manager roles with different access levels
- **Secure Authentication**: Password hashing with PBKDF2
- **Protected Views**: Restricted areas for administrators only

## Technology Stack

- **Backend Framework**: Django 5.2.7
- **Database**: SQLite (development) / MySQL (production-ready)
- **Server**: Gunicorn + Uvicorn for production deployment
- **Static Files**: WhiteNoise for efficient static file serving
- **Template Engine**: Django Templates
- **Authentication**: Django built-in authentication system
- **Password Security**: Django's PBKDF2 password hasher

### Key Dependencies
- `Django==5.2.7` - Web framework
- `gunicorn==23.0.0` - WSGI HTTP Server
- `uvicorn==0.38.0` - ASGI server
- `mysqlclient==2.2.7` - MySQL database connector
- `python-decouple==3.8` - Configuration management
- `whitenoise==6.11.0` - Static file serving

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- MySQL (optional, for production)

### Setup Instructions

1. **Clone the repository**
   ```bash
   git clone https://github.com/DiegoLopezAroca/Prototipo-Ingenieria-Web.git
   cd Prototipo-Ingenieria-Web
   ```

2. **Navigate to the project directory**
   ```bash
   cd proj_iw
   ```

3. **Create a virtual environment**
   ```bash
   # Windows
   python -m venv env_iw
   env_iw\Scripts\activate

   # Linux/Mac
   python3 -m venv env_iw
   source env_iw/bin/activate
   ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Configure environment variables**
   
   Create a `.env` file in the `proj_iw` directory based on `.env.example`:
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` and configure the following variables:
   ```env
   SECRET_KEY=your-secret-key-here
   DEBUG=True
   DB_NAME=your_database_name
   DB_USER=your_database_user
   DB_PASSWORD=your_database_password
   DB_HOST=localhost
   DB_PORT=3306
   RENDER_EXTERNAL_HOSTNAME=localhost
   MODERADOR_PASS=moderator_password
   GESTOR_PASS=manager_password
   ```

6. **Run database migrations**
   ```bash
   python manage.py migrate
   ```

7. **Create a superuser (optional)**
   ```bash
   python manage.py createsuperuser
   ```

8. **Collect static files (for production)**
   ```bash
   python manage.py collectstatic --no-input
   ```

9. **Run the development server**
   ```bash
   python manage.py runserver
   ```

10. **Access the application**
    
    Open your browser and navigate to: `http://localhost:8000`

## Configuration

### Database Configuration

**Development (SQLite)**: The project uses SQLite by default for development.

**Production (MySQL)**: For production, configure MySQL in your `.env` file:
```env
DB_NAME=production_db
DB_USER=db_user
DB_PASSWORD=db_password
DB_HOST=your_host
DB_PORT=3306
```

### User Roles

The system supports three access levels:
1. **Superuser**: Full administrative access
2. **Moderator**: Can manage members, events, and content
3. **Manager (Gestor)**: Can manage members, events, and content
4. **Regular Members**: Limited access to public features

## Project Structure

```
Prototipo-Ingenieria-Web/
├── proj_iw/                      # Main Django project
│   ├── appProjectDjango/         # Main application
│   │   ├── models.py             # Database models (Socio, Eventos, Cuotas, etc.)
│   │   ├── views.py              # View controllers
│   │   ├── urls.py               # URL routing
│   │   ├── forms.py              # Forms (included in models.py)
│   │   ├── templates/            # HTML templates
│   │   ├── static/               # CSS, JS, images
│   │   ├── migrations/           # Database migrations
│   │   └── tests.py              # Unit tests
│   ├── proj_iw/                  # Project settings
│   │   ├── settings.py           # Django settings
│   │   ├── urls.py               # Main URL configuration
│   │   ├── wsgi.py               # WSGI configuration
│   │   └── asgi.py               # ASGI configuration
│   ├── manage.py                 # Django management script
│   ├── requirements.txt          # Python dependencies
│   ├── build.sh                  # Build script for deployment
│   └── .env.example              # Environment variables template
└── README.md                     # This file
```

## Database Schema

### Main Models

- **Socio (Member)**: Stores member information (name, email, password, phone, membership type)
- **Eventos (Events)**: Event details (name, date, location, description, image)
- **Cuotas (Membership Tiers)**: Membership types with pricing and benefits
- **Pagos (Payments)**: Payment records linking members to membership fees
- **Merchandising**: Product catalog with prices and descriptions
- **Contacto (Contact)**: Contact form submissions
- **AsistenciaEvento (Event Attendance)**: Tracks member attendance at events

### Key Relationships

**Many-to-Many:**
- Member ↔ Events (through AsistenciaEvento)

**One-to-Many:**
- Member → Payments
- Membership Tier → Payments
- Member → Contact Messages

## Usage

### For Members

1. **Register**: Create an account with your personal information and select a membership tier
2. **Browse Events**: View upcoming events and their details
3. **Register for Events**: Sign up for events using your email and password
4. **View Merchandising**: Browse available products
5. **Contact**: Send inquiries through the contact form

### For Administrators (Moderator/Manager)

1. **Manage Members**: View member list, edit profiles, track payments
2. **Create Events**: Add new events with details and images
3. **Manage Attendance**: View and edit event participant lists
4. **Add Products**: Create new merchandising items
5. **Create Membership Tiers**: Define membership types and pricing
6. **View Messages**: Access and respond to contact form submissions

### Key URLs

- `/` - Home page
- `/registros/` - Member registration
- `/eventos/` - Event list
- `/cuotas/` - Membership tiers
- `/merchandising/` - Product catalog
- `/contacto/` - Contact form
- `/socios/` - Member directory (restricted)
- `/pagos/` - Payment management (restricted)
- `/admin/` - Django admin panel

## Deployment

### Using the Build Script

For production deployment (e.g., on Render, Heroku):

```bash
chmod +x build.sh
./build.sh
```

This script will:
1. Install all dependencies
2. Collect static files
3. Run database migrations

### Production Checklist

- [ ] Set `DEBUG=False` in `.env`
- [ ] Configure production database (MySQL)
- [ ] Set a strong `SECRET_KEY`
- [ ] Configure `RENDER_EXTERNAL_HOSTNAME` or `ALLOWED_HOSTS`
- [ ] Set up HTTPS/SSL
- [ ] Configure email backend for contact forms
- [ ] Set up proper logging
- [ ] Configure static file storage (WhiteNoise is included)
- [ ] Set up backup strategy for database

## Testing

Run the test suite:
```bash
python manage.py test
```

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Coding Standards

- Follow PEP 8 style guide for Python code
- Use meaningful variable and function names
- Add comments for complex logic
- Write tests for new features
- Update documentation as needed

## License

This project is part of a Web Engineering course prototype. Please consult with the repository owner regarding usage and distribution rights.

## Known Issues

- Legacy plain-text passwords are automatically converted to hashed passwords on first login
- Image uploads are stored as filenames (requires additional storage configuration)

## Support

For questions or issues, please:
1. Check existing GitHub Issues
2. Open a new issue with detailed description
3. Use the contact form in the application

## Version History

- **v1.0** (Current) - Initial release with core membership management features

---

**Note**: This is a prototype developed for educational purposes as part of a Web Engineering course.
