from random import shuffle
from math import sqrt
from math import ceil
import argparse


class StatisticCreator:
    def __init__(self, number_runs, board_size=100, chances_ratio=0.5):
        self.number_runs = number_runs
        self.board_size = board_size
        self.chances_ratio = chances_ratio
        self.cnt_passed = 0
        self.cnt_failed = 0
        self.win_ratio = 0

    def __str__(self):
        return str(self.number_runs) + " boards played, success ratio " + "{:.3f}".format(self.win_ratio)

    def create_statistic(self, verbose):
        for _ in range(self.number_runs):
            prisoner_win = self._execute_game(verbose)
            if prisoner_win:
                self.cnt_passed += 1
            else:
                self.cnt_failed += 1

        self.win_ratio = self.cnt_passed / self.number_runs

    def _execute_game(self, verbose):
        board = ShuffledBoard(board_size=self.board_size, chances_ratio=self.chances_ratio)
        cnt_successful = 0
        cnt_failed = 0

        for prisoner_number in range(1, self.board_size+1):
            prisoner = Prisoner(prisoner_number)
            prisoner.search_number(board)
            if prisoner.number_found:
                cnt_successful += 1
            else:
                cnt_failed += 1

        if verbose:
            print("Successful prisoners: " + str(cnt_successful))
            print("Failed prisoners: " + str(cnt_failed))

        return cnt_failed == 0


class ShuffledBoard:
    def __init__(self, board_size=100, do_shuffle=True, chances_ratio=0.5):
        self.board_size = board_size
        self.max_allowed_steps = int(board_size * chances_ratio)
        self.board_map = list(range(1,board_size+1))
        if do_shuffle:
            shuffle(self.board_map)

    def __str__(self):
        output_str = ""
        quater_size = ceil(sqrt(self.board_size))
        max_digits = len(str(self.board_size))

        for idx, val in enumerate(self.board_map):
            if idx % quater_size == 0:
                output_str += "\n"
            output_str += str(val).zfill(max_digits) + " "

        return output_str


class Prisoner:
    def __init__(self, number):
        self.number = number
        self.number_found = False
        self.tries = 0

    def __str__(self):
        result = "Successful" if self.number_found else "Failed"
        return "Prisoner number " + str(self.number) + ": " + result

    def search_number(self, board):
        next_number = board.board_map[self.number-1]
        self.number_found = next_number == self.number
        self.tries += 1

        while(not self.number_found and self.tries < board.max_allowed_steps):
            next_number = board.board_map[next_number-1]
            self.number_found = next_number == self.number
            self.tries += 1


def run_statistic(cnt_execution):
    statistic = StatisticCreator(cnt_execution, board_size=100)
    statistic.create_statistic(verbose=False)
    print(statistic)


def run_single_game():
    statistic = StatisticCreator(1, board_size=100)
    statistic.create_statistic(verbose=True)


def arg_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--count_stat', type=int, default=1000)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-s', '--stat', action='store_true', help='Execute multiple runs to create statistic.')
    group.add_argument('-o', '--one_run', action='store_true', help='Execute a single run and see how many prisoners are successful and failing.')
    args = parser.parse_args()

    return args.stat, args.one_run, args.count_stat


def main():
    stat_flag, one_run_flag, count_flag = arg_parser()

    if stat_flag:
        run_statistic(count_flag)
    elif one_run_flag:
        run_single_game()


if __name__ == "__main__":
    main()
