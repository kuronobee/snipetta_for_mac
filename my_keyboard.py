import keyboard
import pyperclip
from time import sleep
import snippetwindow as sw
import re
from concurrent.futures import ProcessPoolExecutor
from eval_script import _translate_keyword
import pywinctl as pwc

# import win32gui
# import win32api
# import win32process

import my_sqlite
import platform


CARET_WORD = '%|'

M_EXPAND = 2
M_EXIT = 3

log = ''
store = my_sqlite.snippet_store("snippet.db")
# _keyword = [{
#         "label": 'my name',
#         "snippet": ':name',
#         "word": '黒木　建吾',
#         "script": None,
#         "typing": False,
#     },
#     {
#         "label": 'home address',
#         "snippet": ':address',
#         "word": '宮崎市大坪東3丁目19-20',
#         "script": None,
#         "typing": False,
#     },
#     {
#         "label": 'sudo権限でpython起動',
#         "snippet": ':sudo',
#         "word": 'sudo python %|main.py%|',
#         "script": None,
#         "typing": False,
#     }
# ]
# for _key in _keyword:
#     store.add_snippet(_key)

keywords = store.load_snippet_list()


def callback(key):
    global log
    print(key)
    if key.name is None:
        return

    for keyword in \
            [keyword for keyword in keywords if keyword[:len(log)] == log]:
        if len(log) >= len(keyword):
            continue
        # 文字キー以外の場合は何もしない
        if key.name != 'backspace' and len(key.name) != 1:
            return
        elif key.name == 'backspace':
            log = log[:-1]
            return
        next_c = keyword[len(log)]
        if next_c == key.name:
            log += key.name
            if log == keyword:
                # if _expand_text(keyword):
                #     keyboard.hook_key('tab', handler, suppress=True)
                _expand_text(keyword)
                log = ''
            return

    log = ''


def _expand_text(snippet):
    keyword = store.search_snippet(snippet)
    for _ in range(len(keyword["snippet"])):
        keyboard.press_and_release('backspace')

    if re.search(r'%\[.+?]%', keyword["word"]):
        # caret_pos = get_caret_pos()
        window = pwc.getActiveWindow()
        snip = sw.SnippetWindow((0, 0))# (window.centerx, window.centery))
        with ProcessPoolExecutor(max_workers=1) as executor:
            val = executor.submit(snip.show_window, keyword)

        keyword["word"] = val.result()

    # キャレットの位置を指定
    _caret = keyword["word"].find(CARET_WORD)
    _select = keyword["word"].find(CARET_WORD, _caret + 1)
    keyword["word"] = keyword["word"].replace(CARET_WORD, '')

    # clipboardの内容を一時変数に避難
    tmp = pyperclip.paste()
    pyperclip.copy(_translate_keyword(keyword))
    sleep(0.3)
    # 現在のカーソル位置にペースト(OSにより、ショートカットを切り替える）
    if platform.system() == 'Windows':
        keyboard.press_and_release('control+v')
    elif platform.system() == 'Darwin':
        keyboard.press_and_release('command+v')
    else:
        keyboard.press_and_release('control+shift+v')
    sleep(0.3)
    # clipboardを復元
    pyperclip.copy(tmp if tmp is not None else '')

    if _caret != -1:
        caret = len(keyword["word"]) - _caret \
            if _caret >= 0 else - _caret
        for _ in range(caret):
            keyboard.press_and_release('left')
        sleep(0.2)
    # 指定されている選択範囲を選択
    if _select != -1:
        _select -= len(CARET_WORD)
        # shiftを押しながらrightキーで文字列を選択
        keyboard.press('shift')
        for _ in range(_select - _caret):
            keyboard.press_and_release('right')
        keyboard.release('shift')





