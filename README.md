# Two-Lane One-Time Pad Protocol

A novel 4-party asynchronous secure communication protocol using structured one-time pad allocation to ensure perfect secrecy while preventing pad reuse and maintaining efficient resource utilization.

## 🔐 Overview

The **Two-Lane OTP Protocol** extends traditional two-party one-time pad encryption to support four parties (Alice, Bob, Charlie, and Ellen) with strict secrecy constraints. The protocol achieves perfect secrecy through innovative bidirectional pad distribution across two independent lanes.

### Key Innovation: Two-Lane Architecture

The protocol divides the pad sequence into two independent lanes:
- **Lane 1 (Even Indexes)**: Shared by Alice (forward) and Bob (backward)
- **Lane 2 (Odd Indexes)**: Shared by Charlie (forward) and Ellen (backward)

This structure ensures balanced pad consumption, prevents premature exhaustion, and maintains the fundamental principle that **no pad is ever reused**.

## 🎯 Key Features

### Security Properties
- **Perfect Secrecy**: One-time pad encryption provides information-theoretic security
- **No Pad Reuse**: Structural guarantees prevent cryptographic compromise
- **Secrecy Constraint**: Maximum undelivered message gap (d) enforcement
- **XOR Encryption**: Simple, fast, and provably secure

### Efficiency
- **Balanced Distribution**: Prevents single-party pad exhaustion
- **Parallel Operation**: Multiple parties send without interference
- **Linear Wastage**: Bounded by O(d) ≤ W(n,d) ≤ 0.2n + O(d)
- **Validated Performance**: Monte Carlo simulation with 6000+ trials

## 🏗️ Protocol Architecture

### Pad Allocation Scheme

```
Pad Sequence: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, ...]
              ╱                              ╲
    Lane 1 (Even): 0, 2, 4, 6, 8...    Lane 2 (Odd): 1, 3, 5, 7, 9...
         ╱        ╲                         ╱        ╲
    Alice →        ← Bob              Charlie →      ← Ellen
  (forward)      (backward)          (forward)    (backward)
```

### Party Assignments
- **Alice**: Even-indexed pads, forward traversal (0, 2, 4, 6, ...)
- **Bob**: Even-indexed pads, backward traversal (..., 8, 6, 4, 2, 0)
- **Charlie**: Odd-indexed pads, forward traversal (1, 3, 5, 7, ...)
- **Ellen**: Odd-indexed pads, backward traversal (..., 9, 7, 5, 3, 1)

## 📊 Technical Specifications

### Configuration Parameters
- **n**: Total number of pads (default: 1000)
- **L**: Length of each pad in bits (default: 4028)
- **d**: Maximum undelivered message gap (default: 40)

### Cryptographic Operations

**Encryption:**
```
ciphertext = message ⊕ pad
```

**Decryption:**
```
message = ciphertext ⊕ pad
```

Where ⊕ represents the XOR operation.

## 🚀 Getting Started

### Prerequisites
- Python 3.8 or higher
- No external dependencies (uses only standard library)

### Installation

```bash
git clone https://github.com/vilna-git/two-lane-otp-protocol.git
cd two-lane-otp-protocol
```

## 💻 Usage

### Running the Protocol

```python
from protocol import OneTimePadProtocol

# Initialize protocol
protocol = OneTimePadProtocol(n=1000, L=4028, d=40)

# Send a message (Alice)
message = 0b110101  # Example binary message
ciphertext, pad_index = protocol.send_message("Alice", message)

# Receive and decrypt
decrypted = protocol.get_message(ciphertext, pad_index)

# Verify
assert message == decrypted
```

### Running Monte Carlo Simulation

```bash
# Run with default 1000 trials
python3 simulation.py

# Expected output:
# Average Wasted Pads: {'a': 197, 'b': 213, 'c': 219}
```

**Simulation Scenarios:**
- **Scenario A**: One random party sends all messages
- **Scenario B**: Two random parties send messages
- **Scenario C**: All four parties send messages with random distribution

## 🧪 Validation Results

### Empirical Performance (n=1000, L=4028, d=40)

