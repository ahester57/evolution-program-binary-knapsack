# ahester57

import asyncio
import json
import numpy as np
import random
import time

from ea_bitwise.ga import GA
from ea_bitwise.selection_mechanism.mechanism import SelectionMechanism
from ea_bitwise.selection_mechanism.proportional import Proportional
from ea_bitwise.selection_mechanism.ranking import LinearRanking
from ea_bitwise.selection_mechanism.tournament import DeterministicTournament, StochasticTournament
from ea_bitwise.selection_mechanism.truncation import Truncation


class GAMenu(object):

    def __init__(self) -> None:
        """Concept loosely based on: https://chunkofcode.net/how-to-implement-a-dynamic-command-line-menu-in-python/"""
        pass

    def selection_mechanism_menu(self) -> SelectionMechanism:
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
        ans = -1
        while ans not in range(1, 6):
            ans = self.prompt_int('Which mechanism?', None)
        return [
            None,
            Proportional,
            Truncation,
            DeterministicTournament,
            StochasticTournament,
            LinearRanking
        ][ans]

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
                Select_Mechanism = self.selection_mechanism_menu()
                selection_parameters = {}
                for k, v in Select_Mechanism.parameters().items():
                    selection_parameters.update({k: self.prompt_float(v[0], v[1])})
                options = {
                    'dims': self.prompt_int('Dimensions', 3),
                    'domain_lower': self.prompt_float('Domain Lower Bound', -4.0),
                    'domain_upper': self.prompt_float('Domain Upper Bound', 7.0),
                    'pop_size': self.prompt_int('Population Size', 20),
                    'p_c': self.prompt_float('Prob. of Crossover', 0.65),
                    'p_m': self.prompt_float('Prob. of Mutation', 0.05),
                    't_max': self.prompt_int('Max Generations', 30),
                    'maximize': self.prompt_bool('Maximize', False),
                    'Select_Mechanism': Select_Mechanism,
                    'selection_parameters': selection_parameters
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
                    best_of_runs.sort(key=lambda x:x.fitness_score, reverse=options['maximize'])
                    print(f'\nOptions: {json.dumps(options, sort_keys=True, indent=2, default=str)}')
                    print(f'\nStats over {num_runs} runs:')
                    fitness_scores = [bor.fitness_score for bor in best_of_runs]
                    print(f'Best: {best_of_runs[0]}')
                    print(f'Mean: {np.mean(fitness_scores)}')
                    print(f'Standard Deviation: {np.std(fitness_scores)}')
            except Exception as e:
                print(f'Exception {e.args} occurred in {self.__class__}.enter_menu')


if __name__ == '__main__':
    try:
        asyncio.run(GAMenu().configure_ga())
    except EOFError:
        print('^D')
    except KeyboardInterrupt:
        print('^C')
