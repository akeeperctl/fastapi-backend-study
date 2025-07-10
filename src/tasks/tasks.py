import asyncio
import os
from time import sleep

from PIL import Image

from src.database import async_session_maker_null_pool
from src.tasks.celery_app import celery_instance
from src.utils.db_manager import DBManager


@celery_instance.task
def test_task():
    sleep(5)
    print("Я молодец")


# @celery_instance.task
def compress_image(
    input_path: str,
) -> None:
    """
    Сжимает изображение по ширине до каждого из sizes (px),
    сохраняя пропорции, и сохраняет в output_dir.
    Имена файлов: originalname_{width}px.ext
    """

    sizes: tuple = (1000, 500, 200)
    output_dir: str = "src/static/images"

    # Открываем исходник
    with Image.open(input_path) as img:
        orig_name, ext = os.path.splitext(os.path.basename(input_path))
        for width in sizes:
            # Вычисляем новую высоту по сохранению пропорций
            w_percent = width / float(img.width)
            height = int(float(img.height) * w_percent)

            # Ресайз
            resized = img.resize((width, height), Image.Resampling.LANCZOS)

            # Формируем имя и сохраняем
            output_path = os.path.join(output_dir, f"{orig_name}_{width}px{ext}")

            # При сохранении можно управлять качеством для JPEG
            save_kwargs = {}
            if ext.lower() in (".jpg", ".jpeg"):
                save_kwargs["quality"] = 85
                save_kwargs["optimize"] = True
            resized.save(output_path, **save_kwargs)

            print(f"Сохранено: {output_path}")


async def send_emails_to_users_with_today_checkin_helper():
    async with DBManager(session_factory=async_session_maker_null_pool) as db:
        bookings = await db.bookings.get_bookings_with_today_checkin()
        print(f"{bookings=}")


@celery_instance.task(name="booking_today_checkin")
def send_emails_to_users_with_today_checkin():
    asyncio.run(send_emails_to_users_with_today_checkin_helper())
