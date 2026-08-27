# 918Tech Multi-Repository Deployment Guide

## 🚀 Complete Deployment Workflow

This guide walks through deploying all repository fixes from fix branches to production.

---

## Phase 1: Review (Day 1)

### 1.1 Review Branches

#### Aiceo - Error Handling & Validation
```bash
cd /path/to/Aiceo
git fetch origin fix/error-handling-and-validation
git checkout fix/error-handling-and-validation

# Review changes
git log --oneline main..fix/error-handling-and-validation
# Output should show 4 files added

# View PR template
cat PR_ERROR_HANDLING.md
```

**Files to Review:**
- `utils/error_handler.py` - 200+ lines (error handling core)
- `utils/validators.py` - 250+ lines (input validation)
- `tests/test_error_handling.py` - 300+ lines (20+ test cases)
- `PR_ERROR_HANDLING.md` - PR template and migration guide

#### SmartThreadManager - Glyph Decoder
```bash
cd /path/to/SmartThreadManager
git fetch origin fix/glyph-decoder-robustness
git checkout fix/glyph-decoder-robustness

# Review changes
git log --oneline main..fix/glyph-decoder-robustness
# Output should show 4 files added

# View PR template
cat PR_GLYPH_DECODER.md
```

**Files to Review:**
- `glyph_decoder.py` - 400+ lines (decoder implementation)
- `test_glyph_decoder.py` - 350+ lines (30+ test cases)
- `GLYPH_DECODER_FIXES.md` - Detailed documentation
- `PR_GLYPH_DECODER.md` - PR template and migration guide

#### esp32-mermaid-flipper - Hardware Testing
```bash
cd /path/to/esp32-mermaid-flipper
git fetch origin fix/hardware-testing-docs
git checkout fix/hardware-testing-docs

# Review changes
git log --oneline main..fix/hardware-testing-docs
# Output should show 4 files added

# View PR template
cat PR_HARDWARE_TESTING.md
```

**Files to Review:**
- `test_hardware.py` - 500+ lines (testing framework)
- `run_hardware_tests.py` - 100+ lines (CLI runner)
- `HARDWARE_TESTING.md` - Detailed documentation
- `PR_HARDWARE_TESTING.md` - PR template and migration guide

### 1.2 Code Review Checklist

- [ ] **Error Handling**
  - [ ] Exception hierarchy is logical
  - [ ] Validators cover all use cases
  - [ ] Decorators work as intended
  - [ ] Logging is configurable
  - [ ] No performance regression

- [ ] **Glyph Decoder**
  - [ ] Braille encoding is correct
  - [ ] Caching improves performance
  - [ ] Error recovery works
  - [ ] Round-trip encoding verified
  - [ ] LLM tokenization functional

- [ ] **Hardware Testing**
  - [ ] All device types supported
  - [ ] Tests cover critical functions
  - [ ] Error handling robust
  - [ ] Reporting clear and detailed
  - [ ] CI/CD integration ready

---

## Phase 2: Local Testing (Day 2)

### 2.1 Test Aiceo

```bash
cd /path/to/Aiceo
git checkout fix/error-handling-and-validation

# Install test dependencies
pip install pytest pytest-cov

# Run test suite
pytest tests/test_error_handling.py -v
# Expected: 20+ tests pass, 0 failures

# Check coverage
pytest tests/test_error_handling.py --cov=utils --cov-report=term-missing
# Expected: 95%+ coverage

# Test integration
python3 << 'EOF'
from utils.error_handler import ErrorHandler, handle_errors
from utils.validators import InputValidator, ValidationError

# Test validator
try:
    InputValidator.validate_email("test@example.com")
    print("✓ Email validation works")
except Exception as e:
    print(f"✗ Email validation failed: {e}")

# Test error handler
handler = ErrorHandler()
handler.log_info("Test log message")
print("✓ Error handler initialized")
EOF
```

