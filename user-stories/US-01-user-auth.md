# US-01: User Signup & Login

## 🎯 Goal
As a user, I want to securely sign up and log in to the system so that my subscriptions and meal activities can be tracked personally.

---

## 📚 Description
This feature enables new users (students/professionals) to register an account using their name, email, and password, and securely log in to access personalized features like viewing subscriptions, scanning QR codes, and tracking meal history.

---

## ✅ Acceptance Criteria

- [ ] User can register with `name`, `email`, `password`, and `phone number`.
- [ ] Passwords are securely hashed before saving to the database.
- [ ] Duplicate email registration should return an appropriate error.
- [ ] User receives a token (JWT or session) on successful login.
- [ ] Token is required for accessing user-only routes.
- [ ] Admins and users are handled with separate roles.

---

## 🛠 Tasks

### Frontend
- [ ] Create a registration form
- [ ] Create a login form
- [ ] Integrate with API using Axios
- [ ] Store JWT in localStorage or secure cookie
- [ ] Display login error messages (invalid credentials)

### Backend (FastAPI)
- [ ] Create `/register` route to handle user creation
- [ ] Create `/login` route to issue JWT token
- [ ] Use `bcrypt` or similar to hash and verify passwords
- [ ] Define user model in SQLAlchemy with fields:
  - id, name, email, phone, hashed_password, role
- [ ] Implement JWT authentication dependency
- [ ] Protect private routes using user role

---

## 🔐 Security
- Use HTTPS in production
- Apply input validation and rate limiting (later)
- Never expose password or store plain text
- Hash passwords using `bcrypt`
- Secure JWT secret and set short expiry durations

---

## 📦 API Endpoints

| Method | Endpoint      | Description                    |
|--------|---------------|--------------------------------|
| POST   | /api/register | Register new user              |
| POST   | /api/login    | Authenticate user & get token  |
| GET    | /api/me       | Get current user profile       |

---

## 📝 Notes

- 🔐 Plan to use **FastAPI's OAuth2PasswordBearer** for JWT handling.
- 🔄 Use **Pydantic models** for strict schema validation and safe responses.
- ✅ Store token in frontend with **httpOnly cookie** if you want extra security against XSS.
- 🌐 Extend later to support:
  - **Google login (OAuth2)**
  - **Mobile number with OTP login (using Twilio/MSG91)**
- 👥 Plan role-based access early (`user`, `admin`, possibly `super_admin`) using decorators or dependency injection.
- ⚠️ Handle all error states gracefully: invalid input, expired token, duplicate email, etc.

---

