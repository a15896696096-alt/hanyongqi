# SeerFar WB 后台侦察报告（已脱敏）

注意：
- 本报告仅覆盖 Wildberries（WB）模块。
- 所有敏感信息（账号、密码、完整 token、完整 cookie、Authorization、手机号、邮箱、付款信息）均已隐藏。
- 本报告面向后续开发者编写数据导出/抓取工具使用。

## 一、登录情况

1. 登录入口 URL
- https://seerfar.cn/admin/sign-in.html

2. 登录时是否需要验证码
- 本次实际登录中：否

3. 是否需要短信、邮箱或其他二次验证
- 本次实际登录中：否

4. 登录成功后跳转 URL
- https://seerfar.cn/admin/index.html

5. 登录后 cookie 字段名（仅字段名）
- sf_lang
- userInfo
- alertInfo
- keyword-search-plat
- analysis-plat
- productPlatform
- productListPlat

未直接观察到：
- sa_token
- session
- 独立 token cookie

6. localStorage / sessionStorage 字段名（仅字段名）
- localStorage:
  - fingerprint
  - userInfo
  - userPricing
  - point
  - slider
  - kbPageSize
  - ptPageSize
  - kpPageSize
  - ksPageSize
- sessionStorage:
  - analysis-keyword-plat
  - analysis-keyword-result
  - analysis-keyword

7. 登录状态是否和指纹/设备/IP/语言有关
- 结论：大概率有关，至少与浏览器指纹和语言有关。
- 依据：
  - 页面加载了 FingerprintJS。
  - localStorage 中存在 fingerprint。
  - 实际请求头里稳定出现 Authorization、visitorId、Client-Language。
  - 裸调用部分接口返回 401，而页面上下文内带完整请求头时返回 200。

## 二、后台主要页面清单

### 1. 首页 / Dashboard
- 页面名称：首页 / Dashboard
- 页面 URL：https://seerfar.cn/admin/index.html
- 页面主要用途：WB 销售总览、热销类目 TOP10、热销店铺 TOP10、智能选品卡片总览
- 是否有表格：否
- 是否有图表：是
- 是否有导出按钮：未见明显导出
- 是否需要选择平台 Ozon / Wildberries：有
- 筛选条件：日期范围、类目
- 是否需要分页/滚动加载：否（卡片类）
- 重要性：中

### 2. 热销榜单选品
- 页面名称：热销榜单选品
- 页面 URL：https://seerfar.cn/admin/product-search.html
- 页面主要用途：WB 商品榜单筛选与选品
- 是否有表格：是
- 是否有图表：表格为主
- 是否有导出按钮：有
- 是否需要选择平台：有（WB 可用）
- 筛选条件：类目、上架时间、售价、毛利率、卖家类型、配送方式、SKU、品牌、排序、模式按钮
- 是否需要分页/滚动加载：分页
- 重要性：高

### 3. 市场热词选品
- 页面名称：市场热词选品
- 页面 URL：https://seerfar.cn/admin/market.html
- 页面主要用途：WB 关键词市场筛选
- 是否有表格：是
- 是否有图表：表格为主
- 是否有导出按钮：有
- 是否需要选择平台：有（WB 可用）
- 筛选条件：类目、销售额、月搜热度、月搜增长、竞品数、热词、匹配方式、模式按钮
- 是否需要分页/滚动加载：分页
- 重要性：高

### 4. 热销类目选品
- 页面名称：热销类目选品
- 页面 URL：https://seerfar.cn/admin/category-search.html
- 页面主要用途：WB 类目市场分析
- 是否有表格：是
- 是否有图表：表格为主
- 是否有导出按钮：有
- 是否需要选择平台：有（WB 可用）
- 筛选条件：类目层级、类目及子类目、销售额、销量、销售额增长率、平均价格、平均销售额
- 是否需要分页/滚动加载：分页
- 重要性：高

