import sys
import re
from shutil import unpack_archive, copyfile
from pathlib import Path


CYRILLIC_SYMBOLS = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ"
TRANSLATION = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
               "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "ya", "je", "i", "ji", "g")
TRANS = {}

structure = {'Images': ['JPEG', 'PNG', 'JPG', 'SVG'],
             'Video': ['AVI', 'MP4', 'MOV', 'MKV'],
             'Documents': ['DOC', 'DOCX', 'TXT', 'PDF', 'XLSX', 'PPTX'],
             'Audio': ['MP3', 'OGG', 'WAV', 'AMR'],
             'Archives': ['ZIP', 'GZ', 'TAR'],
             '3D models': ['3DS', 'STEP', 'STP', 'OBJ', 'FBX', 'IGS', 'MB']}

list_name = []


def copy_file(file_path):
    if (file_path.suffix[1:]).upper() in structure['Archives']:
        unpack_archive(file_path, create_folder(file_path) / normalize(
            file_path)[:str(file_path.name).rfind('.')])
    else:
        copyfile(file_path, create_folder(
            file_path) / normalize(file_path))


def create_folder(file_path):
    new_directory = Path(
        f'Organized/{create_volume(file_path) or "Other"}/{(file_path.suffix[1:]).upper()}')
    new_directory.mkdir(parents=True, exist_ok=True)
    return new_directory


def create_volume(file_path):
    for key, value in structure.items():
        for suffix in value:
            if (file_path.suffix[1:]).upper() == suffix:
                return key


def normalize(file_path):
    name = file_path.name[:str(file_path.name).rfind('.')]
    new_name = re.sub(r'\W', '_', name.translate(TRANS)
                      )
    file_name = f'{new_name}{file_path.suffix}'
    list_name.append(file_name)
    if list_name.count(file_name) > 1:
        new_name = f'{new_name}({list_name.count(file_name) - 1})'
    return f'{new_name}{file_path.suffix}'


def parse_folder(path):
    for element in path.iterdir():
        if element.is_dir():
            parse_folder(element)
            if element.name in structure.keys():
                continue
            else:
                try:
                    element.rmdir()
                except:
                    pass
        else:
            copy_file(element)


for c, l in zip(CYRILLIC_SYMBOLS, TRANSLATION):
    TRANS[ord(c)] = l
    TRANS[ord(c.upper())] = l.upper()


def start():
    if sys.argv[1]:
        path = Path(sys.argv[1])
        parse_folder(path)
