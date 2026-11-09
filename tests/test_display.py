"""显示逻辑的单元测试。

对应测试用例：TC-021（中文名/超长名的对齐表现）
这里测的是 BUG-001 修复后新增的两个辅助函数：_disp_width 和 _fit。
"""

import pytest

from contacts_app import _disp_width, _fit


@pytest.mark.parametrize(
    "text, expected",
    [
        ("", 0),
        ("abc", 3),
        ("张三", 4),        # 中文占 2 列
        ("a张b", 4),        # 中英混排
        ("13800000000", 11),
    ],
    ids=["空串", "纯英文", "纯中文", "中英混排", "手机号"],
)
def test_disp_width(text, expected):
    assert _disp_width(text) == expected


def test_fit_短文本补齐空格():
    result = _fit("张三", 8)
    assert _disp_width(result) == 8
    assert result.startswith("张三")


def test_fit_刚好等于宽度不截断():
    result = _fit("abcd", 4)
    assert result == "abcd"


def test_fit_超长文本截断并加省略号():
    result = _fit("张三张三张三张三", 12)
    # 截断后总显示宽度必须等于目标宽度
    assert _disp_width(result) == 12
    assert result.endswith("…")
    assert "张三张三张三张三" not in result


def test_fit_修复BUG001_超长姓名不挤走后续列():
    """回归测试：BUG-001。

    修复前用 f"{name:<10}"，20 个汉字的姓名会占 40 列，把手机号列整体推走。
    修复后姓名列固定 12 列，后续列起始位置不受姓名长度影响。
    """
    name_col = _fit("张三张三张三张三张三张三张三张三张三张三", 12)
    assert _disp_width(name_col) == 12
