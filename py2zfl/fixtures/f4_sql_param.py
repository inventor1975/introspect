name = request.args['name']
cursor.execute("SELECT * FROM u WHERE n = %s", (name,))   # EXPECT: EARNED (parameterised)
cursor.execute("SELECT * FROM u WHERE n = '" + name + "'") # EXPECT: REFUTED (concatenated)
