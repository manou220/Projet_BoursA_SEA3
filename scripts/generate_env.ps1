# Script PowerShell pour générer le fichier .env
# Usage: .\scripts\generate_env.ps1

$ErrorActionPreference = "Stop"

Write-Host "Generating .env file..." -ForegroundColor Cyan

# Vérifier que nous sommes dans le bon répertoire
if (-not (Test-Path "ENV_EXAMPLE.txt")) {
    Write-Host "Error: ENV_EXAMPLE.txt not found. Run this script from Projet-ML-Sea3/Projet-ML-Sea3 directory" -ForegroundColor Red
    exit 1
}

# Vérifier si .env existe déjà
if (Test-Path ".env") {
    $response = Read-Host "File .env already exists. Replace it? (y/N)"
    if ($response -ne "y" -and $response -ne "Y") {
        Write-Host "Operation cancelled." -ForegroundColor Yellow
        exit 0
    }
}

# Générer les valeurs sécurisées
Write-Host "Generating secure values..." -ForegroundColor Cyan

$secretKey = python -c "import secrets; print(secrets.token_hex(32))"
$redisPassword = python -c "import secrets; print(secrets.token_urlsafe(24))"
$postgresPassword = python -c "import secrets; print(secrets.token_urlsafe(24))"

# Lire le template
$content = Get-Content "ENV_EXAMPLE.txt" -Raw

# Remplacer les valeurs
$content = $content -replace 'SECRET_KEY=votre-cle-secrete-generee-ici-changez-moi', "SECRET_KEY=$secretKey"
$content = $content -replace 'REDIS_PASSWORD=changez-moi-en-production', "REDIS_PASSWORD=$redisPassword"
$content = $content -replace 'POSTGRES_PASSWORD=changez-moi-en-production', "POSTGRES_PASSWORD=$postgresPassword"

# Écrire le fichier .env
$content | Set-Content ".env" -Encoding UTF8

Write-Host "`n.env file created successfully!" -ForegroundColor Green
Write-Host "`nGenerated values:" -ForegroundColor Cyan
Write-Host "  SECRET_KEY: $($secretKey.Substring(0, 20))..." -ForegroundColor Gray
Write-Host "  REDIS_PASSWORD: $($redisPassword.Substring(0, 20))..." -ForegroundColor Gray
Write-Host "  POSTGRES_PASSWORD: $($postgresPassword.Substring(0, 20))..." -ForegroundColor Gray
Write-Host "`nIMPORTANT: Keep these values secure!" -ForegroundColor Yellow
Write-Host "The .env file is already in .gitignore and will not be committed." -ForegroundColor Gray

