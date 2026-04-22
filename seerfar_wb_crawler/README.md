# Seerfar WB Crawler

This tool helps Hermes collect authorized Wildberries (WB) data from Seerfar without using visual page analysis.

It uses this workflow:

1. Open Seerfar in Playwright and let the user log in manually.
2. Save the browser session locally.
3. Capture real API request templates while the user or Hermes clicks query buttons.
4. Reuse the saved session and request templates to export paginated data.
5. Write `data/latest.json`, `data/latest.csv`, and `reports/coverage.json`.

The tool does not bypass captcha, paywalls, account limits, or permission checks. It only reuses an authorized browser session.

## Install On Linux

```bash
cd seerfar_wb_crawler
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
python -m playwright install chromium
```

## First Login

```bash
python crawler.py login
```

A browser opens. Log in to Seerfar normally, then press Enter in the terminal. The login state is saved to:

```text
storage/seerfar_state.json
```

## Capture Real Request Templates

Run:

```bash
python crawler.py capture --seconds 180 --out config.yaml
```

In the opened browser, visit the important WB pages and click their query/search buttons:

- `https://seerfar.cn/admin/product-search.html`
- `https://seerfar.cn/admin/market.html`
- `https://seerfar.cn/admin/category-search.html`
- `https://seerfar.cn/admin/store-search.html`
- `https://seerfar.cn/admin/brand-search.html`
- `https://seerfar.cn/admin/keyword-detail.html`

The tool records matching XHR/fetch POST requests and writes a config file.

## Run Export

```bash
python crawler.py run --config config.yaml
```

Outputs:

```text
data/latest.json
data/latest.csv
reports/coverage.json
data/raw/
```

Hermes should read `reports/coverage.json` first. If the status is not `complete`, Hermes should report the missing data instead of calculating final conclusions.

## Useful Commands

```bash
python crawler.py status
python crawler.py run --config config.yaml --target product_wb_search
python crawler.py run --config config.yaml --max-pages 3
```

