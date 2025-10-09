CTProz Construction Website  
Live Site:** (https://ctproz.pro)  
Django • Python • HTML • CSS • JavaScript • Bootstrap • PostgreSQL • Render  

---

Overview  
**CTProz** is a fully functional construction company website built with the **Django framework** and deployed on **Render**.  
It serves as a professional online presence for CTProz Construction — showcasing services, past projects, and providing a contact form that automatically sends confirmation emails to both the client and the business.

---

 🎯 Project Goals  
- ✅ Develop a professional and responsive business website for a real client.  
- 🔒 Deliver a secure, production-ready Django web app.  
- 📧 Automate client–admin communication via Google Workspace SMTP.  
- 🌍 Deploy to a custom domain with SSL and Google Workspace integration.  

---

Technologies Used  

### Backend  
- **Django 5.2.6 (Python 3.13)**  
- **Gunicorn** – WSGI server for production  
- **Render** – Cloud hosting & CI/CD  
- **WhiteNoise** – Static file management  
- **SQLite → PostgreSQL** (production database)  

###Frontend  
- HTML5 • CSS3 • JavaScript  
- Bootstrap (responsive grid & components)  
- Django Template Language (DTL)  

### ✉️ Email & Domain  
- **Google Workspace (info@ctproz.com)** – SMTP configuration  
- **GoDaddy** – Domain management & SSL  
- **Auto Email Confirmation** – Sent to both client and admin  

---

## 📁 Project Structure  
buildright/ # Main Django project configuration
website/ # Core app with views, models, templates, and URLs
static/ # CSS, JS, and image assets
templates/ # HTML templates for all pages
.env # Environment variables (excluded from GitHub)
requirements.txt # Python dependencies
