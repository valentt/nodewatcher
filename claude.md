# Nodewatcher Development Notes

## Admin Credentials
- **URL**: http://localhost:8000/admin/
- **Username**: admin
- **Password**: admin

## IP Pool Wizard
- **Wizard URL**: http://localhost:8000/ip/wizard/
- **Pool List**: http://localhost:8000/ip/pools/

## Docker Commands
```bash
# Start services
docker-compose up -d

# Run migrations
docker-compose exec web python manage.py migrate

# Create superuser
docker-compose exec web python manage.py createsuperuser

# Shell
docker-compose exec web python manage.py shell
```

## IP Addressing Scheme
- **Croatia (HR)**: 10.XX.0.0/16 where XX = first 2 digits of postal code (10-53)
- **Slovenia (SI)**: 10.1XX.0.0/16 where XX = first 2 digits of postal code (10-90)
