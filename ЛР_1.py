import pandas as pd
from datetime import datetime

# Створюємо DataFrame безпосередньо з даними поточного часу
data_frame = pd.DataFrame([{
    "year": datetime.now().year,
    "month": datetime.now().month,
    "day": datetime.now().day,
    "hour": datetime.now().hour,
    "minute": datetime.now().minute,
    "second": datetime.now().second
}])

print(data_frame)

# Зберігаємо DataFrame в CSV-файл без індексу
data_frame.to_csv("filename.csv", index=False)
