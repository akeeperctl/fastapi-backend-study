import shutil

from fastapi import APIRouter, UploadFile, BackgroundTasks

from src.tasks.tasks import compress_image

router = APIRouter(prefix="/images", tags=["Изображения отелей"])


@router.post("/images")
def upload_image(file: UploadFile, background_tasks: BackgroundTasks):
    image_path = f"src/static/images/{file.filename}"
    with open(image_path, "wb+") as new_file:
        shutil.copyfileobj(file.file, new_file)

    # compress_image.delay(image_path)
    background_tasks.add_task(compress_image, image_path)

    return {"status": "ok"}
