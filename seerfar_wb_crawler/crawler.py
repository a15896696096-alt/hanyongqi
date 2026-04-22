#!/usr/bin/env python3
import argparse
import asyncio
import csv
import copy
import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional
from urllib.parse import urljoin, urlparse

import yaml
from playwright.async_api import async_playwright


DEFAULT_BASE_URL = "https://www.seerfar.cn"
DEFAULT_ADMIN_URL = "https://seerfar.cn/admin/index.html"
DEFAULT_LOGIN_URL = "https://seerfar.cn/admin/sign-in.html"
DEFAULT_STORAGE_STATE = "storage/seerfar_state.json"

CORE_PATHS = {
    "/product-report/product/wb/search": {
        "name": "product_wb_search",
        "page": "热销榜单选品",
        "required": True,
    },
    "/keyword-report/market/search/WB": {
        "name": "keyword_market_wb",
        "page": "市场热词选品",
        "required": True,
    },
    "/product-report/category/search/WB": {
        "name": "category_search_wb",
        "page": "热销类目选品",
        "required": True,
    },
    "/product-report/wb/shop/hot/report": {
        "name": "shop_hot_wb",
        "page": "热销店铺选品",
        "required": True,
    },
    "/product-report/wb/brand/hot/report": {
        "name": "brand_hot_wb",
        "page": "热销品牌选品",
        "required": True,
    },
    "/product-report/keyword/detail/shopOrBrand/search/wb": {
        "name": "keyword_shop_or_brand_wb",
        "page": "关键词详情-店铺/品牌",
        "required": False,
    },
}

