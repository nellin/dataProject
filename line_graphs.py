import matplotlib.pyplot as plt
import numpy as np
from scipy import stats
import operator

def make_PLTW_style(axes):
    for item in ([axes.title, axes.xaxis.label, axes.yaxis.label] +
             axes.get_xticklabels() + axes.get_yticklabels()):
        item.set_family('Georgia')
        item.set_fontsize(16)
    plt.gcf().subplots_adjust(bottom=0.15)

def create_line_graph(ser):
    '''
    Creates a line graph which plots the year on the x-axis and the global sales
    on the y-axis
    
    ser : list
        contains the names of series (as strings) that will be represented on
        the line graph
        
        ex: ['Super Mario Galaxy', 'Fifa', 'Halo']
    '''
    global video_games
    datums = []
    for series in ser:
        datums.append([video_game for video_game in video_games if series.lower() in video_game[0].lower()])
    
    for datum in datums:
        titles = [title[0] for title in datum]
        i = len(titles)-1
        while i>=0:
            temp = titles.pop()
            if temp in titles:
                datum[titles.index(temp)][1] += datum[i][1]
                datum[titles.index(temp)][1] = round(datum[titles.index(temp)][1], 2)
                datum[titles.index(temp)][2] = min([datum[titles.index(temp)][2], datum[i][2]])
                del datum[i]
            i -= 1
    
        #print datum
        datum.sort(key=operator.itemgetter(2))
        print datum
        graphX = []
        graphY = []
        for a in datum:
            graphX.append(a[2])            
            graphY.append(a[1])
    
    fig, ax = plt.subplots(1,1)
    ax.plot(graphX, graphY, 'ro')
    ax.plot(graphX, np.poly1d(np.polyfit(graphX, graphY, 1))(graphX))
    ax.set_xticks(range(min(graphX)-1, max(graphX)+2))
    ax.set_yticks(range(int(max(graphY))+2))
    ax.grid(color='k', linestyle='-')
    ax.set_xlabel('Date Released')
    ax.set_ylabel('Millions of copies sold')
    ax.set_title("Analysis of Sequels and Sales")
    for i in range(len(datum)):
        ax.annotate(datum[i][0], (graphX[i],graphY[i]))
    fig.show()
    num_games, p_value = run_ttest(datums)

def create_bar_graph(title):
    global video_games
    datums = [[v[1] for v in video_games if v[0].lower() == title.lower()], [v[3] for v in video_games if v[0].lower() == title.lower()]]
    a = range(len(datums[0]))
    fig, ax  = plt.subplots(1, 1)
    ax.bar(a, datums[0], 0.5, align="center")
    ax.set_xticks(a) 
    ax.set_xticklabels(datums[1])
    ax.set_title('Success of ' + title + ' by Console')
    ax.set_xlabel('Console')
    ax.set_ylabel('Copies sold (millions of games)')
    make_PLTW_style(ax)
    fig.show()

def run_ttest(datums):
    '''
    Returns a tuple pair with the number of video games used and the p value
    
    For t-test:
    Input list is the order in the series
    Output list is the number of sales for the game divided by the mean number
     of sales for the video game series as a whole
    '''
    total_seqs = [] #e.g. Super Mario Galaxy is 1, Super Mario Galaxy 2 is 2
    total_adj_sales = []
    
    for datum in datums:
        datum.sort(key = lambda x: x[2])
        seqs = range(1, len(datum) + 1)
        sales = [video_game[1] for video_game in datum]
        
        avg_sale = sum(sales) / len(sales)
        adjusted_sales = [sale/avg_sale for sale in sales]
        
        total_seqs += seqs
        total_adj_sales += adjusted_sales
    
    seq_array = np.array(total_seqs)
    sales_array = np.array(total_adj_sales)
    
    return (len(total_seqs), stats.ttest_ind(seq_array, sales_array)[1])
    

f = open('videogamesales/vgsales.csv', 'r')

video_games = [] #make 2d list to store relevant data for each video game

f.readline() #skip over the first line (headers)

#read first 10000 lines instead of all of them to avoid counting mission packs and similar add-ons
for i in range(10000):
    line = f.readline()   
    #store data from each line as an array
    data = line.rstrip('\n').split(',')
    
    #get relevant data
    title = data[1]
    console = data[2]
    global_sales = float(data[10])
    try:
        year = int(data[3])
    except ValueError:
        year = None
    
    video_games.append([title, global_sales, year, console])
     
f.close()