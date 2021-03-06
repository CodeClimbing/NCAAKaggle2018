import numpy as np
import pandas as pd
import os


data_path = os.path.abspath('.') + '/DataFiles/'




def get_advanced_metrics(df,csv_name=''):
	#Points Winning/Losing Team
	df['WPts'] = df.apply(lambda row: 2*row.WFGM + row.WFGM3 + row.WFTM, axis=1)
	df['LPts'] = df.apply(lambda row: 2*row.LFGM + row.LFGM3 + row.LFTM, axis=1)

	#Calculate Winning/losing Team Possesion Feature
	wPos = df.apply(lambda row: 0.96*(row.WFGA + row.WTO + 0.44*row.WFTA - row.WOR), axis=1)
	lPos = df.apply(lambda row: 0.96*(row.LFGA + row.LTO + 0.44*row.LFTA - row.LOR), axis=1)
	#two teams use almost the same number of possessions in a game
	#(plus/minus one or two - depending on how quarters end)
	#so let's just take the average
	df['Pos'] = (wPos+lPos)/2

	#Offensive efficiency (OffRtg) = 100 x (Points / Possessions)
	df['WOffRtg'] = df.apply(lambda row: 100 * (row.WPts / row.Pos), axis=1)
	df['LOffRtg'] = df.apply(lambda row: 100 * (row.LPts / row.Pos), axis=1)
	#Defensive efficiency (DefRtg) = 100 x (Opponent points / Opponent possessions)
	df['WDefRtg'] = df.LOffRtg
	df['LDefRtg'] = df.WOffRtg
	#Net Rating = Off.Rtg - Def.Rtg
	df['WNetRtg'] = df.apply(lambda row:(row.WOffRtg - row.WDefRtg), axis=1)
	df['LNetRtg'] = df.apply(lambda row:(row.LOffRtg - row.LDefRtg), axis=1)
	                         
	#Assist Ratio : Percentage of team possessions that end in assists
	df['WAstR'] = df.apply(lambda row: 100 * row.WAst / (row.WFGA + 0.44*row.WFTA + row.WAst + row.WTO), axis=1)
	df['LAstR'] = df.apply(lambda row: 100 * row.LAst / (row.LFGA + 0.44*row.LFTA + row.LAst + row.LTO), axis=1)
	#Turnover Ratio: Number of turnovers of a team per 100 possessions used.
	#(TO * 100) / (FGA + (FTA * 0.44) + AST + TO)
	df['WTOR'] = df.apply(lambda row: 100 * row.WTO / (row.WFGA + 0.44*row.WFTA + row.WAst + row.WTO), axis=1)
	df['LTOR'] = df.apply(lambda row: 100 * row.LTO / (row.LFGA + 0.44*row.LFTA + row.LAst + row.LTO), axis=1)
	                    
	#The Shooting Percentage : Measure of Shooting Efficiency (FGA/FGA3, FTA)
	df['WTSP'] = df.apply(lambda row: 100 * row.WPts / (2 * (row.WFGA + 0.44 * row.WFTA)), axis=1)
	df['LTSP'] = df.apply(lambda row: 100 * row.LPts / (2 * (row.LFGA + 0.44 * row.LFTA)), axis=1)
	#eFG% : Effective Field Goal Percentage adjusting for the fact that 3pt shots are more valuable 
	df['WeFGP'] = df.apply(lambda row:(row.WFGM + 0.5 * row.WFGM3) / row.WFGA, axis=1)      
	df['LeFGP'] = df.apply(lambda row:(row.LFGM + 0.5 * row.LFGM3) / row.LFGA, axis=1)   
	#FTA Rate : How good a team is at drawing fouls.
	df['WFTAR'] = df.apply(lambda row: row.WFTA / row.WFGA, axis=1)
	df['LFTAR'] = df.apply(lambda row: row.LFTA / row.LFGA, axis=1)
	                         
	#OREB% : Percentage of team offensive rebounds
	df['WORP'] = df.apply(lambda row: row.WOR / (row.WOR + row.LDR), axis=1)
	df['LORP'] = df.apply(lambda row: row.LOR / (row.LOR + row.WDR), axis=1)
	#DREB% : Percentage of team defensive rebounds
	df['WDRP'] = df.apply(lambda row: row.WDR / (row.WDR + row.LOR), axis=1)
	df['LDRP'] = df.apply(lambda row: row.LDR / (row.LDR + row.WOR), axis=1)                                      
	#REB% : Percentage of team total rebounds
	df['WRP'] = df.apply(lambda row: (row.WDR + row.WOR) / (row.WDR + row.WOR + row.LDR + row.LOR), axis=1)
	df['LRP'] = df.apply(lambda row: (row.LDR + row.WOR) / (row.WDR + row.WOR + row.LDR + row.LOR), axis=1) 

	df['WPIE'] = df.apply(lambda row: (row.WDR + row.WOR) / (row.WDR + row.WOR + row.LDR + row.LOR), axis=1)
	wtmp = df.apply(lambda row: row.WPts + row.WFGM + row.WFTM - row.WFGA - row.WFTA + row.WDR + 0.5*row.WOR + row.WAst +row.WStl + 0.5*row.WBlk - row.WPF - row.WTO, axis=1)
	ltmp = df.apply(lambda row: row.LPts + row.LFGM + row.LFTM - row.LFGA - row.LFTA + row.LDR + 0.5*row.LOR + row.LAst +row.LStl + 0.5*row.LBlk - row.LPF - row.LTO, axis=1) 
	df['WPIE'] = wtmp/(wtmp + ltmp)
	df['LPIE'] = ltmp/(wtmp + ltmp)

	if csv_name:
		df.to_csv(csv_name, index=False)

	return df


