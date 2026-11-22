# Market brief data

The daily Egypt market brief, shown on the app's Today → Market brief page.

The brief can include notes from private WhatsApp groups, and this repository is public, so every
brief is **encrypted** before it is committed. The key is not in this repository: the app reads it
from Firestore (`settings/market`), which only signed-in team members can read.

- `latest.bin`: today's brief (the app opens this).
- `YYYY-MM-DD.bin`: one file per day.
- `index.json`: `{"dates": [...]}`, newest first (dates only), for the day picker.

To add a day: write the brief as JSON, then run
`MARKET_KEY=<key> python3 tools/market_encrypt.py brief.json` and commit the `market/` changes.
Never commit the plain JSON.

JSON shape: `{date, updated, en: {title, note, sections}, ar: {...}, sources: [{t, u}]}`.
Each section is `{h, bullets: [...]}` or `{h, text}` or `{h, table: {head, rows}, after?}`. Text may use `**bold**`.
