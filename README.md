# automata-realtime-validation
# Designing Automata for Real-Time Applications

**Author:** S G S V GANESH  
**University:** SRM Institute of Science and Technology  

This repository features formal DFA designs for real-time validation (ATM PINs, email syntax, and password policies). It includes executable Python scripts, automated unit tests, a GitHub Actions CI pipeline, and an interactive web simulator deployable on GitHub Pages.

**Interactive Web Simulator:** [View Live Demo Here](https://<LUCKYHAPPYMANI>.github.io/automata-realtime-validation/) *(Replace with your actual GitHub Pages link once deployed)*

---

## 1. ATM PIN Verification Automaton
* **Alphabet ($\Sigma$):** $D_1 = \{1..9\}$, $0 = \{0\}$, $X = \text{non-digits}$
* **Language ($L_{\text{PIN}}$):** $\{ w \in \Sigma^* \mid |w| = 4 \land w_1 \in D_1 \land w_2, w_3, w_4 \in (D_1 \cup \{0\}) \}$ (`[1-9][0-9]{3}`)
* **Accepting State:** `q4`
* **Limitations:** Validates 4-digit lexical structure in $O(1)$ memory, but cannot verify the cryptographic PIN hash against the user's smartcard/HSM or track cross-session account lockout counters.

---

## 2. Email-Format Validation Automaton
* **Alphabet ($\Sigma$):** $A = \{\text{a-z, A-Z, 0-9}\}$, `@`, `.`, $O = \text{other}$
* **Language ($L_{\text{Email}}$):** `[a-zA-Z0-9]+(\.[a-zA-Z0-9]+)*@[a-zA-Z0-9]+(\.[a-zA-Z0-9]+)+`
* **Accepting State:** `q5`
* **Limitations:** Cannot parse nested RFC 5322 comments (which require a Context-Free Grammar / Pushdown Automaton) and cannot verify live DNS `MX` records or mailbox existence.

---

## 3. Password Composition Automaton (Product DFA)
* **Alphabet ($\Sigma$):** $U = \{\text{A-Z}\}$, $D = \{\text{0-9}\}$, $L = \{\text{a-z}\}$
* **Language ($L_{\text{Pass}}$):** Alphanumeric strings containing at least one uppercase letter ($U$) and at least one digit ($D$).
* **States:** $Q = \{q_{00}, q_{10}, q_{01}, q_{11}\}$ tracking $(\text{has\_U}, \text{has\_D})$.
* **Accepting State:** `q11`
* **Limitations:** Combining $k$ independent character classes with minimum length $m$ and repeat constraints causes $O(2^k \cdot m)$ state explosion. Cannot compare `password == confirm_password` (non-regular language $\{ww\}$) or query external breach databases.

---

## 4. Syntax Validation vs. Semantic/Business Rules

| Feature | Syntax Validation (Finite Automaton) | Semantic / Business Rules (App Layer) |
| :--- | :--- | :--- |
| **Scope** | Lexical structure & pattern conformance | Contextual truth, authorization, state |
| **Complexity** | $O(n)$ time, $O(1)$ space | Database I/O, DNS lookups, hashing |
| **Sufficiency** | Sufficient for fast front-line rejection of malformed strings | Required for cross-field matching (`w == w`), DB uniqueness, and rate-limiting |

---

## 5. Project Structure

* `dfa_validator.py` - Core Python execution engine and terminal demonstration.
* `test_dfa.py` - Automated `unittest` suite validating acceptance criteria.
* `index.html` - Interactive web-based state tracer (HTML/JS/Tailwind).
* `.github/workflows/ci.yml` - Continuous Integration pipeline.

## 6. How to Run Locally

```bash
# Run the terminal trace demonstration
python dfa_validator.py

# Run the automated unit tests
python test_dfa.py
