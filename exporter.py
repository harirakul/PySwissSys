from simpledbf import Dbf5

dbf = Dbf5(r'databases\tdexport.dbf', codec='utf-8')

#print(type(dbf.to_dataframe()))
df = dbf.to_dataframe()
df.to_csv(r'databases\tdexport.csv')