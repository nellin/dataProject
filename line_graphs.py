import matplotlib.pyplot as plt

def create_line_graph(ser):
    '''
    Creates a line graph which plots the year on the x-axis and the global sales
    on the y-axis
    
    ser : list
        contains the names of series (as strings) that will be represented on
        the line graph
    '''
    datums = []
    for series in ser:
        datums.append([video_game for video_game in video_games if series in video_game[0].lower()])


f = open('videogamesales/vgsales.csv', 'r')

video_games = [] #make 2d list to store relevant data for each video game

f.readline() #skip over the first line (headers)

for line in f.readlines():    
    #store data from each line as an array
    data = line.rstrip('\n').split(',')
    
    #get relevant data
    title = data[1]
    global_sales = float(data[10])
    try:
        year = int(data[3])
    except ValueError:
        year = 'N/A'
    
    video_games.append([title, global_sales, year])
     
f.close()