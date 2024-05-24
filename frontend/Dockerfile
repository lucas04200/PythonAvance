# Utiliser une image Node.js de base
FROM node:18-alpine

# Définir le répertoire de travail
WORKDIR /app/frontend

# Copier le reste des fichiers
COPY . /app/frontend

# Installer les dépendances
RUN npm install

# Exposer le port
EXPOSE 5173

# Commande pour lancer l'application
CMD ["npm", "run", "dev"]