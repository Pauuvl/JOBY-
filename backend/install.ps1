# Script de Instalación Automática del Backend Joby
# PowerShell Script

Write-Host "🚀 Instalación del Backend Joby" -ForegroundColor Green
Write-Host "================================" -ForegroundColor Green
Write-Host ""

# Verificar Python
Write-Host "📦 Verificando Python..." -ForegroundColor Yellow
python --version
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Python no está instalado. Por favor instala Python 3.10+" -ForegroundColor Red
    exit 1
}

# Crear entorno virtual
Write-Host ""
Write-Host "🐍 Creando entorno virtual..." -ForegroundColor Yellow
python -m venv venv

# Activar entorno virtual
Write-Host ""
Write-Host "✅ Activando entorno virtual..." -ForegroundColor Yellow
.\venv\Scripts\Activate.ps1

# Instalar dependencias
Write-Host ""
Write-Host "📥 Instalando dependencias..." -ForegroundColor Yellow
pip install --upgrade pip
pip install -r requirements.txt

# Copiar .env
Write-Host ""
Write-Host "⚙️  Configurando variables de entorno..." -ForegroundColor Yellow
if (!(Test-Path ".env")) {
    Copy-Item ".env.example" ".env"
    Write-Host "✅ Archivo .env creado. Por favor edítalo con tus credenciales." -ForegroundColor Green
} else {
    Write-Host "⚠️  .env ya existe, no se sobrescribirá." -ForegroundColor Yellow
}

# Preguntar por PostgreSQL
Write-Host ""
Write-Host "🐘 ¿Ya tienes PostgreSQL instalado y configurado? (S/N)" -ForegroundColor Cyan
$pgResponse = Read-Host

if ($pgResponse -eq "N" -or $pgResponse -eq "n") {
    Write-Host ""
    Write-Host "Por favor instala PostgreSQL:" -ForegroundColor Yellow
    Write-Host "1. Descarga desde: https://www.postgresql.org/download/windows/"
    Write-Host "2. Instala PostgreSQL 14 o superior"
    Write-Host "3. Crea la base de datos con:"
    Write-Host "   psql -U postgres"
    Write-Host "   CREATE DATABASE joby_db;"
    Write-Host "   CREATE USER joby_user WITH PASSWORD 'tu_password';"
    Write-Host "   GRANT ALL PRIVILEGES ON DATABASE joby_db TO joby_user;"
    Write-Host ""
    Write-Host "Después de configurar PostgreSQL, ejecuta:"
    Write-Host "   python manage.py migrate" -ForegroundColor Green
    exit 0
}

# Ejecutar migraciones
Write-Host ""
Write-Host "🔄 Ejecutando migraciones..." -ForegroundColor Yellow
python manage.py makemigrations
python manage.py migrate

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Error en las migraciones. Verifica tu configuración de PostgreSQL en .env" -ForegroundColor Red
    exit 1
}

# Crear superusuario
Write-Host ""
Write-Host "👤 ¿Deseas crear un superusuario? (S/N)" -ForegroundColor Cyan
$suResponse = Read-Host

if ($suResponse -eq "S" -or $suResponse -eq "s") {
    python manage.py createsuperuser
}

# Recolectar archivos estáticos
Write-Host ""
Write-Host "📁 Recolectando archivos estáticos..." -ForegroundColor Yellow
python manage.py collectstatic --noinput

Write-Host ""
Write-Host "================================" -ForegroundColor Green
Write-Host "✅ ¡Instalación completada!" -ForegroundColor Green
Write-Host "================================" -ForegroundColor Green
Write-Host ""
Write-Host "Para iniciar el servidor:" -ForegroundColor Cyan
Write-Host "  python manage.py runserver" -ForegroundColor White
Write-Host ""
Write-Host "Para iniciar Celery (notificaciones):" -ForegroundColor Cyan
Write-Host "  celery -A joby_api worker -l info" -ForegroundColor White
Write-Host ""
Write-Host "Panel de administración:" -ForegroundColor Cyan
Write-Host "  http://127.0.0.1:8000/admin/" -ForegroundColor White
Write-Host ""
Write-Host "API Base URL:" -ForegroundColor Cyan
Write-Host "  http://127.0.0.1:8000/api/" -ForegroundColor White
Write-Host ""
