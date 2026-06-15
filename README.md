<h1 align="center">TaDELs-RAG 資料集：實體導向之臺灣法律檢索增強生成評估資料集</h1>

<p align="center">
  <a href="https://huggingface.co/datasets/ncku-sclab/tadels-qa">
    <img src="https://img.shields.io/badge/%E8%B3%87%E6%96%99%E9%9B%86-Hugging%20Face-yellow" alt="資料集">
  </a>
  <a href="https://handed-hesitate-rummage.ngrok-free.dev/benchmark">
    <img src="https://img.shields.io/badge/%E6%B8%AC%E8%A9%A6%E7%B5%90%E6%9E%9C%E4%B8%8A%E5%82%B3-Upload-blue" alt="測試結果上傳">
  </a>
  <a href="https://tadels.law.ncku.edu.tw/">
    <img src="https://img.shields.io/badge/TaDELS-%E5%AE%98%E7%B6%B2-green" alt="TaDELS">
  </a>
</p>

---

## 概述

TaDELs-RAG 資料集是針對臺灣法律文書問答所建立的檢索增強生成（Retrieval-Augmented Generation, RAG）評量資料集。評分以法律實體為核心，檢驗系統回答是否能正確對應原始司法文書中的案號、當事人、法條、裁判結果、行為事實與裁判理由等關鍵資訊。

首版 v1.0 以 COVID-19 疫情期間不實訊息相關司法文書為範圍，收錄 211 篇法律文書與 648 題問答，並提供 7 大類、54 欄位的法律實體標註架構；7 大類包括案件基本資訊、構成要件、罪名競合、民事侵權、程序歷程、前案資訊與援引法源。

本研究將法律 RAG 系統的評分分為檢索品質與生成品質：檢索品質檢查系統是否找到正確來源，生成品質檢查答案中的法律實體是否正確、是否能拒答不可回答題，以及是否產生無依據或與原文矛盾的資訊。

