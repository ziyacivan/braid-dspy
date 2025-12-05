# GSM8K Benchmark Example

This example shows how to use BRAID-DSPy with GSM8K grade school math problems.

```python
import dspy
from braid import BraidReasoning

# Configure DSPy
lm = dspy.OpenAI(model="gpt-4")
dspy.configure(lm=lm)

# Sample GSM8K problems
gsm8k_examples = [
    {
        "problem": "Natalia sold clips to 48 of her friends in April, and then she sold half as many clips in May. How many clips did Natalia sell altogether in April and May?",
        "answer": "72"
    },
    {
        "problem": "A train travels 120 km in 2 hours. What is its speed in km/h?",
        "answer": "60"
    }
]

# Create BRAID module
braid = BraidReasoning(use_generator=True)

# Evaluate on examples
for example in gsm8k_examples:
    result = braid(problem=example["problem"])
    print(f"Problem: {example['problem']}")
    print(f"Expected: {example['answer']}")
    print(f"Got: {result.answer}")
    print(f"Valid: {result.valid}\n")
```

