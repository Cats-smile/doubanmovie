import pandas as pd
import warnings

warnings.filterwarnings('ignore')
data = pd.read_csv('douban.csv', encoding='gbk')
data_1 = data.dropna(how='all', axis=0)  # 丢弃全为空值的行
data_2 = data_1.dropna(how='all', axis=1)  # 丢弃全为空值的列
data_2.fillna({
    # 用fillna填补缺失值，并显示前5行。
    '引言': '无引言'
})
print(data_2['引言'][:5])
print('缺失值个数', '\n', data_2.isnull().sum())  # 查看缺失值个数
print(data_2.columns)  # 打印出全部列的名称

data_2.to_csv('douban.csv', header=None)
