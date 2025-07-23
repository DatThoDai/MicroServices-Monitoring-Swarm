import pandas as pd
import numpy as np
import os

data =[['Nam',10],['Huy',15],['An',14]]
df = pd.DataFrame(data,columns=['Name','Age'])

x = os.environ['MY_X']
y = os.environ['MY_Y']

result = np.mean(df['Age']) + int(x) + int(y)

print(result)