from typing import Dict, Any, Callable


class StepwiseAlgorithm:
    def initialize(self, state: Dict[str, Any]):
        """
        :param state: this will be the same for the whole algorithm. use it as stateful memory
        :return:
        """
        pass

    def step(self, current_step: int, state: Dict[str, Any], evaluate) -> int:
        """
        :param current_step:
        :param state:
        :param evaluate: when this is true, you should evaluate the current iterate
        :return: how many datapoints you have consumed. If None, then 1 is assumed
        """
        pass

    def output(self, current_step: int, state: Dict[str, Any]):
        """
        it's best to return a dictionary with tuples of lists as values, such as
        {
            loss: (epochs, values)
        }
        """
        pass


def as_stepwise_algorithm(initialize: Callable, step: Callable, output: Callable) -> StepwiseAlgorithm:
    return type("AdHocStepwiseAlgorithm", (StepwiseAlgorithm,), {
        "initialize": lambda self, state: initialize(state),
        "step": lambda self, current_step, state, evaluate: step(current_step, state, evaluate),
        "output": lambda self, current_step, state: output(current_step, state),
    })()


def run_stepwise_algorithm(algorithm: StepwiseAlgorithm, do_stop: Callable[[int, dict], bool],
                           do_evaluate: Callable[[int, int, dict], bool]):
    state = dict()
    algorithm.initialize(state)
    current_step = 0
    last_eval = 0

    while not do_stop(current_step, state):
        evaluate = False
        if do_evaluate(current_step, last_eval, state):
            last_eval = current_step
            evaluate = True
        steps_taken = algorithm.step(current_step, state, evaluate)
        if steps_taken is None:
            steps_taken = 1
        current_step += steps_taken

    return algorithm.output(current_step, state)


def run_stepwise_algorithm_basic(algorithm: StepwiseAlgorithm, total_steps: int, evaluate_after: int):
    return run_stepwise_algorithm(algorithm, lambda current_step, state: current_step >= total_steps,
                                  lambda current_step, last_eval,
                                         state: last_eval + evaluate_after <= current_step or current_step == 0)

