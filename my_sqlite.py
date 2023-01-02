import sqlite3

keywords = [
    {
        "snippet": ':name',
        "word": '黒木 建吾',
        "script": None,
        "carret": None,
        "select": None,
    },
    {
        "snippet": ':address',
        "word": '宮崎市大坪東[3]丁目[19]-[20]',
        "script": None,
        "carret": 0,
        "select": None,
    },
    {
        "snippet": ':fcred',
        "word": '<span style="color:red"></span>',
        "script": None,
        "carret": -7,
        "select": None
    },
    {
        "snippet": ':snippet',
        "word": '''{
    "snippet": '',
    "word": '',
    "carret": None,
    "select": None
}''',
        "script": None,
        "carret": 0,
        "select": -1
    },
    {
        "snippet": ':kengo',
        "word": "kengo\nkuroki",
        "script": None,
        "carret": None,
        "select": None
    },
    {
        "snippet": ':select',
        "word": 'select this word',
        "script": None,
        "carret": 7,
        "select": 4
    },
    {
        "snippet": ':all_select',
        "word": 'select all words',
        "script": None,
        "carret": 0,
        "select": -1
    },
    {
        "snippet": ':sudo',
        "word": 'sudo python my_keyboard.py',
        "script": None,
        "carret": 12,
        "select": 14
    },
    {
        "snippet": ':out_link',
        "word": '[]()',
        "script": None,
        "carret": 1,
        "select": None
    },
    {
        "snippet": ':email',
        "word": 'kengo_kuroki@med.miyazaki-u.ac.jp',
        "script": None,
        "carret": None,
        "select": None
    },
    {
        "snippet": ':(',
        "word": '()',
        "script": None,
        "carret": 1,
        "select": None
    },
    {
        "snippet": ':[',
        "word": '[]',
        "script": None,
        "carret": 1,
        "select": None
    },
    {
        "snippet": ':len',
        "word": 'len()',
        "script": None,
        "carret": 4,
        "select": None
    },
    {
        "snippet": ':code',
        "word": '''```python

```''',
        "script": None,
        "carret": 10,
        "select": None
    },
    {
        "snippet": ':date',
        "word": None,
        "script": "datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')",
        "carret": None,
        "select": None
    },
    {
        "snippet": ':clip',
        "word": None,
        "script": "pyperclip.paste()",
        "carret": None,
        "select": None
    }
]


class snippet_store():
    def __init__(self, path):
        self.path = path
        conn = sqlite3.connect(path)
        # カーソルを取得
        cursor = conn.cursor()
        sql = '''
        CREATE TABLE IF NOT EXISTS snippets
        (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            label TEXT,
            snippet TEXT,
            word TEXT,
            script TEXT,
            typing INTEGER
        )'''

        cursor.execute(sql)
        conn.commit()
        cursor.close()
        conn.close()

    def load_snippet_list(self):
        # dbファイルからsnippetのみ抜き出してリストを作成する
        # return [keyword["snippet"] for keyword in keywords]
        conn = sqlite3.connect(self.path)
        cursor = conn.cursor()
        sql = "select snippet from snippets"
        cursor.execute(sql)
        data = cursor.fetchall()
        cursor.close()
        conn.close()

        return [d[0] for d in data]

    def search_snippet(self, snippet):
        conn = sqlite3.connect(self.path)
        cursor = conn.cursor()
        sql = "select word, script from snippets where snippet = ?"
        cursor.execute(sql, [snippet])
        data = cursor.fetchone()
        cursor.close()
        conn.close()
        if data:
            return {"snippet": snippet, "word": data[0], "script": data[1]}
        else:
            return None #{"snippet": snippet, "word": '', "script": ''}


    def add_snippet(self, snippet):
        conn = sqlite3.connect(self.path)
        cursor = conn.cursor()
        sql = "insert into snippets(label,snippet,word,script,typing) values (?,?,?,?,?)"
        params = [snippet["label"], snippet["snippet"], snippet["word"], snippet["script"], snippet["typing"]]
        cursor.execute(sql, params)
        conn.commit()
        cursor.close()
        conn.close()
