"""DSPy signatures for BRAID reasoning."""

import dspy


class BraidPlanSignature(dspy.Signature):
    """
    Signature for GRD planning phase.
    
    This signature defines the input/output structure for generating
    a Guided Reasoning Diagram (GRD) from a problem statement.
    """
    problem = dspy.InputField(
        desc="The problem to solve, described clearly and completely"
    )
    
    grd = dspy.OutputField(
        desc="A Guided Reasoning Diagram in Mermaid flowchart format. "
             "The diagram should map out the solution steps, starting with "
             "problem analysis and ending with the final answer. "
             "Use flowchart TD format with clear node labels."
    )


class BraidExecuteSignature(dspy.Signature):
    """
    Signature for GRD execution phase.
    
    This signature defines the input/output structure for executing
    a Guided Reasoning Diagram step by step.
    """
    problem = dspy.InputField(
        desc="The original problem to solve"
    )
    
    grd = dspy.InputField(
        desc="The Guided Reasoning Diagram (Mermaid format) to follow"
    )
    
    current_step = dspy.InputField(
        desc="The current step in the GRD that needs to be executed"
    )
    
    previous_results = dspy.InputField(
        desc="Results from previous steps (if any)",
        default=""
    )
    
    step_result = dspy.OutputField(
        desc="The result of executing the current step. "
             "This should be a clear, concise output that can be used "
             "in subsequent steps."
    )


class BraidReasoningSignature(dspy.Signature):
    """
    Complete BRAID reasoning signature combining planning and execution.
    
    This is a convenience signature that can be used for end-to-end
    BRAID reasoning in a single call.
    """
    problem = dspy.InputField(
        desc="The problem to solve, described clearly and completely"
    )
    
    grd = dspy.OutputField(
        desc="A Guided Reasoning Diagram in Mermaid flowchart format"
    )
    
    reasoning_steps = dspy.OutputField(
        desc="Step-by-step reasoning following the GRD. "
             "Each step should reference the corresponding GRD node."
    )
    
    answer = dspy.OutputField(
        desc="The final answer to the problem"
    )


class BraidStepSignature(dspy.Signature):
    """
    Signature for executing a single step in a GRD.
    
    Used internally by the BRAID module for step-by-step execution.
    """
    step_description = dspy.InputField(
        desc="Description of the step to execute"
    )
    
    context = dspy.InputField(
        desc="Context from previous steps and the original problem"
    )
    
    step_output = dspy.OutputField(
        desc="Output from executing this step"
    )