def add_elo_rating(df_elos,df):
	df_elos.set_index(['season','team_id'], inplace=True)
	print(df_elos.head())
	df['Welo'] = df.apply(lambda row: df_elos.loc[(row.Season),(row.WTeamID)], axis=1)
	df['Lelo'] = df.apply(lambda row: df_elos.loc[(row.Season),(row.LTeamID)], axis=1)
	return df


def get_season_stats(df,season,team_id,stats):
	wstats = []
	lstats = []
	w = df.loc[(df['WTeamID'] == team_id) & (df['Season'] == season)]
	l = df.loc[(df['LTeamID'] == team_id) & (df['Season'] == season)]
	for stat in stats:
		wstats.append(w['W' + stat].sum())
		lstats.append(l['L' + stat].sum())
	season_stats = [season,team_id] + [(i+j) / (len(w) + len(l)) for i,j in zip(wstats,lstats)]
	return season_stats


def get_all_season_stats(df,stats):
	team_ids = pd.unique(df['WTeamID'].append(df['LTeamID']))
	seasons = pd.unique(df['Season'])
	lists = []
	for season in seasons:
		for team_id in team_ids:
			lists.append(get_season_stats(df,season,team_id,stats))
	seasons_stats = pd.DataFrame(lists,columns=(['Season','TeamID'] + stats))
	seasons_stats.drop(seasons_stats[seasons_stats.isnull().any(axis=1)].index, inplace=True)
	return seasons_stats


def create_outcome(df):
	df['Outcome'] = (df['WTeamID'] < df['LTeamID']).astype(float)
	return df


# Might be useless since tourney games are played in neutral stadium
def get_at_home(df):
	df['WHome'] = (df['WLoc'] == 'H').astype(int)
	df['LHome'] = (df['LLoc'] == 'H').astype(int)


def get_seeds(seed_data):
	def splice_seed(x):
		if len(x) == 4:
			x = x[1:-1]
		else:
			x = x[1:]
		if x[0] == '0':
			x = x[1]
		return x
	seed_data['Seed'] = seed_data['Seed'].apply(splice_seed).astype(float)

	return seed_data


def diff_stats(train, stat_data):
	stat_data.set_index(['Season','TeamID'],inplace=True)
	train = pd.concat([train,train.apply(lambda row: stat_data.loc[row.Season,row.WTeamID] - stat_data.loc[row.Season,row.LTeamID],axis=1)],axis=1)
	return train


def get_diff_stats(train, stat_data):
	stat_data.set_index(['Season','TeamID'],inplace=True)
	for row in train:
		train[row] = train[row].apply(lambda x: stat_data)

def normalize_elos(df):
	df['season_elo'] = ((df['season_elo'] - df['season_elo'].min()) / (df['season_elo'].max() - df['season_elo'].min()))
	return df



def main():
	

	# Import datasets
	teams = pd.read_csv(data_path + 'Teams.csv')
	seeds = pd.read_csv(data_path + 'NCAATourneySeeds.csv')
	reg_season = pd.read_csv(data_path + 'RegularSeasonCompactResults.csv')
	cities = pd.read_csv(data_path + 'Cities.csv')
	conferences = pd.read_csv(data_path + 'Conferences.csv')
	conf_tourney = pd.read_csv(data_path + 'ConferenceTourneyGames.csv')
	game_cities = pd.read_csv(data_path + 'GameCities.csv')
	tourney_results = pd.read_csv(data_path + 'NCAATourneyCompactResults.csv')
	detailed_tourney_results = pd.read_csv(data_path + 'NCAATourneyDetailedResults.csv')
	tourney_all = pd.read_csv(data_path + 'NCAATourneySeedRoundSlots.csv')
	tourney_slots = pd.read_csv(data_path + 'NCAATourneySlots.csv')
	detailed_reg_season = pd.read_csv(data_path + 'RegularSeasonDetailedResults.csv')
	seasons = pd.read_csv(data_path + 'Seasons.csv')
	second_tourney = pd.read_csv(data_path + 'SecondaryTourneyCompactResults.csv')
	detailed_second_tourney = pd.read_csv(data_path + 'SecondaryTourneyTeams.csv')
	team_coaches = pd.read_csv(data_path + 'TeamCoaches.csv')
	team_conferences = pd.read_csv(data_path + 'TeamConferences.csv')
	


	seed_data = get_seeds(seeds)
	print(seed_data.describe())
	

	# Get Tourney data Wteam, Lteam, Season, Winning
	tourney_results.drop(tourney_results.index[tourney_results['Season'] < 2003], inplace=True)
	tourney_results = create_outcome(tourney_results)
	tourney_results = tourney_results[['Season', 'WTeamID', 'LTeamID', 'Outcome']]

	# Get season elo rating and rename columns
	season_elos = pd.read_csv(data_path + 'season_elos.csv')
	season_elos = normalize_elos(season_elos)
	season_elos.rename(columns={'season':'Season','team_id':'TeamID'},inplace=True)
	print(season_elos.describe())
	#df = get_advanced_metrics(detailed_reg_season,csv_name=data_path + 'advanced_reg_season.csv')
	df = pd.read_csv(data_path + 'advanced_reg_season.csv')

	# 1 if winning team has lower id, 0 if losing team has lower id
	df = create_outcome(df)

	#df = add_elo_rating(season_elos,df)
	stats = ['FTAR','ORP','DRP','PIE','eFGP']
	stats_df = get_all_season_stats(df,stats)
	
	train_stats = stats_df.merge(season_elos,on=['Season','TeamID'],validate='one_to_one')
	#train_stats = train_stats.merge(seed_data,on=['Season','TeamID'],validate='one_to_one')
	

	print(diff_stats(tourney_results,train_stats))

	print(train_stats.head())


if __name__ == '__main__':
	main()