### 5. 热销店铺选品
- 页面名称：热销店铺选品
- 页面 URL：https://seerfar.cn/admin/store-search.html
- 页面主要用途：WB 热销店铺分析
- 是否有表格：是
- 是否有图表：表格为主
- 是否有导出按钮：有
- 是否需要选择平台：有（WB 可用）
- 筛选条件：类目、销售额、销量、销售额增长率、店铺评分、开店时长、仅看跨境
- 是否需要分页/滚动加载：分页
- 重要性：高

### 6. 热销品牌选品
- 页面名称：热销品牌选品
- 页面 URL：https://seerfar.cn/admin/brand-search.html
- 页面主要用途：WB 热销品牌分析
- 是否有表格：是
- 是否有图表：表格为主
- 是否有导出按钮：有
- 是否需要选择平台：有（WB 可用）
- 筛选条件：类目、销售额、平均价格、销售额增长率、转化集中度、竞品数
- 是否需要分页/滚动加载：分页
- 重要性：高

### 7. 查关键词
- 页面名称：查关键词
- 页面 URL：https://seerfar.cn/admin/keyword-search.html
- 页面主要用途：输入关键词进入关键词详情页
- 是否有表格：入口页无，详情页有
- 是否有图表：详情页有
- 是否有导出按钮：详情页有
- 是否需要选择平台：有（WB 可用）
- 筛选条件：平台、关键词
- 是否需要分页/滚动加载：详情页有分页/切 tab 加载
- 重要性：高

### 8. 关键词详情
- 页面名称：关键词详情
- 页面 URL：https://seerfar.cn/admin/keyword-detail.html
- 页面主要用途：查看单关键词的搜索热度、销量、销售额、热销产品/店铺/品牌
- 是否有表格：是
- 是否有图表：是
- 是否有导出按钮：有
- 是否需要选择平台：WB 已验证
- 筛选条件：关键词、tab（热销产品/店铺/品牌）
- 是否需要分页/滚动加载：分页 + tab 点击加载
- 重要性：高

### 9. 关键词反查
- 页面名称：关键词反查
- 页面 URL：https://seerfar.cn/admin/keyword-reverse.html
- 页面主要用途：通过 SKU 反查流量关键词
- 是否有表格：应有
- 是否有图表：可能有
- 是否有导出按钮：待进一步点开确认
- 是否需要选择平台：有
- 筛选条件：SKU、剔除变体
- 是否需要分页/滚动加载：可能有
- 重要性：中到高

### 10. 查竞品 / 商品详情
- 页面名称：查竞品 / 商品详情
- 页面 URL：
  - 入口：https://seerfar.cn/admin/analysis.html?analysisType=product
  - 详情：https://seerfar.cn/admin/product-detail.html
- 页面主要用途：按 SKU 查看单商品趋势、流量关键词、变体、相似产品
- 是否有表格：是
- 是否有图表：是
- 是否有导出按钮：有
- 是否需要选择平台：有（WB 已验证）
- 筛选条件：SKU、日期范围、tab
- 是否需要分页/滚动加载：需要切 tab
- 重要性：高

### 11. 查店铺
- 页面名称：查店铺
- 页面 URL：https://seerfar.cn/admin/analysis.html?analysisType=store
- 页面主要用途：按店铺名或店铺 ID 查店铺情报
- 是否有表格：入口页无，结果页应有更多数据
- 是否有图表：可能有
- 是否有导出按钮：入口页未见
- 是否需要选择平台：有（WB）
- 筛选条件：店铺名称或店铺 ID
- 是否需要分页/滚动加载：详情页可能有
- 重要性：中到高

### 12. 查品牌
- 页面名称：查品牌
- 页面 URL：https://seerfar.cn/admin/analysis.html?analysisType=brand
- 页面主要用途：按品牌名或品牌 ID 查品牌数据
- 是否有表格：入口页无，结果页应有
- 是否有图表：可能有
- 是否有导出按钮：入口页未见
- 是否需要选择平台：有（WB）
- 筛选条件：品牌名或品牌 ID
- 是否需要分页/滚动加载：详情页可能有
- 重要性：中

