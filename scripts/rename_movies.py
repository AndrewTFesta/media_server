'''
@title

@description

'''
import argparse
import os
import re
import shutil
from io import BytesIO
from pathlib import Path

import requests
import unicodedata
from PIL import Image

from media_server import data_dir
from media_server.storage import save_data


def get_imdb_entry(movie_title):
    base_url = r'https://v2.sg.media-imdb.com/suggestion/h/'
    search_url = f'{base_url}{movie_title}.json'

    movie_entry = None
    response = requests.get(search_url)
    if response:
        response = response.json()
        if len(response['d']) == 0:
            return None
        info = response['d'][0]
        movie_id = info['id']
        movie_year = info['y']
        movie_name = info['l']
        movie_poster = info['i']
        image_url = movie_poster['imageUrl']

        movie_entry = {
            'name': movie_name,
            'id': movie_id,
            'year': movie_year,
            'poster_url': image_url,
        }
        image_content = requests.get(image_url).content
        image_bytes = BytesIO(image_content)
        image = Image.open(image_bytes)
        movie_entry['poster'] = image
    return movie_entry

def slugify(value, allow_unicode=False):
    """
    Taken from https://github.com/django/django/blob/master/django/utils/text.py
    Convert to ASCII if 'allow_unicode' is False. Convert spaces or repeated
    dashes to single dashes. Remove characters that aren't alphanumerics,
    underscores, or hyphens. Convert to lowercase. Also strip leading and
    trailing whitespace, dashes, and underscores.
    """
    value = str(value)
    if allow_unicode:
        value = unicodedata.normalize('NFKC', value)
    else:
        value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
    value = re.sub(r'[^\w\s-]', '', value.lower())
    return re.sub(r'[-\s]+', '-', value).strip('-_')

def process_movie(movie_directory: Path, destination_dir: Path, archive_dir: Path):
    movie_exts = ['mkv', 'mp4', 'avi', 'webm']
    subtitle_exts = ['sub', 'idx', 'srt']
    year_re = r'(19|20)\d{2}'
    invalid_chars = ['?', ':', '<', '>', '!', '@', '#', '$', '%', '^', '&', '*']
    supervised = False
    dry_run = False

    movie_name = movie_directory.name
    sub_paths = [
        each_subs_path
        for each_ext in subtitle_exts
        for each_subs_path in movie_directory.glob(f'**/*.{each_ext}')
    ]
    movie_candidates = [
        {
            'path': each_movie_path,
            'name': each_movie_path.name,
            'ext': each_movie_path.suffix[1:],
            'size': os.stat(each_movie_path).st_size,
        }
        for each_ext in movie_exts
        for each_movie_path in movie_directory.glob(f'**/*.{each_ext}')
    ]
    movie_candidates = sorted(movie_candidates, key=lambda each_movie_path: each_movie_path['size'], reverse=True)
    if len(movie_candidates) == 0:
        print(f'\tNo video files found for {movie_directory}')
        return

    selected_candidate = movie_candidates[0]
    print(f'\tMovie located: {selected_candidate['name']}')
    print(f'\tFound {len(sub_paths)} subtitle(s)')
    movie_year = list(re.finditer(year_re, movie_name))
    if len(movie_year) != 1:
        print(f'\tPotential issue with movie name: {movie_name}')
        print(f'\tPlease review the entry and process as needed')
        return

    movie_year_match = movie_year[0].regs[0]
    movie_year = movie_name[movie_year_match[0]:movie_year_match[1]]
    movie_name = movie_name[:movie_year_match[0]]
    movie_title = f'{movie_name} ({movie_year})'
    movie_info = get_imdb_entry(movie_title)
    if movie_info is None:
        print(f'\tUnable to get movie info for {movie_title}')
        return

    fixed_name = movie_info['name']
    for each_char in invalid_chars:
        fixed_name = fixed_name.replace(each_char, '')
    print(f'\t{fixed_name} ({movie_year}) {{imdb-{movie_info['id']}}}')

    movie_ident = f'{fixed_name} ({movie_year}) {{imdb-{movie_info['id']}}}'
    each_renamed_dir = destination_dir / movie_ident
    pre_existing_movie = False
    if not each_renamed_dir.exists():
        each_renamed_dir.mkdir(parents=True, exist_ok=True)
    else:
        pre_existing_movie = True
        existing_movies = [
            each_movie_path
            for each_ext in movie_exts
            for each_movie_path in movie_directory.glob(f'**/*.{each_ext}')
        ]
        movie_count = len(existing_movies)
        movie_ident = f'{movie_ident} {{{movie_count}}}'
    renamed_movie_path = each_renamed_dir / f'{movie_ident}.{selected_candidate['ext']}'
    print(f'\tRenaming to:\n\t\t`{renamed_movie_path}`')
    if supervised:
        user_in = input('\t\t[y/n]: ')
        if len(user_in.strip()) > 0 and not user_in.lower().startswith('y'):
            print(f'Renaming cancelled')
            return

    movie_info['size'] = selected_candidate['size']
    movie_info['subs'] = []
    if not dry_run:
        shutil.copy2(selected_candidate['path'], renamed_movie_path)
    for each_sub_path in sub_paths:
        subs_dir = each_renamed_dir / 'subs'
        if not subs_dir.exists():
            subs_dir.mkdir(parents=True, exist_ok=True)
        sub_name = each_sub_path.name
        each_dest_path = subs_dir / sub_name
        if not dry_run:
            shutil.copy2(each_sub_path, each_dest_path)
        movie_info['subs'].append(sub_name)

    poster_image = movie_info.pop('poster')
    poster_ext = poster_image.format
    poster_save_path = each_renamed_dir / f'{movie_ident}.{poster_ext}'
    if not pre_existing_movie:
        poster_image.save(poster_save_path)

    metadata_path = each_renamed_dir / 'metadata.json'
    if not dry_run:
        save_data(movie_info, metadata_path, human_readable=True)
    print(f'\tMoving processed record:\n\t{movie_directory}')
    if not archive_dir.exists():
        archive_dir.mkdir(parents=True, exist_ok=True)
    archive_path = archive_dir / movie_ident
    if not dry_run:
        movie_directory.rename(archive_path)
    return


def main(main_args):
    debug = False

    if debug:
        movies_dir = data_dir / 'movies'
    else:
        movies_dir = Path(r'C:\Users\asala\Documents\media\finished')
        # movies_dir = Path(r'G:\movies')
    destination_dir = movies_dir.parent / 'renamed' / 'movies'
    archive_dir = movies_dir.parent / 'archive' / 'movies'


    movies_dirs = [each_dir for each_dir in movies_dir.iterdir() if each_dir.is_dir()]
    for idx, each_dir in enumerate(movies_dirs):
        percent_complete = (idx / len(movies_dirs)) * 100
        print(f'Processing {idx}/{len(movies_dirs)} -- {percent_complete:0.2f}%\n\t{each_dir}...')
        process_movie(each_dir, destination_dir, archive_dir)
    return


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='')

    args = parser.parse_args()
    main(vars(args))
