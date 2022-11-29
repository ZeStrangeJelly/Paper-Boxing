import turtle
import random

t = turtle.Turtle()
t2 = turtle.Turtle()

def draw_grid(shifted_x):
    '''draws the grid'''
    t.ht()
    t.pu()
    t.goto(shifted_x, 0)
    t.pd()
    t.speed(0)
    t.goto(200 + shifted_x, 0)
    t.goto(200 + shifted_x, 200)
    t.goto(0 + shifted_x, 200)
    t.goto(0 + shifted_x, 0)
    t.goto(0 + shifted_x, 50)
    t.goto(200 + shifted_x, 50)
    t.goto(200 + shifted_x, 100)
    t.goto(0 + shifted_x, 100)
    t.goto(0 + shifted_x, 150)
    t.goto(200 + shifted_x, 150)
    t.up()
    t.goto(0 + shifted_x, 200)
    t.pd()
    t.goto(50 + shifted_x, 200)
    t.goto(50 + shifted_x, 0)
    t.goto(100 + shifted_x, 0)
    t.goto(100 + shifted_x, 200)
    t.goto(150 + shifted_x, 200)
    t.goto(150 + shifted_x, 0)
    t.pu()
    if shifted_x == 0: #Player Grid
        t.goto(100, 215)
        t.write("Player 1 Grid", move = False, align = 'center', font = ('Arial', 15, 'bold'))
    if shifted_x == 300: #Computer Grid
        t.goto(400, 215)
        t.write("Player 2 Grid", move = False, align = 'center', font = ('Arial', 15, 'bold'))
    return shifted_x
    #shifted_x = draw_grid()
    
def place_numbers(List, shifted_x):
    '''takes List and places on grid'''
    x = shifted_x
    y = 0
    for i in List:
        t.pu()
        t.goto(x + 25, y + 160)
        t.write(i, move = False, align = 'center', font = ('Arial', 20, 'normal'))
        #--------
        if x <= 100 + shifted_x:
            x+= 50
        else:
            x = shifted_x
            y -= 50
        
def make_random_list(List):
    '''makes a list of random numbers'''
    List = []
    for x in range(15):
        List.append(str(x + 1))
    random.shuffle(List)
    List.insert(0, 'S')
    return List

def find_max(List):
    '''finds the biggest number in a list of strings of integers'''
    high = 0
    for i in List:
        if int(i) > int(high):
            high = int(i)
    return str(high)
    
def find_min(List):
    '''finds the smallest number in a list of strings of integers'''
    low = 10000
    for i in List:
        if int(i) < int(low):
            low = int(i)
    return str(low)

def enter_currentIndex_return_numList(index, List):
    '''takes the index of the current number the player is on and returns the list of numbers that the player can move to in this turn'''
    r = int(index/4)
    c = index % 4
    index_list = []
    #Above row
    new_r = r - 1
    if new_r >= 0: 
        new_c = c - 1
        if new_c >= 0: #Left column
            new_index = 4 * new_r + new_c
            index_list.append(new_index)
        new_c = c #Same column
        new_index = 4 * new_r + new_c
        index_list.append(new_index)
        new_c = c + 1
        if new_c <= 3: #Right column
            new_index = 4 * new_r + new_c
            index_list.append(new_index)
        new_c = c - 1
    #Same Row
    new_r = r
    new_c = c - 1
    if new_c >= 0: #Left column
        new_index = 4 * new_r + new_c
        index_list.append(new_index)    
    new_c = c + 1
    if new_c <= 3: #Right column
        new_index = 4 * new_r + new_c
        index_list.append(new_index)
    #Below Row
    new_r = r + 1     
    if new_r <= 3: 
        new_c = c - 1
        if new_c >= 0: #Left column
            new_index = 4 * new_r + new_c
            index_list.append(new_index)
        new_c = c #Same column
        new_index = 4 * new_r + new_c
        index_list.append(new_index)
        new_c = c + 1
        if new_c <= 3: #Right column
            new_index = 4 * new_r + new_c
            index_list.append(new_index)
        new_c = c - 1
    adjacent_number_list = []
    for i in index_list:
        adjacent_number_list.append(List[i])
    return adjacent_number_list

def first_turn(List1, List2):
    '''sets up first turn'''
    t.pu()
    t.ht()
    t.goto(25, 175)
    t2.pu()
    t2.ht()
    t2.goto(325, 175)
    player_1_moveList = List1.copy()
    player_2_moveList = List2.copy()
    player_1_moveList.remove('S')
    player_2_moveList.remove('S')
    current_number = 'S'
    x = [player_1_moveList, player_2_moveList, current_number]
    return x

#Stratnum 1 -> Random
#Stratnum 2 -> Biggest Number
#Stratnum 3 -> Probability

