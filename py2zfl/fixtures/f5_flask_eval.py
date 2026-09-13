x = request.args.get('expr')   # flask source -> tainted
eval(x)                        # EXPECT: REFUTED [code]
