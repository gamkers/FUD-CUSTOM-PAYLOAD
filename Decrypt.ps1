# Define the folder path containing the encrypted files
$folderPath = "F:\Testing"

# Prompt user to enter password
$password = Read-Host -Prompt "Enter your password" -AsSecureString

# Convert secure string password to plain text
$plaintextPassword = [System.Runtime.InteropServices.Marshal]::PtrToStringAuto([System.Runtime.InteropServices.Marshal]::SecureStringToBSTR($password))

# Define decryption method
$decryptionMethod = @{
    KeySize = 256
    BlockSize = 128
    Mode = 'CBC'
    Padding = 'PKCS7'
}

# Function to decrypt a file
function Decrypt-File {
    param (
        [string]$FilePath,
        [hashtable]$DecryptionMethod
    )

    # Generate AES decryption object
    $aes = New-Object System.Security.Cryptography.AesManaged
    $aes.KeySize = $DecryptionMethod['KeySize']
    $aes.BlockSize = $DecryptionMethod['BlockSize']
    $aes.Mode = $DecryptionMethod['Mode']
    $aes.Padding = $DecryptionMethod['Padding']

    # Set key and IV
    $aes.Key = [System.Text.Encoding]::UTF8.GetBytes($plaintextPassword.PadRight(32))  # Pad password to match key size (for AES-256)
    $aes.IV = [System.Text.Encoding]::UTF8.GetBytes("1234567890123456")  # Use the same IV used during encryption

    # Create file streams
    $fileStreamIn = [System.IO.File]::OpenRead($FilePath)
    $fileStreamOut = [System.IO.File]::Create(($FilePath -replace '\.enc$', ''))  # Remove .enc extension for decrypted file

    # Create crypto streams
    $cryptoStream = New-Object System.Security.Cryptography.CryptoStream($fileStreamOut, $aes.CreateDecryptor(), 'Write')

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

    # Remove the .enc file
    Remove-Item -Path $FilePath -Force
}

# Decrypt files in the folder
Get-ChildItem -Path $folderPath -Filter *.enc | ForEach-Object {
    Decrypt-File -FilePath $_.FullName -DecryptionMethod $decryptionMethod
}