def computer_strat_index(List, current_number, moveList, enemy_List, enemy_current_number, enemy_moveList, stratnum): 
    '''the general strategy code using index version'''
    if current_number == '0':
        return [moveList, '0']
    cmmnList = find_common_list(List, current_number, moveList)
    if len(cmmnList) != 0: #If there are still possible numbers to go to
        if stratnum == 1: #Random
            newNum = random.choice(cmmnList)
        elif stratnum == 2: #Biggest Number
            newNum = find_max(cmmnList)
        elif stratnum == 3: #Probability (for first player only)
            if enemy_current_number == 0:
                newNum = random.choice(cmmnList)
            else:
                enemy_cmmnList = find_common_list(enemy_List, enemy_current_number, enemy_moveList)
                if len(enemy_cmmnList) == 0:
                    newNum = random.choice(cmmnList)
                else:
                    probList = []
                    for i in cmmnList:
                        probCount = 0
                        enemy_cmmnList_count = len(enemy_cmmnList)
                        for j in enemy_cmmnList:
                            if int(i) >= int(j):
                                probCount += 1
                        probList.append(probCount / enemy_cmmnList_count * 100)
                    average = 0
                    for i in probList:
                        average += i
                    average /= len(probList)
                    if average >= 50:
                        index_of_all_highest_prob = []
                        highest_prob = max(probList)
                        while highest_prob in probList: #problem
                            index_of_all_highest_prob.append(probList.index(highest_prob))
                            probList[probList.index(highest_prob)] = 0
                        low = 100
                        for i in index_of_all_highest_prob:
                            if int(cmmnList[i]) < low:
                                low = int(cmmnList[i])
                        newNum = str(low)
                    if average < 50:
                        newNum = find_min(cmmnList)
        
        moveList.remove(newNum)
        current_number = newNum
        return [moveList, current_number]
    else: #Either trapped or finished the entire board
        return [moveList, '0']

def find_common_list(List, current_number, moveList):
    if current_number == '0':
        return []
    index = List.index(current_number)
    adjacent_num_list = enter_currentIndex_return_numList(index, List)
    #Checks if there are any availiable numbers
    #Makes a list with common numbers from List and moveList
    cmmnList = [value for value in moveList if value in adjacent_num_list] #Lenka, Chinmoy. (11/17/2022) Intersection of Two Lists. GeeksforGeeks. 
    return cmmnList                                                        #https://www.geeksforgeeks.org/python-intersection-two-lists/
    
#Makes lists and prints them out    
empty_list = []
player_1_list = make_random_list(empty_list)
player_2_list = make_random_list(empty_list)
shifted_x1 = draw_grid(0)
place_numbers(player_1_list, shifted_x1)
shifted_x2 = draw_grid(300)
place_numbers(player_2_list, shifted_x2)

#First turn and making moveList and currentNumber variables
ListList = first_turn(player_1_list, player_2_list)
player_1_moveList = ListList[0]
player_2_moveList = ListList[1]
player_1_currentNumber = ListList[2]
player_2_currentNumber = ListList[2]

#Establishes scores
player_1_score = 0
player_2_score = 0

while True:
    #Player 1
    x = computer_strat_index(player_1_list, player_1_currentNumber, player_1_moveList, player_2_list, player_2_currentNumber, player_2_moveList, 3) #Probability
    player_1_moveList = x[0]
    player_1_currentNumber = x[1]
    if player_1_currentNumber == '0': #If nowhere to go
        print("Player 1 cannot move anywhere")
    else:
        print("Player 1 moved to " + str(player_1_currentNumber))
    
    #Player 2
    x = computer_strat_index(player_2_list, player_2_currentNumber, player_2_moveList, player_1_list, player_1_currentNumber, player_1_moveList, 1) #Random
    player_2_moveList = x[0]
    player_2_currentNumber = x[1]
    if player_2_currentNumber == '0': #If nowhere to go
        print("Player 2 cannot move anywhere")
    else:
        print("Player 2 moved to " + str(player_2_currentNumber))

    #When both currentNumber are 0
    if player_1_currentNumber == '0' and player_2_currentNumber == '0':
        break
    #Calculate Score
    if int(player_1_currentNumber) > int(player_2_currentNumber): #If Player 1 has a bigger number
        player_1_score += 1
        
    elif int(player_2_currentNumber) > int(player_1_currentNumber): #If Player 2 has a bigger number
        player_2_score += 1

#Calculate final score
print("Player 1 Score: " + str(player_1_score)) 
print("Player 2 Score: " + str(player_2_score))
if player_1_score > player_2_score:
    print("Player 1 Wins!")
elif player_1_score < player_2_score:
    print("Player 2 Wins!")
else:
    print("Tie!")
    
        

    





    


