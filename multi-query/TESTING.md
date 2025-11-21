# Multi-Query CLI Testing

## Autotest Suite

This directory includes an automated test suite for the multi-query CLI.

### Running Tests

```bash
cd /home/fong/Projects/mini-rag/multi-query
./test-cli.sh
```

### Test Coverage

The autotest validates:

1. **No Arguments Behavior** - Shows error message + available sources list
2. **--list-sources Flag** - Lists all available RAG sources
3. **--help Flag** - Displays usage help
4. **Invalid JSON Handling** - Gracefully handles malformed JSON
5. **Empty Queries Array** - Handles empty queries appropriately
6. **Missing Queries Key** - Shows error + sources when queries key absent
7. **Example File Validation** - Verifies example-queries.json exists and is valid
8. **--list-pdfs Flag** - Lists all PDFs with metadata
9. **Script Permissions** - Ensures run-multiquery.sh is executable
10. **File Existence** - Confirms main Python script exists

### Expected Output

All tests should pass with green checkmarks (✓). If any test fails, the script exits with code 1 and shows which tests failed in red (✗).

### Test Results Example

```
==========================================
Test Summary
==========================================
Total tests: 10
Passed:      10
Failed:      0

All tests passed! ✓
```

### Adding New Tests

To add a new test, follow this pattern in `test-cli.sh`:

```bash
# Test N: Description
run_test "Test description" "$MAIN_SCRIPT --some-flag"
OUTPUT=$($MAIN_SCRIPT --some-flag 2>&1 || true)
if echo "$OUTPUT" | grep -q "expected pattern"; then
    print_result "Test name" "PASS" "Success message"
else
    print_result "Test name" "FAIL" "Failure message"
fi
```

### CI/CD Integration

This test suite can be integrated into CI/CD pipelines:

```bash
# In your CI/CD script
cd multi-query
./test-cli.sh || exit 1
```

## Manual Testing

For manual testing, try these commands:

```bash
# Show error + sources (new feature)
./run-multiquery.sh

# List sources explicitly
./run-multiquery.sh --list-sources

# Query with JSON
./run-multiquery.sh --json '{"queries":["What is SOLID?"]}'

# Query with file
./run-multiquery.sh --json-file example-queries.json

# List PDFs
./run-multiquery.sh --list-pdfs
```
