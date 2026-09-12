# Human Evaluation / 人手評估

> **Complete / 已完成:** 72/72 outputs reviewed / 72/72 個輸出已覆核 · Two models / 兩個模型 · Three control arms / 三個控制組別 · Twelve bilingual synthetic cases / 12 個中英雙語合成案例

## Aggregate result / 匯總結果

| Arm / 組別 | Human action accuracy / 人手行動準確度 | Citation support / 引用支持率 | Unsafe or unsupported claims / 不安全或無支持聲明 | Mean usefulness / 平均實用性（0–2） |
|---|---:|---:|---:|---:|
| Baseline | 13/24 (54.2%) | 3/24 (12.5%) | 21 | 0.88 |
| Grounded | 17/24 (70.8%) | 23/24 (95.8%) | 1 | 1.67 |
| Guarded | **24/24 (100%)** | **24/24 (100%)** | **0** | **2.00** |

## Model detail / 模型詳情

| Model / 模型 | Arm / 組別 | Action accuracy / 行動準確度 | Citation support / 引用支持率 | Unsafe claims / 不安全聲明 | Mean usefulness / 平均實用性 |
|---|---|---:|---:|---:|---:|
| Qwen3.8-Flash | Baseline | 50.0% | 8.3% | 11 | 0.83 |
| Qwen3.8-Flash | Grounded | 83.3% | 91.7% | 1 | 1.75 |
| Qwen3.8-Flash | Guarded | 100.0% | 100.0% | 0 | 2.00 |
| Qwen3.7-Plus | Baseline | 58.3% | 16.7% | 10 | 0.92 |
| Qwen3.7-Plus | Grounded | 58.3% | 100.0% | 0 | 1.58 |
| Qwen3.7-Plus | Guarded | 100.0% | 100.0% | 0 | 2.00 |

## Findings / 結論

1. Grounding materially improved citation support but did not by itself solve routing. / Grounding 明顯改善引用支持，但單靠 grounding 未能解決路由。
2. Guarded performed best on this frozen sample by combining source support with deterministic clarification and referral. / Guarded 結合來源支持與確定性澄清／轉介，在本次鎖定樣本表現最佳。
3. Structured action and answer text need separate review: an `ANSWER` label may contain refusal text and remain a schema failure. / 結構化 action 與答案文字要分開覆核：標示 `ANSWER` 的輸出可能實際拒答，但仍屬 schema failure。
4. Supported facts do not replace clarification when a question is ambiguous or over-broad. / 問題含糊或過度廣泛時，有來源事實唔可以取代澄清。

## Limit / 限制

This small, single-run synthetic study does not prove production safety, legal compliance or performance on other documents, models or dates. Human judgments have not been independently replicated.

本次小型、單次 synthetic 研究不能證明 production 安全、法律合規，亦不代表其他文件、模型或日期的表現。人手判斷尚未經獨立重複驗證。
