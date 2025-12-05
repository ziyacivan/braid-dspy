"""BRAID-aware optimizer for DSPy."""

from typing import Dict, List, Optional, Any, Callable
import dspy
from braid.parser import MermaidParser, GRDStructure
from braid.module import BraidReasoning, BraidResult


class GRDMetrics:
    """Metrics for evaluating GRD quality."""
    
    @staticmethod
    def structural_validity(grd: str) -> float:
        """
        Evaluate structural validity of a GRD.
        
        Returns:
            Score between 0.0 and 1.0 (1.0 = perfectly valid)
        """
        parser = MermaidParser()
        is_valid, _ = parser.validate(grd)
        return 1.0 if is_valid else 0.0
    
    @staticmethod
    def completeness(grd_structure: GRDStructure) -> float:
        """
        Evaluate completeness of a GRD (has start, end, reasonable number of steps).
        
        Returns:
            Score between 0.0 and 1.0
        """
        score = 0.0
        
        # Has start nodes
        if grd_structure.start_nodes:
            score += 0.3
        
        # Has end nodes
        if grd_structure.end_nodes:
            score += 0.3
        
        # Has reasonable number of nodes (between 3 and 20)
        node_count = len(grd_structure.nodes)
        if 3 <= node_count <= 20:
            score += 0.2
        elif node_count > 20:
            score += 0.1  # Too many nodes
        
        # Has edges connecting nodes
        if len(grd_structure.edges) > 0:
            score += 0.2
        
        return min(score, 1.0)
    
    @staticmethod
    def execution_traceability(grd_structure: GRDStructure) -> float:
        """
        Evaluate how traceable/executable the GRD is.
        
        Returns:
            Score between 0.0 and 1.0
        """
        execution_order = grd_structure.get_execution_order()
        
        if not execution_order:
            return 0.0
        
        # Check if all nodes are reachable
        reachable_nodes = set(execution_order)
        all_nodes = {node.id for node in grd_structure.nodes}
        
        if not all_nodes:
            return 0.0
        
        reachability_score = len(reachable_nodes) / len(all_nodes)
        
        # Check for cycles (should be minimal for good reasoning)
        # Simple heuristic: if execution order length equals node count, likely no cycles
        if len(execution_order) == len(grd_structure.nodes):
            cycle_score = 1.0
        else:
            cycle_score = 0.5
        
        return (reachability_score + cycle_score) / 2.0
    
    @staticmethod
    def overall_quality(grd: str, grd_structure: Optional[GRDStructure] = None) -> float:
        """
        Calculate overall GRD quality score.
        
        Args:
            grd: Mermaid code string
            grd_structure: Optional pre-parsed structure
            
        Returns:
            Overall quality score between 0.0 and 1.0
        """
        parser = MermaidParser()
        
        # Structural validity
        validity_score = GRDMetrics.structural_validity(grd)
        if validity_score == 0.0:
            return 0.0
        
        # Parse if not provided
        if grd_structure is None:
            try:
                grd_structure = parser.parse(grd)
            except Exception:
                return 0.0
        
        # Completeness
        completeness_score = GRDMetrics.completeness(grd_structure)
        
        # Execution traceability
        traceability_score = GRDMetrics.execution_traceability(grd_structure)
        
        # Weighted average
        overall = (
            validity_score * 0.4 +
            completeness_score * 0.3 +
            traceability_score * 0.3
        )
        
        return overall


