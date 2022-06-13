import matplotlib.pyplot as plt

#Построение круговой диогграммы
def circle_diagram(id,my_list1, my_list2):  # на вход 2 массива
    my_list = my_list1 + my_list2
    COLOR = 'white'
    plt.rcParams['text.color'] = COLOR
    plt.rcParams['axes.labelcolor'] = COLOR
    plt.rcParams['xtick.color'] = COLOR
    plt.rcParams['ytick.color'] = COLOR
    plt.figure(facecolor='black')
    negative = my_list.count("negative")
    positive = my_list.count("positive")
    neutral = my_list.count("neutral")
    sum = negative+positive+neutral
    help_arr = [negative/sum*100, positive/sum*100, neutral/sum*100]

    plt.title('Ваше настроение за неделю \n')
    plt.pie(help_arr, labels=["негатив", "позитив ",
            " нейтрально"], autopct='%1.1f%%')
    # возвращает график круговой диаграммы
    plt.savefig(f'utils/statistics/{id}_circle.png')
