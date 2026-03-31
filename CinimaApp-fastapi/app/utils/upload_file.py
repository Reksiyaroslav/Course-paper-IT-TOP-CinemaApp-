from fastapi import HTTPException, UploadFile
import os

PATH_IMAGE = "images/"


async def uplodat_file(upload_file: UploadFile, film_name: str) -> str:
    # os.chdir("..")

    os.chdir("app/static")
    if upload_file and upload_file.filename:
        file_ext = upload_file.filename.split(".")[-1].lower()
        if file_ext not in ["jpg", "png", "jpeg"]:
            raise HTTPException(status_code=400, detail="jpg,png,jpeg")
        image_conetxt = await upload_file.read()
        if len(image_conetxt) > 5 * pow(2, 10) * pow(2, 10):
            raise HTTPException(status_code=400, detail="Размер не более 5MB")
        file_name = f"{film_name}_{upload_file.filename}"
        file_path = f"{PATH_IMAGE}{file_name}"
        with open(file_path, "wb") as f:
            f.write(image_conetxt)

    os.chdir("..")
    os.chdir("..")
    return file_path


async def delete_file(name_file: str):
    if name_file == "images/cat.jpg":
        return
    if name_file and os.path.exists(name_file):
        try:
            os.remove(name_file)
            print(f"Файл удален: {name_file}")
        except OSError as e:
            print(f"Ошибка при удалении файла {name_file}: {e}")
