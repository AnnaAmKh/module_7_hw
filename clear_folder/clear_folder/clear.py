import os
from pathlib import Path
import re
import shutil


# Функція для нормалізації імен файлів та папок
CYRILLIC_SYMBOLS = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ'
TRANSLATION = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
               "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "u", "ja", "je", "ji", "g")

TRANS = dict()

for cyrillic, latin in zip(CYRILLIC_SYMBOLS, TRANSLATION):
    TRANS[ord(cyrillic)] = latin
    TRANS[ord(cyrillic.upper())] = latin.upper()


def normalize(name: str) -> str:
    translate_name = re.sub(r'\W', '_', name.translate(TRANS))
    return translate_name
def handle_media(file_name: Path, target_folder: Path):
    target_folder.mkdir(exist_ok=True, parents=True)
    file_name.replace(target_folder / normalize(file_name.name))

def handle_archive(file_name: Path, target_folder: Path):
    target_folder.mkdir(exist_ok=True, parents=True)
    folder_for_file = target_folder / normalize(file_name.name.replace(file_name.suffix, ''))
    folder_for_file.mkdir(exist_ok=True, parents=True)
    try:
        shutil.unpack_archive(str(file_name.absolute()), str(folder_for_file.absolute()))
    except shutil.ReadError:
        folder_for_file.rmdir()
        return
    file_name.unlink()

# Функція для сортування файлів та папок
def sort_folder(folder_path):
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            # Визначення розширення файлу
            file_extension = file.split('.')[-1].upper()
            file_path = os.path.join(root, file)

            destination_folder = ''
            if file_extension in ('JPEG', 'JPG', 'PNG', 'SVG', 'TIF', 'JP2'):
                destination_folder = 'images'
            elif file_extension in ('AVI', 'MP4', 'MOV', 'MKV'):
                destination_folder = 'video'
            elif file_extension in ('DOC', 'DOCX', 'TXT', 'PDF', 'XLSX', 'PPTX', 'CSV', 'JSON', 'GEOJSON', 'PY', 'XML'):
                destination_folder = 'documents'
            elif file_extension in ('MP3', 'OGG', 'WAV', 'AMR'):
                destination_folder = 'audio'
            elif file_extension in ('ZIP', 'GZ', 'TAR'):
                destination_folder = 'archives'

            if destination_folder:
                # Перейменування файлу
                normalized_file_name = normalize(file.split('.')[0])
                new_file_name = f"{normalized_file_name}.{file_extension.lower()}"
                new_file_path = os.path.join(root, destination_folder, new_file_name)

                # Переміщення файлу в папку призначення
                os.makedirs(os.path.join(root, destination_folder), exist_ok=True)
                shutil.move(file_path, new_file_path)

        for folder in dirs:
            # Визначення папки призначення для папок
            if folder in ('images', 'video', 'documents', 'audio', 'archives'):
                continue

            # Перейменування папки
            normalized_folder_name = normalize(folder)
            new_folder_path = os.path.join(root, normalized_folder_name)

            # Переміщення папки
            os.rename(os.path.join(root, folder), new_folder_path)

    # Видалення порожніх папок
    for root, dirs, files in os.walk(folder_path, topdown=False):
        for folder in dirs:
            folder_path = os.path.join(root, folder)
            if not os.listdir(folder_path):
                os.rmdir(folder_path)

# Функція для розпакування архівів
def unpack_archives(folder_path):
    for root, _, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            if file.split('.')[-1].upper() in ('ZIP', 'GZ', 'TAR'):
                destination_folder = 'archives'
                archive_name = os.path.splitext(file)[0]
                archive_path = os.path.join(root, destination_folder, archive_name)

                # Розпаковування архіву
                os.makedirs(os.path.join(root, destination_folder), exist_ok=True)
                shutil.unpack_archive(file_path, archive_path)

if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Введіть шлях до папки для сортування.")
    else:
        target_folder = sys.argv[1]
        sort_folder(target_folder)
        unpack_archives(target_folder)