
# Jumper 3

#!/usr/bin/env python3
import tkinter, time, random, threading, platform
random.seed()



def rangeYield(start, iter, step):		# Une fonction qui permet de renvoyer un objet generator et la boucle for accèdent un à un les éléments de cet iterable, grâce à l'instruction yield.
	i = start							# C'est pour mettre à jour l'index maximal que l'on peut atteindre, car range() ne le fait pas,
										# puisque range() renvoie une liste et non pas un objet generator.
	while i < len(iter):
		yield i
		i += step




class displayBlueThread(threading.Thread):		# Le thread qui permet de mettre à jour l'affichage du carré bleu qui saute (blue) et des palettes.
	def __init__(self, obj):
		threading.Thread.__init__(self)
		self.obj = obj
	
	def run(self):
		self.obj.DBTstarted = True
		
		while (self.obj.running):
			if not self.obj.onGround:										# Mouvement de Blue :
				if self.obj.moveMode >= 5 and self.obj.moveMode <= 10:		# On utilise ici une variable qui décroit pour créer un semblant de physique, cranté donc.
					self.obj.posBlue[1] -= 15
					self.obj.posBlue[3] -= 15
					self.obj.canvas.move("Blue", 0, -15)
					self.obj.scoreUp += 15
					self.obj.moveMode -= 1
				elif self.obj.moveMode == 3 or self.obj.moveMode == 4:
					self.obj.posBlue[1] -= 5
					self.obj.posBlue[3] -= 5
					self.obj.canvas.move("Blue", 0, -5)
					self.obj.scoreUp += 5
					self.obj.moveMode -= 1
				elif self.obj.moveMode == 1 or self.obj.moveMode == 2:
					self.obj.posBlue[1] -= 2
					self.obj.posBlue[3] -= 2
					self.obj.canvas.move("Blue", 0, -2)
					self.obj.scoreUp += 2
					self.obj.moveMode -= 1
				elif self.obj.moveMode == 0: 
					self.obj.moveMode -= 1
				elif self.obj.moveMode == -1 or self.obj.moveMode == -2:
					self.obj.posBlue[1] += 2
					self.obj.posBlue[3] += 2
					self.obj.canvas.move("Blue", 0, 2)
					self.obj.scoreUp -= 2
					self.obj.moveMode -= 1
				elif self.obj.moveMode == -3 or self.obj.moveMode == -4:
					self.obj.posBlue[1] += 5
					self.obj.posBlue[3] += 5
					self.obj.canvas.move("Blue", 0, 5)
					self.obj.scoreUp -= 5
					self.obj.moveMode -= 1
				elif self.obj.moveMode <= -5:
					self.obj.posBlue[1] += 15
					self.obj.posBlue[3] += 15
					self.obj.canvas.move("Blue", 0, 15)
					self.obj.scoreUp -= 15
			
			
			
			if (self.obj.posBlue[3] < 2 * self.obj.h // 3):			# On réalise ici l'animation de descente des palettes
				if (self.obj.moveMode <= 0):						# si Blue passe au-dessus du tiers du bas de la fenêtre.
					self.obj.onGround = False						# On le fait en faisant une copie de la variable de mouvement
				else:												# de Blue, mais on applique le même mouvemement aux palettes.
					if not self.obj.onGround:
						self.obj.onGround = True
					
					if (self.obj.moveModeTemp == -1):
						self.obj.moveModeTemp = self.obj.moveMode
			
					if (self.obj.moveModeTemp >= 5 and self.obj.moveModeTemp <= 10):
						for i in rangeYield(0, self.obj.paletList, 2):
							self.obj.paletList[i] += 15
						
						self.obj.canvas.move("Palet", 0, 15)
						self.obj.scoreUp += 15
						self.obj.moveModeTemp -= 1
					
					elif (self.obj.moveModeTemp == 3 or self.obj.moveModeTemp == 4):
						for i in rangeYield(0, self.obj.paletList, 2):
							self.obj.paletList[i] += 5
						
						self.obj.canvas.move("Palet", 0, 5)
						self.obj.scoreUp += 5
						self.obj.moveModeTemp -= 1
					
					elif (self.obj.moveModeTemp == 1 or self.obj.moveModeTemp == 2):
						for i in rangeYield(0, self.obj.paletList, 2):
							self.obj.paletList[i] += 2
						
						self.obj.canvas.move("Palet", 0, 2)
						self.obj.scoreUp += 2
						self.obj.moveModeTemp -= 1
					
					elif (self.obj.moveModeTemp == 0):
						self.obj.onGround = False
						self.obj.moveModeTemp = -1
						self.obj.moveMode = 0
						
			
			
			
			if (self.obj.posBlue[1] > self.obj.h + 10):		# On gère ici la fin de partie quand Blue tombe.
				self.obj.scoreTime = round(time.time() - self.obj.scoreTimeStart, 1)
				self.obj.onGround = True
				self.obj.running = False
				time.sleep(1)
				
				self.obj.MET.start()
			
			time.sleep(0.05)





class updateBlueData(threading.Thread):				# Le thread qui modifie les positions de Blue et crée la détection de collision.
	def __init__(self, obj):
		threading.Thread.__init__(self)
		self.obj = obj
	
	def run(self):
		self.obj.UBTstarted = True
		
		while (self.obj.running):
			if (self.obj.key == "Right"):			# Ici dans les tests on vérifie si une touche n'a pas été activée.
				self.obj.posBlue[0] += 10			# On en déduit alors en fonction de la touche (gauche ou droite) le mouvemement de Blue adéquat.
				self.obj.posBlue[2] += 10
				self.obj.canvas.move("Blue", "10p", "0p")
				self.obj.key = ""
			elif (self.obj.key == "Left"):
				self.obj.posBlue[0] -= 10
				self.obj.posBlue[2] -= 10
				self.obj.canvas.move("Blue", "-10p", "0p")
				self.obj.key = ""
			elif (self.obj.key == "space"):
				self.obj.bind("<Left>", self.obj.keyBack)
				self.obj.bind("<Right>", self.obj.keyBack)
				self.obj.onGround = False
				self.obj.moveMode = 10
				self.obj.unbind("<space>")
				self.obj.key = ""
			
			for i in rangeYield(0, self.obj.paletList, 2):			# On crée ici la détection de collision entre le haut d'une pallette et le bas de Blue.
				if (self.obj.paletList[i] - 10 <= self.obj.posBlue[3] and self.obj.paletList[i] + 10 >= self.obj.posBlue[3] and self.obj.moveMode <= 0):
					if (self.obj.paletList[i+1] - 30 <= self.obj.posBlue[2] and self.obj.paletList[i+1] + 30 >= self.obj.posBlue[0]):
						self.obj.moveMode = 10
						break
			
			
			time.sleep(0.001)




class updatePaletData(threading.Thread):		# Le thread qui met à jour la liste des palettes et en ajoute sur l'affichage s'il le faut.
	def __init__(self, obj):
		threading.Thread.__init__(self)
		self.obj = obj
	
	def run(self):
		self.obj.UPTstarted = True
		
		while (self.obj.running):
			if (self.obj.paletList[len(self.obj.paletList)-2] >= 20):												# On teste ici s'il faut rajouter des palettes ou non -> génération de nouvelles palettes.
				self.obj.paletList.append(self.obj.paletList[len(self.obj.paletList)-2] - random.randint(60, 90))	# Pour la hauteur, fait relativement à la précedente palette.
				
				a = min(50, self.obj.w - self.obj.paletList[len(self.obj.paletList)-2] - 60)			# Pour la largeur, aussi relativement.
				b = min(50, self.obj.paletList[len(self.obj.paletList)-2] - 60)
				c = self.obj.paletList[len(self.obj.paletList)-2] - random.randint(b, 200)
				d = self.obj.paletList[len(self.obj.paletList)-2] + random.randint(a, 200)
				
				if (random.randint(0, 1) == 0):						# On choisi entre gauche ou droite.
					while (c > self.obj.w - 60 or c < 60):			# On génère ici plein de nombres aléatoires jusqu'à que la prochaine palettes soit dans la fenêtre.
						c = self.obj.paletList[len(self.obj.paletList)-2] - random.randint(b, 200)
						
					self.obj.paletList.append(c)
				else:
					while (d > self.obj.w - 60 or d < 60):
						d = self.obj.paletList[len(self.obj.paletList)-2] + random.randint(a, 200)
						
					self.obj.paletList.append(d)
				
			
			self.obj.canvas.create_rectangle(self.obj.paletList[len(self.obj.paletList)-1] - 50, self.obj.paletList[len(self.obj.paletList)-2] - 7, self.obj.paletList[len(self.obj.paletList)-1] + 50, self.obj.paletList[len(self.obj.paletList)-2] + 7, fill = "red", outline = "black", tag = "Palet")
			
			
			if (self.obj.paletList[0] > self.obj.h):		# On enlève ici les palettes qui sont passées en-dessous du bas de la fenêtre.
				self.obj.paletList.pop(0)					# En fait, utiliser des .pop(i) à un index i sera toujours plus rapide que d'utiliser une liste temporaire dans laquelle
				self.obj.paletList.pop(1)					# on stocke la fin de la liste qu'on a popé un à un, puis on la remet de nouveau un à un (j'ai fait des tests, c'est donc sûr).
			
			
			time.sleep(0.05)




class menuStart(threading.Thread):				# Le thread de menu de départ.
	def __init__(self, obj):
		threading.Thread.__init__(self)
		self.obj = obj
	
	def run(self):
		self.obj.MSTstarted = True
		self.obj.canvas.create_text(self.obj.w // 2, self.obj.h // 2, activefill = "green", fill = "orange", font = (self.obj.textFont, 80, "bold", "roman"), justify = tkinter.CENTER, text = "Press Space to start !", tag = "start", width = self.obj.w)
		
		while (self.obj.key != "space" and self.obj.running):
			time.sleep(0.1)
		
		self.obj.canvas.delete("start")
		self.obj.canvas.create_oval(self.obj.posBlue[0], self.obj.posBlue[1], self.obj.posBlue[2], self.obj.posBlue[3], fill = "blue", outline = "black", width = 1, tag = "Blue")
		self.obj.canvas.create_rectangle(self.obj.paletList[len(self.obj.paletList)-1] - 50, self.obj.paletList[len(self.obj.paletList)-2] - 7, self.obj.paletList[len(self.obj.paletList)-1] + 50, self.obj.paletList[len(self.obj.paletList)-2] + 7, fill = "red", outline = "black", tag = "Palet")
		
		self.obj.UPT.start()
		
		# Compte à rebours jusqu'au départ, le premier saut :
		self.obj.canvas.create_text(self.obj.w // 2, self.obj.h // 2, fill = "pink", font = (self.obj.textFont, 100, "bold", "roman"), justify = tkinter.CENTER, text = "3", tag = "go")
		time.sleep(1)
		self.obj.canvas.delete("go")
		self.obj.canvas.create_text(self.obj.w // 2, self.obj.h // 2, fill = "red", font = (self.obj.textFont, 100, "bold", "roman"), justify = tkinter.CENTER, text = "2", tag = "go")
		time.sleep(1)
		self.obj.canvas.delete("go")
		self.obj.canvas.create_text(self.obj.w // 2, self.obj.h // 2, fill = "magenta", font = (self.obj.textFont, 100, "bold", "roman"), justify = tkinter.CENTER, text = "1", tag = "go")
		time.sleep(1)
		self.obj.canvas.delete("go")
		
		self.obj.scoreTimeStart = time.time()
		
		self.obj.DBT.start()
		self.obj.UBT.start()




class menuEnd(threading.Thread):				# Le thread de fin de jeu.
	def __init__(self, obj):
		threading.Thread.__init__(self)
		self.obj = obj
	
	def run(self):
		self.obj.METstarted = True
		self.obj.key = ""
		self.obj.canvas.delete("all")
		
		if self.obj.scoreUp < 0:
			self.obj.scoreUp = 0
		
		self.obj.bind("<y>", self.obj.keyBack)
		self.obj.bind("<n>", self.obj.keyBack)

		# Game over :
		self.obj.canvas.create_text(self.obj.w // 2, self.obj.h // 2, fill = "red", font = (self.obj.textFont, 80, "bold", "roman"), justify = tkinter.CENTER, text = "Game Over !", tag = "end", width = self.obj.w)
		time.sleep(2)
		self.obj.canvas.delete("end")
		
		# Score board :
		self.obj.canvas.create_text(self.obj.w // 2, 50, fill = "blue", font = (self.obj.textFont, 60, "bold", "roman"), justify = tkinter.CENTER, text = "Score Board", width = self.obj.w)
		self.obj.canvas.create_text(120, self.obj.h // 4, fill = "dark grey", font = (self.obj.textFont, 40, "roman"), justify = tkinter.LEFT, text = "Score Up :", width = self.obj.w)
		self.obj.canvas.create_text(self.obj.w - 80, self.obj.h // 4, fill = "dark grey", font = (self.obj.textFont, 40, "roman"), justify = tkinter.RIGHT, text = str(self.obj.scoreUp), width = self.obj.w)
		self.obj.canvas.create_text(140, self.obj.h // 2, fill = "dark grey", font = (self.obj.textFont, 40, "roman"), justify = tkinter.LEFT, text = "Time Score :", width = self.obj.w)
		self.obj.canvas.create_text(self.obj.w - 80, self.obj.h // 2, fill = "dark grey", font = (self.obj.textFont, 40, "roman"), justify = tkinter.RIGHT, text = str(self.obj.scoreTime), width = self.obj.w)
		self.obj.canvas.create_text(170, 3 * self.obj.h // 4, fill = "dark grey", font = (self.obj.textFont, 40, "roman"), justify = tkinter.LEFT, text = "Up/Time Ratio :", width = self.obj.w)
		self.obj.canvas.create_text(self.obj.w - 80, 3 * self.obj.h // 4, fill = "dark grey", font = (self.obj.textFont, 40,  "roman"), justify = tkinter.RIGHT, text = str(round(self.obj.scoreUp / self.obj.scoreTime, 1)), width = self.obj.w)
		self.obj.canvas.create_text(self.obj.w // 2, self.obj.h - 50, fill = "red", font = (self.obj.textFont, 40,  "roman"), justify = tkinter.RIGHT, text = "Press Esc to quit", width = self.obj.w)
		self.obj.canvas.create_line(0, 3 * self.obj.h // 8, self.obj.w, 3 * self.obj.h // 8, fill = "light grey", width = 0)
		self.obj.canvas.create_line(0, 5 * self.obj.h // 8, self.obj.w, 5 * self.obj.h // 8, fill = "light grey", width = 0)
		self.obj.canvas.create_line(0, 80, self.obj.w, 80, fill = "light blue", width = 2)
		
		self.obj.bind("<Escape>", self.obj.keyBack)
		self.obj.running = True
		
		while (self.obj.key != "Escape" and self.obj.running):
			time.sleep(0.1)
		
		self.obj.canvas.delete("all")
		self.obj.quitter()




class JumperGame(tkinter.Tk):								# La classe principale, d'initialisation du jeu, des attributs, de la fenêtre et des threads.
	def __init__(self, width = 500, height = 600):
		tkinter.Tk.__init__(self, None)
		self.configure(background = "white")
		self.title("Jumper")
		
		self.w = width					# On enregistre ici la largeur et la hauteur de la fenêtre
		self.h = height					# pour réaliser les choses de manière relative à ceci.
		self.onGround = True			# Une variable qui permet en fait d'arrêter le mouvement du Blue.
		self.moveMode = 0				# La variable de mouvemement de Blue.
		self.moveModeTemp = -1			# La même mais utilisée pour les pallettes quand elles descendent.
		self.posBlue = [self.w // 2 - 20, self.h - 67, self.w // 2 + 20, self.h - 27] # Blue's old : x1, y1, x2, y2.
		self.key = ""										# La touche dernièrement activée.
		self.paletList = [self.h - 20, self.w // 2]			# La liste de positions du centre des palettes.
		
		self.scoreTimeStart = 0							# Deux variables pour créer un score en temps.
		self.scoreTime = 0
		self.scoreUp = 0								# Un score de montée en pixels.
		self.UBTstarted = False
		self.DBTstarted = False
		self.UPTstarted = False							# Pour savoir si les threads ont été démarré une fois.
		self.METstarted = False
		self.MSTstarted = False

		if platform.system() == "Darwin":
			self.textFont = "Baoli SC"                  # La famille de polices qui va être utilisée pour tous les textes affichés.
		elif platform.system() == "Windows":
			self.textFont = "MV Boli"
		
		
		self.canvas = tkinter.Canvas(self, width = self.w, height = self.h, bg = "white")	# Le canvas que l'on va utiliser.
		self.quitte = tkinter.Button(self, text = "Quitter", command = self.quitter)		# On ajoute un bouton qui utilise la méthode 'quitter' pour pouvoir
		self.canvas.pack()																	# arrêter les threads, car le bouton windows rouge en croix de la fenêtre 
		self.quitte.pack()																	# ne le fait pas et elle ne s'arrête alors pas, ce qui est embêtant...
		
		self.bind("<space>", self.keyBack)					# On associe ici la barre d'espace qui permet de démarrer le saut et aussi d'associer les touches clavier gauche et droite (voir dans le thread updateBlueData)
		
		
		self.running = True									# La variable sentinelle qui permet d'arrêter les threads au moment voulu.
		self.resizable(width = False, height = False)		# On empêche la fenêtre de pouvoir être redimensionnée (plein écran compris)
		self.focus_set()									# On met la fenêtre au premier plan et on la sélectionne pour capter immédiatment les entrées claviers.
		
		
		self.MST = menuStart(self)
		self.MET = menuEnd(self)
		self.DBT = displayBlueThread(self)					# On déclare les quatre threads du jeu,
		self.UBT = updateBlueData(self)
		self.UPT = updatePaletData(self)
		self.MST.start()
		
		self.mainloop()										# On démarre ici la fenêtre tkinter.
		
	
	def keyBack(self, event):								# La méthode de callback qui reçoit les évenements clavier
		self.key = event.keysym								# et met à jour la variable suivant la touche activée.
	
	def quitter(self):										# La méthode qui permet d'arrêter les threads et la fenêtre. 
		self.running = False
		self.onGround = True
		self.moveMode = 0
		self.quit()



j = JumperGame(width = 600, height = 800)		# L'objet de partie qui lance tout.



# Notes :

""" Ce que l'on peut faire : parcourir un tuple des ids de tous les objets du canvas, on le récupère avec la méthode 'leCanvas'.find_all() ou 'leCanvas'.find_withtag(tag)"""