INTERESTING_KEYWORDS = (
    "product-report",
    "keyword-report",
    "product-search",
    "product-detail",
    "category",
    "keyword",
    "store",
    "seller",
    "brand",
    "trend",
    "sales",
    "hotSales",
    "tracker",
    "dashboard",
    "analysis",
    "rank",
    "sku",
)


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def load_yaml(path: Path) -> Dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(f"Config not found: {path}")
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def write_yaml(path: Path, data: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        yaml.safe_dump(data, f, allow_unicode=True, sort_keys=False)


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def read_json_maybe(value: Optional[str]) -> Any:
    if not value:
        return None
    try:
        return json.loads(value)
    except json.JSONDecodeError:
        return None


def ensure_page_body(body: Dict[str, Any], page_number: int, page_size: int) -> Dict[str, Any]:
    cloned = copy.deepcopy(body or {})
    page = cloned.get("page")
    if not isinstance(page, dict):
        page = {}
        cloned["page"] = page
    page["pageNumber"] = page_number
    page["pageSize"] = page_size
    page.setdefault("orders", [])
    return cloned


def records_from_payload(payload: Any) -> List[Dict[str, Any]]:
    if not isinstance(payload, dict):
        return []
    data = payload.get("data")
    if isinstance(data, dict):
        records = data.get("records")
        if isinstance(records, list):
            return [r if isinstance(r, dict) else {"value": r} for r in records]
        for key in ("list", "rows", "items"):
            value = data.get(key)
            if isinstance(value, list):
                return [r if isinstance(r, dict) else {"value": r} for r in value]
    if isinstance(data, list):
        return [r if isinstance(r, dict) else {"value": r} for r in data]
    return []


def page_info_from_payload(payload: Any) -> Dict[str, Any]:
    data = payload.get("data") if isinstance(payload, dict) else None
    if not isinstance(data, dict):
        return {"totalPages": 1, "total": None, "current": None, "size": None}
    return {
        "totalPages": data.get("totalPages") or data.get("pages") or 1,
        "total": data.get("total"),
        "current": data.get("current"),
        "size": data.get("size"),
        "currentSize": data.get("currentSize"),
        "timeInterval": data.get("timeInterval"),
    }


def flatten(prefix: str, value: Any, row: Dict[str, Any]) -> None:
    if isinstance(value, dict):
        for key, child in value.items():
            next_prefix = f"{prefix}.{key}" if prefix else str(key)
            flatten(next_prefix, child, row)
    elif isinstance(value, list):
        row[prefix] = json.dumps(value, ensure_ascii=False)
    else:
        row[prefix] = value


def write_csv(path: Path, rows: List[Dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    flattened: List[Dict[str, Any]] = []
    fieldnames = set()
    for row in rows:
        flat: Dict[str, Any] = {}
        flatten("", row, flat)
        flattened.append(flat)
        fieldnames.update(flat.keys())
    ordered = ["target", "target_page"] + sorted(k for k in fieldnames if k not in {"target", "target_page"})
    with path.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=ordered, extrasaction="ignore")
        writer.writeheader()
        for row in flattened:
            writer.writerow(row)


def storage_path(config: Dict[str, Any]) -> Path:
    return Path(config.get("storage_state") or DEFAULT_STORAGE_STATE)


def build_full_url(base_url: str, path: str) -> str:
    if path.startswith("http://") or path.startswith("https://"):
        return path
    return urljoin(base_url.rstrip("/") + "/", path.lstrip("/"))


async def browser_context(playwright, config: Dict[str, Any], headless: bool):
    browser = await playwright.chromium.launch(headless=headless)
    state_path = storage_path(config)
    kwargs: Dict[str, Any] = {}
    if state_path.exists():
        kwargs["storage_state"] = str(state_path)
    context = await browser.new_context(**kwargs)
    return browser, context


async def get_auth_headers(page, config: Dict[str, Any]) -> Dict[str, str]:
    values = await page.evaluate(
        """() => {
            const safeDecode = (value) => {
              try { return decodeURIComponent(value); } catch (e) {}
              try { return unescape(value); } catch (e) {}
              return value;
            };
            const cookieObj = {};
            document.cookie.split(';').map(v => v.trim()).filter(Boolean).forEach(item => {
              const idx = item.indexOf('=');
              if (idx >= 0) cookieObj[item.slice(0, idx)] = safeDecode(item.slice(idx + 1));
            });
            return {
              localUserInfo: localStorage.getItem('userInfo'),
              localFingerprint: localStorage.getItem('fingerprint'),
              cookieUserInfo: cookieObj.userInfo || '',
              cookieToken: cookieObj.sa_token || '',
              lang: cookieObj.sf_lang || ''
            };
        }"""
    )
    local_user = read_json_maybe(values.get("localUserInfo"))
    cookie_user = read_json_maybe(values.get("cookieUserInfo"))
    fingerprint = read_json_maybe(values.get("localFingerprint"))

    token = values.get("cookieToken") or ""
    for candidate in (local_user, cookie_user):
        if isinstance(candidate, dict):
            token = token or candidate.get("token") or candidate.get("accessToken") or candidate.get("authorization") or ""

    visitor_id = ""
    if isinstance(fingerprint, dict):
        visitor_id = fingerprint.get("visitorId") or ""

    lang_map = {"zh": "zh-CN", "en": "en-US", "ru": "ru-RU"}
    client_language = config.get("client_language") or lang_map.get(values.get("lang"), "zh-CN")

    headers = {
        "Accept": "application/json, text/plain, */*",
        "Content-Type": "application/json",
        "Client-Language": client_language,
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"
    if visitor_id:
        headers["visitorId"] = visitor_id
    return headers


async def command_login(args) -> int:
    config = load_yaml(Path(args.config)) if args.config else {}
    login_url = config.get("login_url") or DEFAULT_LOGIN_URL
    state_path = storage_path(config)
    state_path.parent.mkdir(parents=True, exist_ok=True)

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()
        await page.goto(login_url, wait_until="domcontentloaded")
        print("Browser opened. Log in normally, then return here and press Enter.")
        await asyncio.to_thread(input)
        await context.storage_state(path=str(state_path))
        await browser.close()
    print(f"Saved login state: {state_path}")
    return 0


async def command_status(args) -> int:
    config = load_yaml(Path(args.config)) if args.config else {}
    state_path = storage_path(config)
    result = {
        "storage_state": str(state_path),
        "storage_state_exists": state_path.exists(),
        "checked_at": utc_now(),
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if state_path.exists() else 1


def request_to_target(path: str, post_body: Any) -> Dict[str, Any]:
    meta = CORE_PATHS.get(path, {})
    name = meta.get("name")
    if not name:
        cleaned = path.strip("/").replace("/", "_").replace("-", "_").lower()
        name = cleaned[:80] or "captured_request"
    return {
        "name": name,
        "page": meta.get("page", "captured"),
        "method": "POST",
        "path": path,
        "required": bool(meta.get("required", False)),
        "pagination": isinstance(post_body, dict) and isinstance(post_body.get("page"), dict),
        "body": post_body if isinstance(post_body, dict) else {},
    }


async def command_capture(args) -> int:
    config = load_yaml(Path(args.config)) if args.config else {}
    admin_url = config.get("admin_url") or DEFAULT_ADMIN_URL
    state_path = storage_path(config)
    if not state_path.exists():
        print(f"Missing login state: {state_path}. Run login first.", file=sys.stderr)
        return 2

    captured: Dict[str, Dict[str, Any]] = {}

    async with async_playwright() as p:
        browser, context = await browser_context(p, config, headless=False)
        page = await context.new_page()

        async def on_response(response):
            try:
                request = response.request
                if request.method.upper() != "POST":
                    return
                parsed = urlparse(request.url)
                path = parsed.path
                haystack = request.url.lower()
                if path not in CORE_PATHS and not any(k.lower() in haystack for k in INTERESTING_KEYWORDS):
                    return
                post_body = read_json_maybe(request.post_data or "")
                if not isinstance(post_body, dict):
                    return
                payload = None
                try:
                    payload = await response.json()
                except Exception:
                    payload = None
                target = request_to_target(path, post_body)
                target["last_status"] = response.status
                if isinstance(payload, dict):
                    target["last_response_keys"] = list(payload.keys())
                    data = payload.get("data")
                    if isinstance(data, dict):
                        target["last_data_keys"] = list(data.keys())
                captured[target["name"]] = target
                print(f"captured {target['name']} {path} status={response.status}")
            except Exception as exc:
                print(f"capture warning: {exc}", file=sys.stderr)

        page.on("response", lambda response: asyncio.create_task(on_response(response)))
        await page.goto(admin_url, wait_until="domcontentloaded")
        print("Capture is running.")
        print("Open WB pages and click query/search buttons. Do not close the browser.")
        await asyncio.sleep(args.seconds)
        await context.storage_state(path=str(state_path))
        await browser.close()

    out_config = {
        "base_url": config.get("base_url") or DEFAULT_BASE_URL,
        "admin_url": admin_url,
        "login_url": config.get("login_url") or DEFAULT_LOGIN_URL,
        "storage_state": str(state_path),
        "client_language": config.get("client_language") or "zh-CN",
        "rate_limit_seconds": config.get("rate_limit_seconds", 1.5),
        "page_size": config.get("page_size", 50),
        "max_pages": config.get("max_pages", 5),
        "targets": list(captured.values()),
    }
    write_yaml(Path(args.out), out_config)
    print(f"Wrote captured config: {args.out}")
    print(f"Captured targets: {len(captured)}")
    return 0 if captured else 1


async def call_target(context, target: Dict[str, Any], config: Dict[str, Any], headers: Dict[str, str], args) -> Dict[str, Any]:
    base_url = config.get("base_url") or DEFAULT_BASE_URL
    url = build_full_url(base_url, target["path"])
    page_size = int(args.page_size or target.get("page_size") or config.get("page_size") or 50)
    max_pages = int(args.max_pages or target.get("max_pages") or config.get("max_pages") or 5)
    rate_limit = float(args.rate_limit if args.rate_limit is not None else config.get("rate_limit_seconds", 1.5))
    method = target.get("method", "POST").upper()
    body_template = target.get("body") or {}
    target_name = target["name"]
    raw_dir = Path(args.raw_dir)
    records: List[Dict[str, Any]] = []
    pages: List[Dict[str, Any]] = []
    errors: List[str] = []

    for page_number in range(1, max_pages + 1):
        body = ensure_page_body(body_template, page_number, page_size) if target.get("pagination", True) else copy.deepcopy(body_template)
        try:
            if method == "GET":
                response = await context.request.get(url, headers=headers, timeout=args.timeout * 1000)
            else:
                response = await context.request.post(url, headers=headers, data=body, timeout=args.timeout * 1000)
            status = response.status
            text = await response.text()
            try:
                payload = json.loads(text)
            except json.JSONDecodeError:
                payload = {"non_json_response": text[:1000]}
            write_json(raw_dir / target_name / f"page_{page_number}.json", payload)
            page_records = records_from_payload(payload)
            info = page_info_from_payload(payload)
            pages.append({"page": page_number, "status": status, "record_count": len(page_records), **info})
            if status >= 400:
                errors.append(f"HTTP {status} on page {page_number}")
                break
            if isinstance(payload, dict) and payload.get("code") not in (None, 200):
                errors.append(f"API code {payload.get('code')} on page {page_number}: {payload.get('msg')}")
                break
            for record in page_records:
                row = {"target": target_name, "target_page": target.get("page", "")}
                row.update(record)
                records.append(row)
            total_pages = int(info.get("totalPages") or 1)
            if not target.get("pagination", True) or page_number >= total_pages or not page_records:
                break
            await asyncio.sleep(rate_limit)
        except Exception as exc:
            errors.append(str(exc))
            break

    return {
        "name": target_name,
        "page": target.get("page"),
        "path": target.get("path"),
        "required": bool(target.get("required", False)),
        "success": not errors and bool(records),
        "record_count": len(records),
        "pages": pages,
        "errors": errors,
        "records": records,
    }


async def command_run(args) -> int:
    config = load_yaml(Path(args.config))
    state_path = storage_path(config)
    if not state_path.exists():
        print(f"Missing login state: {state_path}. Run login first.", file=sys.stderr)
        return 2

    selected = set(args.target or [])
    targets = [t for t in config.get("targets", []) if not selected or t.get("name") in selected]
    if not targets:
        print("No targets selected.", file=sys.stderr)
        return 2

    async with async_playwright() as p:
        browser, context = await browser_context(p, config, headless=not args.show_browser)
        page = await context.new_page()
        await page.goto(config.get("admin_url") or DEFAULT_ADMIN_URL, wait_until="domcontentloaded")
        headers = await get_auth_headers(page, config)
        if "Authorization" not in headers or "visitorId" not in headers:
            await browser.close()
            print("Could not read Authorization or visitorId from saved session. Run login again.", file=sys.stderr)
            return 3

        results = []
        for target in targets:
            print(f"running {target.get('name')} {target.get('path')}")
            result = await call_target(context, target, config, headers, args)
            results.append(result)
        await context.storage_state(path=str(state_path))
        await browser.close()

    all_rows: List[Dict[str, Any]] = []
    output_targets = []
    for result in results:
        all_rows.extend(result.pop("records"))
        output_targets.append(result)

    latest = {
        "generated_at": utc_now(),
        "source": "seerfar",
        "platform": "WB",
        "targets": output_targets,
        "records": all_rows,
    }
    write_json(Path(args.output), latest)
    write_csv(Path(args.csv), all_rows)

    required = [r for r in output_targets if r["required"]]
    failed = [r for r in required if not r["success"]]
    coverage = {
        "generated_at": utc_now(),
        "status": "complete" if not failed else "incomplete",
        "required_targets": len(required),
        "successful_required_targets": len(required) - len(failed),
        "failed_required_targets": [
            {"name": r["name"], "path": r["path"], "errors": r["errors"], "record_count": r["record_count"]}
            for r in failed
        ],
        "targets": [
            {
                "name": r["name"],
                "path": r["path"],
                "required": r["required"],
                "success": r["success"],
                "record_count": r["record_count"],
                "errors": r["errors"],
            }
            for r in output_targets
        ],
        "outputs": {"json": args.output, "csv": args.csv},
    }
    write_json(Path(args.coverage), coverage)
    print(json.dumps(coverage, ensure_ascii=False, indent=2))
    return 0 if coverage["status"] == "complete" else 1


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Seerfar WB data exporter for Hermes.")
    sub = parser.add_subparsers(dest="command", required=True)

    login = sub.add_parser("login", help="Open browser for manual login and save session.")
    login.add_argument("--config", default=None)
    login.set_defaults(func=command_login)

    status = sub.add_parser("status", help="Check whether saved login state exists.")
    status.add_argument("--config", default=None)
    status.set_defaults(func=command_status)

    capture = sub.add_parser("capture", help="Capture real POST request templates from Seerfar pages.")
    capture.add_argument("--config", default=None)
    capture.add_argument("--seconds", type=int, default=180)
    capture.add_argument("--out", default="config.yaml")
    capture.set_defaults(func=command_capture)

    run = sub.add_parser("run", help="Run configured API targets and export data.")
    run.add_argument("--config", default="config.yaml")
    run.add_argument("--target", action="append", help="Run only a named target. Can be repeated.")
    run.add_argument("--output", default="data/latest.json")
    run.add_argument("--csv", default="data/latest.csv")
    run.add_argument("--coverage", default="reports/coverage.json")
    run.add_argument("--raw-dir", default="data/raw")
    run.add_argument("--page-size", type=int, default=None)
    run.add_argument("--max-pages", type=int, default=None)
    run.add_argument("--rate-limit", type=float, default=None)
    run.add_argument("--timeout", type=int, default=60)
    run.add_argument("--show-browser", action="store_true")
    run.set_defaults(func=command_run)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return asyncio.run(args.func(args))


if __name__ == "__main__":
    raise SystemExit(main())
