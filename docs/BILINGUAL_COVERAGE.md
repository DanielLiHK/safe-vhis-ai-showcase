# Bilingual Coverage / 雙語覆蓋

## Publication rule / 發布規則

All human-facing explanations in this showcase must be available in English and Traditional Chinese. Bilingual parity means that the material meaning, limitations and evidence are present in both languages; it does not require word-for-word translation.

本 showcase 所有人類可讀解釋均須提供英文及繁體中文。雙語對等係指兩種語言都包含實質意思、限制及證據，並不要求逐字翻譯。

## Audited surfaces / 已審核範圍

| Surface / 範圍 | Bilingual evidence / 雙語證據 | Status / 狀態 |
|---|---|---|
| Repository overview / Repository 概覽 | Research question, design, results, limits and reproduction guidance / 研究問題、設計、結果、限制及重現指引 | Verified / 已核實 |
| Methodology / 研究方法 | Hypotheses, experiment settings, case categories, metrics, procedure and interpretation boundary / 假設、實驗設定、個案分類、指標、程序及結論界線 | Verified / 已核實 |
| Responsible AI / 負責任 AI | Purpose, prohibited uses, controls, evidence, human oversight and limitations / 目的、禁止用途、控制、證據、人手監督及限制 | Verified / 已核實 |
| Human oversight / 人手監督 | Operating model, human-in-the-loop, human-in-command, review tiers and data minimisation / 運作模式、人在迴路、人類主導、覆核分級及資料最少化 | Verified / 已核實 |
| Evaluation and failures / 評估及失敗 | Table headings, findings, case names, severity, failure descriptions and control lessons / 表格欄名、結論、案例名稱、嚴重程度、失敗描述及控制啟示 | Verified / 已核實 |
| Source and publication governance / 來源及發布治理 | Provenance, scope, security and licence / 來源追溯、範圍、安全及授權 | Verified / 已核實 |
| Structured research data / 結構化研究數據 | Questions, gold points, source titles, publisher, notes, sections and source text / 問題、標準要點、來源名稱、發布者、筆記、章節及來源文字 | Verified / 已核實 |
| Command-line and automation labels / 指令列及自動化標籤 | CLI descriptions, package description, workflow, job and step names / CLI 說明、package 說明、workflow、job 及 step 名稱 | Verified / 已核實 |

## Deliberate technical exceptions / 刻意保留的技術例外

Programming identifiers, JSON keys, command names, model IDs, source IDs, action enums, file paths, hashes, code, shell commands and numeric results remain language-neutral or retain their canonical spelling. Internal exception messages are developer diagnostics rather than the public explanatory record.

程式識別字、JSON keys、command 名稱、model ID、source ID、action enums、檔案路徑、hash、程式碼、shell 指令及數字結果屬語言中立，或須保留 canonical 寫法。內部 exception message 屬開發診斷，並非公開解釋紀錄。

## Verification / 驗證

The release validator checks every required human-facing document, required translation markers, paired English/Chinese fields in the research JSON, and bilingual CLI, workflow and package metadata. Manual paragraph-and-table review remains part of the release gate because automated language detection cannot prove semantic equivalence.

發布 validator 會檢查所有必要人類可讀文件、指定翻譯標記、研究 JSON 的中英文配對欄位，以及雙語 CLI、workflow 及 package metadata。由於自動語言偵測不能證明語義完全對等，逐段及逐表人手覆核仍然係發布關卡之一。

**Last full audit / 最近一次全面審核：2026-09-12**
