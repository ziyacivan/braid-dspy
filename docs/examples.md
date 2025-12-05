# BRAID-DSPy Examples

## Basic Usage

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

## Optimization Example

```python
import dspy
from braid import BraidReasoning, BraidOptimizer
from dspy.teleprompt import MIPROv2

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
base_optimizer = MIPROv2()
optimizer = BraidOptimizer(base_optimizer=base_optimizer)

# Optimize
optimized_braid = optimizer.optimize(braid, trainset)

# Evaluate
testset = [{"problem": "Test problem", "answer": "Test answer"}]
metrics = optimizer.evaluate(optimized_braid, testset)
print(metrics)
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

## Working with GRD Generator

```python
from braid.generator import GRDGenerator

generator = GRDGenerator()

# Generate GRD
result = generator.generate(
    problem="Your problem",
    problem_type="math"
)

if result["valid"]:
    print(result["grd"])
    print(result["parsed_structure"])

# Add custom example
generator.add_example(
    problem="Example problem",
    grd="```mermaid\nflowchart TD\n    A --> B\n```"
)

# Get template
template = generator.get_template("math")
print(template)
```

## Parsing Mermaid Diagrams

```python
from braid.parser import MermaidParser

parser = MermaidParser()

mermaid_code = """```mermaid
flowchart TD
    Start[Start] --> End[End]
```"""

# Parse
grd = parser.parse(mermaid_code)

# Get execution order
execution_order = grd.get_execution_order()
print(execution_order)

# Get nodes and edges
print(f"Nodes: {len(grd.nodes)}")
print(f"Edges: {len(grd.edges)}")

# Extract execution steps
steps = parser.extract_execution_steps(grd)
for step in steps:
    print(f"{step['step_id']}: {step['label']}")
```

## Integration with DSPy Pipelines

```python
import dspy
from braid import BraidReasoning

class MyPipeline(dspy.Module):
    def __init__(self):
        super().__init__()
        self.braid = BraidReasoning()
        self.other_module = dspy.Predict("problem -> answer")
    
    def forward(self, problem):
        # Use BRAID for complex reasoning
        braid_result = self.braid(problem=problem)
        
        # Use result in other modules
        final_result = self.other_module(problem=braid_result.answer)
        return final_result
```

