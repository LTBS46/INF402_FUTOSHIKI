try:
    import table
    ta = table.table(3)
    ta.set_value_at(0, 0, 1)
    ta.set_value_at(1,1,2)
    ta.set_value_at(2,2,3)
    print(ta.gen_dimacs())
    with open("test3.grid", "r") as f:
        print(table.table(3, f.read()))
    import sat
    ta = table.table(30)
    with open("dump1000", "w") as f:
            f.write(ta.gen_dimacs())
finally:
    print("everything fine with 'table.py'")