本資料集取自「法實證法律文件資料庫」（Taiwan Database for Empirical Legal Studies, TaDELS）：[https://itdels.digital.ntu.edu.tw/index.php](https://itdels.digital.ntu.edu.tw/index.php)。

## 資料集內容

| 項目         | 內容                                                                                                                                                                     |
| ------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| 文件範圍     | COVID-19 疫情期間不實訊息相關司法文書，共 211 篇；文書類型包含裁定、刑事判決、簡易判決、起訴書、聲請簡易判決處刑書與小額民事判決等                                       |
| 問答題數     | 共 648 題；題型包含短答題、長答題與不可回答題                                                                                                                            |
| 法律實體標註 | 共 7 大類、54 欄位；完整欄位請見 [資料集頁面中的 `entity_schema.csv`](https://huggingface.co/datasets/ncku-sclab/tadels-qa/blob/main/covid_19_discourse/entity_schema.csv) |
| 資料語言     | 繁體中文                                                                                                                                                                 |

資料以文件為單位切分；同一篇司法文書所對應的題目只會出現在同一個 split，以避免訓練、驗證與計分資料互相重疊。

| Split      | 總題數 | 短答題數 | 長答題數 | 不可回答題數 | 用途                               |
| ---------- | -----: | -------: | -------: | -----------: | ---------------------------------- |
| train      |    446 |      146 |      155 |          145 | 供模型開發、提示設計或系統調整使用 |
| validation |    101 |       34 |       34 |           33 | 供開發階段驗證系統表現使用         |
| test       |    101 |       34 |       34 |           33 | 供模型最終測試與結果比較使用       |
| total      |    648 |      214 |      223 |          211 | 全部問答資料合計                   |

## 法律實體標註架構

法律實體是本資料集用來評估生成答案的核心單位。每個欄位皆定義中文名稱、英文標籤、資料型態、欄位說明、範例、類別與評估類型；完整欄位請見 [資料集頁面中的 `entity_schema.csv`](https://huggingface.co/datasets/ncku-sclab/tadels-qa/blob/main/covid_19_discourse/entity_schema.csv)；機器可讀版本另見 [`entity_schema.json`](https://huggingface.co/datasets/ncku-sclab/tadels-qa/blob/main/covid_19_discourse/entity_schema.json)。

| 類別         | 欄位數 | 說明                                                                                                                                                   |
| ------------ | -----: | ------------------------------------------------------------------------------------------------------------------------------------------------------ |
| 案件基本資訊 |     29 | 記錄文書與案件的基本資料，例如文書類型、裁判機關、案號、當事人、法官、檢察官、適用法條、行為時間、傳播平台、不實訊息內容、裁判結果、處罰內容與裁判理由 |
| 構成要件     |      8 | 記錄法院或檢察機關對犯罪構成要件的判斷，例如訊息是否不實、是否足生公共危害、是否具故意，以及新舊法比較結果                                             |
| 罪名競合     |      5 | 記錄同一事實可能涉及的其他罪名或法律評價，例如誹謗、恐嚇公眾、個人資料保護法非法利用與競合類型                                                         |
| 民事侵權     |      6 | 記錄民事案件中的侵權行為判斷，例如侵權行為類型、名譽損害、被告抗辯、損害賠償與訴訟費用                                                                 |
| 程序歷程     |      3 | 記錄案件所處程序階段，以及同一案件前後階段文書之間的關聯                                                                                               |
| 前案資訊     |      2 | 記錄被告是否有前科或累犯，以及法院是否因此加重處罰                                                                                                     |
| 援引法源     |      1 | 記錄文書中援引的大法官解釋、最高法院判決或判例、上級審判決等法源                                                                                       |

## 評分機制

TaDELs-RAG 資料集的評分分為「檢索品質」與「生成品質」兩部分。檢索品質衡量系統是否找回可支持答案的法律文書；生成品質衡量系統答案是否正確、完整，並忠實於原始文書。

### 檢索品質

| 指標                                  | 適用題型                   | 指標說明                                                                                                                     |
| ------------------------------------- | -------------------------- | ---------------------------------------------------------------------------------------------------------------------------- |
| 前五名正規化折扣累積增益（nDCG@5） | 短答題、長答題、不可回答題 | 衡量系統回傳的前五篇文書是否包含標準答案來源或同案件關聯文書，且相關文書是否排序在前；分數越高，表示檢索結果越能支持後續作答 |

### 生成品質

本研究採實體導向評估，參考資訊檢索與問答評估中的 nugget-based evaluation（資訊單元評估）概念，將完整答案拆成可檢查的資訊單元。於本資料集中，資訊單元具體化為法律實體欄位；短答題與長答題以 Entity Matching Score 評估，不可回答題以 Exact Match 評估，並另計幻覺相關指標。

對可回答題，本資料集重點檢查答案中的法律實體是否正確；對不可回答題，則檢查系統是否能在文件不足時正確拒答。總分（Total）用來彙整不同題型的生成品質，各項指標如下：

| 指標                                  | 適用題型                   | 指標說明                                                                                                 |
| ------------------------------------- | -------------------------- | -------------------------------------------------------------------------------------------------------- |
| 總分（Total）                         | 短答題、長答題、不可回答題 | 整合不同題型的生成品質分數；短答題與長答題採實體比對分數，不可回答題採完全比對分數，再依題型題數加權平均 |
| 實體比對分數（Entity Matching Score） | 短答題、長答題             | 逐項比對系統答案中的法律實體與標準答案，分數越高表示關鍵法律資訊越正確                                   |
| 完全比對（Exact Match）               | 不可回答題                 | 系統必須正確表示「無法從文件判斷」才得分，用以評估系統是否能在資料不足時拒答                             |
| 答案後備（Answer Fallback）           | 短答題、長答題             | 當法律實體比對未命中時，改以完整答案文字進行後備比對，避免內容正確但未結構化抽取的答案被完全低估         |
| 幻覺懲罰（Hallucination Penalty）     | 短答題、長答題             | 對無原文依據或與原文矛盾的額外法律實體給予懲罰，單題懲罰設有上限                                         |
| 幻覺率（Hallucination Rate）          | 短答題、長答題             | 無原文依據或與原文矛盾的法律實體，占系統輸出法律實體總數的比例；數值越低，表示答案越忠實於原始文書       |

實體比對依欄位性質採三種方式。分類欄位採標籤完全比對；短值欄位採標準化後的完全比對、包含比對或清單 F1；長文欄位採語意向量餘弦相似度。欄位所屬的評估類型請見資料集頁面中的 [`entity_schema.csv`](https://huggingface.co/datasets/ncku-sclab/tadels-qa/blob/main/covid_19_discourse/entity_schema.csv) 的 `評估類型` 欄。

## 使用與測試結果上傳

### 取得資料

資料集公開頁面：[https://huggingface.co/datasets/ncku-sclab/tadels-qa](https://huggingface.co/datasets/ncku-sclab/tadels-qa)。使用 `datasets` 套件時，請指定 `covid_19_discourse` subset。

```python
from datasets import load_dataset

ds = load_dataset("ncku-sclab/tadels-qa", "covid_19_discourse")
train = ds["train"]
validation = ds["validation"]
test = ds["test"]
```

211 篇司法文書全文是檢索系統應查找的語料，位於資料集的 `covid_19_discourse/full_content/`。本資料集採開放式評分設計：test split 的標準答案隨資料集公開，以利檢查、重現與方法比較；上傳結果時請勿直接複製標準答案作為系統輸出。

### 測試結果格式

預測檔為 JSON 陣列；每一筆對應 test split 的一道題目。範例見 [`format/predictions.example.json`](format/predictions.example.json)。

```json
[
  {
    "question_id": "A_0001_0008_0165_S_1",
    "answer": "傳染病防治法第63條",
    "reference": ["A_0001_0008_0165", "A_0001_0008_0117"],
    "entities": {
      "LAW": ["傳染病防治法第63條"],
      "LAW_CLASSIFIED": [
        {"article": "傳染病防治法第63條", "role": "構成要件"}
      ]
    }
  }
]
```

| 欄位            | 必填 | 型別     | 說明                                                                                                                                                                       |
| --------------- | ---- | -------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `question_id` | 是   | string   | test split 中的題目編號；每題須提供一筆，且不可重複                                                                                                                      |
| `answer`      | 是   | string   | 系統產生的自然語言答案；不可回答題應明確表示「無法從文件判斷」                                                                                                             |
| `reference`   | 否   | string[] | 系統檢索回傳的文件編號，須依相關性由高至低排序；此欄位用於計算 nDCG@5                                                                                                      |
| `entities`    | 否   | object   | 系統從答案中抽取的法律實體；鍵名應使用[`entity_schema.csv`](https://huggingface.co/datasets/ncku-sclab/tadels-qa/blob/main/covid_19_discourse/entity_schema.csv) 的英文標籤 |

上傳前可先執行格式檢查：

```bash
python validate_submission.py predictions_test.json
```

### 測試結果上傳

請至線上頁面上傳 `predictions_test.json`：[https://handed-hesitate-rummage.ngrok-free.dev/benchmark](https://handed-hesitate-rummage.ngrok-free.dev/benchmark)。系統會檢查格式、計算分數，並於頁面顯示結果。
