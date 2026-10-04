# -*- coding: utf-8 -*-
"""
Created on Thu May 30 21:50:30 2024

@author: user
"""


def submitOpen():
    
    ted1 = tk.Toplevel(ted) # 第二個視窗
    ted1.title("壓力指數測試表")
    
    # 答案
    ted1Lb1 = ["壓力指數解答：","回答3個「是」：您的壓力指數還在能負荷的範圍。","回答4~5個「是」：壓力滿困擾您，雖能勉強應付，但必需認真學習壓力管理了，同時多與良師益友聊一聊。",\
               "回答6~8個「是」：您的壓力很大，趕快去看心理衛生專業人員，接受系統性的心理治療。","回答9個以上「是」：您的壓力已很嚴重，應該看精神專科醫師，依醫師處方用藥物治療與心理治療，幫忙您的生活趕快恢復正常軌道。"]

    
    for i in range(5):
        ted1LbA = tk.Label(ted1,text=ted1Lb1[i])
        ted1LbA.grid(row=i+1,column=0,sticky="w")
        
    submit1 = tk.Button(ted1,text="確認",command=submitOpen2)
    submit1.grid(row=6,column=0)        



def submitOpen2():
    
    ted2 = tk.Toplevel(ted) # 第三個視窗
    ted2.title("壓力指數測試表")
    
    global questionC
    
    
    # 值的總和
    # totel = sum(var.get() for var in questionC)
    
    totel = 0
    for var in questionC:
        totel += var.get()
    
    ted2Lb1 = tk.Label(ted2,text=f"您的選擇了{totel}個是")
    ted2Lb1.grid(row=1,column=0,sticky="w")
    
    # 判斷分數 並給予建議
    if totel<=3:
        
        ted2Lb2 = tk.Label(ted2,text="您的壓力指數還在能負荷的範圍。")
        ted2Lb2.grid(row=2,column=0,sticky="w")
        
    elif totel<=5:
        
        ted2Lb2 = tk.Label(ted2,text="壓力蠻困擾您，雖能勉強應付，但必需認真學習壓力管理了，同時多與良師益友聊一聊。")
        ted2Lb2.grid(row=2,column=0,sticky="w")
        
    elif totel<=8:
        
        ted2Lb2 = tk.Label(ted2,text="您的壓力很大，趕快去看心理衛生專業人員，接受系統性的心理治療。")
        ted2Lb2.grid(row=2,column=0,sticky="w")
        
    else:
        
        ted2Lb2 = tk.Label(ted2,text="您的壓力已很嚴重，應該看精神專科醫師，依醫師處方用藥物治療與心理治療，幫忙您的生活趕快恢復正常軌道。")
        ted2Lb2.grid(row=2,column=0,sticky="w")

    end = tk.Button(ted2,text="確認",command=END)
    end.grid(row=3,column=0)

def END():
    ted.destroy()

import tkinter as tk

ted = tk.Tk()
ted.title("壓力指數測試表")

tedLb = tk.Label(ted,text="預防勝於治療，職場心理健康促進計劃的第一步就是了解現況。")
tedLb1 = tk.Label(ted,text="因此，可利用本表進行壓力評估，評估每位員工的壓力狀況，作為擬訂壓力管理計畫之參考依據。")
tedLb.grid(row=1,column=3)
tedLb1.grid(row=2,column=3)

answer = tk.Label(ted,text="是")
answer1 = tk.Label(ted,text="否")

answer.grid(row=3,column=0,sticky="W")
answer1.grid(row=3,column=1,sticky="W")

question = tk.Label(ted,text="題目")
question.grid(row=3,column=3,sticky="W")

#題目內容
questionA = ["1.您最近是否經常感到緊張，覺得工作總是做不完？","2.您最近是否老是睡不好，常常失眠或睡眠品質不佳？",\
             "3.您最近是否經常有情緒低落、焦慮、煩躁的情況？","4.您最近是否經常忘東忘西、變得很健忘？",\
             "5.您最近是否經常覺得胃口不好？或胃口特別好？","6.您最近六個月內是否生病不只一次了？",\
             "7.您最近是否經常覺得很累，假日都在睡覺？","8.您最近是否經常覺得頭痛、腰痠背痛？",\
             "9.您最近是否經常意見和別人不同？","10.您最近是否注意力經常難以集中？",\
             "11.您最近是否經常覺得未來充滿不確定感？恐懼感？","12.有人說您最近氣色不太好嗎？"]

questionC=[]

for i in range(len(questionA)):
    questionB = tk.Label(ted,text=questionA[i]) #題目
    questionB.grid(row=i+4,column=3,sticky="W") #題目位置
    questionC.append(tk.IntVar())
    answer1= tk.Radiobutton(ted,text="",value="1",variable=questionC[i])  #選擇:是
    answer1_1 = tk.Radiobutton(ted,text="",value="0",variable=questionC[i]) #選擇:否
    answer1.grid(row=i+4,column=0,sticky="W")  #選擇是的位置
    answer1_1.grid(row=i+4,column=1,sticky="W")  #選擇否的位置
    answer1.select() #選擇的預設為是
    
# 提交按鈕 並進入第二個視窗
submit = tk.Button(ted,text="提交",command=submitOpen)
submit.grid(row=16,column=0,columnspan=4)

ted.mainloop()


