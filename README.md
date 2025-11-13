# 🛍️ Django E-Commerce Platform with AI Recommendations

A full-stack e-commerce web application built with Django, featuring intelligent product recommendations powered by machine learning.

## 🚀 Features
- **Product Browsing** – View products with images, descriptions, and prices.
- **Cart & Checkout** – Add items to cart and complete purchases.
- **User Authentication** – Secure login and session management.
- **AI Recommendations** – Suggest products based on user feedback and product categories.
- **Feedback System** – Like/dislike recommendations to personalize future suggestions.
- **Optimized Python Logic** – Fast similarity matching using NumPy and scikit-learn.

## 🧠 Recommendation Engine
Uses content-based filtering to suggest products similar to those the user liked. Feedback updates the recommendation logic in real time.

## 🧰 Tech Stack
- **Backend:** Django, SQLite
- **Frontend:** HTML, CSS
- **AI/ML:** Python, NumPy, scikit-learn

## 📦 Installation
```bash
git clone https://github.com/Chinusoni/ecommerce-ai-django.git
cd ecommerce-ai-django
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

## 📌 Future Enhancements
- Collaborative filtering or deep learning models
- AJAX-based feedback updates
- Admin dashboard for product management
- Cloud deployment (Render, Heroku)

