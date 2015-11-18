from typing import Dict, Any, Callable


class StepwiseAlgorithm:
    def initialize(self, state: Dict[str, Any]):
        pass

    def step(self, current_step: int, state: Dict[str, Any]) -> int:
        pass

    def evaluate(self, current_step: int, state: Dict[str, Any]):
        pass

    def output(self, current_step: int, state: Dict[str, Any]):
        pass


def as_stepwise_algorithm(initialize: Callable, step: Callable, evaluate: Callable,
                          output: Callable) -> StepwiseAlgorithm:
    return type("AdHocStepwiseAlgorithm", (StepwiseAlgorithm,), {
        "initialize": lambda self, state: initialize(state),
        "step": lambda self, current_step, state: step(current_step, state),
        "evaluate": lambda self, current_step, state: evaluate(current_step, state),
        "output": lambda self, current_step, state: output(current_step, state),
    })()


def run_stepwise_algorithm(algorithm: StepwiseAlgorithm, do_stop: Callable[[int, dict], bool],
                           do_evaluate: Callable[[int, int, dict], bool]):
    state = dict()
    algorithm.initialize(state)
    current_step = 0
    last_eval = 0
    algorithm.evaluate(current_step, state)

    while not do_stop(current_step, state):
        steps_taken = algorithm.step(current_step, state)
        current_step += steps_taken

        if do_evaluate(current_step, last_eval, state):
            last_eval = current_step
            algorithm.evaluate(current_step, state)

    if last_eval < current_step:
        algorithm.evaluate(current_step, state)

    return algorithm.output(current_step, state)


def run_stepwise_algorithm_basic(algorithm: StepwiseAlgorithm, total_steps: int, evaluate_after: int):
    return run_stepwise_algorithm(algorithm, lambda current_step, state: current_step >= total_steps,
                                  lambda current_step, last_eval, state: last_eval + evaluate_after <= current_step)
