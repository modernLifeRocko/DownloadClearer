import os
import re

book_exts = {'.epub', '.djvu', '.mobi'}
img_exts = {'.jpg', '.jpeg', '.png', '.gif'}
music_exts = {'.mp3', '.wma', '.ogg', '.wav'}
video_exts = {'.mp4', '.wmv', '.mpeg'}
install_exts = {'.exe', '.deb'}


def get_dirs(test: bool, env='.env') -> dict[str, str]:
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
    book = input(f'is {file} a book?y/n')
    isBook = True if book == 'y' else False
    return isBook


def manual_handle(file: str, dirs: dict[str, str]) -> None:
    print(f'What do you want to do with {file}?')
    opt = int(input("""
        1. Delete
        2. Move to Docs
        3. Do nothing
              """))
    match opt:
        case 1:
            os.remove(file)
        case 2:
            new_file = ''.join(file.split())
            os.rename(file, dirs['DOC']+'/'+new_file)
        case 3:
            print(f'{file} left unchanged. Moved on to next file')
        case _:
            print(f'Didn\'t understand that. Left {file} unchanged')


def main(test=False):
    # get directories for Download, Docs...
    dirs = get_dirs(test)
    os.chdir(dirs['DOWNLOAD'])
    # loop over downfiles
    download_files = os.listdir()
    for file in download_files:
        _, ext = os.path.splitext(file)
        new_file=''.join(file.split())
        # delete installers
        if ext in install_exts:
            os.remove(file)
        # move images
        elif ext in img_exts:
            os.rename(file, dirs['IMG']+'/'+new_file)
        # move books
        elif ext in book_exts:
            os.rename(file, dirs['BOOK']+'/'+new_file)
        # move videos
        elif ext in video_exts:
            os.rename(file, dirs['VIDEO']+'/'+new_file)
        # move music
        elif ext in music_exts:
            os.rename(file, dirs['MUSIC']+'/'+new_file)
        # check if pdf is book
        elif ext == '.pdf':
            isBook = pdfIsBook(file)
        # move to books or docs accordingly
            if isBook:
                os.rename(file, dirs['BOOK']+'/'+new_file)
            else:
                os.rename(file, dirs['DOC']+'/'+new_file)
        # manually deal with other files
        else:
            manual_handle(file, dirs)


if __name__ == "__main__":
    main()
