# Unit and Integration Testing in Python

## Overview

Unit testing is the process of verifying that individual functions or methods behave as expected for a wide range of input cases including standard inputs and edge cases. A unit test isolates a function and ensures its logic works as expected, without being affected by external dependencies.

> The goal of a unit test is to answer the question:  
> **"If everything defined outside this function works correctly, does this function also work correctly?"**

In contrast, **integration testing** ensures that different parts of your application work together properly. These tests verify that modules interact correctly, and test code paths end-to-end.

---


## Key Concepts

### Mocking
Mocking replaces real function calls (like HTTP requests or DB queries) with simulated ones during tests, ensuring tests are isolated and deterministic.

### Parameterization
Parameterization runs the same test with different sets of inputs, reducing duplication and improving test coverage.

### Fixtures
Fixtures provide a reliable, repeatable test setup (like sample data or mocked objects).



## Getting Started

### Running Tests

```bash
$ python -m unittest path/to/test_file.py
