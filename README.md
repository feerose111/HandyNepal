<<<<<<< HEAD
# HandyNepal
=======
# HandyNepal

A platform for local handicraft e-commerce, connecting artisans with customers worldwide.

## Environment Variables Setup

This project uses environment variables to manage sensitive information like database credentials and Django settings. Follow these steps to set up your environment:

1. Create a `.env` file in the project root directory (same level as `manage.py`)
2. Add the following variables to your `.env` file:

```
# Django Settings
SECRET_KEY=your_secret_key_here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database Settings
DB_NAME=your_database_name
DB_USER=your_database_user
DB_PASSWORD=your_database_password
DB_HOST=localhost
DB_PORT=5432
```

3. Replace the placeholder values with your actual configuration

## Installation

1. Clone the repository
2. Create a virtual environment: `python -m venv venv`
3. Activate the virtual environment:
   - Windows: `venv\Scripts\activate`
   - Unix/MacOS: `source venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Set up your `.env` file as described above
6. Run migrations:
   ```
   python manage.py makemigrations
   python manage.py migrate
   ```
7. Create a superuser: `python manage.py createsuperuser`
8. Run the development server: `python manage.py runserver`

## Features

- User authentication with custom user model
- Artisan profiles and stories
- Product collections
- Contact information
- Responsive design

## Contributing

1. Fork the repository
2. Create your feature branch: `git checkout -b feature/your-feature`
3. Commit your changes: `git commit -m 'Add some feature'`
4. Push to the branch: `git push origin feature/your-feature`
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
>>>>>>> 370c5746ba989c0bd01ce00ff0797d72124853f3
