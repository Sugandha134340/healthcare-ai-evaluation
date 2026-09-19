## Regression Testing

### Initial Test Result

The regression suite was executed to verify the booking, cancellation, and rescheduling workflows:

```bash
pytest tests/test_regression.py -v
```

Result:

```text
3 passed
```

### Deliberate Degradation

The booking routing logic was intentionally changed from:

```text
book_appointment
```

to:

```text
check_availability
```

This simulated an agent pipeline regression where the agent selected the wrong tool for a booking request.

The regression suite successfully detected the failure:

```text
test_booking_regression FAILED
```

while the cancellation and rescheduling tests remained unaffected.

### Recovery

The booking routing logic was restored to:

```text
book_appointment
```

The regression suite was executed again:

```bash
pytest tests/test_regression.py -v
```

Result:

```text
3 passed
```

### Conclusion

The regression suite successfully detected a deliberate degradation in the booking workflow and confirmed that the system recovered correctly after the intended routing behavior was restored.
