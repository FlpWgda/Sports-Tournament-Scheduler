import numpy as np

NUMBER_OF_FIXTURES = 6
TEAMS = ['Team A', 'Team B', 'Team C', 'Team D', 'Team E', 'Team F', 'Team G', 'Team H', 'Team I', 'Team J']
MAX_NUMBER_OF_HOME_GAMES = int(NUMBER_OF_FIXTURES/2) if NUMBER_OF_FIXTURES%2 == 0 else int(NUMBER_OF_FIXTURES/2)+1
MAX_NUMBER_OF_AWAY_GAMES = int(NUMBER_OF_FIXTURES/2) if NUMBER_OF_FIXTURES%2 == 0 else int(NUMBER_OF_FIXTURES/2)+1
SAME_COUNTRY_TEAMS = [[TEAMS.index('Team A')+1,TEAMS.index('Team B')+1],
                      [TEAMS.index('Team C')+1,TEAMS.index('Team D')+1]]
SAME_ARENA_TEAMS = [[TEAMS.index('Team A')+1, TEAMS.index('Team B')+1]]

new_schedule = np.zeros((len(TEAMS), NUMBER_OF_FIXTURES))

def fill(schedule):
    next_field = find_empty(schedule)

    # if there is no empty fields in schedule then it satisfies all constraints
    if not next_field:
        return True
    else:
        row, fixture = next_field

    for i in range(1, len(TEAMS) + 1):
        if check(schedule, i, (row, fixture)):
            schedule[row][fixture] = i

            if fill(schedule):
                return True

            # in case of no possibility to satisfy all constraints in further recursion levels this field in a schedule is reseted
            schedule[row][fixture] = 0

    return False

def check(schedule, team, pos):

    # every team can play only one game in each fixture
    for i in range(schedule.shape[0]):
        if schedule[i][pos[1]] == team:
            return False

    # same teams cannot play each other twice
    if pos[0]%2 == 1:
        opposing_team = schedule[pos[0]-1][pos[1]]
        for i in range(0, pos[1]):
            for j in range(schedule.shape[0]):
                if schedule[j][i] == team:
                    if j%2 == 0:
                        if schedule[j+1][i] == opposing_team:
                            return False
                    else:
                        if schedule[j-1][i] == opposing_team:
                            return False

    # home/away games balance needs to be preserved
    counter = 0
    if pos[0]%2 == 0:
        for i in range(0,pos[1]):
            for j in range(0,schedule.shape[0],2):
                if schedule[j][i] == team:
                    counter += 1
                    if counter == MAX_NUMBER_OF_HOME_GAMES:
                        return False
    if pos[0]%2 == 1:
        for i in range(0,pos[1]):
            for j in range(1,schedule.shape[0],2):
                if schedule[j][i] == team:
                    if counter == MAX_NUMBER_OF_AWAY_GAMES:
                        return False
                    counter += 1

    # teams from the same country cannot play each other in this round
    if pos[0]%2 == 1:
        for i in SAME_COUNTRY_TEAMS:
            if (team in i) and (schedule[pos[0]-1][pos[1]] in i):
                return False

    # teams sharing home arena cannot host games in the same fixture
    if pos[0]%2 == 0:
        for i in SAME_ARENA_TEAMS:
            for j in range(0,pos[0],2):
                if (team in i) and (schedule[j][pos[1]] in i):
                    return False

    return True

def find_empty(schedule_space):
    for i in range(len(schedule_space[0])):
        for j in range(len(schedule_space)):
            if schedule_space[j][i] == 0:
                return (j, i)

    return None

def read_schedule(schedule):
    list_of_games = []
    for i in range(schedule.shape[1]):
        for j in range(0,schedule.shape[0],2):
            game = {'fixture': i+1, 'home_team': schedule[j][i], 'away_team': schedule[j+1][i]}
            list_of_games.append(game)

    return list_of_games

def schedule_for_every_team(games_list):
    team_schedules = [[] for i in range(len(TEAMS))]
    for i in list_of_games:
        team_schedules[i['home_team']-1].append((str(i['fixture']) + ': ' + str(TEAMS[i['away_team']-1]) + '(home)'))
        team_schedules[i['away_team']-1].append((str(i['fixture']) + ': ' + str(TEAMS[i['home_team']-1]) + '(away)'))

    for i in range(0,len(team_schedules)):
        print(TEAMS[i],' ',team_schedules[i])

fill(new_schedule)
new_schedule = new_schedule.astype(int)
print(new_schedule)
print()
list_of_games = read_schedule(new_schedule)
schedule_for_every_team(list_of_games)