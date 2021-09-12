import os
import sys
import unittest

sys.path.append(os.path.join(__file__, '..'))
sys.path.append(os.path.join(__file__, '../../src'))
print(sys.path)

from src.ctrl import Ctrl
from testcase.data import TestData


class TestCtrl(unittest.TestCase):
    def setUp(self):
        self.data = TestData()

    def test_extract_guild(self):
        ctrl = Ctrl()
        ctrl.extract_guild_info(self.data.guild_data)
        self.assertEqual(ctrl.uid_name, dict(zip(self.data.ids, self.data.names)))
        self.assertEqual(ctrl.all_uid, set(self.data.ids))

    def test_extract_attack(self):
        ctrl = Ctrl()
        ctrl.extract_guild_info(self.data.guild_data)
        ctrl.extract_date_info(0, self.data.attack_data)
