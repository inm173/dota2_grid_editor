import json
import _USER_DATA
import requests
import pandas as pd

class hero_grid():
        
    """
    Main Class For Making Grids

    ...

    Methods
    -------
    create_hero_grid(grid_name,column_to_sort_by,which_hero_list,heroes_per_line)
        Parameters
        ----------
        grid_name : str
            Name of the grid.
        sort_by : str
            column to sort by, for example ('winrate','personal_match_played').
        heroes_list : str
            'all' for of all heroes, 'played' for using heroes you've at least played for 2 matches.
        
        
        
    role_grid(grid_name,column_to_sort_by,which_hero_list)
        Parameters
        ----------
        grid_name : str
            Name of the grid.
        sort_by : str
            column to sort by, for example ('winrate','personal_match_played').
        heroes_list : str
            'all' for of all heroes, 'played' for using heroes you've at least played for 2 matches.
        
    """
    def __init__(self):
        
        player_stats_json = requests.get(f'https://api.opendota.com/api/players/{_USER_DATA.steam_id}/heroes')
        player_details = requests.get(f'https://api.opendota.com/api/players/{_USER_DATA.steam_id}')
        self.player_name = player_details.json().get('profile').get('personaname')
        self.player_mmr = player_details.json().get('mmr_estimate').get('estimate')
        self.player_stats = pd.DataFrame(player_stats_json.json())
        self.all_heroes = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 119, 120, 121, 123, 126, 128, 129]
        self.favorite_heroes = list(self.player_stats.loc[self.player_stats['games'] >= 2]['hero_id'].astype('int'))
        self.player_stats.drop(columns=['with_games','last_played','with_win','against_games','against_win','win'],inplace=True)
        self.player_stats.rename(columns={'hero_id': 'id','games':'personal_match_played'},inplace=True)
        self.player_stats["id"] = pd.to_numeric(self.player_stats["id"])
        
        
        
    def create_hero_grid(self,grid_name,sort_by,heroes_list,heroes_per_line=7):
      
        if heroes_list == 'played':
            
            heroes = self.favorite_heroes
        else:
            heroes = self.all_heroes
            
        with open(_USER_DATA.dota2_account_id + "/hero_grid_config.json") as json_file,open('heroes_data.csv','r') as hero_json:
            pos = False
            data = json.load(json_file)
            df = pd.read_csv(hero_json)
            df["id"] = pd.to_numeric(df["id"])
            df = df.join(self.player_stats.set_index('id'), on='id')
            df = df[df['id'].isin(heroes)]
            for i,x in zip(data['configs'],range(1000)):
              if i['config_name'] == grid_name:
                pos = x
                break
              else:
                continue
            if pos == False:
              data['configs'].append({"config_name":grid_name,'categories':[]})
              pos = -1
                
                  
            it = -1
            data['configs'][pos] = {'config_name':grid_name,'categories':[]}
            data['configs'][pos].get('categories').append({'category_name':'MMR: ' + str(self.player_mmr),"x_position":0,"y_position":0,"width":8,"height":8,"hero_ids":[]})
            data['configs'][pos].get('categories').append({'category_name':'https://github.com/Psychewolf/dota2_grid_editor',"x_position":100,"y_position":0,"width":8,"height":8,"hero_ids":[]})
            min_win = int(min(df[sort_by])) - 1
            df = df.set_index('id')
            for x in range(0,1100,int(1100/(len(heroes)/heroes_per_line))):
              for y in range(0,510,int(550/heroes_per_line)):
                it+=1
                if it>len(heroes)-1:
                  break
                df = df.sort_values(sort_by,ascending=False)
                now_hero = df.iloc[it]
                category_name = int(now_hero[sort_by])
                hero = str(now_hero.name)
                
                data['configs'][pos].get('categories').append({'category_name':int(category_name),"x_position":x,"y_position":y,"width":6*(category_name - min_win),"height":7*(category_name - min_win),"hero_ids":[hero]})
      
            
        with open(_USER_DATA.dota2_account_id + "/hero_grid_config.json",'w') as json_file:
          json.dump(data,json_file,indent=4)
          
    
    def role_grid(self,grid_name,sorted_by,heroes_list):
        
        
         if heroes_list == 'played':
            heroes = self.favorite_heroes
         else:
            heroes = self.all_heroes

         with open(_USER_DATA.dota2_account_id + "/hero_grid_config.json") as json_file,open('heroes_data.csv','r') as hero_json:
            pos = False
            df = pd.read_csv(hero_json)
            num_to_lane = {1:"safelane",2:"mid",3:"offlane",4:"support",5:"hard-support"}
            data = json.load(json_file)
            df["id"] = pd.to_numeric(df["id"])
            df = df.join(self.player_stats.set_index('id'), on='id')
            df = df[df['id'].isin(heroes)]
            for i,x in zip(data['configs'],range(1000)):
    
              if i['config_name'] == grid_name:
                pos = x
                break
              else:
                continue
            if pos == False:
              data['configs'].append({"config_name":grid_name,'categories':[]})
              pos = -1
    
    
            it = -1
            got = -1
            roles = [1,2,3,4,5]
            
            data['configs'][pos] = {'config_name':grid_name,'categories':[]}
            
            data['configs'][pos].get('categories').append({'category_name':'Grid made for '+str(self.player_name),"x_position":630,"y_position":510,"width":8,"height":8,"hero_ids":[]})
            data['configs'][pos].get('categories').append({'category_name':'Players MMR: ' + str(self.player_mmr),"x_position":630,"y_position":530,"width":8,"height":8,"hero_ids":[]})
            data['configs'][pos].get('categories').append({'category_name':'https://github.com/Psychewolf/dota2_grid_editor',"x_position":630,"y_position":550,"width":8,"height":8,"hero_ids":[]})
            for x in range(0,1100,int(1100/2)-1):
              got += 1
              for y in [0,215,395]:
                it+=1
                if it+1>len(roles):
                  break
                width = 550
                padding = ''
                if roles[it] == 3:
                  width = 1100
                  padding = str('-'*71)

                data['configs'][pos].get('categories').append({'category_name':padding+num_to_lane.get(roles[it])+padding,"x_position":x,"y_position":y,"width":width,"height":160,"hero_ids":list(df[df['lane'] == roles[it]].sort_values(sorted_by,ascending=False)['id'])})
            with open(_USER_DATA.dota2_account_id + "/hero_grid_config.json",'w') as json_file:
              json.dump(data,json_file,indent=4)
    def execute_defaults(self):
        self.role_grid('Rolegrid','winrate','all')   
        self.role_grid('Rolegrid: SORTED BY MATCH PLAYED','personal_match_played','played')
        
        self.create_hero_grid('ALL_HEROES_SORTED_BY_WINRATE','winrate','all')
        self.create_hero_grid('YOUR HEROES SORTED_BY_WINRATE','winrate','played')

     
