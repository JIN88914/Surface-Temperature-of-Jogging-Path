import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 修正檔案路徑
file_path = r"D:\大五\建築設計(八)\dataset\layout\圖表\資料\給chatgpt.xlsx"

# 讀取資料
data = pd.read_excel(file_path)

# 將資料轉換為適合繪圖的格式
data_melted = data.melt(id_vars=['空間類型'], var_name='月份', value_name='溫度')

# 創建散布圖，點樣式改為 'x'，並設定解析度為300dpi
plt.figure(figsize=(12, 6), dpi=300)
sns.scatterplot(data=data_melted, x='月份', y='溫度', hue='空間類型', style='空間類型',
                markers='x', palette='Set2', s=100)

# 修改 x 軸標籤為數字
unique_months = sorted(data_melted['月份'].unique())
plt.xticks(ticks=unique_months, labels=[int(month.replace('月', '')) for month in unique_months])

# 添加標題和標籤
plt.title('不同空間類型在各月份的溫度散布圖', fontsize=16)
plt.xlabel('月份', fontsize=12)
plt.ylabel('溫度 (°C)', fontsize=12)
plt.legend(title='空間類型', fontsize=10, title_fontsize=12)
plt.grid(axis='y', linestyle='--', alpha=0.7)

# 顯示圖表
plt.tight_layout()
plt.show()

