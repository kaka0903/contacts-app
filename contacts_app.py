"""命令行通讯录 v1.0

支持增删改查、模糊搜索、数据持久化。
数据保存在同目录的 contacts.json，重启程序不丢失。

运行：python contacts_app.py
"""

import json

DATA_FILE = "contacts.json"


# ==================================================================
# 数据层：只管读写文件，不管界面
# ==================================================================

def load_contacts():
    """
    读取 contacts.json，返回联系人列表。
    文件不存在时返回 []，不能崩。
    """
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def save_contacts(contacts):
    """把联系人列表写入 contacts.json。"""
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(contacts, f, ensure_ascii=False, indent=2)


# ==================================================================
# 输入层：只管拿到合法输入，不管业务
# ==================================================================

def input_str(prompt):
    """反复要求输入，直到拿到非空字符串。"""
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("  不能为空，请重新输入")


def input_phone(prompt):
    """反复要求输入，直到拿到 11 位纯数字手机号。"""
    while True:
        value = input(prompt).strip()
        if len(value) == 11 and value.isdigit():
            return value
        print("  手机号必须是 11 位数字")


# ==================================================================
# 业务层：你的主战场
# ==================================================================

def find_by_name(contacts, keyword):
    """
    返回姓名中包含 keyword 的所有联系人（列表）。
    提示：模糊匹配用 `keyword in c["name"]`
    """
    return [c for c in contacts if keyword in c["name"]]


def show_all(contacts):
    """打印所有联系人，表格对齐，末尾显示总人数。"""
    if len(contacts) == 0:
        print("通讯录是空的")
        return

    print(f"  {'姓名':<10}{'手机号':<14}{'城市'}")
    print("  " + "-" * 34)

    for c in contacts:
        print(f"  {c['name']:<10}{c['phone']:<14}{c['city']}")

    print(f"  共 {len(contacts)} 人")


def add_contact(contacts):
    """添加一个联系人，并保存。"""
    name = input_str("姓名:")

    if any(c["name"] == name for c in contacts):
        print(f"  「{name}」已存在")
        return

    phone = input_phone("手机号：")
    city = input_str("城市：")
    contacts.append({"name": name, "phone": phone, "city": city})
    save_contacts(contacts)
    print("保存成功")


def search_contact(contacts):
    """按姓名模糊搜索并打印结果。"""
    keyword = input_str("姓名关键字:")
    matches = find_by_name(contacts, keyword)

    if not matches:
        print("未找到")
    else:
        print(f"  {'姓名':<10}{'手机号':<14}{'城市'}")
        print("  " + "-" * 34)
        for c in matches:
            print(f"  {c['name']:<10}{c['phone']:<14}{c['city']}")
        print(f"  找到 {len(matches)} 条")



def update_contact(contacts):
    """修改联系人。手机号和城市留空表示不修改。"""
    name = input_str("要修改的姓名：")
    matches = find_by_name(contacts, name)

    if not matches:
        print(f"  没有找到「{name}」")
        return
    else:
        target = matches[0]
        print(f"  当前：{target['name']} / {target['phone']} / {target['city']}")

        new_phone = input("新手机号（直接回车跳过）：").strip()
        if new_phone:
            if len(new_phone) == 11 and new_phone.isdigit():
                target["phone"] = new_phone
            else:
                print("  格式不对，手机号未修改")

        new_city = input("新城市（直接回车跳过）：").strip()
        if new_city:
            target["city"] = new_city

        save_contacts(contacts)
        print("  已更新")


def delete_contact(contacts):
    """删除联系人，必须二次确认。"""
    name = input_str("要删除的姓名：")
    matches = find_by_name(contacts, name)
    if not matches:
        return
    else:
        target = matches[0]
        confirm = input("确认删除？(y/n)").strip().lower()
        if confirm != "y":
            print("已取消")
            return
        contacts.remove(target)
        save_contacts(contacts)


# ==================================================================
# 界面层：菜单和主流程（已经写好了，不用改）
# ==================================================================

def show_menu(contacts):
    print()
    print("=" * 34)
    print(f"  通讯录    共 {len(contacts)} 人")
    print("=" * 34)
    print("  1. 查看全部")
    print("  2. 添加联系人")
    print("  3. 搜索")
    print("  4. 修改")
    print("  5. 删除")
    print("  0. 退出")
    print("=" * 34)


def main():
    contacts = load_contacts()

    while True:
        show_menu(contacts)
        choice = input("请选择：").strip()

        if choice == "0":
            print("再见！")
            break
        elif choice == "1":
            show_all(contacts)
        elif choice == "2":
            add_contact(contacts)
        elif choice == "3":
            search_contact(contacts)
        elif choice == "4":
            update_contact(contacts)
        elif choice == "5":
            delete_contact(contacts)
        else:
            print("  无效选项，请输入 0-5")


if __name__ == "__main__":
    main()
