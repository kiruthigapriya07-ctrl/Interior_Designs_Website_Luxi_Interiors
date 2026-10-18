# Luxe Interiors - Premium Interior Design Studio Website

A complete full-stack interior design studio website built with Flask backend and MySQL database.

## 🚀 Tech Stack

### Frontend
- HTML5
- CSS3 (Custom, no frameworks)
- Vanilla JavaScript
- Google Fonts (Playfair Display, Lato)

### Backend
- Python 3.8+
- Flask 3.0

### Database
- MySQL 8.0+

## 📁 Project Structure

```
interior-design-website/
│
├── app.py                 # Flask application
├── requirements.txt       # Python dependencies
├── database.sql          # MySQL database schema
├── README.md             # This file
│
├── templates/
│   ├── index.html        # Home page
│   ├── about.html        # About page
│   ├── services.html     # Services page
│   ├── projects.html     # Projects/Portfolio page
│   ├── contact.html      # Contact page
│   └── consultation.html # Consultation booking page
│
├── static/
│   ├── css/
│   │   └── style.css     # Main stylesheet
│   ├── js/
│   │   └── script.js     # Frontend JavaScript
│   └── images/           # Project images folder
│
└── .env                  # Environment variables (create this)
```

## 🛠️ Setup Instructions

### Step 1: Install Python Dependencies

```bash
# Navigate to project directory
cd interior-design-website

# Create virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Step 2: Create MySQL Database

```bash
# Login to MySQL
mysql -u root -p

# Run the database schema
source database.sql;

# Or manually:
mysql -u root -p < database.sql
```

### Step 3: Configure Database Credentials

Create a `.env` file in the project root:

```env
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_NAME=interior_design_studio
DB_PORT=3306
```

**Replace `your_mysql_password` with your actual MySQL root password.**

### Step 4: Run Flask Application

```bash
# Make sure you're in the project directory
# and virtual environment is activated

# Run the Flask app
python app.py
```

The server will start at: `http://localhost:5000`

### Step 5: Open the Website

Open your browser and navigate to:
- **Home:** http://localhost:5000/
- **About:** http://localhost:5000/about
- **Services:** http://localhost:5000/services
- **Projects:** http://localhost:5000/projects
- **Contact:** http://localhost:5000/contact
- **Consultation:** http://localhost:5000/consultation

## 📊 Database Tables

### services
- id, name, description, icon, price_range, created_at

### projects
- id, name, category, location, description, image_url, area_sqft, completion_date, featured, created_at

### consultations
- id, full_name, email, phone, project_type, budget, preferred_date, message, status, created_at

### contact_messages
- id, name, email, phone, subject, message, status, created_at

### testimonials
- id, client_name, client_title, testimonial, rating, project_id, created_at

## 🔌 API Endpoints

### GET /api/projects
Returns all projects from database

### GET /api/services
Returns all services from database

### GET /api/project/<id>
Returns single project by ID

### POST /api/contact
Submit contact form
```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "phone": "+919876543210",
  "subject": "Project Inquiry",
  "message": "I want to discuss my project..."
}
```

### POST /api/consultation
Book consultation
```json
{
  "full_name": "John Doe",
  "email": "john@example.com",
  "phone": "+919876543210",
  "project_type": "Residential Interior Design",
  "budget": "₹5 - ₹10 Lakhs",
  "preferred_date": "2026-09-01",
  "message": "Project details..."
}
```

## 🎨 Features

- ✅ Fully responsive design (mobile-first)
- ✅ Premium UI with smooth animations
- ✅ IntersectionObserver for scroll animations
- ✅ Lazy loading images
- ✅ Before/After image slider
- ✅ Project modal with details
- ✅ Working contact form
- ✅ Consultation booking system
- ✅ MySQL database integration
- ✅ Form validation
- ✅ Accessible navigation
- ✅ SEO-friendly structure

## 🖼️ Adding Project Images

Place your project images in the `static/images/` folder:

```
static/images/
├── villa-interior.jpg
├── office-interior.jpg
├── kitchen-interior.jpg
├── living-room.jpg
├── bedroom-interior.jpg
└── showroom-interior.jpg
```

Update the database with actual image filenames:

```sql
UPDATE projects SET image_url = 'villa-interior.jpg' WHERE id = 1;
```

## 🔒 Security Notes

- Change the default MySQL password in production
- Use environment variables for sensitive data
- Enable HTTPS in production
- Add CSRF protection for forms
- Implement rate limiting for API endpoints

## 📝 Sample Data

The database comes pre-populated with:
- 6 services
- 6 sample projects
- 4 testimonials

## 🐛 Troubleshooting

### Database Connection Error
- Check MySQL is running: `sudo service mysql status`
- Verify credentials in `.env` file
- Ensure database exists: `SHOW DATABASES;`

### Flask Not Starting
- Check if port 5000 is available
- Verify all dependencies installed: `pip list`
- Check Python version: `python --version` (needs 3.8+)

### Forms Not Submitting
- Check browser console for errors
- Verify Flask is running
- Check network tab for API responses

## 📄 License

This project is for educational purposes.

## 👨‍💻 Developer

Built with ❤️ for interior design studios.

---

**Happy Coding! 🎉**
