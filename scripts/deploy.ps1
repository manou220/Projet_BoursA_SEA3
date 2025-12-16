# Script de déploiement PowerShell pour Windows
# Usage: .\scripts\deploy.ps1 [production|development]

param(
    [string]$Env = "production"
)

$ErrorActionPreference = "Stop"

# Couleurs pour les messages
function Write-Info {
    param([string]$Message)
    Write-Host "[INFO] $Message" -ForegroundColor Green
}

function Write-Warn {
    param([string]$Message)
    Write-Host "[WARN] $Message" -ForegroundColor Yellow
}

function Write-Error {
    param([string]$Message)
    Write-Host "[ERROR] $Message" -ForegroundColor Red
}

Write-Info "Déploiement en mode: $Env"

# Vérifier Docker
if (-not (Get-Command docker -ErrorAction SilentlyContinue)) {
    Write-Error "Docker n'est pas installé. Veuillez l'installer d'abord."
    exit 1
}

# Vérifier Docker Compose
$dockerComposeCmd = "docker compose"
if (-not (docker compose version 2>$null)) {
    $dockerComposeCmd = "docker-compose"
    if (-not (Get-Command docker-compose -ErrorAction SilentlyContinue)) {
        Write-Error "Docker Compose n'est pas installé. Veuillez l'installer d'abord."
        exit 1
    }
}

# Vérifier que Docker Desktop est démarré
try {
    docker ps | Out-Null
} catch {
    Write-Error "Docker Desktop n'est pas démarré. Veuillez le démarrer d'abord."
    exit 1
}

# Vérifier le fichier .env
if (-not (Test-Path .env)) {
    Write-Warn "Le fichier .env n'existe pas. Création depuis ENV_EXAMPLE.txt..."
    if (Test-Path ENV_EXAMPLE.txt) {
        Copy-Item ENV_EXAMPLE.txt .env
        Write-Info "Fichier .env créé. Veuillez le configurer avant de continuer."
        
        # Générer SECRET_KEY
        $secretKey = python -c "import secrets; print(secrets.token_hex(32))" 2>$null
        if ($secretKey) {
            (Get-Content .env) -replace 'SECRET_KEY=.*', "SECRET_KEY=$secretKey" | Set-Content .env
            Write-Info "SECRET_KEY généré automatiquement"
        }
        
        Write-Warn "⚠️  Veuillez configurer POSTGRES_PASSWORD et REDIS_PASSWORD dans .env"
        Write-Warn "Appuyez sur Entrée pour continuer ou Ctrl+C pour annuler..."
        Read-Host
    } else {
        Write-Error "ENV_EXAMPLE.txt n'existe pas. Impossible de créer .env"
        exit 1
    }
}

# Charger les variables d'environnement
$envVars = Get-Content .env | Where-Object { $_ -match '^\s*[^#]' -and $_ -match '=' }
foreach ($line in $envVars) {
    if ($line -match '^([^=]+)=(.*)$') {
        $key = $matches[1].Trim()
        $value = $matches[2].Trim()
        [Environment]::SetEnvironmentVariable($key, $value, "Process")
    }
}

# Vérifier les variables obligatoires
if (-not $env:SECRET_KEY -or $env:SECRET_KEY -eq "votre-cle-secrete-generee-ici-changez-moi") {
    Write-Error "SECRET_KEY n'est pas défini ou utilise la valeur par défaut dans .env"
    exit 1
}

if (-not $env:POSTGRES_PASSWORD -or $env:POSTGRES_PASSWORD -eq "changez-moi-en-production") {
    Write-Warn "POSTGRES_PASSWORD n'est pas défini ou utilise la valeur par défaut"
    Write-Warn "Utilisation d'un mot de passe par défaut (non sécurisé pour la production)"
    $env:POSTGRES_PASSWORD = "boursa_password_$(Get-Random)"
}

if (-not $env:REDIS_PASSWORD) {
    Write-Warn "REDIS_PASSWORD n'est pas défini. Redis fonctionnera sans mot de passe"
}

# Créer les répertoires nécessaires
Write-Info "Création des répertoires nécessaires..."
@("uploads", "logs", "logs\nginx", "nginx\ssl", "app\models") | ForEach-Object {
    if (-not (Test-Path $_)) {
        New-Item -ItemType Directory -Path $_ -Force | Out-Null
    }
}

