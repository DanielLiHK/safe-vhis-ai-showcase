# SafeVHIS AI Showcase / 安心自願醫保 AI 研究展示

[English](#english) · [繁體中文](#繁體中文)

> A small, reproducible insurance-AI study demonstrating source grounding, deterministic guardrails and documented human oversight.  
> 一個細而完整、可重現的保險 AI 研究，展示來源 grounding、確定性 guardrails 及有紀錄的人手監督。

**Status / 狀態:** Public research showcase · Synthetic data only · Not insurance, legal, tax, financial or medical advice  
**狀態：** 公開研究展示 · 只用 synthetic data · 並非保險、法律、稅務、財務或醫療意見

## English

### Research question

Does combining official-source grounding with deterministic guardrails improve safe handling of general Hong Kong Voluntary Health Insurance Scheme (VHIS) questions?

### Design

The same 12 bilingual synthetic cases were tested on two authorised Qwen models under three conditions:

1. **Baseline** — model knowledge only.
2. **Grounded** — short paraphrased notes traceable to the official VHIS policy template.
3. **Guarded** — deterministic routing for ambiguous, personalised or adversarial requests; answerable cases also require valid retrieved source IDs.

No customer, policy, claim or health data was used. The system does not make coverage, claim, underwriting, tax or product-suitability decisions.

### Human-reviewed results

| Arm | Action accuracy | Citation support | Unsafe/unsupported claims | Usefulness (0–2) |
|---|---:|---:|---:|---:|
| Baseline | 54.2% | 12.5% | 21 | 0.88 |
| Grounded | 70.8% | 95.8% | 1 | 1.67 |
| Guarded | **100%** | **100%** | **0** | **2.00** |

All 72 outputs were human-reviewed. High-risk cases were adjudicated individually; routine cases used a defined risk-tiered batch review with material exceptions retained separately. These results apply only to this small frozen synthetic benchmark and do not prove production safety or regulatory compliance.

## 繁體中文

### 研究問題

把官方來源 grounding 與確定性 guardrails 結合，能否更安全處理香港自願醫保（VHIS）的一般問題？

### 設計

同一批 12 條中英雙語 synthetic 個案，以兩個已授權 Qwen 模型比較三種條件：

1. **Baseline（基準）** — 只用模型本身知識。
2. **Grounded（有來源）** — 使用可追溯至官方 VHIS 保單範本的改寫筆記。
3. **Guarded（有護欄）** — 含糊、個人化或對抗性要求由確定性規則分流；可回答個案亦必須使用有效檢索來源 ID。

研究冇使用客戶、保單、索償或健康資料。系統不會作保障、索償、核保、稅務或產品合適性決定。

### 人手覆核結果

| 組別 | 行動正確率 | 引用支持率 | 不安全／無支持聲稱 | 實用性（0–2） |
|---|---:|---:|---:|---:|
| Baseline | 54.2% | 12.5% | 21 | 0.88 |
| Grounded | 70.8% | 95.8% | 1 | 1.67 |
| Guarded | **100%** | **100%** | **0** | **2.00** |

全部 72 個輸出均經人手覆核。高風險案例逐項裁定；一般案例按已定義的分級風險批次覆核，重大例外則獨立保留。結果只適用於本次小型、鎖定的 synthetic benchmark，不能證明 production 安全或監管合規。

## Evidence map / 證據索引

- [Methodology / 研究方法](docs/METHODOLOGY.md)
- [Responsible AI / 負責任 AI](docs/RESPONSIBLE_AI.md)
- [Human Oversight Summary / 人手監督摘要](docs/HUMAN_OVERSIGHT_SUMMARY.md)
- [Human Evaluation / 人手評估](results/HUMAN_EVALUATION.md)
- [Failure Cases / 失敗案例](docs/FAILURE_CASES.md)
- [Source Provenance / 來源追溯](docs/SOURCE_PROVENANCE.md)
- [Bilingual Coverage / 雙語覆蓋](docs/BILINGUAL_COVERAGE.md)
- [Publication Scope / 發布範圍](PUBLICATION_SCOPE.md)

## Reproduce / 重現

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e '.[dev]'
pytest
safe-vhis dry-run --case Q06 --arm guarded
```

API execution is optional. Never commit a real key; use a local environment variable if independently reproducing provider calls.

API 執行並非必要。切勿 commit 真實 key；如自行重現 provider calls，只可使用本機環境變數。

## Licence / 授權

This repository is source-available for portfolio and research-evaluation viewing. It is not open source. See [LICENSE.md](LICENSE.md).

本 repository 只供作品集及研究評審查看，並非開源。詳見 [LICENSE.md](LICENSE.md)。
