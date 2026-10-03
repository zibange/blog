# 产品池管理（Pool Manager）参考手册

> 本文档是 content-factory 中「产品池管理」的详细展开。
> 源自 `auto_publish` 模块，已升级为通用内容选题池管理框架。

---

## 一、核心概念

### 1.1 什么是产品池

产品池是**待发布内容的选题清单**，类似于"内容 Backlog"。它管理着所有计划生产但尚未发布的内容条目，配合已发布记录实现：

- 按顺序取用，不重复
- 进度追踪（已发布/待发布/完成度）
- 分类体系管理
- 每日自动取题

### 1.2 核心数据文件

| 文件 | 作用 |
|------|------|
| `product_pool.json` | 选题池（所有计划发布的内容） |
| `published.json` | 已发布记录（已经上线的内容） |

### 1.3 状态流转

```
┌──────────┐    next    ┌────────────┐   mark   ┌─────────────┐
│ 产品池    │ ─────────→ │ 正在生产    │ ───────→ │ 已发布记录   │
│ (待发布)  │            │ (进行中)    │          │ (已完成)     │
└──────────┘            └────────────┘          └─────────────┘
```

- **待发布**：在 product_pool.json 中，但不在 published.json 中
- **已发布**：同时存在于 product_pool.json 和 published.json 中
- `next` 操作取第一个"待发布"的条目

---

## 二、数据结构详解

### 2.1 product_pool.json（选题池）

```json
{
  "description": "内容选题池描述",
  "categories": {
    "display": "显控与显示",
    "perimeter": "周界安防",
    "fiber": "光纤传感"
  },
  "products": [
    {
      "slug": "led-display-control",
      "name": "LED 显示控制系统产品综述",
      "category": "display",
      "audience": "工程端",
      "one_liner": "LED 显控系统是把画面准确映射到大型 LED 屏的大脑与神经。"
    }
  ]
}
```

**字段说明**：

| 字段 | 层级 | 说明 | 必填 |
|------|------|------|------|
| `description` | 根 | 选题池的文字描述 | 否 |
| `categories` | 根 | 分类字典，key=分类ID，value=分类中文名 | 是 |
| `products` | 根 | 选题数组，按优先级排序 | 是 |
| `slug` | product | URL 友好的唯一标识（小写英文+连字符） | 是 |
| `name` | product | 内容标题（中文） | 是 |
| `category` | product | 所属分类 ID，必须在 categories 中存在 | 是 |
| `audience` | product | 目标受众（工程端/决策层/采购/科普） | 是 |
| `one_liner` | product | 一句话定位，作为写作北极星 | 是 |

### 2.2 published.json（已发布记录）

```json
{
  "published": [
    {
      "slug": "led-display-control",
      "name": "LED 显示控制系统产品综述",
      "category": "display",
      "date": "2026-09-20",
      "auto_generated": true
    }
  ]
}
```

**字段说明**：

| 字段 | 说明 |
|------|------|
| `slug` | 文章唯一标识，与 product_pool 中的 slug 对应 |
| `name` | 文章标题 |
| `category` | 所属分类 ID |
| `date` | 发布日期（YYYY-MM-DD） |
| `auto_generated` | 是否自动生成（可选，用于统计） |

---

## 三、标准操作

### 3.1 next — 取下一个待发布内容

**功能**：从产品池中取第一个尚未发布的内容条目

**逻辑**：
1. 读取 product_pool.json 中的所有 products
2. 读取 published.json 中的所有已发布 slug
3. 遍历 products，返回第一个 slug 不在已发布列表中的条目

**返回**：产品对象（含 slug/name/category/audience/one_liner），或 None（全部发布完毕）

**典型用法**：每日自动任务的第一步——取今天要生产的内容

---

### 3.2 list — 列出已发布内容

**功能**：按日期顺序列出所有已发布的内容

**输出格式**：
```
  [2026-09-20] LED 显示控制系统产品综述 (led-display-control) - display
  [2026-09-22] 考勤系统产品综述 (attendance-system) - access
```

**典型用法**：查看历史发布记录

---

### 3.3 status — 查看发布进度

**功能**：显示产品池总览统计

**输出内容**：
- 总计数量
- 已发布数量
- 待发布数量
- 完成度百分比

**典型用法**：周报、月报、进度追踪

---

### 3.4 mark — 标记为已发布

**功能**：将一条内容标记为已发布，添加到 published.json

