# HotelHub 🏨

[![Django](https://img.shields.io/badge/Django-5.1.8-green.svg)](https://www.djangoproject.com/)
[![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Docker](https://img.shields.io/badge/Docker-✓-blue.svg)](https://www.docker.com/)

HotelHub is a modern, scalable hotel management system built with Django, featuring real-time chat capabilities, comprehensive booking management, and robust user authentication. Designed for both small boutique hotels and large hotel chains, HotelHub provides a complete solution for managing accommodations, bookings, and guest communications.

## 🌟 Key Features

### 🔐 User Authentication & Authorization
- **JWT-based Authentication**
  - Secure token-based authentication
  - Refresh token mechanism
  - Token blacklisting for security
- **User Management**
  - Custom user model with extended fields
  - Profile management with avatar support
  - Role-based access control (Admin, Staff, Guest)
- **Security Features**
  - Password validation and hashing
  - Rate limiting for API endpoints
  - CSRF protection

### 🏢 Hotel Management
- **Hotel Operations**
  - Comprehensive hotel listing with detailed information
  - Room type management and pricing
  - Amenities and facilities tracking
  - Location-based search with geocoding
- **Room Management**
  - Dynamic room availability system
  - Room type categorization
  - Pricing and seasonal rates
  - Room status tracking

### 📅 Booking System
- **Reservation Management**
  - Real-time availability checking
  - Multi-room booking support
  - Booking modification and cancellation
  - Automated confirmation emails
- **Payment Integration**
  - Secure payment processing (coming soon)
  - Multiple payment method support
  - Refund management
  - Invoice generation

### 💬 Real-time Chat
- **Communication Features**
  - WebSocket-based chat rooms
  - Real-time messaging
  - File sharing capabilities
  - Message history
- **Room Management**
  - Private and group chat rooms
  - Room moderation tools
  - User presence indicators
  - Message notifications

### ⭐ Favorites System
- **User Preferences**
  - Save favorite hotels
  - Custom lists and categories
  - Quick access to preferred accommodations
  - Price alerts for saved hotels

## 🛠️ Technology Stack

### Backend
- **Framework & Libraries**
  - Django 5.1.8 - Web framework
  - Django REST Framework - API development
  - Django Channels - WebSocket support
  - Celery - Task queue management
  - Redis - Caching and message broker
  - Elasticsearch - Search functionality
  - DRF Spectacular - API documentation

### Database
- **Development**: SQLite
- **Production**: PostgreSQL 
- **Search**: Elasticsearch
- **Cache**: Redis

### Containerization & Deployment
- Docker
- Docker Compose
- Nginx (planned)
- Gunicorn (planned)

## 📦 Prerequisites

- Python 3.12+
- Docker and Docker Compose
- Redis 6.0+
- Elasticsearch 8.0+
- PostgreSQL 15+ (for production)

## 🚀 Getting Started

### Local Development Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/hotelhub.git
   cd hotelhub
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv venv
   # On Windows
   .\venv\Scripts\activate
   # On Unix or MacOS
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Configuration**
   Create a `.env` file in the project root:
   ```env
   # Django Settings
   DEBUG=True
   SECRET_KEY=your-secret-key-here
   ALLOWED_HOSTS=localhost,127.0.0.1
   
   # Database Settings
   DB_ENGINE=django.db.backends.sqlite3
   DB_NAME=db.sqlite3
   
   # Redis Settings
   REDIS_URL=redis://redis:6379/1
   CELERY_BROKER_URL=redis://redis:6379/0
   CELERY_RESULT_BACKEND=redis://redis:6379/0
   
   # Email Settings
   EMAIL_HOST=smtp.gmail.com
   EMAIL_PORT=587
   EMAIL_USE_TLS=True
   EMAIL_HOST_USER=your-email@gmail.com
   EMAIL_HOST_PASSWORD=your-app-password
   ```

5. **Database Setup**
   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   ```

6. **Run Development Server**
   ```bash
   python manage.py runserver
   ```

### 🐳 Docker Development

1. **Build and Start Containers**
   ```bash
   docker-compose up --build
   ```

2. **Run Migrations**
   ```bash
   docker-compose exec web python manage.py migrate
   ```

3. **Create Superuser**
   ```bash
   docker-compose exec web python manage.py createsuperuser
   ```

## 🔧 Production Deployment

### PostgreSQL Configuration

1. **Environment Variables**
   ```env
   DB_ENGINE=django.db.backends.postgresql
   DB_NAME=hotelhub
   DB_USER=your_db_user
   DB_PASSWORD=your_db_password
   DB_HOST=postgres
   DB_PORT=5432
   ```

2. **Docker Compose Configuration**
   ```yaml
   version: '3.8'
   
   services:
     postgres:
       image: postgres:15
       environment:
         POSTGRES_DB: hotelhub
         POSTGRES_USER: your_db_user
         POSTGRES_PASSWORD: your_db_password
       volumes:
         - postgres_data:/var/lib/postgresql/data
       networks:
         - app_net
   
     redis:
       image: redis:8.0
       networks:
         - app_net
   
     elasticsearch:
       image: docker.elastic.co/elasticsearch/elasticsearch:8.14.0
       environment:
         - discovery.type=single-node
         - xpack.security.enabled=false
       volumes:
         - elasticsearch_data:/usr/share/elasticsearch/data
       networks:
         - app_net
   
   volumes:
     postgres_data:
     elasticsearch_data:
   
   networks:
     app_net:
       driver: bridge
   ```

## 📚 API Documentation

The API documentation is available at:
- Swagger UI: `http://localhost:8000/api/schema/swagger-ui/`
- ReDoc: `http://localhost:8000/api/schema/redoc/`

### API Endpoints

- **Authentication**
  - `POST /api/v1/auth/register/` - User registration
  - `POST /api/v1/auth/login/` - User login
  - `POST /api/v1/auth/refresh/` - Refresh token
  - `POST /api/v1/auth/logout/` - User logout

- **Hotels**
  - `GET /api/v1/hotels/` - List hotels
  - `POST /api/v1/hotels/` - Create hotel
  - `GET /api/v1/hotels/{id}/` - Hotel details
  - `PUT /api/v1/hotels/{id}/` - Update hotel
  - `DELETE /api/v1/hotels/{id}/` - Delete hotel

- **Bookings**
  - `GET /api/v1/bookings/` - List bookings
  - `POST /api/v1/bookings/` - Create booking
  - `GET /api/v1/bookings/{id}/` - Booking details
  - `PUT /api/v1/bookings/{id}/` - Update booking
  - `DELETE /api/v1/bookings/{id}/` - Cancel booking

## 🧪 Testing

### Running Tests
```bash
# Run all tests
python manage.py test

# Run specific app tests
python manage.py test accounts
python manage.py test hotels
python manage.py test bookings

# Run with coverage
coverage run --source='.' manage.py test
coverage report
```

### Test Categories
- Unit Tests
- API Tests
- Integration Tests
- WebSocket Tests

## 📝 Project Structure

```
hotelhub/
├── accounts/           # User authentication and profiles
│   ├── models/        # User models
│   ├── serializers/   # API serializers
│   ├── views/         # API views
│   └── tests/         # Test cases
├── bookings/          # Booking management
│   ├── models/        # Booking models
│   ├── serializers/   # Booking serializers
│   ├── views/         # Booking views
│   └── tests/         # Test cases
├── chat/             # Real-time chat
│   ├── consumers/    # WebSocket consumers
│   ├── routing/      # WebSocket routing
│   └── tests/        # Test cases
├── favorites/        # Favorites management
├── hotels/           # Hotel management
├── rooms/            # Room management
├── utils/            # Utility functions
└── hotelhub/         # Project configuration
    ├── settings/     # Settings modules
    ├── urls/         # URL configurations
    └── asgi.py       # ASGI configuration
```

## 🔍 Code Quality

### Linting
```bash
# Run flake8
flake8 .

# Run black
black .

# Run isort
isort .
```

### Pre-commit Hooks
```yaml
repos:
-   repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.4.0
    hooks:
    -   id: trailing-whitespace
    -   id: end-of-file-fixer
    -   id: check-yaml
    -   id: check-added-large-files
-   repo: https://github.com/psf/black
    rev: 23.7.0
    hooks:
    -   id: black
-   repo: https://github.com/PyCQA/isort
    rev: 5.12.0
    hooks:
    -   id: isort
```

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Pull Request Guidelines
- Follow PEP 8 style guide
- Write meaningful commit messages
- Include tests for new features
- Update documentation as needed
- Ensure all tests pass

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Authors

- Your Name - Initial work - [GitHub](https://github.com/yourusername)

## 🙏 Acknowledgments

- Django team for the amazing framework
- All contributors who have helped shape this project
- Open source community for their invaluable tools and libraries

## 📞 Support

For support, email support@hotelhub.com or join our Slack channel.

## 🔮 Roadmap

- [ ] Payment Gateway Integration
- [ ] Mobile App Development
- [ ] Advanced Analytics Dashboard
- [ ] Multi-language Support
- [ ] Hotel Chain Management Features 