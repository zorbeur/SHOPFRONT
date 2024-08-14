import matplotlib.pyplot as plt

# Données
x = [1, 2, 3, 4, 5]
y = [2, 3, 5, 7, 11]

# Création du graphique
plt.plot(x, y, marker='o')

# Ajout des labels
plt.xlabel('X-axis')
plt.ylabel('Y-axis')
plt.title('Test Matplotlib')

# Affichage du graphique
plt.show()
