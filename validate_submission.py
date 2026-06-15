#!/usr/bin/env python3
"""
TaDELS-Bench 投稿格式自驗工具（純標準庫，無相依）。

用法：
    python validate_submission.py predictions_test.json
    python validate_submission.py predictions_test.json --questions test_questions.json

檢查：
  - 最外層為 JSON 陣列
  - 每筆有 question_id (str) / answer (str)
  - reference 若有，須為 list[str]；entities 若有，須為 dict
  - question_id 無重複
  - （可選）對照題目檔，回報缺漏 / 多餘的 question_id
"""
import argparse
import json
import sys


def load_question_ids(path):
    """從題目檔讀出 question_id 集合。支援兩種結構：
    1) [{"question_id": ...}, ...]
    2) [{"qa_pairs": [{"question_id": ...}, ...]}, ...]（原始 GT 結構）
    """
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    ids = set()
    if isinstance(data, list):
        for item in data:
            if not isinstance(item, dict):
                continue
            if "question_id" in item:
                ids.add(item["question_id"])
            for qa in item.get("qa_pairs", []) or []:
                if isinstance(qa, dict) and "question_id" in qa:
                    ids.add(qa["question_id"])
    return ids


def validate(preds):
    errors = []
    if not isinstance(preds, list):
        return ["最外層必須是 JSON 陣列 (list of objects)"], set()
    if not preds:
        return ["預測為空，至少要有一筆"], set()

    seen = set()
    qids = set()
    for i, p in enumerate(preds):
        if not isinstance(p, dict):
            errors.append(f"第 {i} 筆不是物件 (object)")
            continue
        qid = p.get("question_id")
        if not qid or not isinstance(qid, str):
            errors.append(f"第 {i} 筆缺 question_id 或型別不對 (須為非空字串)")
        else:
            if qid in seen:
                errors.append(f"question_id 重複：{qid}")
            seen.add(qid)
            qids.add(qid)
        if "answer" not in p:
            errors.append(f"第 {i} 筆 ({qid}) 缺 answer")
        elif not isinstance(p["answer"], str):
            errors.append(f"第 {i} 筆 ({qid}) answer 須為字串")
        if "reference" in p and not isinstance(p["reference"], list):
            errors.append(f"第 {i} 筆 ({qid}) reference 須為陣列 (list of doc_id)")
        if "entities" in p and not isinstance(p["entities"], dict):
            errors.append(f"第 {i} 筆 ({qid}) entities 須為物件 (dict)")
    return errors, qids


def main():
    ap = argparse.ArgumentParser(description="TaDELS-Bench 投稿格式自驗")
    ap.add_argument("predictions", help="predictions_test.json 路徑")
    ap.add_argument("--questions", help="（可選）test 題目檔，用來檢查涵蓋率")
    args = ap.parse_args()

    try:
        with open(args.predictions, encoding="utf-8") as f:
            preds = json.load(f)
    except Exception as e:
        print(f"✗ 無法讀取/解析 JSON：{e}")
        sys.exit(1)

    errors, pred_ids = validate(preds)

    if args.questions:
        try:
            gold = load_question_ids(args.questions)
        except Exception as e:
            print(f"⚠ 無法讀取題目檔：{e}")
            gold = set()
        if gold:
            missing = gold - pred_ids
            extra = pred_ids - gold
            if missing:
                errors.append(f"缺 {len(missing)} 題未作答，例：{sorted(missing)[:5]}")
            if extra:
                errors.append(f"有 {len(extra)} 個 question_id 不在題目中，例：{sorted(extra)[:5]}")

    if errors:
        print(f"✗ 格式檢查未通過（{len(errors)} 項問題）：")
        for e in errors[:30]:
            print("  -", e)
        if len(errors) > 30:
            print(f"  …（其餘 {len(errors) - 30} 項略）")
        sys.exit(1)

    print(f"✓ 格式 OK：{len(preds)} 筆，{len(pred_ids)} 個唯一 question_id")
    sys.exit(0)


if __name__ == "__main__":
    main()
