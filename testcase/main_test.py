import sys
import unittest
from os.path import dirname, join

sys.path.append(dirname(__file__))
sys.path.append(join(dirname(dirname(__file__)), 'src'))

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
