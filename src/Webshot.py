from typing import Dict
from playwright.sync_api import sync_playwright, ViewportSize
import time
from moviepy.editor import *


def shootGif(html: str,  output: str, duration: float, fps: float = 40, size: ViewportSize = None, tmp_dir: str = '__WEBSHOT_GIF_TMP__'):
    """
    record html content as gif

    Parameters    
    ----------
    html: html content string
    output: output path
    duration: duration to record
    fps: gif fps
    size: ViewportSize:{ width: int,height: int }
    tmp_dir: temporary output dir
    """

    tmp_mv = os.path.normpath(os.path.join(
        output, '..', '__WEBSHOT_GIF_TMP__.webm'))
    shootWebm(html, tmp_mv, duration, size, tmp_dir)
    shootGif(tmp_mv, output, fps)
    os.remove(tmp_mv)


def shootGif(video: str, output: str, fps: float = 40):
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


def shootWebm(html: str,  output: str, duration: float, size: ViewportSize = None, tmp_dir: str = '__WEBSHOT_WEBM_TMP__'):
    """
    record html content as webm

    Parameters    
    ----------
    html: html content string
    output: output path
    duration: duration to record
    size: ViewportSize:{ width: int,height: int }
    tmp_dir: temporary output dir
    """
    with sync_playwright() as p:
        browser = p.webkit.launch(slow_mo=0)
        page = browser.new_page(
            record_video_dir=tmp_dir, record_video_size=size)
        page.set_content(html)
        time.sleep(duration)
        page.close()
        page.video.save_as(output)
        browser.close()
        _rmdir(tmp_dir)


def _rmdir(path):
    for root, dirs, files in os.walk(path, topdown=False):
        for name in files:
            os.remove(os.path.join(root, name))
        for name in dirs:
            os.rmdir(os.path.join(root, name))
    os.rmdir(path)
