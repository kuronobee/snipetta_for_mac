import customtkinter as ctk
import tkinter as tk
import re


class SnippetWindow:
    def __init__(self, position):
        self.position = position

    def _button_ok_click(self):
        val_list = [elm.get() for elm in self.entities]
        for val in val_list:
            self.word = self.pattern.sub(val, self.word, 1)

        self.app.quit()
        self.app.destroy()

    def _on_key_down(self, event):
        self._button_ok_click()

    def show_window(self, snippet):
        """
        スニペットウインドウを表示します
        :return:
        """
        ctk.set_appearance_mode('System')
        ctk.set_default_color_theme('blue')
        self.app = ctk.CTk()
        self.app.title(f'snipetta - コマンド({snippet["snippet"]})')
        self.app.geometry(f"400x240+{self.position[0]}+{self.position[1]}")
        # self.app.configure()
        self.word = snippet["word"]
        self.pattern = re.compile(r'%\[.+?]%')
        self.entities = []

        result = self.pattern.split(self.word)
        blank = re.findall(r'%\[(.+?)]%', self.word)

        height = 100 if self.word.find('\n') != -1 else 30
        txt = ctk.CTkTextbox(master=self.app, height=height, width=200, wrap=tk.NONE, font=("メイリオ",15))
        txt.pack(padx=10, pady=10, fill=tk.BOTH)

        txt.tag_config("yellow", background="#FFFF00", foreground="#808080")

        params = []
        for elem in blank:
            r = elem.split(':')
            if len(r) > 1:
                c = r[1].split('|')
                if len(c) > 1:
                    params.append({"tag": r[0], "default": c[0], "options": c})
                else:
                    params.append({"tag": r[0], "default": r[1], "options": []})
            else:
                params.append({"tag": elem, "default": "", "options": []})

        for index, text in enumerate(result):
            txt.insert("end", text)
            if len(params) > index:
                txt.insert("end", params[index]["tag"], "yellow")

        txt.configure(state=tk.DISABLED)
        for id, param in enumerate(params):
            frame = ctk.CTkFrame(master=self.app)
            label = ctk.CTkLabel(master=frame, width=50, text=param["tag"])
            # optionsが存在する場合は、TextBoxをComboBoxに変更する
            if len(param["options"]) > 0:
                entity = ctk.CTkComboBox(master=frame, values=param["options"])
                entity.set(param["options"][1])
            else:
                entity = ctk.CTkEntry(master=frame, placeholder_text=param["tag"])
                entity.insert("end", param["default"])
            frame.pack(pady=0, side=tk.TOP, fill=tk.BOTH)
            label.pack(padx=10, side=tk.LEFT)
            entity.pack(padx=10, pady=5, side=tk.LEFT)
            entity.bind('<Return>', self._on_key_down)
            self.entities.append(entity)

        if len(self.entities) > 0:
            self.entities[0].focus()

        button = ctk.CTkButton(master=self.app, command=self._button_ok_click, text="OK")
        button.pack(pady=10)
        self.app.mainloop()
        # 生成された文章を出力
        return self.word

