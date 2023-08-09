import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Create a "Hello, World!" dataset
data = {
    'Category': ['Hello', 'World'] * 50,
    'Value': np.random.rand(100)
}

df = pd.DataFrame(data)


# Group the data by category and calculate the sum of each category
grouped_data = df.groupby('Category').sum()

# Create a bar chart
plt.bar(grouped_data.index, grouped_data['Value'])
plt.xlabel('Category')
plt.ylabel('Value')
plt.title('Hello, World! Random Data Bar Chart')
plt.show()
