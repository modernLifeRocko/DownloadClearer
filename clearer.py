import os
import re

book_exts = {'.epub', '.djvu', '.mobi'}
img_exts = {'.jpg', '.jpeg', '.png', '.gif'}
music_exts = {'.mp3', '.wma', '.ogg', '.wav'}
video_exts = {'.mp4', '.wmv', '.mpeg'}


def get_dirs(test, env='.env'):
    dirs = {
        'downloads': None,
        'library': None,
        'img': None,
        'music': None,
        'video': None
    }
    with open(env, 'r') as dir_file:
        lines = dir_file.readlines()
        dirs = dict()
        for line in lines:
            if test:
                lineformat = re.search('(.*)_DIR_TEST=(.*)', line)
                if lineformat:
                    dir_name, dir_path = lineformat.groups()
                    dirs[dir_name] = dir_path
            else:
                lineformat = re.search('(.*)_DIR=(.*)', line)
                if lineformat:
                    dir_name, dir_path = lineformat.groups()
                    dirs[dir_name] = dir_path
    return dirs


def main(test=False):
    # get directories for Download, Docs...
    dirs = get_dirs(test)
    os.chdir(dirs['DOWNLOAD'])
    # loop over downfiles
    download_files = os.listdir()
    for file in download_files:
        name, ext = os.path.splitext(file)
        # delete installers
        # move images
        # move books
        # move videos
        # move music
        # check if pdf is book
        # move to books or docs accordingly
        # manually deal with other files
    pass


if __name__ == "__main__":
    main()
