# 安装与启动指南

掼蛋赛事管理系统（Flask + Flask-Admin + MongoDB）。

> 本项目原始代码为 Python 2 编写，现已适配到 Python 3（详见文末「Python 3 适配说明」）。
> 当前验证环境：**Windows + Python 3.12.10**，应用可正常启动并访问主页。

---

## 1. 前置要求

| 依赖 | 要求 | 说明 |
| --- | --- | --- |
| Python | 3.10 及以上（已验证 3.12.10） | 安装时勾选 *Add to PATH* |
| MongoDB | 4.x / 5.x / 6.x / 7.x 均可 | 数据读写必需；未安装时应用仍可启动，但管理页面查询会报错 |
| pip | 随 Python 安装 | 用于安装项目依赖 |

Windows 安装 MongoDB 简述（本项目当前采用 **Docker 方式**，已验证可用）：

```powershell
# 启动容器：仅绑定本机 127.0.0.1:27017，数据存放在命名卷 guandan_mongo_data
docker run -d --name guandan-mongo --restart unless-stopped `
  -p 127.0.0.1:27017:27017 `
  -v guandan_mongo_data:/data/db `
  mongo:8.0

# 验证
docker exec guandan-mongo mongosh --quiet --eval "db.runCommand({ping:1}).ok"   # 输出 1 即正常
```

> 网络提示：本机直连 Docker Hub 拉取镜像会失败，可改用国内镜像源再打 tag，例如：
> `docker pull docker.1ms.run/library/mongo:8.0` + `docker tag docker.1ms.run/library/mongo:8.0 mongo:8.0`
> （大层下载可能多次重试，等待其自动恢复即可）。
>
> 也可不用 Docker：从 [官网](https://www.mongodb.com/try/download/community) 下载 MSI 安装为 Windows 服务，
> 或免安装 zip 版运行 `mongod --dbpath <数据目录>`。端口验证：`Test-NetConnection localhost -Port 27017`。

## 2. 创建虚拟环境并安装依赖

在项目根目录（`guandan_pvp`）下用 PowerShell 执行：

```powershell
# 1) 创建虚拟环境（目录名 venv）
python -m venv venv

# 2) 激活虚拟环境
.\venv\Scripts\Activate.ps1
# 若提示执行策略受限，可先运行：Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
# （cmd 用户改用 .\venv\Scripts\activate.bat）

# 3) 安装依赖
python -m pip install --upgrade pip
pip install -r requirements.txt
```

如果不便激活，也可以始终用完整路径调用解释器：`.\venv\Scripts\python.exe`。

当前实际安装的关键依赖版本（requirements.txt 未锁版本，装的是最新兼容版）：

| 包 | 版本 |
| --- | --- |
| Flask | 3.1.3 |
| Flask-Admin | 2.2.1 |
| Flask-BasicAuth | 0.2.0 |
| Flask-Babel | 4.0.0 |
| mongoengine | 0.29.3 |
| pymongo | 4.19.0 |
| gevent | 26.9.0 |
| WTForms | 3.3.1 |
| xlrd / xlwt / xlutils | 2.0.2 / 1.3.0 / 2.0.0 |

> 注：`Flask-MongoEngine 1.0.0` 与 Flask 3.x 不兼容（依赖已被移除的 `flask.json.JSONEncoder`），
> 代码中已改为直接使用 `mongoengine` 连接数据库（见 `db.py`），该包保留与否不影响运行。

## 3. 配置 settings.py

`MONGODB_SETTINGS` 当前已按本地 Docker 容器配置好（无认证）：

```python
MONGODB_SETTINGS = {'db': 'guandan', 'host': 'localhost', 'port': 27017}
```

连接远程或开启认证的 MongoDB 时，补充 `username` / `password`（`username` 为空则不认证）。

以下两项仍建议按环境修改：

- `BASIC_AUTH_USERNAME` / `BASIC_AUTH_PASSWORD`：网站登录账号密码（HTTP Basic 认证），默认为 `yourname` / `yourpass`，务必修改。
- `BASIC_AUTH_FORCE = True`：全站强制登录。
- `SECRET_KEY`：建议改为随机字符串。

## 4. 启动项目

### 开发模式（Flask 内置服务器，带调试/热重载）

```powershell
.\venv\Scripts\python.exe main.py
```

浏览器访问 <http://127.0.0.1:5000/>，输入 `settings.py` 中的 Basic Auth 账号密码。

### 生产模式（gevent WSGI 服务器）

```powershell
.\venv\Scripts\python.exe run_server.py
```

监听 `0.0.0.0:5000`。

> 提示：若 MongoDB 不可达，启动时各数据视图的筛选器会逐个等待约 30 秒连接超时，
> 导致首次启动较慢；页面仍可打开，但筛选选项为空。请先确保 MongoDB 服务已运行。

## 5. 快速自检

```powershell
# 语法/导入检查（应在数秒~1分钟内输出 IMPORT OK；无 MongoDB 时因连接超时会偏慢）
.\venv\Scripts\python.exe -c "import main; print('IMPORT OK')"
```

## 6. Python 3 适配说明（相对原始 Python 2 代码的改动）

- 所有 `flask.ext.xxx` 导入改为标准包名（`flask_admin`、`flask_babel`、`flask_basicauth`、`flask_mongoengine` 等）。
- `db.py`：`flask_mongoengine.MongoEngine` 与 Flask 3 不兼容，改为基于 `mongoengine.connect()` 的最小兼容层（保留 `db.init_app(app)` 用法）。
- `main.py`：移除 Flask-Admin 2.x 已删除的 `template_mode='bootstrap3'` 参数（默认使用 Bootstrap4 主题）。
- `templates/admin/base.html`：静态资源路径由 bootstrap3 改为 bootstrap4（jquery/popper/bootstrap/moment/select2 文件名同步更新）。
- `run_server.py`：删除 `execfile` 激活脚本；`gevent.wsgi` 改为 `gevent.pywsgi`。
- `views.py`：`unicode()` → `str()`、整除改 `//`、`dict.values()` 包 `list()` 供随机抽样。
- 各模型 `__unicode__` → `__str__`；包内 `import models` 改为 `from . import models`（namelist / game / game_record）。
- `mongodb.py`：`pymongo.Connection` + `db.authenticate()` 改为 `MongoClient(username/password/authSource)`。
- `data/import_data.py`：`collection.insert()` 改为 `insert_one()`（pymongo 4 API）。
- `filters.py`：筛选器选项查询增加容错，MongoDB 不可达时不再阻断应用启动。

## 7. 已知遗留限制

- **tools/ 目录**：Python 2 + Tkinter 桌面小工具（依赖 `tkFileDialog`、缺失的 `format` 模块），未适配 Python 3，不参与 Web 应用运行，无法直接使用。
- **auth/ 目录**：依赖未安装的 `flask_security`，当前无任何代码引用，属于遗留死代码。
- **data/import_data.py**：历史数据导入脚本，已按 pymongo 4 API 修改，但需要 MongoDB 与对应 Excel 数据文件才能实际运行。
- `templates/rank.html` 等页面的老版 dataTables Excel 导出（`.swf` 方案）在 modern 浏览器下可能失效。
