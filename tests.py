import dim_reduc_runner


if __name__ == '__main__':
    S = [(1, 1), (1, -1), (2, 1), (3, 0), (4, 1), (0, -2), (-1, -1)]
    c = 1
    d = 1
    dim_reduc_runner.run(S, c, d)
