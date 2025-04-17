# -*- coding: cp1251 -*-

import tkinter as tk
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
matplotlib.rc("font", size=6) # для увеличения шрифта подписей графиков
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
import statistics
from tkinter import *


class DashboardApp:
    
    def __init__(self, parent):
        self.parent = parent
        self.parent.title("Аналитика по Yes Online")
        self.create_widgets()
        

    def addlabels(x,y):
        for i in range(len(x)):
             plt.text(i,y[i],y[i])
                
    def create_widgets(self):
        groups = pd.read_csv('groups.csv')
        lessons = pd.read_csv('lessons.csv')
        attendances = pd.read_csv('attendances.csv')
        
        bd_online = pd.merge(lessons, attendances, left_on=lessons['_id'], right_on=attendances['lessonId'], how='inner')
        del bd_online['key_0']
        
        bd_online = pd.merge(bd_online, groups, left_on=bd_online['groupId'], right_on=groups['_id'], how='inner')
        del bd_online['key_0']
        
        bd_online = bd_online[bd_online['filial'] == '63c63702397ca6783eb57fa2']
        
        dates = pd.DataFrame({'count':[], 'month':[], 'year':[], 'date':[]})
        i=0
        
        for year in range(min(bd_online['date'].astype("datetime64[ns]").dt.year), max(bd_online['date'].astype("datetime64[ns]").dt.year)+1):
            for month in range(1, 13):
                count = bd_online[bd_online['date'].astype("datetime64[ns]").dt.year == year]
                count = (count[count['date'].astype("datetime64[ns]").dt.month == month])['date'].count()
                dates.loc[i]=[count,month,year,str(month)+'-'+str(year)]
                i+=1
                
        dates.groupby(dates['year'])
        dates.groupby(dates['month'])  
        dates=dates[11:-3]
        total = 0
        
        for d in dates['count']:
            total += d
        num1 = round(total/len(dates), 1)
        mean1 = round(statistics.mean(dates['count']), 1)
        median1 = statistics.median(dates['count'])
                
        fig = plt.figure(figsize=(4, 2)) # создаем картинку
        ax = plt.axes()
        featureOne = 'Месяц'
        featureTwo = 'Количество посещений'
        
        # помещаем точки на график
        ax.scatter(dates['date'], dates['count'], s=10)
        plt.plot(dates['date'], dates['count'], '-')
        
        plt.axhline (y=mean1, color='red', linestyle='--', label = 'Среднее')
        plt.axhline (y=median1, color='green', linestyle='--', label = 'Медиана')
        
        plt.legend()
        
        # отображаем картинку
        ax.set_xlabel(featureOne)
        ax.set_ylabel(featureTwo)
        plt.xticks(rotation=90)
        plt.subplots_adjust(bottom=0.3)
        plt.grid()
        canvas1 = FigureCanvasTkAgg(fig, master = parent)
        canvas1.get_tk_widget().grid(row=5, column=3)
        canvas1.draw()
        
        label2 = tk.Label(text="", font=("Helvetica", 14))
        label2.grid(row=5, column=0)
        stat_label1 = tk.Label(text="Основными данными для этого графика \nявляются посещения каждого студента \n( 1 урок * кол-во студентов в группе ). \n\nТочкой на графике является среднее \nкол-во посещений всех студентов в месяц. \n\nСреднее кол-во посещений студентами в месяц: " + str(num1) + "\n\nМедиана по графику равна: " + str(median1), font=("Helvetica", 12)) #attendance
        stat_label1.grid(row=5, column=1)
        label2 = tk.Label(text="", font=("Helvetica", 14))
        label2.grid(row=5, column=2)
        # ГРАФИК grid(row=5, column=3)
        label2 = tk.Label(text="", font=("Helvetica", 14))
        label2.grid(row=5, column=4)
        

if __name__ == "__main__":
    
    parent = tk.Tk()
    app = DashboardApp(parent)
    parent.mainloop()
