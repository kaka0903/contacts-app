"""核心业务逻辑的单元测试。

对应测试用例：TC-010 / TC-011 / TC-012 / TC-013（搜索模块）
这些是纯函数，不读文件、不打印，最适合做单元测试。
"""

import pytest

from contacts_app import find_by_name


CONTACTS = [
    {"name": "张三", "phone": "13800000000", "city": "杭州"},
    {"name": "李四", "phone": "13900001111", "city": "北京"},
    {"name": "小明", "phone": "13700000000", "city": "上海"},
    {"name": "小红", "phone": "13600000000", "city": "上海"},
]


@pytest.mark.parametrize(
    "keyword, expected",
    [
        ("张三", ["张三"]),          # TC-010 精确匹配
        ("张", ["张三"]),            # TC-011 模糊匹配
        ("小", ["小明", "小红"]),      # 一个关键字命中多条
        ("王", []),                  # TC-012 无匹配
        ("上海", []),                # 匹配的是姓名，不是城市
    ],
    ids=["精确匹配", "模糊匹配", "多结果", "无匹配", "不搜城市"],
)
def test_find_by_name(keyword, expected):
    result = find_by_name(CONTACTS, keyword)
    assert [c["name"] for c in result] == expected


def test_find_by_name_空关键字返回全部():
    """记录当前行为：空关键字会匹配所有姓名（因为 "" in "任意字符串" 恒为 True）。

    注意：这是「实现行为」，不是「需求规定」。按 TC-013 的备注，需求待确认——
    产品也可能期望空关键字时返回空列表或提示重输。
    一旦需求明确，本测试的断言应随之调整。
    """
    result = find_by_name(CONTACTS, "")
    assert len(result) == len(CONTACTS)


def test_find_by_name_空列表():
    assert find_by_name([], "张") == []


def test_find_by_name_不修改原列表():
    """纯函数不应产生副作用。"""
    before = [c.copy() for c in CONTACTS]
    find_by_name(CONTACTS, "张")
    assert CONTACTS == before
