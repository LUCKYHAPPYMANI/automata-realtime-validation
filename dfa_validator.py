#!/usr/bin/env python3
"""
Task: Designing Automata for Real-Time Applications
Applications:
  1. ATM PIN Verification ([1-9][0-9]{3})
  2. Email-Format Validation (local@domain.tld)
  3. Password Composition Verification (Product DFA: Uppercase x Digit)
"""

class DFA:
    def __init__(self, name: str, start_state: str, accept_states: set, transition_fn):
        self.name = name
        self.start_state = start_state
        self.accept_states = set(accept_states)
        self.transition_fn = transition_fn

    def validate(self, input_str: str):
        state = self.start_state
        trace = [state]
        for ch in input_str:
            state = self.transition_fn(state, ch)
            trace.append(state)
        is_valid = state in self.accept_states
        return is_valid, " -> ".join(trace)


# 1. ATM PIN DFA Transition Function
def pin_delta(state: str, ch: str) -> str:
    if state == "q0":
        return "q1" if ch in "123456789" else "q_dead"
    elif state == "q1":
        return "q2" if ch.isdigit() else "q_dead"
    elif state == "q2":
        return "q3" if ch.isdigit() else "q_dead"
    elif state == "q3":
        return "q4" if ch.isdigit() else "q_dead"
    return "q_dead"


# 2. Email Format DFA Transition Function
def email_delta(state: str, ch: str) -> str:
    is_alnum = ch.isalnum()
    if state == "q0":
        return "q1" if is_alnum else "q_dead"
    elif state == "q1":
        if is_alnum: return "q1"
        if ch == ".": return "q2"
        if ch == "@": return "q3"
    elif state == "q2":
        return "q1" if is_alnum else "q_dead"
    elif state == "q3":
        return "q3_dom" if is_alnum else "q_dead"
    elif state == "q3_dom":
        if is_alnum: return "q3_dom"
        if ch == ".": return "q4"
    elif state == "q4":
        return "q5" if is_alnum else "q_dead"
    elif state == "q5":
        if is_alnum: return "q5"
        if ch == ".": return "q4"
    return "q_dead"


# 3. Password Composition DFA Transition Function (Product DFA: has_U x has_D)
def password_delta(state: str, ch: str) -> str:
    if state == "q_dead" or not ch.isalnum():
        return "q_dead"
    has_u = state in ("q10", "q11") or ch.isupper()
    has_d = state in ("q01", "q11") or ch.isdigit()
    return f"q{int(has_u)}{int(has_d)}"


# Instantiate DFAs
PIN_DFA = DFA("1. ATM PIN Validator", "q0", {"q4"}, pin_delta)
EMAIL_DFA = DFA("2. Email Format Validator", "q0", {"q5"}, email_delta)
PASS_DFA = DFA("3. Password Policy Validator", "q00", {"q11"}, password_delta)


def run_demo():
    test_suite = [
        (PIN_DFA, [
            ("4829", True, "Valid 4-digit PIN"),
            ("9000", True, "Valid PIN with trailing zeros"),
            ("0123", False, "Invalid: starts with leading 0"),
            ("482", False, "Invalid: length < 4"),
            ("48291", False, "Invalid: length > 4"),
            ("48a9", False, "Invalid: contains non-digit"),
        ]),
        (EMAIL_DFA, [
            ("alex.99@uni.edu", True, "Valid standard email"),
            ("dev@s.co.in", True, "Valid multi-part TLD"),
            ("@uni.edu", False, "Invalid: missing local part"),
            ("a..b@u.edu", False, "Invalid: consecutive dots"),
            ("a@b@c.com", False, "Invalid: multiple @ symbols"),
            ("a@b.", False, "Invalid: trailing dot / empty TLD"),
        ]),
        (PASS_DFA, [
            ("aB3", True, "Valid: has lowercase, uppercase, digit"),
            ("9Z", True, "Valid: minimal digit + uppercase"),
            ("Pass123", True, "Valid alphanumeric password"),
            ("password", False, "Invalid: missing uppercase and digit"),
            ("Admin", False, "Invalid: missing digit"),
            ("12345", False, "Invalid: missing uppercase"),
        ]),
    ]

    print("=" * 88)
    print(" FINITE AUTOMATA REAL-TIME VALIDATION DEMONSTRATION")
    print("=" * 88)

    for dfa, cases in test_suite:
        print(f"\n[{dfa.name}]")
        print("-" * 88)
        print(f"{'Input String':<18} | {'Status':<8} | {'Check':<6} | {'State Transition Trace'}")
        print("-" * 88)
        for sample, expected, reason in cases:
            actual, trace = dfa.validate(sample)
            status = "ACCEPT" if actual else "REJECT"
            passed = "PASS" if actual == expected else "FAIL"
            print(f"{sample:<18} | {status:<8} | {passed:<6} | {trace} ({reason})")


if __name__ == "__main__":
    run_demo()