### 13. 查类目
- 页面名称：查类目
- 页面 URL：https://seerfar.cn/admin/analysis.html?analysisType=category
- 页面主要用途：按类目做市场分析
- 是否有表格：理论上有
- 是否有图表：理论上有
- 是否有导出按钮：未稳定验证
- 是否需要选择平台：有（WB）
- 筛选条件：类目及子类目
- 是否需要分页/滚动加载：可能有
- 重要性：中
- 备注：当前复现不稳定，建议第一版工具先不依赖它

### 14. 关键词监控
- 页面名称：关键词监控
- 页面 URL：https://seerfar.cn/admin/product-tracker.html?keyword-tracking
- 页面主要用途：监控产品关键词排名趋势
- 是否有表格：有
- 是否有图表：可能有
- 是否有导出按钮：有
- 是否需要选择平台：有（WB）
- 筛选条件：产品分组、产品ID、日期范围
- 是否需要分页/滚动加载：有
- 重要性：中

### 15. 商品列表
- 页面名称：商品列表
- 页面 URL：https://seerfar.cn/admin/product-list.html
- 页面主要用途：授权店铺后的商品管理
- 是否有表格：有
- 是否有图表：否
- 是否有导出按钮：当前页未见明显导出
- 是否需要选择平台：有（WB）
- 筛选条件：店铺名称、卖家商品编号、SKU、状态
- 是否需要分页/滚动加载：有
- 重要性：低到中

## 三、Network 接口清单

### 1. 商品榜单接口
- 对应页面：热销榜单选品
- 触发动作：点击“查询”
- 请求方法：POST
- 接口 URL/path：/product-report/product/wb/search
- 请求参数示例：
  - reviewCount / reviewRating / questionsAndAnswers / price / monthlyRevenue / monthlySales / monthlySalesRate / grossMargin 等区间对象
  - creationDate
  - categoryIds
  - fulfillment
  - titleKeywords
  - skus
  - sellerName
  - brand
  - variationsMerge
  - searchDate
  - filterRemoveProduct
  - page.pageNumber / page.pageSize / page.orders
- 请求头是否需要 Authorization：是
- 请求头是否需要 visitorId：是
- 请求头是否需要 Client-Language：是
- 返回 JSON 顶层结构：code / msg / data
- data 主要字段名：records / total / size / current / currentSize / totalPages / orders / timeInterval
- 是否分页：是
- 分页参数名：page.pageNumber / page.pageSize
- 对应页面数据：商品榜单表格
- 是否出现错误码：裸调易 401；页面内 200
- 重要程度：高

### 2. 关键词市场接口
- 对应页面：市场热词选品
- 触发动作：点击“查询”
- 请求方法：POST
- 接口 URL/path：/keyword-report/market/search/WB
- 请求参数示例：
  - price / monthlySales / monthlyRevenue / reviews / ratings / searchVolume / searchChange30 / searchChange90 / sellers / products / viewsSharing / conversionSharing / marketSpace
  - categories
  - keywords
  - matchType
  - searchDate
  - platform
  - page.pageNumber / page.pageSize / page.orders
- 请求头是否需要 Authorization：是
- 请求头是否需要 visitorId：是
- 请求头是否需要 Client-Language：是
- 返回 JSON 顶层结构：code / msg / data
- data 主要字段名：records / total / size / current / currentSize / totalPages / orders / timeInterval
- 是否分页：是
- 分页参数名：page.pageNumber / page.pageSize
- 对应页面数据：关键词市场表格
- 是否出现错误码：裸调易 401
- 重要程度：高

### 3. 类目榜单接口
- 对应页面：热销类目选品
- 触发动作：点击“查询”
- 请求方法：POST
- 接口 URL/path：/product-report/category/search/WB
- 请求参数示例：
  - monthlyRevenue / revenueRate / monthlySales / avgPrice / avgRevenue / avgSales / avgReviewRating / avgReviewCount / avgWeight / avgVolume / sellers / products / conversionSharing / crossBorderSellerRevenueRate / revenueRatio / signingRate / avgCtr
  - categoryIds
  - searchDate
  - platform
  - page.pageNumber / page.pageSize / page.orders
