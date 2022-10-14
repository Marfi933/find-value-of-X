from threading import *
from time import *


class BruteForce:
    def __init__(self, expr, unknown='X', low=0, high=9, count_of_solutions=1):
        """
        :param expr: expression to solve
        :param unknown: unknown variable to solve
        :param operation: operation to solve
        :param low: lower bound of the range (0-9)
        :param high: upper bound of the range (0-9)
        :param count_of_solutions: number of solutions to find
        """
        self.check_input(expr, unknown, low, high, count_of_solutions)
        self.expr = expr
        self.unknown = unknown
        self.low = low
        self.high = high
        self.count_of_solutions = count_of_solutions
        self.numbers = []

    @staticmethod
    def check_input(expr, unknown, low, high, count_of_solutions):
        """
        Check if input is valid.
        :param expr: expression to solve
        :param unknown: unknown variable to solve
        :param operation: operation to solve
        :param low: lower bound of the range (0-9)
        :param high: upper bound of the range (0-9)
        :return: True if input is valid, raise ValueError otherwise
        """
        if not isinstance(expr, str):
            raise TypeError('Expression must be a string')
        if not isinstance(unknown, str):
            raise TypeError('Unknown must be a string')
        if not isinstance(low, int):
            raise TypeError('Low must be an integer')
        if not isinstance(high, int):
            raise TypeError('High must be an integer')
        if not isinstance(count_of_solutions, int):
            raise TypeError('Count of solutions must be an integer')

    def split_expr(self):
        """
        Split expression into two parts.
        :return: two parts of the expression
        """
        x = self.expr.split('+')
        y = x[1].split('=')
        x = x[0]
        return [x] + y

    def replace_unknown(self, expr, unknown, num):
        """
        Replace unknown variable with number.
        :param expr: expression to solve
        :param unknown: unknown variable to solve
        :param num: number to replace unknown variable
        :return: expression with replaced unknown variable
        """
        return expr.replace(unknown, num)

    def digit_count(self, string):
        """
        Count digits in string.
        :param string: string to count digits
        :return: number of digits in string
        """
        return len(string)

    def unknown_count(self, string):
        """
        Count unknown variables in string.
        :param string: string to count unknown variables
        :return: number of unknown variables in string
        """
        c = 0
        for i in string:
            if i == self.unknown:
                c += 1
        return c

    @staticmethod
    def is_safe(str1, str2):
        """
        Check if two strings are safe to add.
        :param str1: first string
        :param str2: second string
        :return: True if strings are safe to add, False otherwise
        """
        for i in str1:
            if i in str2:
                return False
        return True

    def check_zero(self, string):
        """
        Check if string starts with 0.
        :param string: string to check
        :return: True if string starts with 0, False otherwise
        """
        return string[0] == '0' and len(string) > 1

    def generate_numbers(self, string):
        """
        Generate all possible numbers with given length.
        :param string: string to generate numbers
        :return: list of all possible numbers
        """

        list_of_numbers = []

        if self.unknown_count(string) == 0:
            return [string]

        else:
            numbers = []
            for i in range(self.low, self.high + 1):
                if str(i) not in string and str(i) not in list_of_numbers and not (self.check_zero(string)):
                    numbers += self.generate_numbers(string.replace(self.unknown, str(i), 1))
                    list_of_numbers.append(str(i))
            return numbers

    def find_solutions(self,key, numbers):
        """
        Find solutions.
        :param key: key to choose the solution
        :param numbers: list of numbers
        :return: dict of list of solutions
        """
        dict_solution = {}
        for i in range(len(numbers[0])):
            for j in range(len(numbers[1])):
                for k in range(len(numbers[2])):

                    if self.is_safe(numbers[0][i], numbers[1][j]) and self.is_safe(numbers[0][i],
                                                                                   numbers[2][k]) and self.is_safe(
                        numbers[1][j], numbers[2][k]):

                        if eval(f"{numbers[0][i]}{'+'}{numbers[1][j]}") == eval(numbers[2][k]):

                            dict_solution[key] = [numbers[0][i], numbers[1][j], numbers[2][k]]

                            if key == self.count_of_solutions:
                                return dict_solution

                            key += 1

        if len(dict_solution) == 0:
            raise ValueError('No solutions found')

        return dict_solution

    # time complexity: O(n^3)
    def solve(self, key=1):
        """
        Solve the expression.
        :param key: key to choose the solution
        :return: return dict of list of solutions
        """

        if self.count_of_solutions == 0:
            raise ValueError(f'Count of solutions must be greater than 0')

        dict_solution = {}
        split_data = self.split_expr()
        numbers, list_of_numbers = [], []

        numbers += [self.generate_numbers(split_data[0]) if self.unknown_count(split_data[0]) > 0 else [split_data[0]]]
        numbers += [self.generate_numbers(split_data[1]) if self.unknown_count(split_data[1]) > 0 else [split_data[1]]]
        numbers += [self.generate_numbers(split_data[2]) if self.unknown_count(split_data[2]) > 0 else [split_data[2]]]

        dict_solution = self.find_solutions(key, numbers)

        return dict_solution

class ThreadReturnValue(Thread):
    """
    Thread class with a return value.
    """
    def __init__(self, *init_args, **init_kwargs):
        Thread.__init__(self, *init_args, **init_kwargs)
        self._return = None

    def run(self):
        """
        Run the thread.
        :return:
        """
        self._return = self._target(*self._args, **self._kwargs)

    def join(self):
        """
        Join the thread.
        :return:
        """
        Thread.join(self)
        return self._return


class ThreadBruteForce(BruteForce):
    def __init__(self, expr, unknown='X', low=0, high=9, count_of_solutions=1):
        """
        Initialize the class.
        :param expr: expression to solve
        :param unknown: unknown variable to solve
        :param low: lowest number to use
        :param high: highest number to use
        :param count_of_solutions: number of solutions to find
        """
        super().__init__(expr, unknown, low, high, count_of_solutions)
        self.threads = []

    def solve(self, key=1):
        """
        Solve the expression. Find combinations of numbers in separate threads.
        :param key: key to choose the solution
        :return: return dict of list of solutions
        """
        split_data = self.split_expr()
        numbers = []

        for i in range(3):
            self.threads.append(ThreadReturnValue(target=self.generate_numbers, args=(split_data[i],)))
            self.threads[i].start()

        for thread in self.threads:
            numbers += [thread.join()]

        self.threads = []

        return self.find_solutions(key, numbers)


def compare_time_run():
    """
    Compare time of running the program with and without threads.
    :return:  None
    """
    b = BruteForce('84X+3XX=XXXX', count_of_solutions=2)
    tb = ThreadBruteForce('84X+3XX=XXXX', count_of_solutions=2)
    start = time()
    b.solve()
    end = time()
    print(f'BruteForce time: {end - start}')
    start = time()
    tb.solve()
    end = time()
    print(f'ThreadBruteForce time: {end - start}')

b = BruteForce('84X+3XX=XXXX', count_of_solutions=2)
print(b.solve())
b2 = BruteForce('XX+XX=3X')
b3 = BruteForce('X+X=X', count_of_solutions=100)
print(b2.solve())
print(b3.solve())
tb = ThreadBruteForce('84X+3XX=XXXX', count_of_solutions=2)
print(tb.solve())
compare_time_run()

