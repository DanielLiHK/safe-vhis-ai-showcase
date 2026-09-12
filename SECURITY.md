# Security / 安全

## Secrets / 機密資料

Never commit API keys, workspace credentials or real `.env` files. Use local environment variables or GitHub Actions secrets. If exposure is suspected, revoke and rotate the credential immediately and inspect repository history and workflow logs.

切勿 commit API key、workspace 憑證或真實 `.env`。只可使用本機環境變數或 GitHub Actions secrets。如懷疑外洩，應立即撤銷及更換憑證，並檢查 repository history 及 workflow logs。

## Data boundary / 數據界線

Only synthetic questions are permitted. Do not enter customer names, identity numbers, medical records, policy numbers, claim details or other personal data.

只准使用 synthetic 問題。不可輸入客戶姓名、身份證號碼、醫療紀錄、保單號碼、索償資料或其他個人資料。

## Reporting / 報告問題

Do not place secrets or personal data in a public issue. Contact the repository owner privately and rotate any affected credential first.

切勿在公開 issue 貼出 secret 或個人資料。請私下聯絡 repository owner，並優先更換受影響憑證。
