param(
  [string]$DatabaseUrl,
  [string]$SecretKey = "dev-secret",
  [int]$Port = 8000
)

$cwd = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location (Join-Path $cwd "..")

function Fail($msg) { Write-Host $msg; exit 1 }

$py = (Get-Command python -ErrorAction SilentlyContinue)
if (-not $py) { $py = (Get-Command py -ErrorAction SilentlyContinue) }
if (-not $py) { Fail "Python not found. Please install Python and add to PATH." }

& $py.Source -m pip install -r requirements.txt
if ($LASTEXITCODE -ne 0) { Fail "Dependency installation failed." }

if (-not $DatabaseUrl) { $DatabaseUrl = $env:DATABASE_URL }
if (-not $DatabaseUrl) { Fail "Provide -DatabaseUrl or set DATABASE_URL env." }

$env:DATABASE_URL = $DatabaseUrl
$env:SECRET_KEY = $SecretKey

$code = @'
import os, sys
import psycopg2
url = os.environ.get('DATABASE_URL')
try:
    conn = psycopg2.connect(url)
    conn.close()
    print('DB OK')
    sys.exit(0)
except Exception as e:
    print('DB ERROR:', e)
    sys.exit(1)
'@

$tmp = Join-Path $env:TEMP "db_test.py"
Set-Content -Path $tmp -Value $code -Encoding UTF8
& $py.Source $tmp
if ($LASTEXITCODE -ne 0) { Remove-Item $tmp -Force; Fail "Database connection failed. Check DATABASE_URL." }
Remove-Item $tmp -Force

& $py.Source -m flask --app backend.app:create_app run --host=0.0.0.0 --port $Port
