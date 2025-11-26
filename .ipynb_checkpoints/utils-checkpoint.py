import numpy as np
import pandas as pd

x = pd.date_range(start='2025-01-01', periods=12, freq='MS')
print(x)

def generate_random_sales(min_val, max_val, size):
    return np.random.randint(min_val,max_val,size)

a = generate_random_sales(50,101,12)
b = generate_random_sales(30,81,12)
c = generate_random_sales(20,61,12)
d = generate_random_sales(10,51,12)

data1 = {
    'Date' : x,
    'Product_A' : a,
    'Product_B' : b,
    'Product_C' : c,
    'Product_D' : d
}
initial = pd.DataFrame(data1)
initial.describe()
initial.to_csv('/home/mlk/PycharmProjects/ML_cours/project_sales/data/initial.csv', index=False)

#Build DataFrame
final = initial.copy()
final.rename(columns={'Date': 'Month'}, inplace=True)

final['Total_sales'] = final[['Product_A','Product_B','Product_C',
                              'Product_D']].sum(axis=1)
final['Average_sales'] = final[['Product_A','Product_B','Product_C',
                                'Product_D']].mean(axis=1)
final['Month_over_Month_Growth'] = final['Total_sales'].pct_change() * 100

final['Quarter'] = pd.to_datetime(final['Month']).dt.quarter

final['Max_sales_Product'] = final[['Product_A','Product_B','Product_C',
                              'Product_D']].idxmax(axis=1)
final['Min_sales_Product'] = final[['Product_A','Product_B','Product_C',
                              'Product_D']].idxmin(axis=1)

final.to_csv('/home/mlk/PycharmProjects/ML_cours/project_sales/data/final.csv', index=False)

#Pivot & Table Summaries
pivot_avg = pd.pivot_table(
    final,
    values= ['Product_A','Product_B','Product_C','Product_D','Total_sales'],    
    index = ['Quarter'],
    aggfunc= 'mean'
    
)

pivot_total = final.groupby('Quarter')['Total_sales'].sum().to_frame()
pivot_total.columns = ['Total_sales/quarter']

#combine
#output = pd.concat([pivot_avg, pivot_total], axis=1)
output = pivot_avg.join(pivot_total)
output.to_csv('/home/mlk/PycharmProjects/ML_cours/project_sales/data/output.csv')

#Key Insight
id_best_month = final['Total_sales'].idxmax()
best_mounth = final.loc[id_best_month,'Month']

best_product = final[['Product_A','Product_B','Product_C',
                     'Product_D']].sum(axis=0).idxmax()

best_quarter = output['Total_sales/quarter'].idxmax()







