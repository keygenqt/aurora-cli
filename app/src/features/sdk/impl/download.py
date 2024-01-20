import os
import time
from multiprocessing.pool import ThreadPool as Pool
from pathlib import Path

import click
import requests
from alive_progress import alive_bar


# Download files with progress
def multi_download(urls):
    downloads = {}
    files = []
    total_length = 0
    click.echo('')

    # Get size files and check exist
    for url in urls:
        file_name = os.path.basename(url)
        download_path = str(Path.home() / "Downloads" / file_name)
        files.append(download_path)
        if os.path.isfile(download_path):
            click.echo('Already exists: {}'.format(file_name))
        else:
            downloads[url] = download_path
            response = requests.head(url)
            total_length += int(response.headers.get('content-length'))
            click.echo('Download: {}'.format(file_name))

    # Check has downloads files
    if not downloads:
        return files

    # Run download
    click.echo('')
    pool = Pool(len(downloads.keys()) + 1)
    pool.apply_async(_multi_progress, [total_length, downloads.values()])
    for key, value in downloads.items():
        pool.apply_async(_download, [key, value])

    pool.close()
    pool.join()

    return files


# Run download file
def _download(url, file):
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(file, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024):
                f.write(chunk)


# Show progress
def _multi_progress(total_length, files):
    download_length = 0
    with alive_bar(total_length) as bar:
        while download_length < total_length:
            time.sleep(1)
            file_size = 0
            for file in files:
                if os.path.isfile(file):
                    file_stats = os.stat(file)
                    file_size += file_stats.st_size
            bar(file_size - download_length)
            download_length = file_size
