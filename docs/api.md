# BRAID-DSPy API Reference

## Core Classes

### BraidReasoning

Main module for BRAID reasoning in DSPy.

```python
from braid import BraidReasoning

braid = BraidReasoning(
    use_generator=True,
    max_execution_steps=20,
    validate_grd=True
)
```

#### Parameters

- `use_generator` (bool): Whether to use GRDGenerator for planning (default: True)
- `max_execution_steps` (int): Maximum number of steps to execute (default: 20)
- `validate_grd` (bool): Whether to validate GRD syntax before execution (default: True)

#### Methods

##### `forward(problem: str, grd: Optional[str] = None, problem_type: Optional[str] = None) -> BraidResult`

Execute BRAID reasoning on a problem.

**Parameters:**
- `problem`: The problem to solve
- `grd`: Optional pre-generated GRD (if None, will be generated)
- `problem_type`: Optional problem type hint for generation

**Returns:** `BraidResult` object

##### `__call__(problem: str, **kwargs) -> BraidResult`

Make the module callable.

### BraidResult

Result object returned by `BraidReasoning`.

**Attributes:**
- `problem` (str): Original problem
- `grd` (str): Generated or provided GRD in Mermaid format
- `parsed_grd` (GRDStructure): Parsed GRD structure
- `reasoning_steps` (List[Dict]): List of reasoning steps executed
- `answer` (str): Final answer
- `execution_trace` (List[Dict]): Execution trace
- `valid` (bool): Whether the result is valid
- `error` (Optional[str]): Error message if invalid

### BraidOptimizer

BRAID-aware optimizer for DSPy.

```python
from braid import BraidOptimizer

optimizer = BraidOptimizer(
    base_optimizer=None,
    grd_quality_weight=0.5,
    execution_quality_weight=0.5
)
```

#### Methods

##### `optimize(module: BraidReasoning, trainset: List[Dict], metric: Optional[Callable] = None, num_threads: int = 1) -> BraidReasoning`

Optimize a BraidReasoning module.

##### `evaluate(module: BraidReasoning, testset: List[Dict], metric: Optional[Callable] = None) -> Dict[str, float]`

Evaluate a BraidReasoning module on a test set.

## Signatures

### BraidPlanSignature

Signature for GRD planning phase.

**Fields:**
- `problem` (InputField): The problem to solve
- `grd` (OutputField): Guided Reasoning Diagram in Mermaid format

### BraidExecuteSignature

Signature for GRD execution phase.

**Fields:**
- `problem` (InputField): The original problem
- `grd` (InputField): The GRD to follow
- `current_step` (InputField): Current step to execute
- `previous_results` (InputField): Results from previous steps
- `step_result` (OutputField): Result of executing current step

## Utility Classes

### MermaidParser

Parser for Mermaid flowchart diagrams.

```python
from braid.parser import MermaidParser

parser = MermaidParser()
grd = parser.parse(mermaid_code)
```

#### Methods

- `parse(mermaid_code: str) -> GRDStructure`: Parse Mermaid code
- `validate(mermaid_code: str) -> Tuple[bool, Optional[str]]`: Validate syntax
- `extract_execution_steps(grd: GRDStructure) -> List[Dict]`: Extract execution steps

### GRDGenerator

Generator for Guided Reasoning Diagrams.

```python
from braid.generator import GRDGenerator

generator = GRDGenerator(
    examples=None,
    max_retries=3,
    temperature=0.3
)
```

#### Methods

- `generate(problem: str, problem_type: Optional[str] = None, custom_instructions: Optional[str] = None) -> Dict`: Generate GRD
- `add_example(problem: str, grd: str)`: Add custom example
- `get_template(problem_type: str) -> Optional[str]`: Get template for problem type

## Utility Functions

### extract_mermaid_code(text: str) -> Optional[str]

Extract Mermaid diagram code from text that may contain markdown code blocks.

### validate_mermaid_syntax(mermaid_code: str) -> bool

Basic validation of Mermaid syntax.

### parse_grd_structure(mermaid_code: str) -> Dict[str, Any]

Parse Mermaid code to extract GRD structure information.

