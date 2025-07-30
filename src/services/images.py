import shutil

from fastapi import UploadFile, BackgroundTasks

from src.services.base import BaseService
from src.tasks.tasks import compress_image


class ImageService(BaseService):
    # FIXME: здесь в идеале нужно сделать интерфейс файла и background_tasks
    #  чтобы убрать из сервисов зависимость от фреймворка FastAPI
    @staticmethod
    def upload_image(file: UploadFile, background_tasks: BackgroundTasks):
        """Загрузить изображение на сервер"""

        image_path = f"src/static/images/{file.filename}"
        with open(image_path, "wb+") as new_file:
            shutil.copyfileobj(file.file, new_file)

        # compress_image.delay(image_path)
        background_tasks.add_task(compress_image, image_path)
