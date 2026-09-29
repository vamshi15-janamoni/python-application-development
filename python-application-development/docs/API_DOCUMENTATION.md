# API Documentation

Base URL: `http://127.0.0.1:5000`

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/` | API status |
| GET | `/users` | Get all users |
| GET | `/users/<id>` | Get one user |
| POST | `/users` | Create user |
| PUT | `/users/<id>` | Update user |
| DELETE | `/users/<id>` | Delete user |

### POST example
```json
{"name": "Vamshi", "email": "vamshi@example.com"}
```

The API validates required fields and rejects duplicate email addresses.