class BraidOptimizer(dspy.Module):
    """
    BRAID-aware optimizer for DSPy.
    
    This optimizer extends DSPy's optimization capabilities by:
    1. Optimizing GRD generation quality
    2. Optimizing step-by-step execution
    3. Providing GRD-specific metrics
    """
    
    def __init__(
        self,
        base_optimizer: Optional[dspy.Module] = None,
        grd_quality_weight: float = 0.5,
        execution_quality_weight: float = 0.5
    ):
        """
        Initialize the BRAID optimizer.
        
        Args:
            base_optimizer: Base DSPy optimizer to use (e.g., MIPROv2)
            grd_quality_weight: Weight for GRD quality in optimization
            execution_quality_weight: Weight for execution quality in optimization
        """
        super().__init__()
        
        self.base_optimizer = base_optimizer
        self.grd_quality_weight = grd_quality_weight
        self.execution_quality_weight = execution_quality_weight
        self.metrics = GRDMetrics()
    
    def optimize(
        self,
        module: BraidReasoning,
        trainset: List[Dict[str, Any]],
        metric: Optional[Callable] = None,
        num_threads: int = 1
    ) -> BraidReasoning:
        """
        Optimize a BraidReasoning module.
        
        Args:
            module: The BraidReasoning module to optimize
            trainset: Training examples with 'problem' and optionally 'answer' keys
            metric: Optional custom metric function
            num_threads: Number of threads for parallel optimization
            
        Returns:
            Optimized BraidReasoning module
        """
        if metric is None:
            metric = self._default_metric
        
        # If base optimizer is provided, use it
        if self.base_optimizer:
            # Optimize the planning phase (GRD generation)
            optimized_module = self._optimize_planning(module, trainset, metric)
            
            # Optimize the execution phase
            optimized_module = self._optimize_execution(optimized_module, trainset, metric)
            
            return optimized_module
        else:
            # Simple optimization: improve prompts based on metrics
            return self._simple_optimize(module, trainset, metric)
    
    def _optimize_planning(
        self,
        module: BraidReasoning,
        trainset: List[Dict[str, Any]],
        metric: Callable
    ) -> BraidReasoning:
        """Optimize the planning (GRD generation) phase."""
        # Collect GRD quality metrics
        grd_scores = []
        
        for example in trainset:
            problem = example.get("problem", "")
            if not problem:
                continue
            
            # Generate GRD
            if module.use_generator and module.generator:
                gen_result = module.generator.generate(problem=problem)
                grd = gen_result.get("grd", "")
                grd_structure = gen_result.get("parsed_structure")
            else:
                plan_result = module.plan(problem=problem)
                grd = plan_result.grd
                try:
                    grd_structure = module.parser.parse(grd)
                except Exception:
                    grd_structure = None
            
            # Evaluate quality
            quality = self.metrics.overall_quality(grd, grd_structure)
            grd_scores.append({
                "problem": problem,
                "grd": grd,
                "quality": quality
            })
        
        # Use base optimizer if available
        if self.base_optimizer:
            # Optimize the plan signature
            plan_trainset = [
                dspy.Example(problem=ex["problem"], grd=ex["grd"])
                for ex in grd_scores
            ]
            module.plan = self.base_optimizer.compile(
                student=module.plan,
                trainset=plan_trainset
            )
        
        return module
    
    def _optimize_execution(
        self,
        module: BraidReasoning,
        trainset: List[Dict[str, Any]],
        metric: Callable
    ) -> BraidReasoning:
        """Optimize the execution phase."""
        # Collect execution results
        execution_results = []
        
        for example in trainset:
            problem = example.get("problem", "")
            expected_answer = example.get("answer", "")
            
            if not problem:
                continue
            
            # Run BRAID reasoning
            result = module(problem=problem)
            
            # Evaluate execution quality
            execution_score = metric(result, expected_answer)
            
            execution_results.append({
                "problem": problem,
                "result": result,
                "score": execution_score
            })
        
        # Use base optimizer if available
        if self.base_optimizer:
            # Optimize the execute step signature
            step_trainset = []
            for ex in execution_results:
                result = ex["result"]
                for step in result.reasoning_steps:
                    step_trainset.append(dspy.Example(
                        step_description=step["label"],
                        context=f"Problem: {ex['problem']}",
                        step_output=step["result"]
                    ))
            
            if step_trainset:
                module.execute_step = self.base_optimizer.compile(
                    student=module.execute_step,
                    trainset=step_trainset
                )
        
        return module
    
    def _simple_optimize(
        self,
        module: BraidReasoning,
        trainset: List[Dict[str, Any]],
        metric: Callable
    ) -> BraidReasoning:
        """Simple optimization without base optimizer."""
        # Just collect metrics and return module
        # In a real implementation, this could use few-shot learning
        # or prompt engineering improvements
        return module
    
    def _default_metric(self, result: BraidResult, expected_answer: Optional[str] = None) -> float:
        """
        Default metric for evaluating BRAID results.
        
        Args:
            result: BraidResult object
            expected_answer: Optional expected answer for comparison
            
        Returns:
            Score between 0.0 and 1.0
        """
        score = 0.0
        
        # GRD quality
        if result.parsed_grd:
            grd_quality = self.metrics.overall_quality(result.grd, result.parsed_grd)
            score += grd_quality * self.grd_quality_weight
        
        # Execution quality
        if result.reasoning_steps:
            # Check if we have reasonable number of steps
            step_count = len(result.reasoning_steps)
            if 2 <= step_count <= 15:
                step_score = 1.0
            elif step_count > 15:
                step_score = 0.5
            else:
                step_score = 0.0
            
            # Check if answer is present
            answer_score = 1.0 if result.answer else 0.0
            
            execution_score = (step_score + answer_score) / 2.0
            score += execution_score * self.execution_quality_weight
        
        # Answer correctness (if expected answer provided)
        if expected_answer and result.answer:
            # Simple string similarity (could be improved with semantic similarity)
            expected_lower = expected_answer.lower().strip()
            answer_lower = result.answer.lower().strip()
            
            if expected_lower in answer_lower or answer_lower in expected_lower:
                score += 0.2
        
        return min(score, 1.0)
    
    def evaluate(
        self,
        module: BraidReasoning,
        testset: List[Dict[str, Any]],
        metric: Optional[Callable] = None
    ) -> Dict[str, float]:
        """
        Evaluate a BraidReasoning module on a test set.
        
        Args:
            module: The BraidReasoning module to evaluate
            testset: Test examples with 'problem' and optionally 'answer' keys
            metric: Optional custom metric function
            
        Returns:
            Dictionary of evaluation metrics
        """
        if metric is None:
            metric = self._default_metric
        
        scores = []
        grd_qualities = []
        execution_scores = []
        
        for example in testset:
            problem = example.get("problem", "")
            expected_answer = example.get("answer")
            
            if not problem:
                continue
            
            result = module(problem=problem)
            
            # Overall score
            score = metric(result, expected_answer)
            scores.append(score)
            
            # GRD quality
            if result.parsed_grd:
                grd_quality = self.metrics.overall_quality(result.grd, result.parsed_grd)
                grd_qualities.append(grd_quality)
            
            # Execution score
            if result.reasoning_steps:
                exec_score = len(result.reasoning_steps) / 10.0  # Normalize
                execution_scores.append(min(exec_score, 1.0))
        
        return {
            "average_score": sum(scores) / len(scores) if scores else 0.0,
            "average_grd_quality": sum(grd_qualities) / len(grd_qualities) if grd_qualities else 0.0,
            "average_execution_score": sum(execution_scores) / len(execution_scores) if execution_scores else 0.0,
            "total_examples": len(testset),
            "valid_results": len(scores)
        }

