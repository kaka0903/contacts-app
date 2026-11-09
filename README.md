# 通讯录管理系统（Command-Line Contacts Manager）

![Tests](https://github.com/kaka0903/contacts-app/actions/workflows/test.yml/badge.svg)

一个用 Python 实现的命令行通讯录，支持增删改查、模糊搜索、数据持久化。

这是我学习 Python 的第 7 天完成的第一个完整项目，随后补齐了测试用例、缺陷报告与 pytest 自动化测试。

---

## 功能

| 功能 | 说明 |
|---|---|
| 查看全部 | 表格形式展示所有联系人，显示总人数 |
| 添加联系人 | 姓名唯一性校验、手机号 11 位格式校验 |
| 模糊搜索 | 输入"小"可搜到"小明"和"小红" |
| 修改 | 支持只改手机号或只改城市，留空表示跳过 |
| 删除 | 二次确认，防止误删 |
| 数据持久化 | 所有数据保存在 `contacts.json`，重启程序不丢失 |

---

## 健壮性设计

程序对以下异常输入做了处理，不会崩溃：

- 姓名输入为空 → 提示后重新输入
- 手机号不是 11 位数字 → 提示后重新输入
- 菜单输入非法选项 → 提示后返回菜单
- `contacts.json` 不存在 → 从空列表开始
- `contacts.json` 内容被损坏（非法 JSON）→ 从空列表开始，不抛异常

---

## 技术栈

- **Python 3.12+**
- 标准库 `json`（数据序列化）、`unicodedata`（终端显示宽度计算）
- 无运行时第三方依赖
- 测试：`pytest`

---

## 测试

本项目有一套完整的测试资产：

| 类型 | 内容 | 位置 |
|---|---|---|
| 测试用例 | 30 条，含设计依据与执行结果 | `测试用例表.xlsx` |
| 缺陷报告 | 2 个缺陷，含复现步骤、根因、修复建议 | `缺陷报告.md` |
| 自动化测试 | 22 个 pytest 用例，覆盖核心逻辑/显示/存储 | `tests/` |

```bash
pip install -r requirements-dev.txt
pytest -v
```

测试通过 GitHub Actions 在每次 push 时自动执行（Python 3.12 / 3.13 双版本）。

**覆盖范围**

- `test_core.py` — 搜索逻辑：精确/模糊/多结果/无匹配，空关键字行为，纯函数无副作用
- `test_display.py` — 中文与全角字符的显示宽度计算、补齐与截断（BUG-001 回归）
- `test_storage.py` — 文件读写往返、文件缺失、文件损坏、中文不转义、空数组落盘（BUG-002 相关）

---

## 运行

```bash
python contacts_app.py
```

首次运行会自动创建 `contacts.json`。

---

## 项目结构

```
contacts_app.py            主程序
├── _disp_width()            计算终端显示宽度（中文占 2 列）
├── _fit()                   按显示宽度补齐/截断
├── load_contacts()          读取数据（含损坏文件容错）
├── save_contacts()          写入数据
├── input_str()              非空字符串输入
├── input_phone()            手机号格式校验
├── find_by_name()           模糊匹配
├── show_all()               表格展示
├── add_contact()            添加
├── search_contact()         搜索
├── update_contact()         修改
├── delete_contact()         删除
└── main()                   菜单主循环

tests/
├── test_core.py             搜索逻辑单元测试
├── test_display.py          显示宽度与截断（BUG-001 回归）
└── test_storage.py          文件读写与容错

conftest.py                  把项目根目录加入 sys.path
pytest.ini                   pytest 配置
requirements-dev.txt         开发依赖（仅 pytest）
.github/workflows/test.yml   GitHub Actions 持续集成
```

**分层设计**：数据层（读写文件）／输入层（校验输入）／业务层（增删改查）／界面层（菜单）四层分离，
每一层只做一件事。

---

## 数据格式

```json
[
  {
    "name": "张三",
    "phone": "13800000000",
    "city": "杭州"
  }
]
```

---

## 后续计划

- [x] 为功能补充自动化测试（pytest，22 个用例）
- [x] 接入 GitHub Actions 持续集成
- [ ] 按城市分组统计
- [ ] 导出为 CSV
- [ ] 手机号脱敏显示
- [ ] 添加创建时间戳
