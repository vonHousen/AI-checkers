import pstats


def main():
    ProfileReader.read_print_stats()


# najpierw odpalasz komende np taka:     python -m cProfile -o profiling_results board.py
# potem:                                 python profileReader.py
# widzisz w ktorych funkacjach program spedzil najwiecej czasu

class ProfileReader:
    @staticmethod
    def read_print_stats():
        stats = pstats.Stats("profiling_results")
        # stats.sort_stats("cumtime")  # całkowity czas spedzony w funkcji i jej wywołaniach
        stats.sort_stats("tottime")  # czas spędzony tylko w tej funkcji
        stats.print_stats(30)


if __name__ == '__main__':
    main()
