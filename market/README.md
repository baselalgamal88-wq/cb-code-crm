# Market brief data

The daily Egypt market brief, shown on the app's Today → Market brief page.

Briefs include notes from private WhatsApp groups, and this repository is public, so every
brief is **encrypted** before it is committed. Keys are not in this repository.

- `latest.bin`, `YYYY-MM-DD.bin`: the team brief. The key is in Firestore `settings/market`, which everyone signed in can read.
- `latest.mgr.bin`, `YYYY-MM-DD.mgr.bin`: the managers-only part, shown only to Basel. Use it for Leaders & Managers group items and commissions. The key is in Firestore `admin/market`, which only Basel can read.
- `index.json`: `{"dates": [...]}`, newest first (dates only), for the day picker.

To add a day:

    MARKET_KEY=<team key> python3 tools/market_encrypt.py team.json
    MARKET_MGR_KEY=<managers key> python3 tools/market_encrypt.py --managers managers.json

Then commit only the `market/` changes. Never commit the plain JSON.

JSON shape (both files): `{date, updated, en: {title, note, sections}, ar: {...}, sources: [{t, u}]}`.
Each section is `{h, bullets: [...]}`, `{h, text}` or `{h, table: {head, rows}, after?}`. Text may use `**bold**`.

## New (preferred): brief saved in Firestore, no keys needed

The daily run opens the app in Basel's signed-in browser and calls:

```js
await cbSaveBrief(team, managers)   // team = what agents see, managers = Basel only (or null)
```

- `team` goes to Firestore `settings/brief_<date>` (all signed-in team members can read it).
- `managers` goes to `admin/brief_<date>` (Basel only).
- `settings/brief_index` keeps the last 60 dates, newest first.

The Market page reads Firestore first and falls back to the encrypted files in this folder.
