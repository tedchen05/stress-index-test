# -*- coding: utf-8 -*-
"""
Created on Thu May 30 21:50:30 2024

@author: 陳皓均

壓力指數測試表視窗介面
"""
import tkinter as tk
import webbrowser
from tkinter import ttk

from stress_core import (INTRO, LEVELS, QUESTIONS, SOURCE, SOURCE_URL,
                         StressError, evaluate, unanswered)

APP_TITLE = "壓力指數測試表"
FONT = "微軟正黑體"

PRIMARY = "#1F5FAD"
TEXT = "#222222"
MUTED = "#666666"
ERROR = "#C0392B"
BG = "#F5F7FA"
CARD_BG = "#FFFFFF"
CARD_BORDER = "#C9D8EC"
ROW_LINE = "#E6ECF3"
NUMBER_BG = "#E8F0FA"
HIGHLIGHT_BG = "#F3F7FC"

LEVEL_COLORS = ["#1E7E34", "#B88A00", "#D26900", "#C0392B"]  # 對應 LEVELS

YES, NO, NONE = 1, 0, -1  # 作答變數的值
SIDE_WIDTH = 320  # 右側欄寬度


# 建立白底卡片
def make_card(parent, **pack_options):
    card = tk.Frame(parent, bg=CARD_BG, highlightthickness=1,
                    highlightbackground=CARD_BORDER, padx=16, pady=12)
    card.pack(**pack_options)
    return card


