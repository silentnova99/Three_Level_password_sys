# Three-Level Authentication System

A Flask-based multi-factor authentication (MFA) web application implementing three layers of security:
1. **Level 1**: Username & Password Authentication
2. **Level 2**: Email-based OTP Verification
3. **Level 3**: QR Code-based One-Time Code Authentication

## Features

✨ **Three-Layer Security**
- Password-based login with username verification
- Email OTP (One-Time Password) confirmation
- QR code scanning with random code validation

🔐 **User Management**
- User registration with email verification
- Secure session management
- Password storage (with recommendations for hashing)
- User logout functionality

📱 **Modern UI**
- Responsive HTML templates
- Bootstrap-styled forms
- QR code generation and display
- Real-time error handling

## Project Structure

```
three_level_auth/
├── app.py                 # Main Flask application
├── db_config.py          # Database configuration
├── requirements.txt      # Python dependencies
├── templates/            # HTML templates
│   ├── base.html         # Base template
│   ├── login.html        # Level 1 - Username/Password
│   ├── level2.html       # Level 2 - Email OTP
│   ├── level3.html       # Level 3 - QR Code
│   ├── dashboard.html    # Success page
│   ├── register.html     # User registration
│   ├── error.html        # Error page
│   └── success.html      # Success page
└── static/
    └── style.css         # Styling
```

## Installation

### Prerequisites
- Python 3.7+
- MySQL Server
- pip (Python package manager)

### Setup Steps

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/three-level-auth.git
cd three-level-auth
```

2. **Create a virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure the database**
- Update `db_config.py` with your MySQL credentials:
```python
def get_db_connection():
    conn = mysql.connector.connect(
        host="localhost",
        user="your_mysql_user",
        password="your_mysql_password",
        database="three_level_auth_db"
    )
    return conn
```

5. **Create the database**
```sql
CREATE DATABASE three_level_auth_db;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100) UNIQUE NOT NULL,
    email VARCHAR(100) NOT NULL,
    password VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

6. **Run the application**
```bash
python app.py
```

Visit `http://localhost:5000` in your browser.

## Usage

### Registration
1. Click "Register" on the login page
2. Enter username, email, and password
3. Submit the form

### Authentication Flow

**Level 1 - Username & Password**
- Enter registered username and password
- Click "Login"

**Level 2 - Email OTP**
- Enter your registered email
- OTP will be generated and displayed (in demo mode)
- Enter the OTP and click "Verify"

**Level 3 - QR Code Authentication**
- A QR code is generated containing a random 3-digit code
- Scan the QR code or read the code from the modal
- Enter the code and click "Submit"
- Upon successful authentication, access the dashboard

### Dashboard
- View your username after successful authentication
- Click "Logout" to end the session

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Redirect to Level 1 |
| `/register` | GET, POST | User registration |
| `/level1` | GET, POST | Username/Password login |
| `/level2` | GET, POST | Email OTP verification |
| `/level3` | GET, POST | QR code authentication |
| `/dashboard` | GET | Success page (authenticated) |
| `/logout` | GET | Clear session and logout |

## Dependencies

- **flask** - Web framework
- **mysql-connector-python** - MySQL database connector
- **qrcode** - QR code generation
- **Pillow** - Image processing (for QR codes)

## Security Recommendations

⚠️ **For Production Use:**
- Hash passwords using `werkzeug.security` or `bcrypt`
- Use environment variables for sensitive data
- Enable HTTPS/SSL
- Implement rate limiting
- Send OTP via actual email service (e.g., SendGrid, Gmail)
- Use session tokens instead of storing user data directly
- Add CSRF protection
- Implement database connection pooling

## Screenshots

### Level 1 - Login
![Level 1 Login](C:\Users\diwan\Pictures\Screenshots\Screenshot 2025-12-02 103142.png)

### Level 2 - OTP Verification
![Level 2 OTP](C:\Users\diwan\Pictures\Screenshots\Screenshot 2025-12-02 103252.png)

### Level 3 - QR Code
![Level 3 QR](C:\Users\diwan\Pictures\Screenshots\Screenshot 2025-12-02 103347.png)

### Dashboard
![Dashboard](C:\Users\diwan\Pictures\Screenshots\Screenshot 2025-12-02 103529.png)

## Troubleshooting

### Database Connection Error
- Ensure MySQL is running
- Check credentials in `db_config.py`
- Verify database exists

### OTP Not Appearing
- Check browser console for errors
- Ensure JavaScript is enabled
- Verify session storage

### QR Code Not Generating
- Ensure `qrcode` package is installed
- Check Pillow library is available
- Verify `/tmp` directory has write permissions

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Author

Created as a demonstration of multi-factor authentication implementation in Flask.

## Contact

For questions or suggestions, please open an issue in the repository.

---

**Note**: This project is for educational purposes. For production environments, implement proper security measures including password hashing, email verification, and HTTPS.