| Scenario | Description | Avg Wasted Pads | Wastage % |
|----------|-------------|-----------------|-----------|
| A | Single party active | ~197 | 19.7% |
| B | Two parties active | ~213 | 21.3% |
| C | All parties active | ~219 | 21.9% |

### Theoretical Bounds

**Pad Wastage Formula:**
```
O(d) ≤ W(n,d) ≤ 0.2n + O(d)
```

Where:
- **Lower bound**: Minimal wastage from secrecy constraint enforcement
- **Upper bound**: Linear scaling with pad sequence length
- **0.2n term**: Empirically derived from simulation results

### Wastage Analysis

**Sources of Wastage:**
1. **Unused lanes**: When only one lane is active (single party scenario)
2. **Forced discards**: Secrecy constraint (d) prevents using old pads
3. **Randomized selection**: Stochastic message distribution reduces efficiency

**Key Finding**: Wastage remains well below theoretical maximum of n/2, demonstrating protocol efficiency.

## 🔍 Protocol Implementation

### Core Components

**1. Initialization**
```python
class OneTimePadProtocol:
    def __init__(self, n, L, d):
        self.n = n  # Total pads
        self.L = L  # Pad length
        self.d = d  # Max undelivered gap
        self.pad_sequence = [random.getrandbits(L) for _ in range(n)]
        # ... party assignments
```

**2. Message Sending**
```python
def send_message(self, sender, message):
    pad_index = self.parties[sender].pop(0)
    self.last_used_pad[sender] = pad_index
    ciphertext = self.xor_encrypt(message, self.pad_sequence[pad_index])
    return ciphertext, pad_index
```

**3. Secrecy Constraint Enforcement**
```python
def enforce_constraints(self, sender):
    for party in self.parties:
        if party != sender:
            if self.last_used_pad[sender] - self.last_used_pad[party] > self.d:
                raise ValueError("Secrecy condition violated")
```

## 📁 Project Structure

```
two-lane-otp-protocol/
├── protocol.py         # Core protocol implementation
├── simulation.py       # Monte Carlo validation
├── README.md           # This file
├── LICENSE             # MIT License
└── .gitignore          # Git ignore rules
```

## 🎓 Theoretical Foundation

### Perfect Secrecy

The protocol achieves **information-theoretic security** through one-time pad encryption:

**Shannon's Theorem**: If the key is:
1. Truly random
2. As long as the message
3. Never reused

Then the ciphertext reveals **zero information** about the plaintext.

### Protocol Guarantees

✅ **No pad reuse**: Structural lane separation prevents accidental reuse  
✅ **Perfect secrecy**: XOR with random pads provides information-theoretic security  
✅ **Bounded wastage**: Linear scaling ensures practical efficiency  
✅ **Asynchronous operation**: Parties communicate independently

## 🐛 Troubleshooting

**Issue**: "Secrecy condition violated"
- **Cause**: Gap between party pad usage exceeds d
- **Solution**: Increase d parameter or ensure more balanced message distribution

**Issue**: "No available pads for [party]"
- **Cause**: Party exhausted allocated pads
- **Solution**: Increase n (total pads) or redistribute messages

## 📚 Academic Context

**Course**: Cryptography and Network Security  
**Institution**: NYU (April 2025)  
**Student**: Oleksandra Kovalenko

### Assignment Objectives
- Design a multi-party secure communication protocol
- Implement one-time pad encryption with perfect secrecy
- Validate efficiency through Monte Carlo simulation
- Analyze pad wastage and resource utilization

## 🔬 Future Enhancements

Potential improvements:
- Dynamic pad generation for unlimited messages
- Key distribution mechanism for practical deployment
- Adaptive d parameter based on network conditions
- Integration with quantum random number generators

## 📄 License

MIT License - Free to use for educational and research purposes.

## 📧 Contact

Questions or feedback? Open an issue on GitHub.

## 🙏 Acknowledgments

- Prof. [Course Instructor] for cryptography fundamentals
- NYU Computer Science Department
- Shannon's seminal work on information theory

---

**⚠️ Security Note**: This is an educational implementation. Production cryptographic systems require:
- Secure random number generation
- Authenticated key distribution
- Side-channel attack prevention
- Formal security audits

**Never roll your own crypto for production use!**
