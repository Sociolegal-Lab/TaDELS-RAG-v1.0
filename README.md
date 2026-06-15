# TaDELS-Bench

**Taiwan Discourse / Legal-document QA Benchmark** — 台灣法律文書問答評測。

你只要在**固定格式**下跑出預測，我們幫你跑評分。不需要你自己準備 ground truth、embedding 模型或評分程式。

- 📦 資料集（HuggingFace）：[`ncku-sclab/tadels-qa`](https://huggingface.co/datasets/ncku-sclab/tadels-qa) — subset `covid_19_discourse`
- 🏆 排行榜：見本 repo [`leaderboard.md`](leaderboard.md) 與線上 `/benchmark` 頁
- 📐 評分指標：Entity Matching Score、Unanswerable EM、Hallucination、nDCG@5

---

## 一、流程

```
①下載 test 題目 + 文件語料  →  ②跑你自己的 RAG / 模型
        →  ③產出 predictions_test.json（固定格式）
        →  ④投稿（網頁上傳 或 GitHub PR）  →  我們評分、上排行榜
```

## 二、拿資料

```python
from datasets import load_dataset

ds = load_dataset("ncku-sclab/tadels-qa", "covid_19_discourse")
test = ds["test"]          # 101 題；每筆有 question_id / question / type / entities(JSON 字串)
# 文件語料（你檢索的對象）在資料集的 covid_19_discourse/full_content/ 211 份判決書全文
```

> 註：這是榮譽制（open）benchmark，test 答案也公開，請自律不要直接抄答案。

## 三、固定預測格式

`predictions_test.json` 是一個 **JSON 陣列**，每筆對應一題：

```json
[
  {
    "question_id": "A_0001_0008_0165_S_1",
    "answer": "傳染病防治法第63條",
    "reference": ["A_0001_0008_0165", "A_0001_0008_0117"],
    "entities": {
      "LAW": ["傳染病防治法第63條"],
      "LAW_CLASSIFIED": [{"article": "傳染病防治法第63條", "role": "構成要件"}]
    }
  }
]
```

| 欄位 | 型別 | 說明 |
|---|---|---|
| `question_id` | str | **必填**，要對得上 test 題目 |
| `answer` | str | **必填**，你的答案；`unanswerable` 題請填「無法從文件判斷」 |
| `reference` | list[str] | 檢索回的 doc_id 排序（高→低），算 nDCG@5 用 |
| `entities` | dict | 抽取的法律實體（schema 見資料集 `entity_schema.json`）|

投稿前先自驗格式：

```bash
python validate_submission.py predictions_test.json
# 想同時檢查題目涵蓋率：
python validate_submission.py predictions_test.json --questions test_questions.json
```

## 四、投稿（兩種擇一）

**A. 網頁上傳（最快）** — 到實驗室 benchmark 頁 `https://handed-hesitate-rummage.ngrok-free.dev/benchmark`，登入後拖曳 `predictions_test.json`，當場出分數並進排行榜。

**B. GitHub PR** — 把檔案放到 `submissions/<自訂名稱>/predictions_test.json`（資料夾名稱可自由命名），開 PR。維護者合併後跑評分、更新 `leaderboard.md`。詳見 [`submissions/README.md`](submissions/README.md)。

## 五、評分指標

| 指標 | 說明 |
|---|---|
| **Entity Matching Score**（主分數）| 逐欄位比對結構化 entity（A 分類/B 短值/C 長文 embedding），entity 全失效時 fallback 比對整段答案 |
| **Unanswerable EM** | `unanswerable` 題是否正確回答「無法判斷」 |
| **Hallucination P_h / Rate** | 輸出了 GT 沒有、文件也不支持的 entity 之懲罰（越低越好）|
| **nDCG@5** | `reference` 檢索排序品質 |

完整定義見資料集的 `eval/EVAL_README.md`。

## 授權

- 資料集：CC-BY-4.0（見 HF）
- 本 repo 程式碼：MIT

維護：Sociolegal Lab, NCKU（`ncku-sclab`）
