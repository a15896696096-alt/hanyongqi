# Instructions For Hermes

When the user says that Seerfar data is needed, use this crawler instead of visually browsing the Seerfar pages.

## Linux Runtime Note

The crawler is a Python 3 + Playwright tool. Install dependencies with:

```bash
pip install -r requirements.txt
python -m playwright install --with-deps chromium
```

The `login` and `capture` commands need a visible browser. If the Linux environment has no GUI, ask the user to run these commands in a desktop/VNC session or with a virtual display. After `storage/seerfar_state.json` and `config.yaml` exist, normal `run` exports can run headlessly.

## Standard Workflow

1. Go to the crawler directory:

```bash
cd seerfar_wb_crawler
```

2. Check whether login state exists:

```bash
python crawler.py status
```

3. If login state is missing or expired, ask the user to run:

```bash
python crawler.py login
```

4. If `config.yaml` does not exist or the needed API target is missing, run:

```bash
python crawler.py capture --seconds 180 --out config.yaml
```

During capture, open the required Seerfar page and click the query/search buttons so the crawler can record the real API request body.

5. Export data:

```bash
python crawler.py run --config config.yaml
```

6. Always read this file first:

```text
reports/coverage.json
```

If `status` is not `complete`, do not produce final business conclusions. Report which required targets failed or are missing.

7. If coverage is complete, read:

```text
data/latest.json
```

Use that data for analysis, summary, comparison, and calculation.

## Important Rule

Do not output account passwords, full cookies, full tokens, or full Authorization headers.

## Recommended First Targets

- `product_wb_search`
- `keyword_market_wb`
- `category_search_wb`
- `shop_hot_wb`
- `brand_hot_wb`
- `keyword_shop_or_brand_wb`
