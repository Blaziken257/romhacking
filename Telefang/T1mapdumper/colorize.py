def colorize(t,p):
        c = []
        for i, v in enumerate(t):
                c.append([])
                for j, w in enumerate(t[i]):
                        k = t[i][j] % 4
                        c[i].append(p[k])
        return c
