# BRAID-DSPy Integration Guide

## Overview

BRAID-DSPy integrates seamlessly with the DSPy framework, providing structured reasoning capabilities through Guided Reasoning Diagrams (GRD).

## Installation

```bash
pip install braid-dspy
```

## Basic Integration

### 1. Configure DSPy

First, configure DSPy with your language model:

```python
import dspy

# For OpenAI
lm = dspy.OpenAI(model="gpt-4", api_key="your-api-key")
dspy.configure(lm=lm)

# For other providers, use appropriate DSPy LM class
```

### 2. Use BRAID Module

```python
from braid import BraidReasoning

braid = BraidReasoning()
result = braid(problem="Your problem here")
```

## Advanced Integration

### Using with DSPy Optimizers

BRAID works with DSPy's optimization framework:

```python
from braid import BraidReasoning, BraidOptimizer
from dspy.teleprompt import MIPROv2

# Create base optimizer
base_optimizer = MIPROv2()

# Create BRAID optimizer
braid_optimizer = BraidOptimizer(base_optimizer=base_optimizer)

# Optimize
optimized_braid = braid_optimizer.optimize(braid, trainset)
```

### Custom Signatures

You can use BRAID signatures in your own DSPy modules:

```python
from braid.signatures import BraidPlanSignature
import dspy

class MyModule(dspy.Module):
    def __init__(self):
        super().__init__()
        self.plan = dspy.Predict(BraidPlanSignature)
    
    def forward(self, problem):
        result = self.plan(problem=problem)
        return result.grd
```

### Combining with Other DSPy Modules

BRAID modules can be combined with other DSPy modules:

```python
import dspy
from braid import BraidReasoning

class ComplexPipeline(dspy.Module):
    def __init__(self):
        super().__init__()
        self.braid = BraidReasoning()
        self.validator = dspy.Predict("answer -> validated_answer")
        self.formatter = dspy.Predict("answer -> formatted_output")
    
    def forward(self, problem):
        # Use BRAID for reasoning
        braid_result = self.braid(problem=problem)
        
        # Validate answer
        validated = self.validator(answer=braid_result.answer)
        
        # Format output
        formatted = self.formatter(answer=validated.validated_answer)
        
        return formatted
```

## Best Practices

### 1. GRD Generation

- Use `use_generator=True` for better GRD quality
- Provide `problem_type` hints when possible
- Use pre-generated GRDs for consistent results

### 2. Validation

- Always enable `validate_grd=True` in production
- Check `result.valid` before using results
- Handle errors gracefully

### 3. Optimization

- Use BRAID optimizer with base optimizer for best results
- Provide diverse training examples
- Monitor GRD quality metrics

### 4. Error Handling

```python
from braid import BraidReasoning

braid = BraidReasoning()

try:
    result = braid(problem="Your problem")
    if result.valid:
        # Use result
        print(result.answer)
    else:
        # Handle invalid result
        print(f"Error: {result.error}")
except Exception as e:
    # Handle exception
    print(f"Exception: {e}")
```

## Performance Considerations

1. **GRD Generation**: First call may be slower due to GRD generation
2. **Caching**: Consider caching GRDs for repeated problems
3. **Execution Steps**: Limit `max_execution_steps` for faster execution
4. **Parallel Processing**: Use `num_threads` in optimizer for parallel optimization

## Troubleshooting

### Common Issues

1. **LM Not Configured**: Ensure DSPy is configured with `dspy.configure(lm=...)`
2. **Invalid GRD**: Check GRD syntax, enable validation
3. **Execution Errors**: Check `execution_trace` for step-by-step errors
4. **Import Errors**: Ensure all dependencies are installed

### Debugging

Enable verbose output:

```python
import logging
logging.basicConfig(level=logging.DEBUG)

# Your BRAID code here
```

Check execution trace:

```python
result = braid(problem="Your problem")
for trace in result.execution_trace:
    print(trace)
```

## Migration Guide

### From Standard DSPy

If you're using standard DSPy modules:

1. Replace `dspy.ChainOfThought` with `BraidReasoning`
2. Update result handling to use `BraidResult`
3. Add GRD validation where needed

### Example Migration

**Before:**
```python
import dspy

class MyModule(dspy.Module):
    def __init__(self):
        super().__init__()
        self.reasoning = dspy.ChainOfThought("problem -> answer")
    
    def forward(self, problem):
        return self.reasoning(problem=problem)
```

**After:**
```python
from braid import BraidReasoning

class MyModule(dspy.Module):
    def __init__(self):
        super().__init__()
        self.reasoning = BraidReasoning()
    
    def forward(self, problem):
        result = self.reasoning(problem=problem)
        return result.answer
```

