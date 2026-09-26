import os
import re
import datetime
import sqlite3
from shutil import rmtree


script_folder = os.path.dirname(os.path.abspath(__file__))
log_file = os.path.join(script_folder, "logs.db")


book_exts = {'.epub', '.djvu', '.mobi', 'azw3'}
img_exts = {'.jpg', '.jpeg', '.png', '.gif', '.PNG', '.JPEG'}
music_exts = {'.mp3', '.wma', '.ogg', '.wav'}
video_exts = {'.mp4', '.wmv', '.mpeg', '.mov'}
install_exts = {'.exe', '.deb', 'rpm'}
ignore_exts = {'.ini'} #windows download folder contains desktop.ini, which should be ignored



def get_dirs(test: bool, env='.env') -> dict[str, str]:
    env = os.path.join(script_folder, env)
    dirs = dict()
    with open(env, 'r') as dir_file:
        lines = dir_file.readlines()
        dirs = dict()
        for line in lines:
            if test:
                lineformat = re.search('(.*)_DIR_TEST="(.*)"', line)
                if lineformat:
                    dir_name, dir_path = lineformat.groups()
                    dirs[dir_name] = dir_path
            else:
                lineformat = re.search('(.*)_DIR="(.*)"', line)
                if lineformat:
                    dir_name, dir_path = lineformat.groups()
                    dirs[dir_name] = dir_path
    return dirs


def pdfIsBook(file: str) -> bool:
    book = input(f'is {file} a book?(y/n) ').strip().lower()
    return book == 'y'


def manual_handle(file: str, dirs: dict[str, str]) -> None:
    print(f'What do you want to do with {file}?')
    opt = int(input(
        "1. Delete\n"
        "2. Move to Docs\n"
        "3. Do nothing\n"
    ).strip())
    match opt:
        case 1:
            delete_path(file)
        case 2:
            new_file = ''.join(file.split())
            os.rename(file, dirs['DOC']+'/'+new_file)
            write_log(file, dirs['DOC'])
        case 3:
            print(f'{file} left unchanged. Moved on to next file')
            write_log(file, 'DOWNLOAD')
        case _:
            print("Didn\'t understand that. Try again")
            manual_handle(file, dirs)


def delete_path(path: str) -> None:
    if os.path.isfile(path):
        os.remove(path)
    else:
        rmtree(path)



def write_log(moved_file, directory):
    with sqlite3.connect(log_file) as logs:
        logs.execute("""
        CREATE TABLE IF NOT EXISTS log_file (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT NOT NULL,
        file_name TEXT NOT NULL,
        destination TEXT NOT NULL
        )
        """)
        logs.execute("""
        INSERT INTO log_file (timestamp, file_name, destination)
        VALUES (?,?,?)       
        """,
        (datetime.datetime.now().isoformat(), moved_file, directory)            
        )
    

def main(test=False):
    # get directories for Download, Docs...
    dirs = get_dirs(test)
    os.chdir(dirs['DOWNLOAD'])
    # loop over downfiles
    download_files = os.listdir()
    for file in download_files:
        _, ext = os.path.splitext(file)
        new_file = ''.join(file.split())
        # delete installers
        if ext in ignore_exts:
            write_log(file, 'DOWNLOAD')
        elif ext in install_exts:
            os.remove(file)
            write_log(file, '(deleted)')
        
        #images, books, videos, music and pdfs
        elif ext in (img_exts | book_exts | video_exts | music_exts) or ext == '.pdf':
            # move images
            if ext in img_exts:
                dir = 'IMG'
            # move books
            elif ext in book_exts:
                dir = 'BOOK'
            # move videos
            elif ext in video_exts:
                dir = 'VIDEO'
            # move music
            elif ext in music_exts:
                dir = 'MUSIC'
            # check if pdf is book
            elif ext == '.pdf':
                isBook = pdfIsBook(file)
            # move to books or docs accordingly
                if isBook:
                    dir = 'BOOK'
                else:
                    dir = 'DOC'

            os.rename(file, dirs[dir]+'/'+new_file)
            write_log(file, dirs[dir])

        # manually deal with other files
        else:
            manual_handle(file, dirs)



if __name__ == "__main__":
    main()