- 请求头是否需要 Authorization：是
- 请求头是否需要 visitorId：是
- 请求头是否需要 Client-Language：是
- 返回 JSON 顶层结构：code / msg / data
- data 主要字段名：records / total / size / current / currentSize / totalPages / orders / timeInterval
- 是否分页：是
- 分页参数名：page.pageNumber / page.pageSize
- 对应页面数据：类目榜单表格
- 是否出现错误码：裸调易 401
- 重要程度：高

### 4. 热销店铺接口
- 对应页面：热销店铺选品
- 触发动作：点击“查询”
- 请求方法：POST
- 接口 URL/path：/product-report/wb/shop/hot/report
- 请求参数示例：
  - monthlyRevenue / count / avgSales / avgPrice / monthlySales / revenueRate / avgRevenue / avgRating / avgReviewCount / rating / registrationTime / suppRatio
  - keyType / key / categories / searchDate
  - page.pageNumber / page.pageSize / page.orders
- 请求头是否需要 Authorization：是
- 请求头是否需要 visitorId：是
- 请求头是否需要 Client-Language：是
- 返回 JSON 顶层结构：code / msg / data
- data 主要字段名：records / total / size / current / currentSize / totalPages / orders / timeInterval
- 是否分页：是
- 分页参数名：page.pageNumber / page.pageSize
- 对应页面数据：热销店铺表格
- 是否出现错误码：裸调易 401
- 重要程度：高

### 5. 热销品牌接口
- 对应页面：热销品牌选品
- 触发动作：点击“查询”
- 请求方法：POST
- 接口 URL/path：/product-report/wb/brand/hot/report
- 请求参数示例：
  - monthlyRevenue / revenueRate / monthlySales / avgPrice / avgRevenue / avgSales / avgRating / avgReviewCount / avgWeight / avgVolume / sellers / count / conversionSharing / returnCancellationRate / crossBorderSellerRevenueRate
  - categoryIds / categories / searchDate / platform
  - page.pageNumber / page.pageSize / page.orders
- 请求头是否需要 Authorization：是
- 请求头是否需要 visitorId：是
- 请求头是否需要 Client-Language：是
- 返回 JSON 顶层结构：code / msg / data
- data 主要字段名：records / total / size / current / currentSize / totalPages / orders / timeInterval
- 是否分页：是
- 分页参数名：page.pageNumber / page.pageSize
- 对应页面数据：品牌榜单表格
- 是否出现错误码：裸调易 401
- 重要程度：高

### 6. 关键词详情顶部统计接口（店铺/品牌）
- 对应页面：关键词详情 -> 店铺/品牌 tab
- 触发动作：点击“店铺”或“品牌” tab
- 请求方法：POST
- 接口 URL/path：/product-report/keyword/detail/shopOrBrand/top/wb
- 请求参数示例：
  - {"keyword":"туфли","type":"shop"}
  - {"keyword":"туфли","type":"brand"}
- 请求头是否需要 Authorization：是
- 请求头是否需要 visitorId：是
- 请求头是否需要 Client-Language：是
- 返回 JSON 顶层结构：code / msg / data
- data 主要字段名：revenues / sales
- 是否分页：否
- 对应页面数据：顶部统计或图表
- 是否出现错误码：未见
- 重要程度：中到高

### 7. 关键词详情列表接口（店铺/品牌）
- 对应页面：关键词详情 -> 店铺/品牌 tab
- 触发动作：点击“店铺”或“品牌” tab
- 请求方法：POST
- 接口 URL/path：/product-report/keyword/detail/shopOrBrand/search/wb
- 请求参数示例：
  - 店铺 type=shop
  - 品牌 type=brand
  - 含 keyword、page、排序及各筛选区间
- 请求头是否需要 Authorization：是
- 请求头是否需要 visitorId：是
- 请求头是否需要 Client-Language：是
- 返回 JSON 顶层结构：code / msg / data
- data 主要字段名：records / total / size / current / currentSize / totalPages / orders / timeInterval
- 是否分页：是
- 分页参数名：page.pageNumber / page.pageSize
- 对应页面数据：关键词详情中的店铺或品牌列表
- 是否出现错误码：未见
- 重要程度：高