**Expected Output:**
```
===== 20 passed in 0.12s =====
✓ Email validation works
✓ Error handler initialized
```

### 2.2 Test SmartThreadManager

```bash
cd /path/to/SmartThreadManager
git checkout fix/glyph-decoder-robustness

# Install test dependencies
pip install pytest pytest-cov

# Run test suite
pytest test_glyph_decoder.py -v
# Expected: 30+ tests pass, 0 failures

# Check coverage
pytest test_glyph_decoder.py --cov=glyph_decoder --cov-report=term-missing
# Expected: 90%+ coverage

# Test performance
python3 << 'EOF'
import time
from glyph_decoder import GlyphDecoder

decoder = GlyphDecoder()
glyphs = '⠁⠂⠄⠈' * 25  # 100 glyphs

# Warm up
for g in glyphs:
    decoder.decode(g)

# Measure
start = time.time()
for g in glyphs:
    decoder.decode(g)
end = time.time()

stats = decoder.get_stats()
print(f"100 glyphs in {(end-start)*1000:.1f}ms")
print(f"Stats: {stats}")
EOF
```

**Expected Output:**
```
===== 30 passed in 0.18s =====
100 glyphs in 5.2ms
Stats: {'decoded': 104, 'cached': 100, 'failed': 0}
```

### 2.3 Test esp32-mermaid-flipper

```bash
cd /path/to/esp32-mermaid-flipper
git checkout fix/hardware-testing-docs

# Install test dependencies
pip install pyserial

# Option A: With hardware connected
python3 run_hardware_tests.py
# Expected: All devices pass tests

# Option B: Without hardware (dry run)
python3 << 'EOF'
from test_hardware import HardwareTestSuite, DeviceStatus

suite = HardwareTestSuite()
print(f"✓ Hardware test suite initialized")
print(f"✓ Ready for {len(suite.testers)} device(s)")
EOF
```

**Expected Output (with hardware):**
```
ESP32-S3-Camera                        [✓ PASS]
ESP32-WROOM-32E                        [✓ PASS]
Flipper-Zero                           [✓ PASS]
```

---

## Phase 3: Merge & Deploy (Day 3-4)

### 3.1 Create Pull Requests

#### For Aiceo
```bash
cd /path/to/Aiceo
git checkout fix/error-handling-and-validation

# Create PR with description from PR_ERROR_HANDLING.md
# Title: "Add error handling and input validation"
# Description: Copy from PR_ERROR_HANDLING.md
# Reviewers: Suggest team members
# Labels: enhancement, testing
```

#### For SmartThreadManager
```bash
cd /path/to/SmartThreadManager
git checkout fix/glyph-decoder-robustness

# Create PR with description from PR_GLYPH_DECODER.md
# Title: "Add robust glyph decoder with braille encoding"
# Description: Copy from PR_GLYPH_DECODER.md
# Reviewers: Suggest team members
# Labels: enhancement, performance
```

#### For esp32-mermaid-flipper
```bash
cd /path/to/esp32-mermaid-flipper
git checkout fix/hardware-testing-docs

# Create PR with description from PR_HARDWARE_TESTING.md
# Title: "Add hardware testing infrastructure"
# Description: Copy from PR_HARDWARE_TESTING.md
# Reviewers: Suggest team members
# Labels: enhancement, testing, hardware
```

### 3.2 Merge Strategy

#### Option A: Squash Merge (Recommended)
```bash
# Keep history clean
git checkout main
git pull origin main
git merge --squash fix/error-handling-and-validation
git commit -m "Add error handling and input validation (squashed)"
git push origin main
```

#### Option B: Regular Merge
```bash
# Preserve full history
git checkout main
git pull origin main
git merge fix/error-handling-and-validation
git push origin main
```

#### Option C: Rebase & Merge
```bash
# Linear history
git checkout main
git pull origin main
git merge --rebase fix/error-handling-and-validation
git push origin main
```

