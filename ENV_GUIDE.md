# Environment Variables Guide for HandyNepal

## Overview

This project uses environment variables to securely manage sensitive information like database credentials and Django settings. This approach keeps sensitive data out of version control and allows for different configurations in development, testing, and production environments.

## Setup Instructions

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

## Environment Variables Explained

### Django Settings

- `SECRET_KEY`: A secret key used for cryptographic signing in Django. Should be a long, random string.
- `DEBUG`: Set to `True` for development, `False` for production.
- `ALLOWED_HOSTS`: Comma-separated list of hosts/domains that your Django site can serve.

### Database Settings

- `DB_NAME`: The name of your PostgreSQL database.
- `DB_USER`: The username to connect to your database.
- `DB_PASSWORD`: The password for the database user.
- `DB_HOST`: The host where your database is running (usually 'localhost' for development).
- `DB_PORT`: The port your database is running on (default is '5432' for PostgreSQL).

## Different Environments

You can create different `.env` files for different environments:

- `.env.development` - For local development
- `.env.testing` - For testing environments
- `.env.production` - For production deployment

To use a specific environment file, you can specify it when running your application:

```bash
# For development (default)
python manage.py runserver

# For production (example using a custom script)
ENV_FILE=.env.production python manage.py runserver
```

## Security Best Practices

1. **Never commit your `.env` file to version control**. It's already added to `.gitignore`.
2. Use strong, unique passwords for your database.
3. In production, set `DEBUG=False` and specify exact `ALLOWED_HOSTS`.
4. Regularly rotate your `SECRET_KEY` in production.
5. Consider using a secrets management service for production environments.

## Troubleshooting

If you encounter issues with environment variables:

1. Verify that your `.env` file exists in the correct location.
2. Check that the variable names match exactly what's expected in `settings.py`.
3. Ensure there are no spaces around the `=` sign in your `.env` file.
4. Make sure the `python-decouple` package is installed (`pip install python-decouple`).

## Additional Resources

- [Python Decouple Documentation](https://github.com/henriquebastos/python-decouple)
- [Django Settings Best Practices](https://docs.djangoproject.com/en/stable/topics/settings/)
