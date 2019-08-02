import numpy as np
import pandas as pd
names = pd.read_csv('names.csv')

#print(names.head(1))
#print(names.tail(4))
#print(names.describe())
#print(names.sort_values(by='Rank').head(20))
#print(names.sort_values(by='Count', ascending=False).head(20))
#print(names[names['Gender'] == 'FEMALE'].head(5))
print(names[(names['Gender'] == 'FEMALE') & (names['Rank'] > 80)].head(5))