### 3.3 Merge Checklist

- [ ] **Aiceo**
  - [ ] PR review complete (2+ approvals)
  - [ ] All tests pass
  - [ ] Code coverage >85%
  - [ ] No conflicts with main
  - [ ] Merge to main
  - [ ] Delete fix branch

- [ ] **SmartThreadManager**
  - [ ] PR review complete (2+ approvals)
  - [ ] All tests pass
  - [ ] Performance verified
  - [ ] No conflicts with main
  - [ ] Merge to main
  - [ ] Delete fix branch

- [ ] **esp32-mermaid-flipper**
  - [ ] PR review complete (2+ approvals)
  - [ ] Hardware tests pass
  - [ ] Documentation complete
  - [ ] No conflicts with main
  - [ ] Merge to main
  - [ ] Delete fix branch

---

## Phase 4: CI/CD Integration (Day 4)

### 4.1 GitHub Actions Setup

#### Create `.github/workflows/tests.yml`
```yaml
name: Tests
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [3.9, '3.10', 3.11]
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: ${{ matrix.python-version }}
      - run: pip install -r requirements-test.txt
      - run: pytest -v --cov --cov-report=xml
      - uses: codecov/codecov-action@v3
```

#### Create `requirements-test.txt`
```
pytest>=7.0
pytest-cov>=3.0
pyserial>=3.5
```

### 4.2 GitHub Actions for Hardware Testing

#### Create `.github/workflows/hardware.yml`
```yaml
name: Hardware Tests
on: [push]
if: github.ref == 'refs/heads/main'

jobs:
  hardware:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - run: pip install pyserial
      - name: Run hardware tests
        run: python3 run_hardware_tests.py
        continue-on-error: true
```

### 4.3 Set Up Branch Protection

For each repository:

1. Go to Settings → Branches
2. Add rule for `main` branch:
   - ✓ Require pull request reviews before merging
   - ✓ Dismiss stale pull request approvals
   - ✓ Require status checks to pass before merging
   - ✓ Require branches to be up to date before merging
   - ✓ Include administrators

### 4.4 Enable Code Coverage Reports

```bash
# For each repo, ensure CodeCov is enabled
# Visit: https://codecov.io/gh/918Tech/[repo]
```

---

## Phase 5: Deployment to Production (Day 5)

### 5.1 Pre-Deployment Checklist

- [ ] All tests passing on main branch
- [ ] Code coverage >85% on all repos
- [ ] Documentation updated
- [ ] No breaking changes
- [ ] Performance validated
- [ ] Security review complete
- [ ] Team notified

### 5.2 Deployment Steps

#### Aiceo Deployment
```bash
cd /path/to/Aiceo
git checkout main
git pull origin main

# Update requirements if needed
pip install -r requirements.txt

# Run full test suite
pytest tests/ -v

# Deploy to staging
# ./deploy.sh staging

# Deploy to production
# ./deploy.sh production
```

#### SmartThreadManager Deployment
```bash
cd /path/to/SmartThreadManager
git checkout main
git pull origin main

# Run full test suite
pytest -v

# Deploy
# Depends on your deployment method
```

#### esp32-mermaid-flipper Deployment
```bash
cd /path/to/esp32-mermaid-flipper
git checkout main
git pull origin main

# Update firmware if needed
# ./scripts/build_firmware.sh

# Run hardware tests
python3 run_hardware_tests.py

# Deploy
# Your deployment process here
```

### 5.3 Post-Deployment Verification

```bash
# Check services are running
systemctl status aiceo
systemctl status smartthreads

# Verify functionality
curl http://localhost:8000/health  # Aiceo

# Check logs for errors
tail -f /var/log/aiceo.log
tail -f /var/log/smartthreads.log

# Monitor error rates
# Check your monitoring dashboard
```

### 5.4 Rollback Plan

If issues are encountered:

