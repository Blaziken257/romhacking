def colorize(t,p):
        """Assigns 16x16 tiles certain palettes."""
        c = []
        for i, v in enumerate(t):
                c.append([])
                for j, w in enumerate(t[i]):
                        k = t[i][j] % 4
                        c[i].append(p[k])
        return c
