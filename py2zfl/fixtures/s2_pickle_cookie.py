import pickle
data = request.cookies['session']
pickle.loads(data)            # EXPECT: REFUTED [deser]