### 8. 通知接口
- 对应页面：全局自动加载
- 触发动作：页面刷新/切换后自动触发
- 请求方法：GET
- 接口 URL/path：/user-center/notification/latest
- 请求参数示例：?regtime=[已隐藏]
- 请求头是否需要 Authorization：是
- 请求头是否需要 visitorId：是
- 请求头是否需要 Client-Language：是
- 返回 JSON 顶层结构：code / msg / data
- data 主要字段名：notifications / unReadCount / popUpMessages
- 是否分页：否
- 对应页面数据：通知中心
- 重要程度：低

## 四、重点验证的公开线索接口

### 1. /user-center/user/currentPricing
- 是否存在：大概率存在
- 是否需要登录：是
- 是否返回 code 200：直接裸 fetch 返回 401；未稳定抓到页面内 200
- 返回 data 主要字段名：未拿到 200 结果
- 对应页面用途：套餐/会员能力判断
- 是否适合程序直接调用：适合，但不是第一版核心接口

### 2. /product-report/hotSales/search/OZON
- 是否存在：未做 Ozon 侦察（按要求仅 WB）
- 是否需要登录：未知
- 是否返回 code 200：未验证
- 返回 data 主要字段名：未验证
- 对应页面用途：Ozon 热销商品
- 是否适合程序直接调用：本次不纳入

### 3. /product-report/hotSales/search/WB
- 是否存在：疑似存在，但本次未在页面内稳定抓到该 path
- 是否需要登录：是
- 是否返回 code 200：直接裸 fetch 返回 401
- 返回 data 主要字段名：未直接拿到 200 返回
- 对应页面用途：热销商品榜单
- 是否适合程序直接调用：若真实可用则可，但建议第一版优先使用已稳定抓到的 /product-report/product/wb/search

### 4. /product-report/category/salesTrend/search/OZON
- 是否存在：未做 Ozon 侦察
- 是否需要登录：未知
- 是否返回 code 200：未验证
- 返回 data 主要字段名：未验证
- 对应页面用途：Ozon 类目销售趋势
- 是否适合程序直接调用：本次不纳入

### 5. /product-report/category/salesTrend/search/WB
- 是否存在：疑似存在
- 是否需要登录：是
- 是否返回 code 200：直接裸 fetch 返回 401；页面内未稳定抓到该 path 的 200
- 返回 data 主要字段名：未拿到 200 数据
- 对应页面用途：类目趋势图
- 是否适合程序直接调用：可能适合，但第一版先不依赖它

### 6. /user-center/dashboard/article
- 是否存在：大概率存在
- 是否需要登录：是
- 是否返回 code 200：直接裸 fetch 返回 401；本次未稳定抓到页面内 200
- 返回 data 主要字段名：未拿到 200 数据
- 对应页面用途：首页文章/资讯
- 是否适合程序直接调用：非核心，可忽略

## 五、数据完整性检查

1. 商品/市场分析必须要有的数据
- 商品：SKU、标题、类目、品牌、店铺、价格、销量、销售额、增长率、卖家类型、配送方式、评论数、评分、上架时间
- 关键词：关键词、搜索热度、搜索增长、市场空间、转化集中度、竞对数、竞品数、关联热销产品/店铺/品牌
- 店铺：店铺名/ID、销售额、销量、店铺评分、开店时长
- 品牌：品牌名/ID、销售额、销量、增长、转化集中度
- 类目：类目名/ID、销售额、销量、增长率、平均价格

2. 必需接口
- /product-report/product/wb/search
- /keyword-report/market/search/WB
- /product-report/category/search/WB
- /product-report/wb/shop/hot/report
- /product-report/wb/brand/hot/report
- /product-report/keyword/detail/shopOrBrand/search/wb

3. 可选接口
- /product-report/keyword/detail/shopOrBrand/top/wb
- /user-center/user/currentPricing
- /user-center/dashboard/article
- 监控类接口
- 类目趋势类接口

