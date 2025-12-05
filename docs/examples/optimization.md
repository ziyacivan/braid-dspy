# Optimization Example

This example shows how to optimize BRAID modules for better performance.

## Basic Optimization

```python
import dspy
from braid import BraidReasoning, BraidOptimizer

# Configure DSPy
lm = dspy.OpenAI(model="gpt-4")
dspy.configure(lm=lm)

# Create module
braid = BraidReasoning()

# Training examples
trainset = [
    {"problem": "Problem 1", "answer": "Answer 1"},
    {"problem": "Problem 2", "answer": "Answer 2"},
]

# Create optimizer
optimizer = BraidOptimizer()

# Optimize
optimized_braid = optimizer.optimize(braid, trainset)

# Evaluate
testset = [{"problem": "Test problem", "answer": "Test answer"}]
metrics = optimizer.evaluate(optimized_braid, testset)
print(metrics)
```

## Using with Base Optimizer

```python
from dspy.teleprompt import MIPROv2
from braid import BraidReasoning, BraidOptimizer

# Create base optimizer
base_optimizer = MIPROv2()

# Create BRAID optimizer
braid_optimizer = BraidOptimizer(base_optimizer=base_optimizer)

# Optimize
optimized_braid = braid_optimizer.optimize(braid, trainset)
```

## Custom Metrics

```python
from braid import BraidReasoning, BraidOptimizer

def custom_metric(result, expected_answer):
    score = 0.0
    if result.answer and expected_answer:
        if expected_answer.lower() in result.answer.lower():
            score += 0.5
        if result.parsed_grd:
            score += 0.3
        if len(result.reasoning_steps) >= 2:
            score += 0.2
    return score

optimizer = BraidOptimizer()
optimized = optimizer.optimize(braid, trainset, metric=custom_metric)
```