```bash
# Revert to previous version
git revert HEAD
git push origin main

# Or reset to previous commit
git reset --hard <previous-commit>
git push -f origin main

# Restart services
sudo systemctl restart aiceo
sudo systemctl restart smartthreads
```

---

## Phase 6: Monitoring & Optimization (Ongoing)

### 6.1 Monitoring Dashboards

Set up monitoring for:
- Error rates
- Test pass rates
- Performance metrics (latency, throughput)
- Resource usage (CPU, memory)
- Log aggregation

### 6.2 Metrics to Track

**Aiceo:**
- Validation failure rate
- Error handling recovery rate
- Log volume
- API response times

**SmartThreadManager:**
- Glyph decoding success rate
- Cache hit rate
- Latency (cached vs uncached)
- Memory usage

**esp32-mermaid-flipper:**
- Device connection success rate
- Test pass rate
- Hardware failure rate
- Connection stability

### 6.3 Weekly Review

```bash
# Generate metrics report
python3 << 'EOF'
import json
from datetime import datetime

report = {
    'timestamp': datetime.now().isoformat(),
    'aiceo': {
        'validations_run': 0,
        'validations_passed': 0,
        'errors_logged': 0,
    },
    'smartthreads': {
        'decode_success': 0,
        'cache_hit_rate': 0,
        'avg_latency_ms': 0,
    },
    'hardware': {
        'devices_tested': 3,
        'devices_passed': 3,
        'connection_failures': 0,
    }
}

print(json.dumps(report, indent=2))
EOF
```

### 6.4 Issue Tracking

Create GitHub issues for any:
- Performance regressions
- Test failures
- Validation errors
- Hardware connection issues
- Documentation updates needed

---

## Quick Reference Commands

### Review Branches
```bash
# Aiceo
cd Aiceo && git checkout fix/error-handling-and-validation

# SmartThreadManager
cd SmartThreadManager && git checkout fix/glyph-decoder-robustness

# esp32-mermaid-flipper
cd esp32-mermaid-flipper && git checkout fix/hardware-testing-docs
```

### Run Tests
```bash
# Aiceo
pytest tests/test_error_handling.py -v --cov=utils

# SmartThreadManager
pytest test_glyph_decoder.py -v --cov=glyph_decoder

# esp32-mermaid-flipper
python3 run_hardware_tests.py
```

### Merge Branches
```bash
# For each repo
git checkout main
git merge --squash fix/<branch-name>
git commit -m "Merge: [description]"
git push origin main
git branch -d fix/<branch-name>
```

---

## Troubleshooting

### Test Failures
```bash
# Run with verbose output
pytest -vv --tb=long

# Run specific test
pytest test_file.py::TestClass::test_method -v

# Run with debugging
pytest --pdb -v
```

### Merge Conflicts
```bash
# View conflicts
git status

# Resolve manually
git add <resolved-files>
git commit -m "Resolve merge conflicts"
```

### CI/CD Failures
```bash
# Check logs
git log --oneline

# Review GitHub Actions output
# Visit: https://github.com/918Tech/[repo]/actions
```

---

## Support & Documentation

- **Aiceo**: See `FIXES.md` and `PR_ERROR_HANDLING.md`
- **SmartThreadManager**: See `GLYPH_DECODER_FIXES.md` and `PR_GLYPH_DECODER.md`
- **esp32-mermaid-flipper**: See `HARDWARE_TESTING.md` and `PR_HARDWARE_TESTING.md`
- **Overview**: See `FIXES_SUMMARY.md` and `DEPLOYMENT_READINESS.md`

---

## Success Criteria

✅ **Deployment Complete When:**
- All fix branches merged to main
- All tests passing in CI/CD
- No errors in production logs
- Metrics show normal operation
- Team confirmed working correctly
- Documentation updated
- Monitoring alerts configured

---

**Status**: Ready for deployment
**Last Updated**: 2026-08-27
**Next Review**: After production deployment