4. 可忽略页面/接口
- 首页资讯/文章
- 学习中心
- 套餐/订单
- 设置
- 通知接口
- 商品列表/授权店铺管理（第一版可不抓）
- 查类目分析入口（当前复现不稳定）

5. 有没有页面能看到数据，但 Network 里找不到明显 JSON 接口
- 有些分析页和详情页受加载时机影响，肉眼能看到结果，但单次监听未必稳定抓到。
- 后续工具建议保留页面监听/重试机制。

6. 有没有必须通过点击、滚动、翻页、切 tab 才能加载的数据
- 有
- 关键词详情的店铺/品牌 tab 需要点击
- 商品详情不同 tab 需要点击
- 列表页翻页/排序/筛选会触发更多请求

7. 有没有一次只返回部分数据、需要循环分页
- 有，绝大多数列表接口都是分页
- 常见字段：total / current / size / totalPages / records

8. 有没有时间范围限制
- 有
- 多页面有近7天、近30天、近60天、近90天、近半年等区间
- 商品详情页可见 30 天维度
- 监控页有固定时间范围

9. 有没有套餐权限限制
- 有迹象
- 不同页面曾出现“免费会员”与“付费会员”文案
- 说明某些能力或字段可能受套餐影响

10. 有没有官方导出按钮，导出是否足够完整
- 有，多个核心页面都看到“导出”
- 但未逐个下载文件并比对完整性
- 结论：可作为备用，不建议作为唯一主方案

## 六、反爬和限制

1. 是否出现验证码：否
2. 是否出现滑块/人机验证/短信验证：否
3. 是否出现 429：否
4. 是否出现账号暂停/冷却/倒计时：否
5. 是否有明显请求频率限制：未直接看到，但建议保守限速
6. 是否有 fingerprint / visitorId / 语言标识：有
7. 只用接口请求是否可能成功：第一版不建议；应保留浏览器登录 session
8. 建议后续工具方式：B
- B. Playwright 登录后保存 session，再调用接口
- 若某些页难稳定构造请求，再回退 C（Playwright 打开网页并监听接口）

## 七、结构化总结

