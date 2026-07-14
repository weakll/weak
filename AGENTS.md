# 美食街夜市官网 — 项目说明

## 项目概述

美食街夜市官网是一个前后端分离的 Web 应用，为夜市商家和顾客提供信息展示平台。

## 技术栈

- **前端：** Vue 3 + Vite + Vue Router 4 + Axios
- **后端：** Django 6.0 + Django REST Framework 3.17
- **后台管理：** SimpleUI（中文美化主题）
- **数据库：** SQLite（开发环境）
- **Python：** 3.14.6
- **Node.js：** v26.3.0

## 项目结构

`
美食街夜市官网/
├── frontend/                    # Vue 前端项目
│   ├── src/
│   │   ├── router/index.js      # 路由配置
│   │   ├── views/               # 页面组件
│   │   ├── components/          # 通用组件
│   │   ├── App.vue              # 根组件
│   │   ├── main.js              # 入口文件
│   │   └── style.css            # 全局样式
│   ├── vite.config.js           # Vite 配置（含 /api 代理）
│   └── package.json             # 前端依赖
├── night_market/                # Django 项目配置
│   ├── settings.py              # 全局配置
│   ├── urls.py                  # 根路由
│   └── wsgi.py / asgi.py        # 部署入口
├── market/                      # Django 应用（业务逻辑）
│   ├── models.py                # 数据模型
│   ├── views.py                 # 视图（API 接口）
│   ├── admin.py                 # 后台管理配置
│   └── urls.py                  # 应用路由
├── .venv/                       # Python 虚拟环境
├── manage.py                    # Django 管理命令
└── db.sqlite3                   # 开发数据库
`

## 开发环境

### 启动服务

两个服务需要同时运行：

`ash
# 终端 1：启动 Django 后端（端口 8000）
.venv\Scripts\python.exe manage.py runserver 0.0.0.0:8000

# 终端 2：启动 Vue 前端（端口 5173）
cd frontend && npm run dev
`

### 服务地址

| 服务 | 地址 |
|---|---|
| 前端页面 | http://localhost:5173 |
| 后端 API | http://localhost:8000/api/ |
| 管理后台 | http://localhost:8000/admin/ |

## 管理后台

- 地址：http://localhost:8000/admin/
- 超级管理员：admin / admin123
- 主题：SimpleUI（中文）
- 时区：Asia/Shanghai

## 关键配置

- INSTALLED_APPS 包含：simpleui, django.contrib.admin, rest_framework, corsheaders, market
- CORS 开发环境已放开所有来源
- 语言为中文（zh-hans）
- 时区为 Asia/Shanghai
- Vite 已配置 /api 代理到 Django 后端（http://localhost:8000）

## 开发约定

### 代码风格
- 后端 Python 代码遵循 PEP 8
- 前端 Vue 3 使用 Composition API + script setup 语法
- 视图文件名使用 PascalCase
- 路由路径使用 kebab-case

### 工作原则
1. 优先输出小范围、可审核的代码变更，不做大规模重构
2. 修改代码前先确认待改动的文件，用 3-6 个要点说明修改方案
3. 绝不编造 API、配置项或文件路径；不确定时先在项目内搜索确认
4. 代码改动需与现有风格、架构保持一致
5. 使用 .venv 中的 Python（.venv/Scripts/python.exe）执行后端操作
6. 前端依赖管理使用 npm

### API 规范
- Django REST Framework 视图集优先使用 ViewSet 或 ModelViewSet
- API 路由统一放在 /api/ 前缀下
- 使用 DRF 序列化器进行数据校验和序列化
- 响应格式统一使用 JSON