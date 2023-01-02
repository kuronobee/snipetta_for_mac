import datetime

def _translate_keyword(keyword):
    """
    キーワードオブジェクトを読み込んで文字列を生成します
    :param keyword:
    :return: string
    """
    if keyword['word'] is not None:
        return keyword['word']
    elif keyword['script'] is not None:
        try:
            return eval(keyword['script'])
        except Exception as e:
            return f'Error:{e.__str__()}'
    else:
        return ''