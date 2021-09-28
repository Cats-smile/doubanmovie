import numpy as np
import pandas as pd
import warnings
warnings.filterwarnings('ignore')
data = pd.read_csv('douban.csv', encoding='gbk')
data.shape
data.head()
data.info()

data['引言'] = data['引言'].fillna("['无引言']")
data['引言'][:5]