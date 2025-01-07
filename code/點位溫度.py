import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 设置数据路径
data_path = r"D:\大五\建築設計(八)\dataset\layout\圖表\資料\都市單車路徑點位溫度.xlsx"

# 读取数据，假设有效数据从第三行开始
data = pd.read_excel(data_path, header=0)

# 数据转置以方便提取每个点位的数据
data_transposed = data.transpose()
data_transposed.columns = data_transposed.iloc[0]  # 使用数据的第一行作为列标题
data_transposed = data_transposed.drop(data_transposed.index[0])

# 将列标题中的 Segment ID 和 Point Index 提取出来
data_transposed.reset_index(inplace=True)
data_transposed[['Segment ID', 'Point Index']] = data_transposed['index'].str.extract(r'(\d+)\.(\d+)')
data_transposed.drop('index', axis=1, inplace=True)

# 将提取出来的 Segment ID 和 Point Index 转换为数字
data_transposed['Segment ID'] = pd.to_numeric(data_transposed['Segment ID'], errors='coerce')
data_transposed['Point Index'] = pd.to_numeric(data_transposed['Point Index'], errors='coerce')

# 处理 NaN 值
data_transposed.dropna(subset=['Segment ID', 'Point Index'], inplace=True)

# 分组绘图
segment_ids = data_transposed['Segment ID'].unique()
segments_per_plot = 4  # 每个图显示 4 个 Segment ID
num_plots = len(segment_ids) // segments_per_plot + (len(segment_ids) % segments_per_plot > 0)

for i in range(num_plots):
    fig, axes = plt.subplots(nrows=segments_per_plot, figsize=(40, 5 * segments_per_plot))
    for ax, segment_id in zip(axes, segment_ids[i*segments_per_plot:(i+1)*segments_per_plot]):
        segment_data = data_transposed[data_transposed['Segment ID'] == segment_id]
        sns.lineplot(ax=ax, x='Point Index', y='March', data=segment_data, marker='o', label='March', color='blue')
        sns.lineplot(ax=ax, x='Point Index', y='July', data=segment_data, marker='o', label='July', color='red')
        sns.lineplot(ax=ax, x='Point Index', y='September', data=segment_data, marker='o', label='September', color='green')
        sns.lineplot(ax=ax, x='Point Index', y='December', data=segment_data, marker='o', label='December', color='purple')
        print(segment_data)
        s = segment_data.to_numpy()
        for j in range(1, len(s)):
            should_mark = False
            max_y = 0
            for k in range(3, 7):
                max_y = max(max_y, s[j][k])
                if abs(s[j][k] - s[j - 1][k]) > 2:
                    should_mark = True
            if should_mark:
                ax.annotate(str(int(s[j][0])), (s[j][0], max_y + 1))
        
        ax.legend()
    plt.tight_layout()
    plt.show()

