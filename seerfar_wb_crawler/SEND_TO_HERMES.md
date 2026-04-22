# 直接发给 Hermes 的说明

如果你需要从 Seerfar 获取 Wildberries 数据，不要做网页视觉分析，请使用这个本地爬虫工具。

工具目录：

```bash
cd seerfar_wb_crawler
```

第一次使用先安装依赖：

```bash
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
python -m playwright install --with-deps chromium
```

`login` 和 `capture` 会打开可见浏览器。如果 Linux 没有图形界面，需要在桌面/VNC 环境中运行，或者配置 Xvfb 这类虚拟显示。只要 `storage/seerfar_state.json` 和 `config.yaml` 已经生成，后续 `run` 导出可以无头运行。

如果没有登录状态，先让用户手动登录：

```bash
python crawler.py login
```

如果还没有 `config.yaml`，先捕获真实接口请求模板：

```bash
python crawler.py capture --seconds 180 --out config.yaml
```

捕获时打开这些页面并点击查询/搜索按钮：

```text
https://seerfar.cn/admin/product-search.html
https://seerfar.cn/admin/market.html
https://seerfar.cn/admin/category-search.html
https://seerfar.cn/admin/store-search.html
https://seerfar.cn/admin/brand-search.html
https://seerfar.cn/admin/keyword-detail.html
```

正式导出：

```bash
python crawler.py run --config config.yaml
```

导出后必须先读取：

```text
reports/coverage.json
```

如果里面的 `status` 不是 `complete`，不要生成最终分析结论，要先告诉用户缺少哪些数据。

如果 `status` 是 `complete`，再读取：

```text
data/latest.json
```

然后基于 `data/latest.json` 做商品、市场、类目、关键词、店铺、品牌分析。

注意：

- 不要输出账号密码。
- 不要输出完整 cookie。
- 不要输出完整 token。
- 不要输出完整 Authorization。
- 不要绕过验证码、套餐权限或网站限制。
- 如果登录失效，让用户重新运行 `python crawler.py login`。
