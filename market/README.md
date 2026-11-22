# Market brief data

The daily Egypt market brief, shown on the app's Today → Market brief page.

- `latest.json`: today's brief (the app opens this).
- `YYYY-MM-DD.json`: one file per day, same shape.
- `index.json`: `{"dates": [...]}`, newest first, so the app can show earlier days.

Shape: `{date, updated, en: {title, note, sections}, ar: {...}, sources: [{t, u}]}`.
Each section is `{h, bullets: [...]}` or `{h, text}` or `{h, table: {head, rows}, after?}`. Text may use `**bold**`.
Only public web information goes here: this repository is public.
