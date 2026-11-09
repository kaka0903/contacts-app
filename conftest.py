"""pytest 根配置。

作用：把项目根目录加入 sys.path，让 tests/ 里可以直接 `from contacts_app import ...`，
不必在每个测试文件里重复写 sys.path.insert。
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
