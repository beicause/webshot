from playwright.sync_api import sync_playwright, ViewportSize
import time
from moviepy.editor import *
from typing import Tuple
from os import path
import click


def videoToGif(video: str, output: str, fps: float = 40):
    """
    convert video to gif

    Parameters    
    ----------
    video: video path
    output: output gif path
    fps: gif fps
    """
    clip = VideoFileClip(video)
    clip.write_gif(output, fps=fps)
    clip.close()


def shootWebmFromStr(html: str,  output: str, duration: float, size: ViewportSize = None, tmp_dir: str = '__WEBSHOT_WEBM_TMP__'):
    """
    record html content as webm

    Parameters    
    ----------
    html: html content
    output: output path
    duration: duration to record
    size: ViewportSize:{ width: int,height: int }
    tmp_dir: temporary output dir
    """
    with sync_playwright() as p:
        browser = p.webkit.launch()
        page = browser.new_page(
            record_video_dir=tmp_dir, record_video_size=size, viewport=size)
        page.set_content(html)
        time.sleep(duration)
        page.close()
        page.video.save_as(output)
        _rmdir(tmp_dir)
        browser.close()


def shootWebmFromFile(file: str,  output: str, duration: float, size: ViewportSize = None, tmp_dir: str = '__WEBSHOT_WEBM_TMP__'):
    """
    record html content from file and save as webm

    Parameters    
    ----------
    file: input file path
    output: output path
    duration: duration to record
    size: ViewportSize:{ width: int,height: int }
    tmp_dir: temporary output dir
    """
    html_file = open(file, encoding='utf-8')
    html = html_file.read()
    html_file.close()
    shootWebmFromStr(html, output, duration, size, tmp_dir)


def _rmdir(path):
    for root, dirs, files in os.walk(path, topdown=False):
        for name in files:
            os.remove(os.path.join(root, name))
        for name in dirs:
            os.rmdir(os.path.join(root, name))
    os.rmdir(path)


@click.command('webshoot')
@click.argument('file', type=str, required=True)
@click.option('--output', '-o', type=str)
@click.option('--duration', '-d', required=True, type=float)
@click.option('--size', '-s', nargs=2, type=int)
@click.option('--tmp', type=str)
def webshot(file: str,  output: str, duration: float, size: Tuple[int, int], tmp: str):
    if output == None:
        name, ext = path.splitext(path.basename(file))
        output = name+'.webm'
    if tmp == None:
        tmp = '__WEBSHOT_WEBM_TMP__'
    click.echo('start...')
    shootWebmFromFile(file, output, duration, None if size == None else {
                      'width': size[0], 'height': size[1]}, tmp)
    click.echo('write file: '+output)


if __name__ == '__main__':
    webshot()
