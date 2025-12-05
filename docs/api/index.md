# API Reference

This section provides detailed API documentation for BRAID-DSPy.

```{toctree}
:maxdepth: 2

module
parser
generator
optimizer
signatures
```

## Core Classes

### BraidReasoning

Main module for BRAID reasoning in DSPy.

```{eval-rst}
.. autoclass:: braid.module.BraidReasoning
   :members:
   :undoc-members:
   :show-inheritance:
```

### BraidResult

Result object returned by BraidReasoning module.

```{eval-rst}
.. autoclass:: braid.module.BraidResult
   :members:
   :undoc-members:
```

## Parser

### MermaidParser

Parser for Mermaid flowchart diagrams.

```{eval-rst}
.. autoclass:: braid.parser.MermaidParser
   :members:
   :undoc-members:
   :show-inheritance:
```

### GRDStructure

Structure representing a parsed GRD.

```{eval-rst}
.. autoclass:: braid.parser.GRDStructure
   :members:
   :undoc-members:
```

## Generator

### GRDGenerator

Generator for Guided Reasoning Diagrams.

```{eval-rst}
.. autoclass:: braid.generator.GRDGenerator
   :members:
   :undoc-members:
   :show-inheritance:
```

## Optimizer

### BraidOptimizer

BRAID-aware optimizer for DSPy.

```{eval-rst}
.. autoclass:: braid.optimizer.BraidOptimizer
   :members:
   :undoc-members:
   :show-inheritance:
```

### GRDMetrics

Metrics for evaluating GRD quality.

```{eval-rst}
.. autoclass:: braid.optimizer.GRDMetrics
   :members:
   :undoc-members:
```

## Signatures

### BraidPlanSignature

Signature for GRD planning phase.

```{eval-rst}
.. autoclass:: braid.signatures.BraidPlanSignature
   :members:
   :undoc-members:
   :show-inheritance:
```

### BraidExecuteSignature

Signature for GRD execution phase.

```{eval-rst}
.. autoclass:: braid.signatures.BraidExecuteSignature
   :members:
   :undoc-members:
   :show-inheritance:
```