**参数**：
- product 对象（至少包含 slug、name、category）
- auto_generated（可选，是否自动生成）

**副作用**：
- 在 published 数组末尾追加新条目
- 自动填入当前日期

**典型用法**：发布成功并验证通过后调用

---

### 3.5 add — 新增选题

**功能**：向产品池中添加新的内容条目

**参数**：完整的 product 对象（slug/name/category/audience/one_liner）

**校验**：
- slug 不能与现有条目重复
- category 必须在 categories 中存在

**典型用法**：扩充选题库

---

## 四、Python 实现参考

> 以下是产品池管理的核心逻辑，可直接复用到任何 Python 项目中。

```python
import json
import os
from datetime import datetime


class PoolManager:
    def __init__(self, pool_file, published_file):
        self.pool_file = pool_file
        self.published_file = published_file

    def _load_json(self, filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)

    def _save_json(self, filepath, data):
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def get_next(self):
        """获取下一个待发布的内容"""
        pool = self._load_json(self.pool_file)
        published = self._load_json(self.published_file)

        published_slugs = {item["slug"] for item in published["published"]}

        for product in pool["products"]:
            if product["slug"] not in published_slugs:
                return product

        return None

    def mark_published(self, product, auto_generated=True):
        """标记为已发布"""
        published = self._load_json(self.published_file)
        today = datetime.now().strftime("%Y-%m-%d")

        published["published"].append({
            "slug": product["slug"],
            "name": product["name"],
            "category": product["category"],
            "date": today,
            "auto_generated": auto_generated
        })

        self._save_json(self.published_file, published)

    def get_status(self):
        """获取发布状态统计"""
        pool = self._load_json(self.pool_file)
        published = self._load_json(self.published_file)

        total = len(pool["products"])
        done = len(published["published"])

        return {
            "total": total,
            "published": done,
            "remaining": total - done,
            "progress": done / total * 100 if total > 0 else 0
        }
```

---

## 五、最佳实践

### 5.1 产品池设计

1. **分类数量**：5-10 个为宜
   - 太少：区分度不够
   - 太多：筛选器拥挤，用户选择困难

2. **选题数量**：建议一次性规划 20-50 个
   - 太少：很快做完，需要频繁补充
   - 太多：管理成本高，优先级容易变化

3. **排序策略**：
   - 按优先级排序（高优先级在前）
   - 按难度排序（先易后难，快速建立信心）
   - 按热度/时效性排序（热点在前）

4. **受众统一**：
   - 同批次选题尽量受众一致
   - 保证内容调性统一

### 5.2 命名规范

- **slug**：小写英文 + 连字符，URL 友好
  - ✅ `led-display-control`
  - ❌ `LED显示控制`、`led_display_control`、`ledDisplayControl`

- **分类 ID**：简短英文单词
  - ✅ `display`、`access`、`fiber`
  - ❌ `显示与控制`、`category-1`

### 5.3 一句话定位（one_liner）

这是最重要的字段，它是全文的"北极星"。

**好的 one_liner 标准**：
- 用一句话讲清"这是什么、为什么值得关注"
- 包含核心价值主张
- 不超过 50 字

**示例**：
- ✅ "LED 显控系统是把画面准确映射到大型 LED 屏的大脑与神经。"
- ✅ "振动光纤是一根光纤即一条无形警戒线的智能周界感知终端。"
- ❌ "这是一篇关于 LED 显控的产品综述文章。"（废话，没价值）

---

## 六、迁移到新领域

产品池管理逻辑完全通用，迁移时只需：

1. 替换 `product_pool.json` 中的 `categories` 和 `products`
2. 清空 `published.json` 中的 `published` 数组（保留空数组结构）

管理代码、状态机、操作接口零改动。

---

## 七、扩展方向

产品池管理可以根据需要扩展以下能力：

| 扩展能力 | 说明 |
|---------|------|
| **优先级管理** | 为每个产品增加 priority 字段，支持动态排序 |
| **标签系统** | 增加 tags 字段，支持多维度筛选 |
| **依赖关系** | 产品之间有前置依赖，必须按顺序发布 |
| **版本管理** | 同一产品支持多次更新/重写 |
| **多人协作** | 增加 assignee 字段，分配给不同作者 |
| **审核流程** | 增加 draft → review → published 多状态流转 |

当前实现是"最简可用版"，按需扩展即可。