```json
{
  "login": {
    "captcha_required": false,
    "two_factor_required": false,
    "auth_storage_keys": [
      "cookie: sf_lang",
      "cookie: userInfo",
      "cookie: alertInfo",
      "localStorage: fingerprint",
      "localStorage: userInfo",
      "localStorage: userPricing",
      "localStorage: point",
      "localStorage: slider",
      "sessionStorage: analysis-keyword-plat",
      "sessionStorage: analysis-keyword-result",
      "sessionStorage: analysis-keyword"
    ],
    "headers_likely_required": [
      "Authorization",
      "visitorId",
      "Client-Language"
    ]
  },
  "recommended_crawler_mode": "B",
  "important_pages": [
    {
      "name": "热销榜单选品",
      "url": "https://seerfar.cn/admin/product-search.html",
      "importance": "高",
      "reason": "核心商品榜单入口，适合抓 SKU、销量、销售额、品牌、店铺等基础数据。"
    },
    {
      "name": "市场热词选品",
      "url": "https://seerfar.cn/admin/market.html",
      "importance": "高",
      "reason": "关键词市场核心入口，适合抓搜索热度、增长、市场空间、竞品数。"
    },
    {
      "name": "热销类目选品",
      "url": "https://seerfar.cn/admin/category-search.html",
      "importance": "高",
      "reason": "适合抓类目层级市场数据。"
    },
    {
      "name": "热销店铺选品",
      "url": "https://seerfar.cn/admin/store-search.html",
      "importance": "高",
      "reason": "适合分析头部卖家与店铺结构。"
    },
    {
      "name": "热销品牌选品",
      "url": "https://seerfar.cn/admin/brand-search.html",
      "importance": "高",
      "reason": "适合分析品牌竞争格局。"
    },
    {
      "name": "关键词详情",
      "url": "https://seerfar.cn/admin/keyword-detail.html",
      "importance": "高",
      "reason": "可从关键词维度拆解商品、店铺、品牌。"
    },
    {
      "name": "商品详情",
      "url": "https://seerfar.cn/admin/product-detail.html",
      "importance": "高",
      "reason": "可拿到单 SKU 趋势、流量关键词、相似产品等深度数据。"
    }
  ],
  "important_apis": [
    {
      "page": "热销榜单选品",
      "method": "POST",
      "path": "/product-report/product/wb/search",
      "purpose": "获取商品榜单列表",
      "pagination": true,
      "required": true,
      "main_fields": ["records", "total", "current", "size", "totalPages", "timeInterval"]
    },
    {
      "page": "市场热词选品",
      "method": "POST",
      "path": "/keyword-report/market/search/WB",
      "purpose": "获取关键词市场列表",
      "pagination": true,
      "required": true,
      "main_fields": ["records", "total", "current", "size", "totalPages", "timeInterval"]
    },
    {
      "page": "热销类目选品",
      "method": "POST",
      "path": "/product-report/category/search/WB",
      "purpose": "获取类目市场列表",
      "pagination": true,
      "required": true,
      "main_fields": ["records", "total", "current", "size", "totalPages", "timeInterval"]
    },
    {
      "page": "热销店铺选品",
      "method": "POST",
      "path": "/product-report/wb/shop/hot/report",
      "purpose": "获取热销店铺列表",
      "pagination": true,
      "required": true,
      "main_fields": ["records", "total", "current", "size", "totalPages", "timeInterval"]
    },
    {
      "page": "热销品牌选品",
      "method": "POST",
      "path": "/product-report/wb/brand/hot/report",
      "purpose": "获取热销品牌列表",
      "pagination": true,
      "required": true,
      "main_fields": ["records", "total", "current", "size", "totalPages", "timeInterval"]
    },
    {
      "page": "关键词详情-店铺/品牌",
      "method": "POST",
      "path": "/product-report/keyword/detail/shopOrBrand/search/wb",
      "purpose": "获取关键词关联店铺或品牌列表",
      "pagination": true,
      "required": true,
      "main_fields": ["records", "total", "current", "size", "totalPages", "timeInterval"]
    }
  ],
  "risks": [
    "必须保持浏览器登录 session，裸接口请求容易返回 401",
    "请求头依赖 Authorization、visitorId、Client-Language",
    "页面含 fingerprint 机制，完全脱离浏览器环境成功率可能下降",
    "部分页面可能受套餐权限影响",
    "个别分析页复现不稳定，不建议第一版过度依赖"
  ],
  "export_options": [
    {
      "page": "热销榜单选品",
      "format": "导出按钮（通常为 Excel/CSV，未逐个下载核实）",
      "is_complete_enough": false
    },
    {
      "page": "市场热词选品",
      "format": "导出按钮（通常为 Excel/CSV，未逐个下载核实）",
      "is_complete_enough": false
    },
    {
      "page": "热销类目选品",
      "format": "导出按钮（通常为 Excel/CSV，未逐个下载核实）",
      "is_complete_enough": false
    },
    {
      "page": "热销店铺选品",
      "format": "导出按钮（通常为 Excel/CSV，未逐个下载核实）",
      "is_complete_enough": false
    },
    {
      "page": "热销品牌选品",
      "format": "导出按钮（通常为 Excel/CSV，未逐个下载核实）",
      "is_complete_enough": false
    },
    {
      "page": "关键词详情",
      "format": "导出按钮（通常为 Excel/CSV，未逐个下载核实）",
      "is_complete_enough": false
    }
  ],
  "developer_notes": "第一版建议使用 Playwright 登录并保存 session，然后直接复用页面请求头调用核心 POST 接口。优先抓 /product-report/product/wb/search、/keyword-report/market/search/WB、/product-report/category/search/WB、/product-report/wb/shop/hot/report、/product-report/wb/brand/hot/report、/product-report/keyword/detail/shopOrBrand/search/wb。所有列表接口都要做分页循环，并把时间范围、排序、类目、关键词等条件参数化。不要第一版就依赖导出按钮，也不要优先做 article/currentPricing 这类非核心接口。若某些详情页接口难稳定复现，就保留 Playwright 页面监听方案作为回退。"
}
```
