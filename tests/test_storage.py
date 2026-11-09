"""文件读写的单元测试。

对应测试用例：TC-028（contacts.json 被改坏）与持久化相关用例。

关键技巧：用 monkeypatch 把模块里的 DATA_FILE 替换成临时路径，
这样测试不会碰你真实的 contacts.json，也不会互相污染。
"""

import json

import pytest

import contacts_app


@pytest.fixture
def temp_data_file(tmp_path, monkeypatch):
    """把 contacts_app.DATA_FILE 指向临时文件，测试结束后自动还原。"""
    path = tmp_path / "contacts.json"
    monkeypatch.setattr(contacts_app, "DATA_FILE", str(path))
    return path


def test_保存后能原样读回(temp_data_file):
    data = [
        {"name": "张三", "phone": "13800000000", "city": "杭州"},
        {"name": "李四", "phone": "13900001111", "city": "北京"},
    ]
    contacts_app.save_contacts(data)

    assert temp_data_file.exists()
    assert contacts_app.load_contacts() == data


def test_文件不存在时返回空列表(temp_data_file):
    assert not temp_data_file.exists()
    assert contacts_app.load_contacts() == []


def test_文件内容损坏时返回空列表(temp_data_file):
    """TC-028：手工把文件改坏，程序不能崩。"""
    temp_data_file.write_text("这不是合法的 JSON {{{", encoding="utf-8")
    assert contacts_app.load_contacts() == []


def test_保存的文件是合法JSON且中文不被转义(temp_data_file):
    contacts_app.save_contacts([{"name": "张三", "phone": "13800000000", "city": "杭州"}])

    raw = temp_data_file.read_text(encoding="utf-8")
    assert "张三" in raw, "ensure_ascii=False 应让中文原样写入"
    assert json.loads(raw)[0]["name"] == "张三"


def test_空列表保存后仍然是空数组(temp_data_file):
    """TC-018 的底层验证：删光记录后必须写成 []，不能是 null 或空文件。"""
    contacts_app.save_contacts([])

    raw = temp_data_file.read_text(encoding="utf-8").strip()
    assert raw == "[]"
    assert contacts_app.load_contacts() == []
