from __future__ import absolute_import
from typing import Dict, Any, Callable


class StepwiseAlgorithm(object):
    def initialize(self, state):
        pass

    def step(self, current_step, state):
        pass

    def evaluate(self, current_step, state):
        pass

    def output(self, current_step, state):
        pass


def as_stepwise_algorithm(initialize, step, evaluate,
                          output):
    return type(u"AdHocStepwiseAlgorithm", (StepwiseAlgorithm,), {
        u"initialize": lambda self, state: initialize(state),
        u"step": lambda self, current_step, state: step(current_step, state),
        u"evaluate": lambda self, current_step, state: evaluate(current_step, state),
        u"output": lambda self, current_step, state: output(current_step, state),
    })()


def run_stepwise_algorithm(algorithm, do_stop,
                           do_evaluate):
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


def run_stepwise_algorithm_basic(algorithm, total_steps, evaluate_after):
    return run_stepwise_algorithm(algorithm, lambda current_step, state: current_step >= total_steps,
                                  lambda current_step, last_eval, state: last_eval + evaluate_after <= current_step)
