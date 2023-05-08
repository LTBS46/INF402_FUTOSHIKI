try:
    import table
    #ta = table.table(3)
    #ta.set_value_at(0, 0, 1)
    #ta.set_value_at(1,1,2)
    #ta.set_value_at(2,2,3)
    #print(ta.gen_dimacs())
    #with open("test3.grid", "r") as f:
    #    print(table.table(3, f.read()))
    import sat
    with open("test5w.json", "r") as f:
        t2 = table.table(f.read())
        print(t2)
        s = sat.solve(t2.gen_dimacs())
        print(s)
        print(table.table(5, s))
finally:
    print("everything fine with 'table.py'")