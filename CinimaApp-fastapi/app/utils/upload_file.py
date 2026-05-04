from fastapi import HTTPException, UploadFile
from pathlib import Path
from json import dumps
PATH_APP = Path("app")
PATH_STATIC = PATH_APP / "static"
PATH_IMAGE = PATH_STATIC / "images"
PATH_VIDEO = PATH_STATIC / "video"


async def uplodat_file_image(upload_file: UploadFile, film_name: str) -> str:
    # os.chdir("..")

    # os.chdir("app/static")
    if upload_file and upload_file.filename:
        file_ext = upload_file.filename.split(".")[-1].lower()
        if file_ext not in ["jpg", "png", "jpeg","webp"]:
            raise HTTPException(status_code=400, detail="jpg,png,jpeg,webp")
        image_conetxt = await upload_file.read()
        if len(image_conetxt) > 5 * pow(2, 10) * pow(2, 10):
            raise HTTPException(status_code=400, detail="Размер не более 5MB")
        file_name = f"{film_name}.{file_ext}"
        FILE_PATH = PATH_IMAGE / file_name
        FILE_PATH.write_bytes(image_conetxt)
        # with open(file_path, "wb") as f:
        #     f.write(image_conetxt)

    # os.chdir("..")
    # os.chdir("..")

    return f"images/{file_name}"


async def uplodat_file_video(upload_file: UploadFile, film_name: str) -> str:
    # os.chdir("..")

    # os.chdir("app/static")
    if upload_file and upload_file.filename:
        file_ext = upload_file.filename.split(".")[-1].lower()
        print(file_ext)
        if file_ext != "mp4":
            raise HTTPException(status_code=400, detail="файл должен быть mp4")
        video_conetxt = await upload_file.read()
        if len(video_conetxt) > 500 * pow(2, 10) * pow(2, 10):
            raise HTTPException(status_code=400, detail="Размер не более 500MB")
        file_name = f"{film_name}.{file_ext}"
        FILE_PATH = PATH_VIDEO / file_name
        FILE_PATH.write_bytes(video_conetxt)
        # with open(file_path, "wb") as f:
        #     f.write(image_conetxt)

    # os.chdir("..")
    # os.chdir("..")
    return f"video/{FILE_PATH.name}"

async def create_json(data:dict):
   json_buuf =  dumps(data,indent=3,ensure_ascii=False).encode("utf-8")
   return json_buuf


def delete_file(name_file: str):
    if name_file == "images/cat.jpg":
        return
    full_path = PATH_STATIC / name_file
    if full_path.exists():
        try:
            full_path.unlink()
            print(f"Файл удален: {name_file}")
        except OSError as e:
            print(f"Ошибка при удалении файла {name_file}: {e}")
