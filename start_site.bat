@echo off
:: Sanal ortam oluştur (ilk sefer için)
if not exist venv (
    python -m venv venv
    echo Sanal ortam oluşturuldu.
)

:: Sanal ortamı aktif et
call venv\Scripts\activate.bat

:: Gerekli paketleri yükle
pip install --upgrade pip
pip install flask python-dotenv requests

:: Sunucuyu başlat
python app.py

pause
