# 发布部署引擎（Publish Engine）参考手册

> 本文档是 content-factory 中「发布部署引擎」的详细展开。
> 源自 `blog-publish`，纯前端静态博客方案。

---

## 一、方案概述

### 1.1 技术栈

| 组件 | 说明 |
|------|------|
| HTML/CSS/JS | 原生三件套，无构建依赖 |
| marked.js | Markdown 解析 |
| DOMPurify | HTML 安全过滤 |
| highlight.js | 代码高亮 |
| GitHub Pages | 静态托管（通过 Gitee 镜像推送） |

### 1.2 核心优势

- **纯静态，零后端**：无需服务器，迁移零成本（整个文件夹拷贝即可）
- **Markdown 客户端渲染**：新增文章无需构建，直接 push MD 文件即可
- **国内可访问**：通过 Gitee 镜像推送，无需代理/VPN
- **功能完整**：明暗主题、分类筛选、阅读目录、上/下篇

### 1.3 部署方案对比

| | Gitee 镜像→GitHub Pages | 直连 GitHub Pages | Cloudflare Workers | Gitee Pages |
|---|---|---|---|---|
| 本地 push 速度 | 秒推（Gitee 国内直连） | 时通时断 | — | 秒推 |
| 需要代理 | **否** | 是 | — | 否 |
| GitHub 同步 | Gitee 自动镜像 | 直连 | — | 不同步 |
| 自定义域名 | 免费 | 免费 | 免费+自动HTTPS | 需付费版 |
| CDN 缓存 | 10 分钟 | 10 分钟 | 可配置，可 Purge | — |
| 限制 | Gitee 需实名认证 | 无 | 25MB 单文件限制 | 需实名认证 |

---

## 二、项目结构

```
blog/
├── index.html              # 首页（Hero + 文章列表 + 分类筛选）
├── article.html            # 文章阅读页（封面 + 目录 + 正文）
├── articles.json           # 文章清单（核心配置文件）
├── CNAME                   # GitHub Pages 自定义域名（可选）
├── wrangler.jsonc          # Cloudflare Workers 部署配置（可选）
├── articles/               # 文章文件夹（每篇一个子目录）
│   ├── {slug}/
│   │   ├── {file}.md       # Markdown 文章
│   │   └── images/         # 文章图片
│   └── ...
└── assets/
    ├── css/
    │   └── style.css       # 全站样式（含明暗双主题）
    └── js/
        ├── main.js         # 首页逻辑（列表渲染、筛选、主题切换）
        └── article.js      # 文章页逻辑（MD 加载、目录、滚动高亮）
```

---

## 三、articles.json 配置详解

### 3.1 完整结构

```json
{
  "site": {
    "title": "站点名称",
    "subtitle": "副标题",
    "author": "作者名",
    "description": "站点简介"
  },
  "categories": [
    { "id": "cat-1", "name": "分类一" },
    { "id": "cat-2", "name": "分类二" }
  ],
  "articles": [
    {
      "slug": "article-1",
      "title": "文章一标题",
      "category": "cat-1",
      "date": "2026-01-01",
      "cover": "images/cover.png",
      "file": "文章一.md",
      "readTime": 20,
      "excerpt": "一句话摘要。"
    }
  ]
}
```

### 3.2 字段速查表

**site（站点全局信息）**

| 字段 | 含义 | 用途 |
|------|------|------|
| `title` | 站点名称 | 导航栏 logo、浏览器标签标题 |
| `subtitle` | 副标题 | 拼接到浏览器标签标题尾部 |
| `author` | 作者名 | 预留字段 |
| `description` | 站点简介 | SEO meta description |

**categories（分类列表）**

| 字段 | 含义 |
|------|------|
| `id` | 分类唯一标识（英文），文章 category 字段关联此值 |
| `name` | 分类显示名称（中文） |

**articles（文章清单数组）**

