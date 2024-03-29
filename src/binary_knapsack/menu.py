# ahester57

import asyncio
import json
import numpy as np
import random
import time

from binary_knapsack.ga import GA
from binary_knapsack.penalty_method.absolute import AbsolutePenalty
from binary_knapsack.penalty_method.dynamic import DynamicPenalty
from binary_knapsack.penalty_method.logarithmic import LogarithmicPenalty
from binary_knapsack.penalty_method.method import PenaltyMethod
from binary_knapsack.selection_mechanism.mechanism import SelectionMechanism
from binary_knapsack.selection_mechanism.proportional import Proportional
from binary_knapsack.selection_mechanism.ranking import LinearRanking
from binary_knapsack.selection_mechanism.tournament import DeterministicTournament, StochasticTournament
from binary_knapsack.selection_mechanism.truncation import Truncation
from binary_knapsack.test_problem.knapsack import BinaryKnapsack
from binary_knapsack.test_problem.problem import TestProblem
from binary_knapsack.crossover_method.method import CrossoverMethod
from binary_knapsack.crossover_method.majority_voting import MajorityVoting
from binary_knapsack.crossover_method.p_uniform import PUniform
from binary_knapsack.crossover_method.single_point import SinglePoint


class GAMenu(object):

    def __init__(self) -> None:
        """Concept loosely based on: https://chunkofcode.net/how-to-implement-a-dynamic-command-line-menu-in-python/"""
        pass

    def problem_to_solve_menu(self) -> TestProblem:
        """Menu for test problems.

        Returns:
            tuple[TestProblem, dict]: (The type of problem to solve, Its parameters)
        """
        print('''
=================================
        Problems To Solve
=================================
    1 - Binary Knapsack
=================================
''')
        options = [
            None,
            BinaryKnapsack
        ]
        ans = -1
        while ans not in range(1, len(options)):
            ans = self.prompt_int('Which problem?', 1)
        Problem_To_Solve : TestProblem = options[ans]
        problem_parameters = {}
        for k, v in Problem_To_Solve.parameters().items():
            dtype = type(v[1])
            assert(dtype in (float, int))
            if dtype is float:
                problem_parameters.update({k: self.prompt_float(v[0], v[1])})
            elif dtype is int:
                problem_parameters.update({k: self.prompt_int(v[0], v[1])})
        return Problem_To_Solve, problem_parameters

    def penalty_method_menu(self) -> PenaltyMethod:
        """Menu for penalty methods.

        Returns:
            tuple[PenaltyMethod, dict]: (The chosen penalty method, Its parameters)
        """
        print('''
=================================
        Penalty Methods
=================================
    1 - Logarithmic
    2 - Absolute
    3 - Dynamic
=================================
''')
        options = [
            None,
            LogarithmicPenalty,
            AbsolutePenalty,
            DynamicPenalty
        ]
        ans = -1
        while ans not in range(1, len(options)):
            ans = self.prompt_int('Which Penalty Method?', 1)
        Penalty_Method : PenaltyMethod = options[ans]
        penalty_parameters = {}
        for k, v in Penalty_Method.parameters().items():
            dtype = type(v[1])
            assert(dtype in (float, int))
            if dtype is float:
                penalty_parameters.update({k: self.prompt_float(v[0], v[1])})
            elif dtype is int:
                penalty_parameters.update({k: self.prompt_int(v[0], v[1])})
        return Penalty_Method, penalty_parameters

    def selection_mechanism_menu(self) -> SelectionMechanism:
        """Menu for selection mechanisms.

        Returns:
            tuple[SelectionMechanism, dict]: (The chosen selection mechanism, Its parameters)
        """
        print('''
=================================
        Selection Mechanisms
=================================
    1 - Proportional
    2 - Truncation
    3 - Tournament (Deterministic)
    4 - Tournament (Stochastic)
    5 - Linear Ranking
=================================
''')
        options = [
            None,
            Proportional,
            Truncation,
            DeterministicTournament,
            StochasticTournament,
            LinearRanking
        ]
        ans = -1
        while ans not in range(1, len(options)):
            ans = self.prompt_int('Which mechanism?', 1)
        Select_Mechanism : SelectionMechanism = options[ans]
        selection_parameters = {}
        for k, v in Select_Mechanism.parameters().items():
            dtype = type(v[1])
            assert(dtype in (float, int))
            if dtype is float:
                selection_parameters.update({k: self.prompt_float(v[0], v[1])})
            elif dtype is int:
                selection_parameters.update({k: self.prompt_int(v[0], v[1])})
        return Select_Mechanism, selection_parameters

    def crossover_method_menu(self) -> CrossoverMethod:
        """Menu for crossover methods.

        Returns:
            tuple[CrossoverMethod, dict]: (The chosen crossover method, Its parameters)
        """
        print('''
=================================
        Crossover Methods
=================================
    1 - Single Point
    2 - P-Uniform
    3 - Majority Voting
=================================
''')
        options = [
            None,
            SinglePoint,
            PUniform,
            MajorityVoting
        ]
        ans = -1
        while ans not in range(1, len(options)):
            ans = self.prompt_int('Which Crossover Method?', 1)
        Crossover_Method : CrossoverMethod = options[ans]
        crossover_parameters = {}
        for k, v in Crossover_Method.parameters().items():
            dtype = type(v[1])
            assert(dtype in (float, int))
            if dtype is float:
                crossover_parameters.update({k: self.prompt_float(v[0], v[1])})
            elif dtype is int:
                crossover_parameters.update({k: self.prompt_int(v[0], v[1])})
        return Crossover_Method, crossover_parameters

    def input_display(self, name:str, default=None) -> str:
        """Generate the string to be displayed in an prompt.

        Args:
            name (str): The prompt name.
            default (str, optional): The default value if no answer provided.

        Returns:
            str: The string to be used in an input prompt.
        """
        if default is not None:
            return f'''=================================
{name} [{default}]: '''
        else:
            return f'''=================================
{name}: '''

    def prompt_int(self, name:str, default:int=None) -> int:
        """Prompt for an integer value.
        
        Args:
            name (str): The prompt name.
            default (int, optional): The default value if no answer provided.

        Returns:
            int: The user-provided input.
        """
        assert default is None or type(default) is int
        ans = ''
        while len(ans) == 0:
            ans = input(self.input_display(name, default))
            if ans == '' and default is not None:
                return default
            try:
                return int(ans)
            except ValueError:
                ans = ''

    def prompt_float(self, name:str, default:float=None) -> float:
        """Prompt for a float value.
        
        Args:
            name (str): The prompt name.
            default (float, optional): The default value if no answer provided.

        Returns:
            float: The user-provided input.
        """
        assert default is None or type(default) is float
        ans = ''
        while len(ans) == 0:
            ans = input(self.input_display(name, default))
            if ans == '' and default is not None:
                return default
            try:
                return float(ans)
            except ValueError:
                ans = ''

    def prompt_bool(self, name:str, default:bool=None) -> bool:
        """Prompt for a bool value.
        
        Args:
            name (str): The prompt name.
            default (bool, optional): The default value if no answer provided.

        Returns:
            bool: The user-provided input.
        """
        assert default is None or type(default) is bool
        ans = ''
        while len(ans) == 0 or ans[0] not in 'YyNn':
            default_display = 'Y/n'
            if not default:
                default_display = 'y/N'
            ans = input(self.input_display(name, default_display))
            if ans == '' and default is not None:
                return default
        return ans[0].upper() == 'Y'

    async def configure_ga(self) -> GA:
        while True:
            try:
                random.seed(time.time())
                Problem_To_Solve, \
                    problem_parameters = self.problem_to_solve_menu()
                problem_instance = Problem_To_Solve(**problem_parameters)
                Penalty_Method, \
                    penalty_parameters = self.penalty_method_menu()
                Select_Mechanism, \
                    selection_parameters = self.selection_mechanism_menu()
                Crossover_Method, \
                    crossover_parameters = self.crossover_method_menu()
                options = {
                    'pop_size': self.prompt_int('Population Size', 30),
                    'p_m': self.prompt_float('Probability of Mutation', 0.05),
                    't_max': self.prompt_int('Max Generations', 50),
                    'maximize': self.prompt_bool('Maximize', True),
                    'Select_Mechanism': Select_Mechanism,
                    'selection_parameters': selection_parameters,
                    'problem_instance': problem_instance,
                    'Crossover_Method': Crossover_Method,
                    'crossover_parameters': crossover_parameters,
                    'Penalty_Method': Penalty_Method,
                    'penalty_parameters': penalty_parameters
                }
                if self.prompt_bool('Single run?', False):
                    await GA(
                        **options,
                        rand_seed=self.prompt_int('Random Seed', random.randint(1, 123456789))
                    ).simulate()
                elif self.prompt_bool('Collect stats?', True):
                    num_runs = self.prompt_int('Number of Runs', 30)
                    best_of_runs = await asyncio.gather(*[GA(
                        **options,
                        rand_seed=random.randint(1, 123456789)).simulate()
                        for r in range(num_runs)
                    ])
                    print(best_of_runs)
                    print(problem_instance)
                    best_of_runs.sort(key=lambda x:x[0].fitness_score, reverse=options['maximize'])
                    options.update({'problem_parameters': problem_parameters})
                    print(f'\nOptions: {json.dumps(options, sort_keys=True, indent=2, default=str)}')
                    print(f'\nStats over {num_runs} runs:')
                    fitness_scores = [bor[0].fitness_score for bor in best_of_runs]
                    generations = [bor[1] for bor in best_of_runs]
                    print(f'Best Overall: {best_of_runs[0]}')
                    print(f'Mean Best Fitness: {np.mean(fitness_scores)}')
                    print(f'Standard Deviation of Best Fitness: {np.std(fitness_scores)}')
                    print(f'Mean Generation Best Was Acheived: {np.mean(generations)}')
                    print(f'Standard Deviation of Generations: {np.std(generations)}')
            except AssertionError as ae:
                raise ae
            except Exception as e:
                print(f'Exception {e.args} occurred in {self.__class__}.enter_menu')


if __name__ == '__main__':
    try:
        asyncio.run(GAMenu().configure_ga())
    except EOFError:
        print('^D')
    except KeyboardInterrupt:
        print('^C')
