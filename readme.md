### 1. Nastavit systémovou proměnnou DATABASE_URL, ve které bude připojovací string do databáze.
### 2. V souboru /frontend/src/api/api.ts nastavit axiosBaseUrl na příslušnou adresu hostovaného backendu.
### 3. Pro backend je připravený Dockerfile (/backend/Dockerfile), který lze použít pro vytvoření image a nasazení na server.
### 4. Pro frontend je připravený Dockerfile (/frontend/Dockerfile), který lze použít pro vytvoření image a nasazení na server.
### 5. Inicializace tabulek a vytvoření schématu databáze proběhne automaticky při prvním spuštění backendu. Vytvoří se také administrátorský účet a uživatelské role.