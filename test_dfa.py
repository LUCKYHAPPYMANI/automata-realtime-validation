import unittest
from dfa_validator import PIN_DFA, EMAIL_DFA, PASS_DFA

class TestRealTimeAutomata(unittest.TestCase):

    def test_atm_pin_dfa(self):
        self.assertTrue(PIN_DFA.validate("4829")[0])
        self.assertTrue(PIN_DFA.validate("9000")[0])
        self.assertFalse(PIN_DFA.validate("0123")[0])
        self.assertFalse(PIN_DFA.validate("482")[0])
        self.assertFalse(PIN_DFA.validate("48291")[0])
        self.assertFalse(PIN_DFA.validate("48a9")[0])

    def test_email_dfa(self):
        self.assertTrue(EMAIL_DFA.validate("alex.99@uni.edu")[0])
        self.assertTrue(EMAIL_DFA.validate("dev@s.co.in")[0])
        self.assertFalse(EMAIL_DFA.validate("@uni.edu")[0])
        self.assertFalse(EMAIL_DFA.validate("a..b@u.edu")[0])
        self.assertFalse(EMAIL_DFA.validate("a@b@c.com")[0])
        self.assertFalse(EMAIL_DFA.validate("a@b.")[0])

    def test_password_dfa(self):
        self.assertTrue(PASS_DFA.validate("aB3")[0])
        self.assertTrue(PASS_DFA.validate("9Z")[0])
        self.assertTrue(PASS_DFA.validate("Pass123")[0])
        self.assertFalse(PASS_DFA.validate("password")[0])
        self.assertFalse(PASS_DFA.validate("Admin")[0])
        self.assertFalse(PASS_DFA.validate("12345")[0])

if __name__ == "__main__":
    unittest.main(verbosity=2)