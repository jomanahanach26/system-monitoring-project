import unittest
from alarm import Alarm, AlarmManager


class TestAlarm(unittest.TestCase):
    """Testar att larm skapas med giltiga värden."""

    def test_create_alarm(self):
        alarm = Alarm("cpu", 80)
        self.assertEqual(alarm.category, "cpu")
        self.assertEqual(alarm.level, 80.0)

    def test_invalid_category(self):
        with self.assertRaises(ValueError):
            Alarm("network", 50)

    def test_invalid_level(self):
        with self.assertRaises(ValueError):
            Alarm("cpu", 150)


class TestAlarmManager(unittest.TestCase):
    """Testar att larmhanteraren fungerar."""

    def test_add_alarm(self):
        manager = AlarmManager()
        alarm = Alarm("ram", 70)

        manager.add_alarm(alarm)

        self.assertEqual(len(manager.alarms), 1)

    def test_remove_alarm(self):
        manager = AlarmManager()
        alarm = Alarm("cpu", 80)
        manager.add_alarm(alarm)

        manager.remove_alarm(1)

        self.assertEqual(len(manager.alarms), 0)

    def test_sort_alarms(self):
        manager = AlarmManager()

        manager.add_alarm(Alarm("ram", 70))
        manager.add_alarm(Alarm("cpu", 90))
        manager.add_alarm(Alarm("cpu", 50))

        manager.sort_alarms()

        self.assertEqual(
            [(alarm.category, alarm.level) for alarm in manager.alarms],
            [("cpu", 50.0), ("cpu", 90.0), ("ram", 70.0)]
        )


if __name__ == "__main__":
    unittest.main()