# HotelHub 🏨

[![Django](https://img.shields.io/badge/Django-5.1.8-green.svg)](https://www.djangoproject.com/)
[![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Docker](https://img.shields.io/badge/Docker-✓-blue.svg)](https://www.docker.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15+-blue.svg)](https://www.postgresql.org/)
[![Redis](https://img.shields.io/badge/Redis-6.0+-red.svg)](https://redis.io/)
[![Elasticsearch](https://img.shields.io/badge/Elasticsearch-8.0+-green.svg)](https://www.elastic.co/)
[![Celery](https://img.shields.io/badge/Celery-✓-green.svg)](https://docs.celeryq.dev/)

HotelHub is a modern, scalable hotel management system built with Django, featuring real-time chat capabilities, comprehensive booking management, and robust user authentication. Designed for both small boutique hotels and large hotel chains, HotelHub provides a complete solution for managing accommodations, bookings, and guest communications.
## 👥  Project Owners 
- Eyyub, Ehmed, Əbil – [Eyyub](https://github.com/Eyyub01) | [Əhmed](https://github.com/hmd37) | [Əbil](https://github.com/ebilebilli)


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
  - Celery Beat - Periodically check, Automatically set
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


## 📦 Prerequisites

- Python 3.12+
- Docker and Docker Compose
- Redis 6.0+
- Elasticsearch 8.0+
- PostgreSQL 15+ (for production)

## 📚 API Documentation

The API documentation is available at:
- Swagger UI: `http://localhost:8000/api/schema/swagger-ui/`
- ReDoc: `http://localhost:8000/api/schema/redoc/`

### API Endpoints

-- **Authentication**
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
  - `GET /api/v1/hotels/{id}/photos/` - List hotel photos
  - `POST /api/v1/hotels/{id}/photos/` - Create hotel photo
  - `DELETE /api/v1/hotels/{id}/photos/{photo_id}/` - Delete hotel photo

- **Rooms**
  - `GET /api/v1/rooms/` - List rooms
  - `POST /api/v1/room/create/` - Create room
  - `GET /api/v1/room/{id}/` - Room details
  - `GET /api/v1/rooms/{id}/hotel/` - List rooms for hotel
  - `GET /api/v1/rooms/search/` - Search rooms
  - `GET /api/v1/room/photos/{id}/` - List room photos

- **Bookings**
  - `GET /api/v1/bookings/` - List bookings
  - `POST /api/v1/bookings/` - Create booking
  - `GET /api/v1/bookings/{id}/` - Booking details
  - `PUT /api/v1/bookings/{id}/` - Update booking
  - `DELETE /api/v1/bookings/{id}/` - Cancel booking

- **Favorites**
  - `GET /api/v1/favorites/` - List favorites
  - `GET /api/v1/favorite/{id}/` - Favorite details
  - `POST /api/v1/favorite/room/{id}/create/` - Create favorite for room
  - `POST /api/v1/favorite/hotel/{id}/create/` - Create favorite for hotel

- **Cities**
  - `GET /api/v1/cities/` - List cities
  - `GET /api/v1/cities/{pk}/` - City details

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

## 🔍 Code Quality


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

## 🙏 Acknowledgments

- Django team for the amazing framework
- All contributors who have helped shape this project
- Open source community for their invaluable tools and libraries

## 📞 Support

For support, email support@hotelhub.com or join our Slack channel.

