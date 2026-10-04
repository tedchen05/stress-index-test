# 壓力指數測試表

以 tkinter 製作的職場壓力自我評估小工具，回答 12 道題目後，依「是」的數量給出壓力程度與建議。

本專案為聯成電腦 Python 課程的練習作品。

題目與評分標準來源：[衛生福利部國民健康署 健康九九+網站 — 壓力指數測試](https://health99.hpa.gov.tw/health99/HC/D/115/StressIndex)

## 功能

- 12 道題目以「是／否」按鈕作答，上方**進度條**即時顯示作答進度
- 按「查看結果」後，右側顯示「是」的數量、壓力等級與建議，並在評分標準中標示所屬等級
- 有題目未作答時，**紅色標示未答題號**並列出是第幾題
- 「重新作答」一鍵清除所有作答
- 介面(`stress_gui.py`)與邏輯(`stress_core.py`)分開，題目與評分標準集中在 `stress_core.py` 管理

| 「是」的數量 | 壓力等級 | 建議 |
|---|---|---|
| 0～3 個 | 壓力可負荷 | 壓力指數還在能負荷的範圍 |
| 4～5 個 | 需要壓力管理 | 認真學習壓力管理，多與良師益友聊一聊 |
| 6～8 個 | 壓力很大 | 尋求心理衛生專業人員，接受系統性的心理治療 |
| 9～12 個 | 壓力嚴重 | 看精神專科醫師，接受藥物治療與心理治療 |

---

## 安裝

只使用 Python 內建的 `tkinter`，不需安裝額外套件。

- Python 3.8 以上(Anaconda 或官方版皆可)
- 若要打包成 exe，再安裝 PyInstaller：

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

---

## 執行

### 方法一：終端機

```bash
python stress_gui.py
```

### 方法二：VS Code 按 F5

1. 按 `Ctrl + Shift + P`，輸入 `Python: Select Interpreter`，選擇要使用的 Python
2. 按 **F5**

在「執行與偵錯」面板(`Ctrl + Shift + D`)上方可以切換：

| 選項 | 作用 |
|---|---|
| 執行壓力指數測試表 | 開啟測驗視窗(預設) |
| 執行目前開啟的檔案 | 執行目前正在編輯的檔案 |

### 打包成 exe

```bash
pyinstaller -F -w -n 壓力指數測試表 stress_gui.py
```

產出的執行檔在 `dist/` 資料夾。

---

## 使用方式

1. 開啟程式後，逐題點選「是」或「否」，上方進度條顯示已答題數
2. 按「**查看結果**」或直接按 Enter
3. 右側顯示「是」的數量、壓力等級與建議，評分標準中所屬等級會以粗體標示
4. 想重新測驗時按「**重新作答**」

---

## 常見問題

**Q：按「查看結果」出現「尚未完成」？**
A：還有題目沒作答，左側紅色題號就是未答的題目，作答後再按一次即可。

**Q：執行時出現 `No module named tkinter`？**
A：部分精簡版 Python 未附 tkinter，請改用 Anaconda 或從 python.org 下載的官方安裝版。

**Q：打包後的 exe 開啟時跳出黑色命令列視窗？**
A：打包時加上 `-w` 參數即可隱藏。

**Q：測驗結果可以當作診斷嗎？**
A：不行，本表僅供自我評估參考，如有身心不適請洽專業醫療人員。

---

## 檔案說明

```
stress-index-test/
├── stress_gui.py          # 視窗介面(主程式，執行這個)
├── stress_core.py         # 核心功能：題目、評分標準、計算結果
├── requirements.txt       # 打包需要的套件
└── .vscode/
    ├── launch.json        # VS Code 按 F5 的執行設定
    └── extensions.json    # 建議安裝的 VS Code 擴充功能
```