# Générer les certificats SSL auto-signés si nécessaire
if (-not (Test-Path "nginx\ssl\cert.pem") -or -not (Test-Path "nginx\ssl\key.pem")) {
    Write-Warn "Certificats SSL non trouvés. Génération de certificats auto-signés..."
    if (Get-Command openssl -ErrorAction SilentlyContinue) {
        New-Item -ItemType Directory -Path "nginx\ssl" -Force | Out-Null
        openssl req -x509 -nodes -days 365 -newkey rsa:2048 `
            -keyout "nginx\ssl\key.pem" `
            -out "nginx\ssl\cert.pem" `
            -subj "/C=FR/ST=State/L=City/O=BoursA/CN=localhost" 2>$null
        if ($LASTEXITCODE -eq 0) {
            Write-Info "Certificats SSL générés"
        } else {
            Write-Warn "Impossible de générer les certificats SSL. Continuez sans HTTPS ou configurez-les manuellement."
        }
    } else {
        Write-Warn "OpenSSL n'est pas installé. Les certificats SSL ne seront pas générés."
    }
}

# Arrêter les conteneurs existants
Write-Info "Arrêt des conteneurs existants..."
& $dockerComposeCmd.Split(' ') down 2>$null | Out-Null

# Construire les images
Write-Info "Construction des images Docker..."
& $dockerComposeCmd.Split(' ') build
if ($LASTEXITCODE -ne 0) {
    Write-Error "Échec de la construction des images"
    exit 1
}

# Démarrer les services
Write-Info "Démarrage des services..."
if ($Env -eq "production") {
    & $dockerComposeCmd.Split(' ') up -d
} else {
    & $dockerComposeCmd.Split(' ') up -d postgres redis flask_app
}
if ($LASTEXITCODE -ne 0) {
    Write-Error "Échec du démarrage des services"
    exit 1
}

# Attendre que les services soient prêts
Write-Info "Attente du démarrage des services..."
Start-Sleep -Seconds 10

# Vérifier la santé des services
Write-Info "Vérification de la santé des services..."

# Vérifier PostgreSQL
try {
    $pgUser = if ($env:POSTGRES_USER) { $env:POSTGRES_USER } else { "boursa_user" }
    docker exec boursa_postgres pg_isready -U $pgUser 2>$null | Out-Null
    if ($LASTEXITCODE -eq 0) {
        Write-Info "✅ PostgreSQL est prêt"
    } else {
        Write-Warn "⚠️  PostgreSQL n'est pas encore prêt"
    }
} catch {
    Write-Warn "⚠️  Impossible de vérifier PostgreSQL"
}

# Vérifier Redis
try {
    docker exec boursa_redis redis-cli ping 2>$null | Out-Null
    if ($LASTEXITCODE -eq 0) {
        Write-Info "✅ Redis est prêt"
    } else {
        Write-Warn "⚠️  Redis n'est pas accessible (peut être normal si un mot de passe est requis)"
    }
} catch {
    Write-Warn "⚠️  Impossible de vérifier Redis"
}

# Vérifier l'application Flask
Start-Sleep -Seconds 5
$appPort = if ($env:APP_PORT) { $env:APP_PORT } else { "5000" }
try {
    $response = Invoke-WebRequest -Uri "http://localhost:$appPort/health" -TimeoutSec 5 -ErrorAction Stop
    if ($response.StatusCode -eq 200) {
        Write-Info "✅ L'application Flask est prête"
    }
} catch {
    Write-Warn "⚠️  L'application Flask n'est pas encore prête. Vérifiez les logs: docker compose logs flask_app"
}

# Afficher les informations de connexion
Write-Info "Déploiement terminé!"
Write-Host ""
Write-Host "Services disponibles:"
Write-Host "  - Application Flask: http://localhost:$appPort"
if ($Env -eq "production") {
    $nginxHttp = if ($env:NGINX_HTTP_PORT) { $env:NGINX_HTTP_PORT } else { "80" }
    $nginxHttps = if ($env:NGINX_HTTPS_PORT) { $env:NGINX_HTTPS_PORT } else { "443" }
    Write-Host "  - Nginx HTTP: http://localhost:$nginxHttp"
    Write-Host "  - Nginx HTTPS: https://localhost:$nginxHttps"
}
$pgPort = if ($env:POSTGRES_PORT) { $env:POSTGRES_PORT } else { "5432" }
$redisPort = if ($env:REDIS_PORT) { $env:REDIS_PORT } else { "6379" }
Write-Host "  - PostgreSQL: localhost:$pgPort"
Write-Host "  - Redis: localhost:$redisPort"
Write-Host ""
Write-Host "Commandes utiles:"
Write-Host "  - Voir les logs: docker compose logs -f"
Write-Host "  - Arrêter: docker compose down"
Write-Host "  - Redémarrer: docker compose restart"
Write-Host "  - Statut: docker compose ps"

