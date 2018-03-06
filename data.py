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

def get_elo_rating():
	pass




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
	tourney_seeds = pd.read_csv(data_path + 'NCAATourneySeeds.csv')
	tourney_slots = pd.read_csv(data_path + 'NCAATourneySlots.csv')
	detailed_reg_season = pd.read_csv(data_path + 'RegularSeasonDetailedResults.csv')
	seasons = pd.read_csv(data_path + 'Seasons.csv')
	second_tourney = pd.read_csv(data_path + 'SecondaryTourneyCompactResults.csv')
	detailed_second_tourney = pd.read_csv(data_path + 'SecondaryTourneyTeams.csv')
	team_coaches = pd.read_csv(data_path + 'TeamCoaches.csv')
	team_conferences = pd.read_csv(data_path + 'TeamConferences.csv')
	season_elos = pd.read_csv(data_path + 'season_elos.csv')

	#df = get_advanced_metrics(detailed_reg_season,csv_name=data_path + 'advanced_reg_season.csv')
	df = pd.read_csv(data_path + 'advanced_reg_season.csv')
	print(df.head())
	df['WPIE'].groupby(df['Season'], df['WTeamID']).describe()



if __name__ == '__main__':
	main()
