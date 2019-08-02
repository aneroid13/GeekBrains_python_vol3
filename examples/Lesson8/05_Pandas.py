import pandas
import numpy
# В данном примере мы создали объект типа series, содержащий различные типы данных.

series = pandas.Series([1,2,3,4,5, numpy.nan, "строка", 9])
print(series)

df1 = pandas.DataFrame(numpy.array([1,2,3,4,5,6]).reshape(2,3))
print(df)

df1 = pandas.DataFrame(numpy.array([1,2,3,4,5,6]).reshape(2,3), columns=list('ABC'), index=list('XY'))
print(df)

df2 = pandas.DataFrame(numpy.arange(1, 7501).reshape(500,15))
print(df2.head(2))

print(df2.head())

print( df2.tail())

print( df2.tail(1))


df3 = pandas.DataFrame(numpy.arange(1, 100, 0.12).reshape(33,25))
print(df3.describe())

print(df3.iloc[:5,:10])

print(df3.iloc[-5:]) # df3.tail(5)

print(df3.iloc[:5]) # df3.head(5)

df4 = df3.rename(columns=lambda c: chr(65+c))
print(df4.loc[:5, 'A':'D'])

print(df4.loc[:5, ('A','D')])


