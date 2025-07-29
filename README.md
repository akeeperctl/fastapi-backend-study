docker build -t booking_image .

docker network create myapp

docker run --name booking_db \
    -p 6432:5432 \
    -e POSTGRES_USER=abcde \
    -e POSTGRES_PASSWORD=abcde \
    -e POSTGRES_DB=booking \
    --network=myapp \
    -d postgres:16

docker run --name booking_cache \
    -p 7379:6379 \
    --network=myapp \
    -d redis:7.4

docker run --name booking_back `
    -p 7777:8000 `
    --network=myapp `
    booking_image

docker run --name booking_celery `
    --network=myapp `
    booking_image `
    celery --app=src.tasks.celery_app:celery_instance worker -l INFO