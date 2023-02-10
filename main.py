from __future__ import print_function
import time
import cfbd
from cfbd.rest import ApiException
from pprint import pprint
import sys, getopt

def recruit_draft_expected(configuration, stars = None, position = None, state = None, team = None):
    # create an instance of the API class
    draft = cfbd.DraftApi(cfbd.ApiClient(configuration))
    recruit = cfbd.RecruitingApi(cfbd.ApiClient(configuration))
    # game_id = 56 # int | Game id filter (optional)
    # year = 2018 # int | Year/season filter for games (optional)
    # week = 5 # int | Week filter (optional)
    # season_type = 'regular' # str | Season type filter (regular or postseason) (optional) (default to regular)
    # team = 'team_example' # str | Team (optional)
    # home = 'home_example' # str | Home team filter (optional)
    # away = 'away_example' # str | Away team filter (optional)
    # conference = 'conference_example' # str | Conference abbreviation filter (optional)
    # position = 'safety'

    # require 1 recruit parameter
    parameters = [stars, position, state, team]
    none_count = 0
    for item in parameters:
      if item == None:
        none_count += 1
    if none_count > 3:
      print('Please provide at least 1 recruit parameter')
      return

    try:
        # gets recruits that fit parameters
        if position and state and team:
          recruit_list = []
          for year in range(2008, 2017):
            recruit_list.extend(recruit.get_recruiting_players(year = year, position = position, state = state, team = team))
        elif not position and state and team:
          recruit_list = []
          for year in range(2008, 2017):
            recruit_list.extend(recruit.get_recruiting_players(year = year, state = state, team = team))
        elif not position and not state and team:
          recruit_list = []
          for year in range(2008, 2017):
            recruit_list.extend(recruit.get_recruiting_players(year = year, team = team))
        elif position and not state and team:
          recruit_list = []
          for year in range(2008, 2017):
            recruit_list.extend(recruit.get_recruiting_players(year = year, position = position, team = team))
        elif position and state and not team:
          recruit_list = []
          for year in range(2008, 2017):
            recruit_list.extend(recruit.get_recruiting_players(year = year, position = position, state = state))
        elif position and not state and not team:
          recruit_list = []
          for year in range(2008, 2017):
            recruit_list.extend(recruit.get_recruiting_players(year = year, position = position))
        elif not position and state and not team:
          recruit_list = []
          for year in range(2008, 2017):
            recruit_list.extend(recruit.get_recruiting_players(year = year, state = state))
        elif not position and state and not team:
          recruit_list = []
          for year in range(2008, 2017):
            recruit_list.extend(recruit.get_recruiting_players(year = year))

        # converting Recruit objects to dictionary objects
        recruit_dict_list = []
        for rec in recruit_list:
          rec_dict = rec.to_dict()
          recruit_dict_list.append(rec.to_dict())

         
        # filtering by star rating
        if stars:
          temp_list = recruit_dict_list.copy()
          for rec in temp_list:
            if stars != rec['stars']:
              recruit_dict_list.remove(rec)
            
              
             
        # print(recruit_dict_list[0])
        # for rec in recruit_dict_list:
        #   print(rec['name'])
        
        # get draft picks
        draft_list = []
        for year in range(2011, 2022):
          draft_list.extend(draft.get_draft_picks(year = year))
        draft_dict_list = []
        for player in draft_list:
          draft_dict_list.append(player.to_dict())

        # find relevent recruits that were drafted
        drafted_recruits = []
        for rec in recruit_dict_list:
          for player in draft_dict_list:
            if rec['name'] == player['name']:
              drafted_recruits.append(player)

        # stats for relevent recruits
        percent_drafted = len(drafted_recruits) / len(recruit_dict_list)
        print('Percent of recruits drafted: ' + str(percent_drafted * 100) + '%')
        
        round_sum = 0
        pick_sum = 0
        for player in drafted_recruits:
          round_sum += player['round']
          pick_sum += player['overall']
        round_average = round_sum / len(drafted_recruits)
        pick_average = pick_sum / len(drafted_recruits)
        print('Average round drafted: ' + str(round_average))
        print('Average overall pick position drafted: ' + str(pick_average))
        
    #     draft_list = draft.get_draft_picks(position=position)
    #     recruit_list = recruit.get_recruiting_players(year=2015)
    #     draft_dict = draft_list[1].to_dict()
    #     draft_name = draft_dict['name']
    #     for recruit in recruit_list:
    #         recruit_dict = recruit.to_dict()
    #         #print(recruit_dict['name'])
    #         if recruit_dict['name'] == draft_name:
    #             print(draft_name + 'was a ' + str(recruit_dict['stars']) + ' star prospect')
    #  #   pprint(draft_list[1].id)
    except ApiException as e:
        print("Exception when calling BettingApi->get_lines: %s\n" % e)

def main(argv):
    API_KEY = ''
    opts, args = getopt.getopt(argv,"hk:o:", ["key="])
    for opt, arg in opts:
        if opt == '-h':
            print ('test.py -key <API_KEY>')
            sys.exit()
        elif opt in ("-k", "--key"):
            f = open(arg, 'r')
            API_KEY = f.read()

    # Configure API key authorization: ApiKeyAuth
    configuration = cfbd.Configuration()
    configuration.api_key['Authorization'] = API_KEY
    # Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
    configuration.api_key_prefix['Authorization'] = 'Bearer'

    recruit_draft_expected(configuration, stars = 5, team = 'Texas A&M')
    
    return 0

if __name__ == "__main__":
   main(sys.argv[1:])

