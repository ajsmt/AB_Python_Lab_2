import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import sqlite3
from sklearn.preprocessing import LabelEncoder

def main():
    print("Лабораторная работа 3. Обработка данных на языке Python")
    print('Анализ набора данных "German Credit Data"\n\n\n')
    
    print("______1)Загрузка и подготовка данных______")
    
    #Назначение именованных столбцов согласно предоставленной спецификации.
    columns = [
        "checking_status",
        "duration",
        "credit_history",
        "purpose",
        "credit_amount",
        "savings",
        "employment",
        "installment_rate",
        "personal_status",
        "other",
        "residence_since",
        "property",
        "age",
        "other_installments_plans",
        "housing",
        "existing_credits",
        "job",
        "number_of_liable",
        "telephone",
        "foreing_worker",
        "class"
    ]
    
    #загрузка набора данных "German Credit Data"
    df = pd.read_csv("./statlog+german+credit+data/german.data", sep=" ", names=columns)
    print("часть данных:")
    print(df.head())
    
    #обработка возможных пропущенных значений
    missing_values = df.isnull().sum().sum()
    print("кол-во пропущенных значений: " + str(missing_values))
    
    print("\n\n\n______2)Анализ данных______")
    
    #описание числовых признаков
    print("описание числовых признаков:")
    print(df.describe())
    
    #описание числовых признаков
    print("анализ категориальных признаков:")
    print(df.describe(include=["object"]))
    
    #кодирование категориальных признаков в числовой формат для дальнейшего анализа.
    df_encoded = df.copy()
    le = LabelEncoder()
    for column in df_encoded.columns:
        if df_encoded[column].dtype == "object":
            df_encoded[column] = le.fit_transform(df_encoded[column])
    
    print("анализ закодированных категориальных признаков:")
    print(df_encoded.describe())
    
    print("\n\n\n______3)Обработка и исследование взаимосвязей______")
    #обработка и исследование взаимосвязей
    #построение корреляционной матрицы числовых признаков.
    plt.figure(figsize=(14, 12))
    sns.heatmap(df_encoded.corr(), annot=True, fmt=".2f", cmap="coolwarm")
    plt.title(" корреляционная матрица числовых признаков")
    plt.show()
    
    #группировки и агрегация
    print("\nгруппировка по целям: средняя сумма и срок кредита")
    group_purpose = df.groupby(["purpose", "class"])[["credit_amount", "duration"]].mean().round(1)
    print(group_purpose.sort_values(by="credit_amount", ascending=False))
    
    print("\nгруппировка по классу риска (1=Good, 2=Bad):")
    group_class = df.groupby("class")[["credit_amount", "age", "duration"]].mean().round(1)
    print(group_class)
    
    print("\nгруппировка по кредитной истории (среднее число нынешних кредитов):")
    history_group = df.groupby(["credit_history", "class"])["existing_credits"].mean()
    print(history_group.sort_values(ascending=False))
    
    print("\nгруппировка по проценту рассрочки (средняя сумма кредита):")
    rate_group = df.groupby(["installment_rate", "class"])["credit_amount"].mean()
    print(rate_group)
    
    print("\nгруппировка по работе (средняя сумма кредита):")
    job_group = df.groupby(["job", "class"])["credit_amount"].mean().sort_values(ascending=False)
    print(job_group)
    
    print("\nгруппировка по типу имущества (средняя сумма кредита):")
    prop_group = df.groupby(["property", "class"])["credit_amount"].mean().sort_values(ascending=False)
    print(prop_group)
    
    print("\nгруппировка по типу имущества (средний срок кредита):")
    prop_dur_group = df.groupby(["property", "class"])["duration"].mean().sort_values(ascending=False)
    print(prop_dur_group)
    
    print("\nгруппировка средней длительность кредита в зависимости от Работы и Класса:")
    job_dur_group = df.groupby(['job', 'class'])['duration'].mean().round(1).unstack()
    print(job_dur_group)
    
    print("\n\n\n______4)Визуализация данных______")

    #barplot
    plt.figure(figsize=(10, 6))
    order_purpose = df.groupby("purpose")["credit_amount"].mean().sort_values(ascending=False).index
    sns.barplot(x="credit_amount", y="purpose", data=df, order=order_purpose, hue="class", palette="deep")
    plt.title("средняя сумма кредита по целям кредита")
    plt.xlabel("mean credit_amount")
    plt.ylabel("purpose")
    plt.show()

    #boxplot
    plt.figure(figsize=(8, 6))
    sns.boxplot(data=df, x="class", y="credit_amount", hue="class", palette="deep")
    plt.title('распределение сумм кредита для хороших (1) и плохих (2) типов заемщиков')
    plt.xlabel("class")
    plt.ylabel("credit_amount")
    plt.show()

    #pointplot
    plt.figure(figsize=(10, 6))
    plt.title("зависимость суммы кредита от процента рассрочки")
    sns.pointplot(data=df, x="installment_rate", y="credit_amount", capsize=.2, hue="class", palette="deep")
    plt.xlabel("installment_rate")
    plt.ylabel("credit_amount")
    plt.grid(True)
    plt.show()

    #boxplot
    plt.figure(figsize=(10, 6))
    order_prop = df.groupby("property")["credit_amount"].mean().sort_values(ascending=False).index
    sns.boxplot(data=df, x="property", y="credit_amount", order=order_prop, hue="class", palette="deep")
    plt.title("связь типа имущества и суммы кредита")
    plt.show()
    
    #boxplot 
    plt.figure(figsize=(10, 6))
    order_prop_dur = df.groupby("property")["duration"].mean().sort_values(ascending=False).index
    sns.boxplot(data=df, x="property", y="duration", order=order_prop_dur, hue="class", palette="deep")
    plt.title("связь типа имущества и длительности кредита")
    plt.show()

    #boxplot
    plt.figure(figsize=(10, 6))
    order_job_dur = df.groupby("job")["duration"].mean().sort_values(ascending=False).index
    sns.boxplot(data=df, x="job", y="duration", order=order_job_dur, hue="class", palette="deep")
    plt.title("связь работы и длительности кредита")
    plt.show()
    
    print("\n\n\n______5)Работа с базой данных______")
    
    #подключение к базе данных и загрузка данных
    conn = sqlite3.connect("german_data.db")
    cursor = conn.cursor()
    df.to_sql("credits", conn, if_exists="replace", index=False)
    print("база данных подключена и заполнена")
    
    #запросы к базе данных
    q1 = """
    SELECT purpose, credit_amount, duration, age, job, class
    FROM credits
    ORDER BY credit_amount DESC
    LIMIT 5
    """
    print("запрос: назначение, размер и длительность кредита, возраст и наличие работы:")
    print(pd.read_sql(q1, conn))

    q2 = """
    SELECT purpose, 
        COUNT(*) as count, 
        ROUND(AVG(credit_amount), 0) as avg_amount
    FROM credits
    GROUP BY purpose
    ORDER BY avg_amount DESC
    """
    print("запрос: количество и средний размер кредита по целям кредита")
    print(pd.read_sql(q2, conn))

    q3 = """
    SELECT age, credit_amount, duration
    FROM credits
    WHERE class = 2 AND property = "A124" AND credit_amount >= 4000
    ORDER BY credit_amount DESC
    LIMIT 5
    """
    print("запрос: возраст кредитора, размер и длительности кредита, при условии что размер кредита не меньше 4000")
    print(pd.read_sql(q3, conn))
    
    #отсоединение базы данных
    conn.close()
    print("база данных отключена")
    
    print("====конец выполнения лабораторной работы====")


if __name__ == "__main__":
    main()