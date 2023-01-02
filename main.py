import pyautogui as pag
import portalocker
import keyboard
import my_keyboard
import time

def main():
    # 多重起動を防止する
    lockfile = open('_.lock', "a+")
    try:
        portalocker.lock(lockfile,
                         portalocker.LOCK_EX | portalocker.LOCK_NB)
    except IOError:
        # 既に起動済み
        print('Already running!')
        exit(1)

    # while True:
        # キーボードの監視
    keyboard.on_press(my_keyboard.callback)
    keyboard.wait('esc')
    print("テキスト展開を終了します。")
        # # キーボード監視の中断
        # keyboard.unhook_all()
        # pag.alert('テキスト展開を一時停止します\nshift+pauseで再開します')
        # keyboard.wait('esc')
        # pag.alert('テキスト展開を再開しました')


if __name__ == '__main__':
    main()
