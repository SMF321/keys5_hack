from tabnanny import check
import time
import seaborn as sns
import matplotlib
from matplotlib import pyplot as plt

#Функция построения графиков 
def Statistics(id, question):
    time.sleep(0.6)
    matplotlib.rc('axes', edgecolor='r')
    sns.set_style('darkgrid')
    
    COLOR = 'white'
    plt.rcParams['text.color'] = COLOR
    plt.rcParams['axes.labelcolor'] = COLOR
    plt.rcParams['xtick.color'] = COLOR
    plt.rcParams['ytick.color'] = COLOR
    x1 = []
    x2 = []
    x3 = []
    for i in range(1, len(question[0])+1):
        x1.append(i)
    for i in range(1, len(question[1])+1):
        x2.append(i)
    for i in range(1, len(question[2])+1):
        x3.append(i)
    y = question[0]
    plt.figure(facecolor='black')
    plt.style.use('dark_background')
    plt.xlim(1, len(x1))
    plt.ylim(0, 10)
    plt.plot(x1, y)
    plt.title('Результаты ответов на вопрос:\n'
              '«Насколько Вы удовлетворены\n материалами модуля?»',
              fontsize=18,
              color='White'
              )
    plt.xlabel('Опрос', color='White')
    plt.ylabel('Балл', color='White')
    plt.savefig(f'utils/statistics/{id}_graph1.png')
    plt.figure(facecolor='black')
    y = question[1]
    plt.style.use('dark_background')
    plt.xlim(1, len(x2))
    plt.ylim(0, 10)
    plt.plot(x2, y)
    plt.title('Результаты ответов на вопрос:\n'
              '«Насколько материалы модуля\n были Вам интересны?»',
              fontsize=18,
              color='White'
              )
    plt.xlabel('Опрос', color='White')
    plt.ylabel('Балл', color='White')
    plt.savefig(f'utils/statistics/{id}_graph2.png')
    plt.figure(facecolor='black')
    y = question[2]
    plt.style.use('dark_background')
    plt.xlim(1, len(x3))
    plt.ylim(0, 10)
    plt.plot(x3, y)
    plt.title('Результаты ответов на вопрос:\n'
              '«Насколько материалы модуля\n были Вам понятны?»',
              fontsize=18,
              color='White'
              )
    plt.xlabel('Опрос', color='White')
    plt.ylabel('Балл', color='White')
    plt.savefig(f'utils/statistics/{id}_graph3.png')
