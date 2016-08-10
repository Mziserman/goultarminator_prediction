# import json
# from sklearn import tree
# import numpy as np

# from sklearn.ensemble import RandomForestClassifier
# from sklearn.linear_model import LogisticRegression
# from sklearn import svm
# from sklearn.naive_bayes import GaussianNB
# from sklearn.neighbors import KNeighborsClassifier






# class Composition(object):
# 	def __init__(self):
# 		with open('history.json') as data_file:
# 			self.history = json.load(data_file)

# 		X = []
# 		y = []
# 		i = 0
# 		for game in self.history:
# 			winner_composition = self.composition_classe_to_number(game.get('winner').get('composition'))
# 			loser_composition = self.composition_classe_to_number(game.get('loser').get('composition'))

# 			if i == 1:
# 				i = 0
# 				X.append([winner_composition, loser_composition])
# 				y.append(1)
# 			else:
# 				i = 1
# 				X.append([loser_composition, winner_composition])
# 				y.append(0)




# 		X_fit = X[+100:]
# 		y_fit = y[+100:]

# 		X_test = X[:+100]
# 		y_test = y[:+100]
# 		X_fit = np.array(X_fit)
# 		y_fit = np.array(y_fit)
# 		nsamples, nx, ny = X_fit.shape
# 		X_fit = X_fit.reshape((nsamples,nx*ny))

# 		X_test = np.array(X_test)
# 		y_test = np.array(y_test)
# 		nsamples, nx, ny = X_test.shape
# 		X_test = X_test.reshape((nsamples,nx*ny))

# 		model = RandomForestClassifier()
# 		# Train the model using the training sets and check score
# 		model.fit(X_fit, y_fit)
# 		# #Equation coefficient and Intercept
# 		predict = model.predict(X_test)
# 		print(predict)
# 		print(y_test)
# 		win = 0
# 		lose = 0
# 		for i in predict - y_test:
# 			if i == 0:
# 				win = win + 1
# 			else:
# 				lose = lose + 1

# 		print("wins : ", win)
# 		print("loses : ", lose)
# 	def composition_classe_to_number(self, composition):
# 		number_composition = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
# 		for classe in composition:
# 			number_composition[self.classe_to_number(classe)] = 1

# 		return number_composition
	
# 	def composition_number_to_classe(self, composition):
# 		classe_composition = []
# 		for number in composition:
# 			classe_composition.append(self.number_to_classe(number))

# 		return classe_composition

# 	def classe_to_number(self, classe):
# 		return {
# 			'Osamodas': 0,
# 			'Sacrieur': 1,
# 			'Pandawa': 2,
# 			'Eniripsa': 3,
# 			'Eliotrope': 4,
# 			'Enutrof': 5,
# 			'Iop': 6,
# 			'Sadida': 7,
# 			'Sram': 8,
# 			'Feca': 9,
# 			'Ecaflip': 10,
# 			'Zobal': 11,
# 			'Cra': 12,
# 			'Steamer': 13,
# 			'Xelor': 14,
# 			'Roublard': 15
# 		}[classe]
	
# 	def number_to_classe(self, number):
# 		return {
# 			0: 'Osamodas',
# 			1: 'Sacrieur',
# 			2: 'Pandawa',
# 			3: 'Eniripsa',
# 			4: 'Eliotrope',
# 			5: 'Enutrof',
# 			6: 'Iop',
# 			7: 'Sadida',
# 			8: 'Sram',
# 			9: 'Feca',
# 			10: 'Ecaflip',
# 			11: 'Zobal',
# 			12: 'Cra',
# 			13: 'Steamer',
# 			14: 'Xelor',
# 			15: 'Roublard'
# 		}[number]

# composition = Composition()