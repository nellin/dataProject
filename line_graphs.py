import matplotlib.pyplot as plt

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
    print datums

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

f = open('videogamesales/vgsales.csv', 'r')

video_games = [] #make 2d list to store relevant data for each video game

f.readline() #skip over the first line (headers)

for line in f.readlines():    
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