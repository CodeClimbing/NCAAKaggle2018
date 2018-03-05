import numpy as np
import pandas as pd
import os


data_path = os.path.abspath('.') + '/DataFiles/'





def main():
	# Import datasets
	teams = pd.read_csv('Teams.csv')
	seeds = pd.read_csv('NCAATourneySeeds.csv')
	reg_season = pd.read_csv('RegularSeasonCompactResults.csv')
	cities = pd.read_csv('Cities.csv')
	conferences = pd.read_csv('Conferences.csv')
	conf_tourney = pd.read_csv('ConferenceTourneyGames.csv')
	game_cities = pd.read_csv('GameCities.csv')
	tourney_results = pd.read_csv('NCAATourneyCompactResults.csv')
	detailed_tourney_results = pd.read_csv('NCAATourneyDetailedResults.csv')
	tourney_all = pd.read_csv('NCAATourneySeedRoundSlots.csv')
	tourney_seeds = pd.read_csv('NCAATourneySeeds.csv')
	tourney_slots = pd.read_csv('NCAATourneySlots.csv')
	detailed_reg_season = pd.read_csv('RegularSeasonDetailedResults.csv')
	seasons = pd.read_csv('Seasons.csv')
	second_tourney = pd.read_csv('SecondaryTourneyCompactResults.csv')
	detailed_second_tourney = pd.read_csv('SecondaryTourneyTeams.csv')
	team_coaches = pd.read_csv('TeamCoaches.csv')
	team_conferences = pd.read_csv('TeamConferences.csv')
	

	print(teams.head())
