# 壓力指數測試表

以 tkinter 製作的職場壓力自我評估小工具，回答 12 道題目後，依「是」的數量給出壓力程度與建議。

本專案為聯成電腦 Python 課程的練習作品。

題目與評分標準來源：[衛生福利部國民健康署 健康九九+網站 — 壓力指數測試](https://health99.hpa.gov.tw/health99/HC/D/115/StressIndex)

## 功能

- 12 道壓力評估題目，每題以「是／否」單選作答(預設為「是」)
- 提交後顯示評分標準說明
- 確認後統計「是」的數量，顯示壓力程度與建議：
  - 3 個以下：壓力還在能負荷的範圍
  - 4～5 個：需要認真學習壓力管理
  - 6～8 個：建議尋求心理衛生專業人員協助
  - 9 個以上：建議就醫，接受藥物與心理治療

## 安裝

只使用 Python 內建的 `tkinter`，不需安裝額外套件。

- Python 3.8 以上(Anaconda 或官方版皆可)
- 若要打包成 exe，再安裝 PyInstaller：

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## 執行

```bash
python 壓力指數測試表.py
```

在 VS Code 中也可直接按 F5，選擇「執行壓力指數測試表」。

### 打包成 exe

```bash
pyinstaller --onefile --noconsole 壓力指數測試表.py
```

產出的執行檔在 `dist/` 資料夾。

## 使用方式

1. 開啟程式後，逐題勾選「是」或「否」
2. 按「提交」，跳出評分標準說明視窗(視窗開啟時主視窗無法操作)
3. 按「確認」，關閉評分標準視窗，顯示您選擇的「是」數量與對應建議
4. 再按「確認」關閉程式

## 常見問題

**Q：執行時出現 `No module named tkinter`？**
A：部分精簡版 Python 未附 tkinter，請改用 Anaconda 或從 python.org 下載的官方安裝版。

**Q：打包後的 exe 開啟時跳出黑色命令列視窗？**
A：打包時加上 `--noconsole` 參數即可隱藏。

**Q：中文顯示成亂碼？**
A：請確認 `.py` 檔以 UTF-8 編碼儲存。

**Q：測驗結果可以當作診斷嗎？**
A：不行，本表僅供自我評估參考，如有身心不適請洽專業醫療人員。
