# Basic Usage

## Simple Problem Solving

```python
import dspy
from braid import BraidReasoning

# Configure DSPy
lm = dspy.OpenAI(model="gpt-4", api_key="your-api-key")
dspy.configure(lm=lm)

# Create BRAID module
braid = BraidReasoning()

# Solve a problem
result = braid(problem="If a train travels 120 km in 2 hours, what is its speed?")

print(f"Answer: {result.answer}")
print(f"\nGRD:\n{result.grd}")
print(f"\nReasoning Steps:")
for step in result.reasoning_steps:
    print(f"  {step['step_number']}. {step['label']}: {step['result']}")
```

## Using Pre-generated GRD

```python
from braid import BraidReasoning

braid = BraidReasoning()

pre_generated_grd = """```mermaid
flowchart TD
    Start[Problem Analysis] --> Identify[Identify values]
    Identify --> Calculate[Calculate]
    Calculate --> Answer[Final Answer]
```"""

result = braid(problem="Your problem", grd=pre_generated_grd)
print(result.answer)
```

## Custom Configuration

```python
from braid import BraidReasoning

braid = BraidReasoning(
    use_generator=True,
    max_execution_steps=15,
    validate_grd=True
)
```

