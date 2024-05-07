# Download directory cleaner
A CLI tool to deal with the mess that is my Downloads directory.
I'm running it on WSL to handle the Windows downloads.
What do I mean with dealing with the mess?
Precisely, this script:
- Deletes installers (.exe, .deb files).
- Moves books to BOOK_DIR (.epub, .mobi, .djvu).
- Moves image files to IMG_DIR.
- Moves audio files to MUSIC_DIR.
- Moves video files to VIDEO_DIR.
- PDF files are moved to BOOK_DIR or DOC_DIR depending on whether they're books or not.
- For other files asks user whether to delete, send to DOC_DIR, or do nothing


## Usage
Clone the repo.
Rename .env_template to .env and write the corresponding paths to your case.
Run clearer.py
I make no assurances that it runs on your system.


## Known issues & improvements
~~Doesn't delete subdirectories.~~

Handle other files by date of last use

Create a pdf classifier