| 字段 | 含义 | 示例 |
|------|------|------|
| `slug` | 文章唯一标识，决定文件夹路径和 URL 参数 | `"led-display-control"` |
| `title` | 文章标题 | `"LED 显示控制系统产品综述"` |
| `category` | 所属分类 ID | `"display"` |
| `date` | 发布日期（YYYY-MM-DD），首页按此降序 | `"2026-09-30"` |
| `cover` | 封面图相对路径（相对于文章文件夹） | `"images/cover.png"` |
| `file` | MD 文件名（文章文件夹内的实际文件名） | `"LED显控产品综述.md"` |
| `readTime` | 阅读时长（分钟），中文约 350 字/分钟 | `20` |
| `excerpt` | 一句话摘要，首页卡片正文区 | `"一句话概括..." |

### 3.3 ⚠️ 语法纪律（导致全站白屏的常见坑）

1. **绝对不要在字符串值中使用中文双引号 `""`**
   - JSON 解析器会将其视为字符串结束符
   - 改用书名号 `「」` 或单引号 `''` 替代
   - 错误示例：`"excerpt": "定"吞吐与存储"的大脑"` ❌
   - 正确示例：`"excerpt": "定「吞吐与存储」的大脑"` ✅

2. 数组最后一个元素后**不要加逗号**
   - 错误：`}, ]` ❌
   - 正确：`} ]` ✅

3. JSON 中**不能有注释**
   - 错误：`// 这是注释` ❌

---

## 四、Gitee 镜像 → GitHub Pages 部署链路

### 4.1 为什么用镜像方案

国内直连 GitHub 不稳定，Gitee 秒推，镜像同步全自动：

```
本地 git push gitee main
    ↓ 秒推（国内直连 Gitee，无需 VPN）
Gitee 仓库更新
    ↓ Gitee 镜像同步（自动，几秒~几分钟）
GitHub 仓库更新
    ↓ GitHub Pages 检测到 push（自动，1~2 分钟）
GitHub Pages 重新构建
    ↓ CDN 缓存刷新（约 10 分钟）
线上站点更新
```

### 4.2 一次性配置步骤

**前提条件**：
- Gitee 账号已完成**实名认证**
- Gitee 仓库已创建
- GitHub 仓库已创建
- 本地已添加两个 remote

**配置步骤**：

1. **生成 GitHub Classic Token**：
   - 打开 `https://github.com/settings/tokens`
   - 点击 **Tokens (classic)** → **Generate new token (classic)**
   - Note 填 `gitee-mirror`，Expiration 选 `No expiration`
   - 勾选 **`repo`**（第一个大项，包含子项全选）
   - 生成后复制 token（`ghp_` 开头，只显示一次）

2. **在 Gitee 配置镜像**：
   - 打开 Gitee 仓库 → **管理**
   - 找到 **仓库镜像** 或 **Mirror 管理**
   - 添加镜像目标：
     - 镜像方向：**推送**（Gitee → GitHub）
     - 目标仓库地址：`https://github.com/{user}/{repo}.git`
     - 用户名：`{github-username}`
     - 密码：粘贴 GitHub Token
   - 保存

3. **验证**：
   - 本地 `git push gitee main` 推送一次
   - 检查 GitHub 仓库 commits 页面是否出现最新 commit

### 4.3 日常操作（4 行命令）

```powershell
cd path\to\blog
git add -A
git commit -m "更新文章"
git push gitee main
```

> **注意**：不要在 GitHub 网页上直接编辑文件，否则下次 Gitee 同步会产生冲突。所有编辑在本地完成。

---

## 五、发布五步验证法

> 按顺序验证，不要跳步，否则容易被 CDN 缓存误导。

### 第一步：确认 Gitee 仓库已更新

```powershell
git fetch gitee ; git log --oneline gitee/main -3
```

应看到最新 commit hash 在第一行。

---

### 第二步：确认 GitHub 仓库已同步

用 WebFetch 访问 GitHub API（注意：是 API，不是网页）：

```
https://api.github.com/repos/{user}/{repo}/commits?per_page=3
```

检查返回 JSON 第一条的 `sha` 和 `commit.message` 是否为最新 commit。

> **坑点**：不要用 `raw.githubusercontent.com` 验证！它有 CDN 缓存，可能返回旧内容。GitHub API 直连源仓库，无缓存。

---

### 第三步：确认 articles.json 已更新

用 WebFetch 访问带时间戳的 articles.json（时间戳绕过 CDN 缓存）：

```
https://{your-domain}/articles.json?v={当前时间戳}
```

检查返回 JSON 的 `articles` 数组是否包含新文章的 slug。

> **坑点**：不带 `?v=时间戳` 会命中 CDN 缓存返回旧数据。`main.js` 中已内置 `?v=${Date.now()}`，但手动验证时需要自己加。

---

### 第四步：确认首页动态渲染正确

用浏览器验证（WebFetch 无法替代，因为它不执行 JS）：

检查项：
- 顶部统计数字（文章数 = articles 数组长度）
- 最新文章区域的文章卡片数量（含新文章卡片）
- 分类筛选按钮数量（= categories 数组长度 + 1 个"全部"）

