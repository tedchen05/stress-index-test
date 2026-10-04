# -*- coding: utf-8 -*-
"""
Created on Thu May 30 21:50:30 2024

@author: 陳皓均

壓力指數測試表核心功能
"""
from dataclasses import dataclass

SOURCE = "衛生福利部國民健康署 健康九九+網站"
SOURCE_URL = "https://health99.hpa.gov.tw/health99/HC/D/115/StressIndex"

INTRO = ("預防勝於治療，職場心理健康促進計劃的第一步就是了解現況。"
         "可利用本表評估壓力狀況，作為擬訂壓力管理計畫之參考依據。")

QUESTIONS = [
    "您最近是否經常感到緊張，覺得工作總是做不完？",
    "您最近是否老是睡不好，常常失眠或睡眠品質不佳？",
    "您最近是否經常有情緒低落、焦慮、煩躁的情況？",
    "您最近是否經常忘東忘西、變得很健忘？",
    "您最近是否經常覺得胃口不好？或胃口特別好？",
    "您最近六個月內是否生病不只一次了？",
    "您最近是否經常覺得很累，假日都在睡覺？",
    "您最近是否經常覺得頭痛、腰痠背痛？",
    "您最近是否經常意見和別人不同？",
    "您最近是否注意力經常難以集中？",
    "您最近是否經常覺得未來充滿不確定感？恐懼感？",
    "有人說您最近氣色不太好嗎？",
]


# 顯示在介面上的錯誤
class StressError(Exception):
    pass


# 壓力等級
@dataclass(frozen=True)
class Level:
    limit: int  # 「是」的數量上限
    range_text: str
    name: str
    advice: str


LEVELS = [
    Level(3, "0～3 個", "壓力可負荷",
          "您的壓力指數還在能負荷的範圍。"),
    Level(5, "4～5 個", "需要壓力管理",
          "壓力蠻困擾您，雖能勉強應付，但必需認真學習壓力管理了，"
          "同時多與良師益友聊一聊。"),
    Level(8, "6～8 個", "壓力很大",
          "您的壓力很大，趕快去看心理衛生專業人員，接受系統性的心理治療。"),
    Level(len(QUESTIONS), f"9～{len(QUESTIONS)} 個", "壓力嚴重",
          "您的壓力已很嚴重，應該看精神專科醫師，依醫師處方用藥物治療與心理治療，"
          "幫忙您的生活趕快恢復正常軌道。"),
]


# 測驗結果
@dataclass
class StressResult:
    yes_count: int
    level_index: int  # 對應 LEVELS 的位置

    # 壓力等級
    @property
    def level(self):
        return LEVELS[self.level_index]


# 依「是」的數量取得等級位置
def level_index_of(yes_count):
    for index, level in enumerate(LEVELS):
        if yes_count <= level.limit:
            return index
    return len(LEVELS) - 1


# 取得未作答的題號(從1開始)
def unanswered(answers):
    return [no for no, answer in enumerate(answers, start=1)
            if answer is None]


# 檢查作答並計算結果，answers 為 True(是)、False(否)、None(未答)
def evaluate(answers):
    if len(answers) != len(QUESTIONS):
        raise StressError(f"題數不符，應為 {len(QUESTIONS)} 題")
    missing = unanswered(answers)
    if missing:
        numbers = "、".join(str(no) for no in missing)
        raise StressError(f"還有 {len(missing)} 題未作答：第 {numbers} 題")
    yes_count = sum(answers)
    return StressResult(yes_count, level_index_of(yes_count))
