# 🏋️‍♂️ TalaveraFitness

TalaveraFitness is a full-stack fitness web app that generates personalized workout routines and demonstrates exercises with video guides.  

## ✨ Features
- User signup/login system  
- Personalized workout plans based on user input  
- Exercise videos stored on AWS S3  
- Responsive design for desktop and mobile  
- Admin panel for managing users and content
- Email contact form functionality

## 🛠 Tech Stack
- **Backend:** Python, Flask, SQLAlchemy  
- **Frontend:** HTML, CSS, JavaScript, Jinja2  
- **Database:** SQLite (dev), Postgres/MySQL (prod)  
- **Cloud:** AWS EC2, S3, Route 53  
- **Server:** Nginx + Gunicorn  
- **Authentication:** Flask-Login, Flask-Bcrypt
- **Email:** Flask-Mail
- **Admin:** Flask-Admin

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- AWS S3 bucket for video storage
- Email service (Gmail recommended for development)

### Installation

1. **Clone the repository**
```bash
git clone <your-repository-url>
cd PT_flask
```

2. **Create and activate virtual environment**
```bash
python3 -m venv app/venv
source app/venv/bin/activate  # On Windows: app\venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables**
Create a `.env` file in the project root with the following variables:
```env
DATABASE_URL=sqlite:///app/ptraining.db
AWS_BUCKET_NAME=your-s3-bucket-name
AWS_ACCESS_KEY_ID=your-aws-access-key
AWS_SECRET_ACCESS_KEY=your-aws-secret-key
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
SECRET_KEY=your-secret-key
```

5. **Initialize the database**
```bash
cd app
python3 starting_app.py
```

6. **Populate the database with workout data**
```bash
python3 data/create_data.py
```

7. **Run the application**
```bash
python3 starting_app.py
```

The app will be available at `http://127.0.0.1:5000`

## 📁 Project Structure
```
PT_flask/
├── app/
│   ├── data/           # Data creation scripts
│   ├── migrations/     # Database migrations
│   ├── static/         # CSS, JS, images
│   ├── templates/      # HTML templates
│   ├── venv/          # Virtual environment
│   ├── models.py      # Database models
│   ├── starting_app.py # Main Flask application
│   └── ...
├── requirements.txt
└── README.md
```

## 🔧 Configuration

### AWS S3 Setup
1. Create an S3 bucket for storing workout videos
2. Configure CORS if needed
3. Set up IAM user with S3 access
4. Add credentials to `.env` file

### Email Configuration
For Gmail:
1. Enable 2-factor authentication
2. Generate an app password
3. Use app password in `MAIL_PASSWORD`

## 🗄️ Database

The app uses SQLAlchemy with the following main models:
- **User**: User accounts and profiles
- **Workouts**: Exercise definitions and video links
- **Routine**: Workout routines
- **Day_of_routine**: Individual workout days
- **UserProgress**: User progress tracking

## 🚀 Deployment

For production deployment:
1. Use PostgreSQL or MySQL instead of SQLite
2. Set up proper environment variables
3. Configure Nginx as reverse proxy
4. Use Gunicorn as WSGI server
5. Set up SSL certificates

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📝 License

[Add your license information here]

