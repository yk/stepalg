
class StepwiseAlgorithm(object):
    def initialize(self, state):
        """
        :param state: this will be the same for the whole algorithm. use it as stateful memory
        :return:
        """
        pass

    def step(self, current_step, state, evaluate):
        """
        :param current_step:
        :param state:
        :param evaluate: when this is true, you should evaluate the current iterate
        :return: how many datapoints you have consumed. If None, then 1 is assumed
        """
        pass

    def output(self, current_step, state):
        """
        it's best to return a dictionary with tuples of lists as values, such as
        {
            loss: (epochs, values)
        }
        """
        pass


def as_stepwise_algorithm(initialize, step, output):
    """
    :param initialize: callable (state)
    :param step: callable (current_step, state, evaluate) -> steps_taken
    :param output: callable (current_step, state) -> dict
    :return:
    """
    return type("AdHocStepwiseAlgorithm", (StepwiseAlgorithm,), {
        "initialize": lambda self, state: initialize(state),
        "step": lambda self, current_step, state, evaluate: step(current_step, state, evaluate),
        "output": lambda self, current_step, state: output(current_step, state),
    })()


def run_stepwise_algorithm(algorithm, do_stop,
                           do_evaluate):
    """

    :param algorithm:
    :param do_stop: callable (current_step, state) -> bool
    :param do_evaluate: callable (current_step, last_eval, state) -> bool
    :return:
    """
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


def run_stepwise_algorithm_basic(algorithm, total_steps, evaluate_after):
    return run_stepwise_algorithm(algorithm, lambda current_step, state: current_step >= total_steps,
                                  lambda current_step, last_eval,
                                         state: last_eval + evaluate_after <= current_step or current_step == 0)

