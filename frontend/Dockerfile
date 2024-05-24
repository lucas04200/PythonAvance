# Utiliser une image Node.js de base
FROM node:18-alpine

WORKDIR /app/frontend

COPY . /app/frontend

RUN npm install

# Exposer le port
EXPOSE 5173

# Commande pour lancer l'application
CMD ["npm", "run", "dev"]