# 主視窗
class StressApp:

    # 建立視窗
    def __init__(self, root):
        self.root = root
        self.answers = []  # 每題的作答變數
        self.rows = []  # 每題的(題號標籤, 是按鈕, 否按鈕)

        root.title(APP_TITLE)
        root.configure(bg=BG)
        root.resizable(False, False)
        self._setup_style()

        self._build_header()
        body = tk.Frame(root, bg=BG, padx=20)
        body.pack(fill="both", expand=True)
        self._build_questions(body)
        self._build_side(body)
        self._build_footer()

        root.bind("<Return>", lambda event: self.submit())

    # 設定進度條樣式
    def _setup_style(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Answer.Horizontal.TProgressbar", thickness=8,
                        background=PRIMARY, troughcolor=ROW_LINE,
                        bordercolor=ROW_LINE, lightcolor=PRIMARY,
                        darkcolor=PRIMARY)

    # 版面

    # 標題列
    def _build_header(self):
        header = tk.Frame(self.root, bg=BG, padx=20, pady=16)
        header.pack(fill="x")
        tk.Label(header, text=APP_TITLE, font=(FONT, 20, "bold"), bg=BG,
                 fg=PRIMARY).pack(anchor="w")
        tk.Label(header, text=INTRO, font=(FONT, 10), bg=BG, fg=MUTED,
                 justify="left", wraplength=880).pack(anchor="w")

    # 左側題目清單
    def _build_questions(self, parent):
        card = make_card(parent, side="left", fill="y")
        title = tk.Frame(card, bg=CARD_BG)
        title.pack(fill="x")
        tk.Label(title, text="最近一個月，您是否有以下情況？",
                 font=(FONT, 12, "bold"), bg=CARD_BG, fg=TEXT).pack(
            side="left")
        self.progress_label = tk.Label(title, bg=CARD_BG, fg=MUTED,
                                       font=(FONT, 10))
        self.progress_label.pack(side="right")
        self.progress_bar = ttk.Progressbar(
            card, maximum=len(QUESTIONS),
            style="Answer.Horizontal.TProgressbar")
        self.progress_bar.pack(fill="x", pady=(6, 10))

        for no, question in enumerate(QUESTIONS, start=1):
            tk.Frame(card, bg=ROW_LINE, height=1).pack(fill="x")
            row = tk.Frame(card, bg=CARD_BG, pady=5)
            row.pack(fill="x")

            number = tk.Label(row, text=str(no), width=3, bg=NUMBER_BG,
                              fg=PRIMARY, font=(FONT, 10, "bold"))
            number.pack(side="left")
            tk.Label(row, text=question, bg=CARD_BG, fg=TEXT,
                     font=(FONT, 11), anchor="w").pack(
                side="left", fill="x", expand=True, padx=(10, 12))

            answer = tk.IntVar(value=NONE)
            no_button = self._choice(row, "否", NO, answer)
            no_button.pack(side="right")
            yes_button = self._choice(row, "是", YES, answer)
            yes_button.pack(side="right", padx=(0, 6))

            self.answers.append(answer)
            self.rows.append((number, yes_button, no_button))

    # 建立是/否按鈕
    def _choice(self, parent, text, value, variable):
        return tk.Radiobutton(
            parent, text=text, value=value, variable=variable,
            indicatoron=False, width=4, font=(FONT, 10, "bold"),
            bg=CARD_BG, fg=MUTED, selectcolor=PRIMARY,
            activebackground=HIGHLIGHT_BG, relief="solid", offrelief="solid",
            bd=1, cursor="hand2", command=self._on_answer)

    # 右側結果、評分標準與按鈕
    def _build_side(self, parent):
        side = tk.Frame(parent, bg=BG, width=SIDE_WIDTH)
        side.pack(side="left", fill="y", padx=(16, 0))
        side.pack_propagate(False)  # 固定寬度，結果文字變動時視窗不跳動

        buttons = tk.Frame(side, bg=BG)
        buttons.pack(fill="x", side="bottom")
        tk.Button(buttons, text="查看結果 (Enter)", font=(FONT, 12, "bold"),
                  bg=PRIMARY, fg="white", activebackground="#184C8A",
                  activeforeground="white", relief="flat", cursor="hand2",
                  pady=6, command=self.submit).pack(fill="x")
        tk.Button(buttons, text="重新作答", font=(FONT, 10), bg=CARD_BG,
                  fg=PRIMARY, activebackground=HIGHLIGHT_BG, relief="solid",
                  bd=1, cursor="hand2", command=self.reset).pack(
            fill="x", pady=(8, 0))

        result = make_card(side, fill="x")
        tk.Label(result, text="測驗結果", bg=CARD_BG, fg=MUTED,
                 font=(FONT, 10)).pack(anchor="w")
        self.count_label = tk.Label(result, bg=CARD_BG,
                                    font=(FONT, 24, "bold"))
        self.count_label.pack(anchor="w")
        self.level_label = tk.Label(result, bg=CARD_BG,
                                    font=(FONT, 13, "bold"))
        self.level_label.pack(anchor="w")
        self.advice_label = tk.Label(result, bg=CARD_BG, font=(FONT, 10),
                                     justify="left", anchor="nw", height=3,
                                     padx=0, bd=0, highlightthickness=0)
        self.advice_label.pack(fill="x", pady=(2, 0))
        self.advice_label.bind("<Configure>", self._fit_wrap)

        self._build_levels(side)
        self.reset()

    # 依標籤實際寬度設定換行寬度(標籤無內距與邊框)
    def _fit_wrap(self, event):
        event.widget.config(wraplength=event.width - 2)

    # 評分標準，測驗後標示所屬等級
    def _build_levels(self, parent):
        card = make_card(parent, fill="x", pady=12)
        tk.Label(card, text="評分標準(回答「是」的數量)", bg=CARD_BG, fg=MUTED,
                 font=(FONT, 10)).pack(anchor="w", pady=(0, 4))

        self.level_rows = []
        for level, color in zip(LEVELS, LEVEL_COLORS):
            row = tk.Frame(card, bg=CARD_BG, padx=6, pady=3)
            row.pack(fill="x")
            labels = [
                tk.Label(row, width=2, bg=color),
                tk.Label(row, text=level.range_text, width=8, anchor="w",
                         bg=CARD_BG, fg=TEXT, font=(FONT, 10)),
                tk.Label(row, text=level.name, anchor="w", bg=CARD_BG,
                         fg=TEXT, font=(FONT, 10)),
            ]
            labels[0].pack(side="left")
            labels[1].pack(side="left", padx=(8, 0))
            labels[2].pack(side="left")
            self.level_rows.append((row, labels))

    # 頁尾來源與聲明
    def _build_footer(self):
        footer = tk.Frame(self.root, bg=BG, padx=20, pady=10)
        footer.pack(fill="x")
        tk.Label(footer, text="題目來源：", bg=BG, fg=MUTED,
                 font=(FONT, 9)).pack(side="left")
        link = tk.Label(footer, text=SOURCE, bg=BG, fg=PRIMARY,
                        font=(FONT, 9, "underline"), cursor="hand2")
        link.pack(side="left")
        link.bind("<Button-1>", lambda event: webbrowser.open(SOURCE_URL))
        tk.Label(footer, text="本測驗僅供自我評估參考，不能取代專業診斷",
                 bg=BG, fg=MUTED, font=(FONT, 9)).pack(side="right")

    # 作答

    # 取得目前作答，未答為 None
    def current_answers(self):
        values = [answer.get() for answer in self.answers]
        return [None if value == NONE else value == YES for value in values]

    # 更新按鈕顏色與作答進度
    def _on_answer(self):
        for answer, row in zip(self.answers, self.rows):
            number, yes_button, no_button = row
            value = answer.get()
            yes_button.config(fg="white" if value == YES else MUTED)
            no_button.config(fg="white" if value == NO else MUTED)
            if value != NONE:
                number.config(bg=NUMBER_BG, fg=PRIMARY)

        done = len(QUESTIONS) - len(unanswered(self.current_answers()))
        self.progress_label.config(text=f"作答進度 {done} / {len(QUESTIONS)}")
        self.progress_bar.config(value=done)

    # 計算並顯示結果
    def submit(self):
        answers = self.current_answers()
        try:
            result = evaluate(answers)
        except StressError as error:
            self._show_error(str(error), unanswered(answers))
        else:
            self._show_result(result)

    # 顯示測驗結果並標示等級
    def _show_result(self, result):
        color = LEVEL_COLORS[result.level_index]
        self.count_label.config(text=f"{result.yes_count} 個「是」", fg=color)
        self.level_label.config(text=result.level.name, fg=color)
        self.advice_label.config(text=result.level.advice, fg=TEXT)
        self._mark_level(result.level_index)

    # 顯示錯誤並以紅色標示未答題號
    def _show_error(self, text, missing):
        self.count_label.config(text="尚未完成", fg=ERROR)
        self.level_label.config(text=" ")
        self.advice_label.config(text=text, fg=ERROR)
        self._mark_level(None)
        for no in missing:
            self.rows[no - 1][0].config(bg=ERROR, fg="white")

    # 標示所屬等級，None 表示清除
    def _mark_level(self, index):
        for i, (row, labels) in enumerate(self.level_rows):
            selected = i == index
            bg = HIGHLIGHT_BG if selected else CARD_BG
            row.config(bg=bg)
            for label in labels[1:]:
                label.config(bg=bg, font=(FONT, 10,
                                          "bold" if selected else "normal"))

    # 清除作答與結果
    def reset(self):
        for answer, (number, _, _) in zip(self.answers, self.rows):
            answer.set(NONE)
            number.config(bg=NUMBER_BG, fg=PRIMARY)
        self.count_label.config(text="—", fg=PRIMARY)
        self.level_label.config(text=" ")
        self.advice_label.config(text="全部作答後按「查看結果」", fg=TEXT)
        self._mark_level(None)
        self._on_answer()


# 啟動程式
def main():
    root = tk.Tk()
    StressApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
