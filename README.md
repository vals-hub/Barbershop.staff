# Barbershop.staff

The `server/` directory contains a FastAPI backend tailored for the barbers/staff
application. Barbers can authenticate, review their appointments, manage services,
and configure working hours. A SQLModel-powered database keeps data persistent so
customer bookings appear instantly on the staff dashboard.

## Getting started locally

1. Create and activate a Python 3.11+ virtual environment.
2. Install dependencies:
   ```bash
   pip install -r server/requirements.txt
   ```
3. Copy the example environment file and update values if needed:
   ```bash
   cp server/.env.example server/.env
   ```
4. Start the API:
   ```bash
   cd server
   uvicorn app.main:app --host 0.0.0.0 --port 8000
   ```

On first launch the application creates a SQLite database (`demo.db`) with demo
content:

- Barber account: `barber@example.com` / `password123`
- Sample services, appointments, and weekday working hours

Use these credentials to explore the staff flows immediately.

## Available endpoints

All endpoints are mounted under the `/api` prefix.

| Method & Path                 | Description                                      |
|------------------------------|--------------------------------------------------|
| `POST /api/auth/register`    | Register a new staff account                      |
| `POST /api/auth/login`       | Authenticate and receive a JWT access token       |
| `GET /api/appointments`      | List appointments (filterable by `barber_id`)     |
| `POST /api/appointments`     | Create an appointment                             |
| `GET /api/services`          | Retrieve services (filterable by `barber_id`)     |
| `POST /api/services`         | Add a new service                                 |
| `PATCH /api/services/{id}`   | Update service details                            |
| `DELETE /api/services/{id}`  | Remove a service                                  |
| `GET /api/working-hours`     | List working hours (filterable by `barber_id`)    |
| `POST /api/working-hours`    | Create availability for a day                     |
| `PATCH /api/working-hours/{id}` | Update start/end times                         |
| `DELETE /api/working-hours/{id}` | Remove availability window                    |

## Database configuration

By default the API stores data in a local SQLite database so it can run without
external infrastructure. Set the `DATABASE_URL` environment variable (for
example to a managed PostgreSQL instance) to use a different backend when
deploying to Render or another cloud platform. The `.env.example` file lists all
relevant environment variables, including `SECRET_KEY`, `ACCESS_TOKEN_EXPIRE_MINUTES`,
and `JWT_ALGORITHM` for token signing.

## Running with Docker

```bash
cd server
docker build -t barbershop-api .
docker run --rm -it -p 8000:8000 --env-file .env barbershop-api
```

Render (and most PaaS platforms) automatically set the `PORT` environment
variable; the provided Dockerfile and start command use this variable so no
further changes are required.
