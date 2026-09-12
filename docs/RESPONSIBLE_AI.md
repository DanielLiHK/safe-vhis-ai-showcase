# Responsible AI Record / 負責任 AI 紀錄

## Purpose and limits / 目的與限制

SafeVHIS evaluates whether source grounding and deterministic routing improve general VHIS explanations. It is a research showcase, not a consumer advice or decision system.

SafeVHIS 評估來源 grounding 及確定性分流能否改善一般 VHIS 解釋。佢係研究展示，並非消費者建議或決策系統。

| Allowed / 容許 | Prohibited / 禁止 |
|---|---|
| Explain supplied general source notes / 解釋已提供的一般來源筆記 | Decide claim eligibility or payment / 判斷索償資格或賠償 |
| Compare experimental controls / 比較實驗控制 | Recommend a product or insurer / 推薦產品或保險公司 |
| Detect unsupported citations / 偵測無支持引用 | Underwrite, price or profile a person / 核保、定價或評估個人 |
| Route uncertainty to a human / 把不確定情況轉介人手 | Process customer or health data / 處理客戶或健康資料 |

## Controls and evidence / 控制與證據

| Risk / 風險 | Control / 控制 | Evidence / 證據 |
|---|---|---|
| Hallucinated terms / 虛構條款 | Retrieved source allow-list and citation validation / 檢索來源 allow-list 及引用驗證 | Tests and aggregate results |
| Personalised decision / 個人化決定 | Deterministic `REFER_TO_HUMAN` routing / 確定性人手轉介 | Boundary cases |
| Ambiguity / 含糊問題 | `ASK_CLARIFICATION` before reliance / 依賴答案前先澄清 | Q07 and Q11 |
| Prompt injection / 提示注入 | Instruction hierarchy and fail-safe deferral / 指令層級及故障安全轉介 | Q10 |
| Personal-data exposure / 個人資料外洩 | Synthetic-only data and public-release scan / 只用 synthetic data 及發布掃描 | Dataset and manifest |
| Cherry-picking / 只揀成功案例 | Frozen cases and retained failures / 鎖定個案及保留失敗 | Methodology and failure cases |

## Human oversight / 人手監督

The study uses risk-based, proportionate human oversight. High-risk and boundary outputs were adjudicated individually; routine outputs were batch-reviewed under fixed criteria with material exceptions retained. The project owner remained human-in-command for scope, rejection, stopping and public disclosure. Automated metrics were not rewritten after outputs were seen.

研究採用風險為本、相稱的人手監督。高風險及邊界輸出逐項裁定；一般輸出按固定準則批次覆核，重大例外獨立保留。項目負責人在範圍、否決、停止及公開披露方面保持 human-in-command。睇到輸出後冇改寫自動指標。

This design is aligned with the risk-based terminology in the [PCPD Model Personal Data Protection Framework](https://www.pcpd.org.hk/english/resources_centre/publications/files/ai_protection_framework.pdf). Alignment is not regulatory approval or a legal conclusion.

設計用語對齊[私隱專員公署《人工智能：個人資料保障模範框架》](https://www.pcpd.org.hk/english/resources_centre/publications/files/ai_protection_framework.pdf)的風險為本概念，但不代表監管批准或法律結論。

## Limitations / 限制

- Twelve synthetic cases cannot establish production safety.
- The source set is deliberately narrow.
- Keyword routing can miss indirect personalisation or create false positives.
- Model behaviour can change after the recorded evaluation.
- Human grading contains judgment and has not been independently replicated.

- 12 條 synthetic 個案不足以證明 production 安全。
- 來源集合刻意收窄。
- 關鍵字分流可能漏掉間接個人化或產生 false positive。
- 模型行為可在評測後改變。
- 人手評分包含判斷，亦未經獨立重複驗證。
