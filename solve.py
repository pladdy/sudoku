import sudoku.grid as grid

g = grid.Grid()

print("Building a grid...")
# puzzle sourced from https://websudoku.com/
g.add_row([0, 5, 4, 9, 6, 0, 0, 3, 8])
g.add_row([0, 0, 0, 0, 0, 0, 4, 0, 0])
g.add_row([7, 0, 2, 3, 5, 4, 0, 6, 9])
g.add_row([0, 7, 0, 0, 9, 3, 0, 0, 0])
g.add_row([4, 0, 0, 0, 0, 0, 0, 0, 2])
g.add_row([0, 0, 0, 6, 2, 0, 0, 4, 0])
g.add_row([6, 4, 0, 1, 8, 9, 3, 0, 5])
g.add_row([0, 0, 3, 0, 0, 0, 0, 0, 0])
g.add_row([8, 2, 0, 0, 3, 5, 6, 9, 0])

g.show()
g.solve()
print("--------- Answer: ---------")
g.show()
