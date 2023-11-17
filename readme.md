# Shatel Test (Registration Users)

This is a test project for registering users from a large CSV file.

## Backend (Django)


1. Install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

2. Apply database migrations:
   ```bash
   python manage.py migrate
   ```

3. Create a superuser (admin) for accessing the Django admin panel:
   ```bash
   python manage.py createsuperuser
   ```

4. Start the Django development server:
   ```bash
   python manage.py runserver
   ```
Now, you can access the Django admin panel at [http://localhost:8000/admin](http://localhost:8000/admin) and use the superuser credentials.

## Frontend (React)

To run the React frontend, follow these steps:

1. Install the required Node.js packages:
   ```bash
   npm install
   ```

2. Start the development server:
   ```bash
   npm run dev
   ```

This will start the development server for the React app.

### Build (React)

If you need to build the React app for production, use the following command:

```bash
npm run build
```

## Project Structure

- `backend/`: Django, root project and registration_user settings
- `frontend/`: React vite-project
- `requirements.txt`: List of Python dependencies
- `package.json`: Node.js package configuration
- `tsconfig.json`: TypeScript configuration for the React app
- `tsconfig.node.json`: TypeScript configuration for Node.js