# -*- coding: utf-8 -*-
"""
Created on Thu May 30 21:50:30 2024

@author: 陳皓均

壓力指數測試表：回答12道題目，依「是」的數量評估壓力程度並給予建議
"""

import tkinter as tk

TITLE = "壓力指數測試表"

INTRO = [
    "預防勝於治療，職場心理健康促進計劃的第一步就是了解現況。",
    "因此，可利用本表進行壓力評估，評估每位員工的壓力狀況，"
    "作為擬訂壓力管理計畫之參考依據。",
]

QUESTIONS = [
    "1.您最近是否經常感到緊張，覺得工作總是做不完？",
    "2.您最近是否老是睡不好，常常失眠或睡眠品質不佳？",
    "3.您最近是否經常有情緒低落、焦慮、煩躁的情況？",
    "4.您最近是否經常忘東忘西、變得很健忘？",
    "5.您最近是否經常覺得胃口不好？或胃口特別好？",
    "6.您最近六個月內是否生病不只一次了？",
    "7.您最近是否經常覺得很累，假日都在睡覺？",
    "8.您最近是否經常覺得頭痛、腰痠背痛？",
    "9.您最近是否經常意見和別人不同？",
    "10.您最近是否注意力經常難以集中？",
    "11.您最近是否經常覺得未來充滿不確定感？恐懼感？",
    "12.有人說您最近氣色不太好嗎？",
]

# 壓力等級：(「是」的數量上限, 數量說明, 建議)
LEVELS = [
    (3, "3個以下", "您的壓力指數還在能負荷的範圍。"),
    (5, "4~5個",
     "壓力蠻困擾您，雖能勉強應付，但必需認真學習壓力管理了，"
     "同時多與良師益友聊一聊。"),
    (8, "6~8個",
     "您的壓力很大，趕快去看心理衛生專業人員，接受系統性的心理治療。"),
    (len(QUESTIONS), "9個以上",
     "您的壓力已很嚴重，應該看精神專科醫師，依醫師處方用藥物治療與心理治療，"
     "幫忙您的生活趕快恢復正常軌道。"),
]


# 依「是」的數量取得建議
def get_advice(yes_count):
    for limit, _, advice in LEVELS:
        if yes_count <= limit:
            return advice
    return LEVELS[-1][2]


# 壓力指數測試表主程式
class StressTestApp:

    # 建立主視窗與題目
    def __init__(self, root):
        self.root = root
        self.root.title(TITLE)
        self.answers = []

        for row, text in enumerate(INTRO):
            tk.Label(root, text=text).grid(row=row, column=2)

        header_row = len(INTRO)
        tk.Label(root, text="是").grid(row=header_row, column=0, sticky="w")
        tk.Label(root, text="否").grid(row=header_row, column=1, sticky="w")
        tk.Label(root, text="題目").grid(row=header_row, column=2, sticky="w")

        for i, question in enumerate(QUESTIONS, start=header_row + 1):
            answer = tk.IntVar(value=1)  # 預設為「是」
            tk.Radiobutton(root, value=1, variable=answer).grid(
                row=i, column=0, sticky="w")
            tk.Radiobutton(root, value=0, variable=answer).grid(
                row=i, column=1, sticky="w")
            tk.Label(root, text=question).grid(row=i, column=2, sticky="w")
            self.answers.append(answer)

        tk.Button(root, text="提交", command=self.show_criteria).grid(
            row=header_row + len(QUESTIONS) + 1, column=0, columnspan=3)

    # 開啟子視窗並鎖定主視窗
    def open_window(self):
        window = tk.Toplevel(self.root)
        window.title(TITLE)
        window.transient(self.root)
        window.grab_set()
        return window

    # 顯示評分標準
    def show_criteria(self):
        window = self.open_window()
        tk.Label(window, text="壓力指數解答：").grid(
            row=0, column=0, sticky="w")
        for row, (_, label, advice) in enumerate(LEVELS, start=1):
            tk.Label(window, text=f"回答{label}「是」：{advice}").grid(
                row=row, column=0, sticky="w")
        tk.Button(window, text="確認",
                  command=lambda: self.show_result(window)).grid(
            row=len(LEVELS) + 1, column=0)

    # 統計「是」的數量並顯示建議
    def show_result(self, criteria_window):
        criteria_window.destroy()
        yes_count = sum(answer.get() for answer in self.answers)

        window = self.open_window()
        tk.Label(window, text=f"您選擇了{yes_count}個「是」").grid(
            row=0, column=0, sticky="w")
        tk.Label(window, text=get_advice(yes_count)).grid(
            row=1, column=0, sticky="w")
        tk.Button(window, text="確認", command=self.root.destroy).grid(
            row=2, column=0)


if __name__ == "__main__":
    root = tk.Tk()
    StressTestApp(root)
    root.mainloop()