> **坑点**：WebFetch 只返回静态 HTML，无法验证动态渲染的数字和文章列表。必须用浏览器验证。

---

### 第五步：如果首页未更新

- 等待 10 分钟（GitHub Pages CDN 缓存周期）
- 浏览器 `Ctrl+Shift+R` 强制刷新
- fetch 请求已加 `?v=时间戳`，理论上不受 CDN 缓存影响

---

## 六、CDN 缓存机制与绕过

### 6.1 缓存原理

GitHub Pages 通过 HTTP 响应头 `Cache-Control: max-age=600` 控制缓存，CDN 边缘节点缓存约 10 分钟。

即使 JS 中写 `cache: 'no-cache'`，请求仍可能被 CDN 直接返回缓存内容，不回源。

### 6.2 绕过方案（已实施）

在 `main.js` 和 `article.js` 中，fetch 请求加时间戳参数：

```javascript
// articles.json
const res = await fetch(`articles.json?v=${Date.now()}`, { cache: 'no-store' });

// MD 文件
const mdRes = await fetch(`articles/${slug}/${file}?v=${Date.now()}`, { cache: 'no-store' });
```

URL 变化使 CDN 视为新资源，强制回源。

同时更新 `index.html` 中 JS 版本号 `?v=N` 确保浏览器加载最新 JS。

### 6.3 GitHub Pages 不可配置

GitHub Pages 不提供缓存配置面板，不能自定义 `Cache-Control` 或手动刷新 CDN。唯一有效方法就是 URL 查询参数。

---

## 七、域名绑定

### 7.1 CNAME 文件

仓库根目录 `CNAME` 文件（无扩展名），内容为一行域名：

```
blog.example.com
```

### 7.2 DNS 解析配置

**子域名**（如 `blog.example.com`）：

| 类型 | 主机记录 | 记录值 |
|------|---------|--------|
| CNAME | `blog` | `{github-username}.github.io` |

**根域名**（如 `example.com`），添加 4 条 A 记录：

```
185.199.108.153
185.199.109.153
185.199.110.153
185.199.111.153
```

### 7.3 开启 HTTPS

GitHub Pages Settings → Pages → 勾选 Enforce HTTPS（DNS 生效后出现）。

---

## 八、本地预览

```powershell
cd path\to\blog
python -m http.server 8765
```

访问 `http://localhost:8765/`。

> **不要直接双击 HTML**，否则 `fetch` 加载 MD 会被浏览器 file:// 协议拦截，导致白屏。

---

## 九、常见问题排查

| 问题 | 原因 | 解决 |
|------|------|------|
| Gitee push 认证失败 | Gitee 账号密码或 Token 错误 | 在终端手动 `git push gitee main`，输入正确凭据 |
| Gitee push `reference already exists` | Gitee 仓库已有相同 commit | 实际已推送成功，用 `git log gitee/main` 确认 |
| GitHub 未同步 | Gitee 镜像延迟或有冲突 | 检查 Gitee 仓库镜像设置，确认 Token 有效 |
| 首页文章数没变 | GitHub Pages CDN 缓存旧 articles.json | 等待 10 分钟；fetch 已加 `?v=时间戳` 自动绕过 |
| 首页分类数没变 | 旧版本 index.html 写死了数字 | 已修复为动态读取，更新 JS 版本号 |
| 浏览器显示旧页面 | 浏览器缓存 | `Ctrl+Shift+R` 强制刷新 |
| 页面显示"加载文章列表失败" | articles.json 中含中文双引号 `""` | 将 `""` 改为 `「」` 或单引号 `''`，重新推送 |
| git pull 合并冲突 | 远程和本地同时修改了 articles.json | 手动编辑冲突文件，保留正确版本后 commit |
| GitHub "DNS check unsuccessful" | GitHub DNS 检测缓存延迟 | 实际已生效，点击 Check again 或等待 |
| 本地双击 HTML 白屏 | fetch 被 file:// 协议拦截 | 用 `python -m http.server` 启动本地服务 |

---

## 十、迁移到新博客

只需 5 步：

1. **拷贝 blog 文件夹**到新位置（整个文件夹，结构不变）
2. **修改 articles.json**：更新 site 信息、categories、清空 articles
3. **清空 articles/ 目录**：保留空目录结构，删除旧文章
4. **配置 Git 仓库**：`git init`，添加新的 GitHub/Gitee remote
5. **配置 Gitee 镜像**：按第四章步骤配置镜像同步

框架零改动，5 分钟完成迁移。
