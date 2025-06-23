# VLLMSPA - Authentication System

This project includes a complete authentication system with login and register functionality, built with React frontend and Flask backend.

## Features

- ✅ User registration with validation
- ✅ User login with JWT tokens
- ✅ Protected routes
- ✅ Persistent authentication state
- ✅ Modern, responsive UI
- ✅ Form validation and error handling
- ✅ Automatic redirect after login

## Project Structure

```
VLLMSPA/
├── backend/
│   ├── app/
│   │   ├── routes/
│   │   │   ├── auth_routes.py      # Authentication endpoints
│   │   │   └── protected_routes.py # Protected route example
│   │   ├── models.py               # User model
│   │   └── __init__.py             # Flask app configuration
│   ├── requirements.txt
│   └── run.py
├── frontend/
│   ├── src/
│   │   ├── contexts/
│   │   │   └── AuthContext.jsx     # Authentication state management
│   │   ├── components/
│   │   │   ├── ProtectedRoute.jsx  # Route protection component
│   │   │   └── Navbar.jsx          # Updated navbar with auth
│   │   ├── pages/
│   │   │   ├── Login.jsx           # Login page
│   │   │   ├── Register.jsx        # Register page
│   │   │   └── Auth.css            # Authentication styles
│   │   └── App.jsx                 # Updated with auth routes
│   └── package.json
└── README.md
```

## Quick Start with Docker Compose

The easiest way to run the application is using Docker Compose:

1. **Start all services:**
   ```bash
   docker-compose up -d
   ```

2. **Initialize the database (if you get "relation user does not exist" error):**
   ```bash
   # Option 1: Use the reset script
   chmod +x reset-db.sh
   ./reset-db.sh
   
   # Option 2: Manual reset
   docker-compose down
   docker volume rm vllmspa_pgdata
   docker-compose up -d
   sleep 10
   docker-compose exec flask python init_db.py
   ```

3. **Access the application:**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:5000

## Manual Setup Instructions

### Backend Setup

1. **Navigate to the backend directory:**
   ```bash
   cd backend
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**
   Create a `.env` file in the backend directory with:
   ```env
   SECRET_KEY=your-super-secret-key-change-this-in-production
   DATABASE_URL=sqlite:///app.db
   CORS_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
   OLLAMA_MODEL=llama3.1:8b
   PRELOAD_MODEL=true
   ```

5. **Initialize the database:**
   ```bash
   python init_db.py
   ```

6. **Run the backend server:**
   ```bash
   python run.py
   ```
   The backend will be available at `http://localhost:5000`

### Frontend Setup

1. **Navigate to the frontend directory:**
   ```bash
   cd frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Run the development server:**
   ```bash
   npm run dev
   ```
   The frontend will be available at `http://localhost:3000`

## API Endpoints

### Authentication Endpoints

- `POST /auth/register` - Register a new user
  - Body: `{"username": "string", "password": "string"}`
  - Response: `{"msg": "User registered successfully"}`

- `POST /auth/login` - Login user
  - Body: `{"username": "string", "password": "string"}`
  - Response: `{"access_token": "jwt_token"}`

- `GET /protected` - Protected route example
  - Headers: `Authorization: Bearer <token>`
  - Response: `{"logged_in_as": "username"}`

## Usage

1. **Register a new account:**
   - Navigate to `/register`
   - Fill in username and password
   - Click "Create Account"

2. **Login:**
   - Navigate to `/login`
   - Enter your credentials
   - Click "Sign In"

3. **Access protected routes:**
   - After login, you'll be redirected to the home page
   - All protected routes are now accessible
   - The navbar will show "Logout" instead of "Login"

4. **Logout:**
   - Click the "Logout" button in the navbar
   - You'll be redirected to the login page

## Troubleshooting

### Database Issues

If you encounter "relation 'user' does not exist" error:

1. **For Docker Compose:**
   ```bash
   # Reset the database completely
   docker-compose down
   docker volume rm vllmspa_pgdata
   docker-compose up -d
   sleep 10
   docker-compose exec flask python init_db.py
   ```

2. **For manual setup:**
   ```bash
   cd backend
   python init_db.py
   ```

### CORS Issues

- Make sure the backend CORS_ORIGINS includes your frontend URL
- For Docker: `http://localhost:3000`
- For development: `http://localhost:5173`

### Port Conflicts

- Frontend runs on port 3000 (Docker) or 5173 (development)
- Backend runs on port 5000
- Change ports in `docker-compose.yaml` or `vite.config.js` if needed

## Features in Detail

### Authentication Context
- Manages user authentication state across the application
- Handles token storage in localStorage
- Provides login, register, and logout functions
- Automatically sets Authorization headers for API calls

### Protected Routes
- Wraps components that require authentication
- Redirects unauthenticated users to login page
- Preserves the original destination for post-login redirect

### Form Validation
- Client-side validation for registration form
- Password confirmation matching
- Username and password length requirements
- Real-time error clearing

### Error Handling
- Displays server errors in user-friendly format
- Handles network errors gracefully
- Shows loading states during API calls

### Responsive Design
- Mobile-friendly authentication forms
- Modern gradient backgrounds
- Smooth animations and transitions
- Consistent styling across components

## Security Features

- JWT token-based authentication
- Password hashing with Werkzeug
- CORS configuration for frontend-backend communication
- Protected routes with automatic redirects
- Token storage in localStorage with automatic cleanup

## Development Notes

- The backend uses PostgreSQL in Docker, SQLite for manual setup
- JWT tokens are used for session management
- CORS is configured to allow frontend development server
- All authentication state is managed through React Context

## Next Steps

- Add password reset functionality
- Implement email verification
- Add user profile management
- Enhance security with refresh tokens
- Add rate limiting for authentication endpoints 