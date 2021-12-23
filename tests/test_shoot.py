
from src.Webshot import shootWebmFromFile, webshot
from click.testing import CliRunner
from os import path


def test_shootwebm():
    # https://github.com/beicause/csvg
    file = 'tests/bubble.svg'
    shootWebmFromFile(file, 'test_out/api-bubble.webm',
                      11, {'width': 500, 'height': 500})


def test_cli():
    runner = CliRunner()
    res = runner.invoke(
        webshot, 'tests/bubble.svg -d 11 -o test_out/cli-bubble.webm -s 500 500')
    assert(res.exit_code, 0)
