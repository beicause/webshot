# webshot

record web animation as webm or gif.

## Usage

```py
from Webshot import shootWebm,shootGif

shootWebm(html: str,  output: str, duration: float, size: Dict[str, int] = None, tmp_dir: str = '__WEBSHOT_WEBM_TMP__')
shootGif(html: str,  output: str, duration: float, fps: float = 40, size: Dict[str, int] = None, tmp_dir: str = '__WEBSHOT_GIF_TMP__')

```
