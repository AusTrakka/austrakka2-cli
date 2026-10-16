[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)][string]$InputCsv
)
$ErrorActionPreference = 'Stop'
if (-not (Test-Path -Path $InputCsv)) {
    throw "Input CSV file not found at '$InputCsv'."
}

function Remove-Diacritics {
    param ([string]$text)

    $normalized = $text.Normalize([System.Text.NormalizationForm]::FormD)
    $sb = [System.Text.StringBuilder]::new()
    foreach ($char in $normalized.ToCharArray()) {
        $category = [System.Globalization.CharUnicodeInfo]::GetUnicodeCategory($char)
        if ($category -ne [System.Globalization.UnicodeCategory]::NonSpacingMark) {
            [void]$sb.Append($char)
        }
    }
    return $sb.ToString()
}

function Test-IsNonLatinScript {
    param ([string]$text)
    $latinOrCommon = 0
    $other = 0
    foreach ($char in $text.ToCharArray()) {
        if ([char]::IsWhiteSpace($char) -or [char]::IsPunctuation($char)) { continue }
        $script = [System.Globalization.CharUnicodeInfo]::GetUnicodeCategory($char)
        if ($char -match '[a-zA-Z]') { $latinOrCommon++ }
        elseif ($char -gt [char]0x02AF) { $other++ } # past Latin Extended-B
    }
    return ($other -gt 0 -and $latinOrCommon -eq 0)
}

function Get-TrakkaUsername {
    param (
        [string]$fullName,
        [string]$fallbackSeed  # e.g. email local-part or userId, used if transliteration yields nothing
    )

    $trimmedName = $fullName.Trim()

    if (Test-IsNonLatinScript -text $trimmedName) {
        Write-Warning "Name '$fullName' is non-Latin script (e.g. Thai/CJK/Arabic) - accent-stripping cannot produce a meaningful ASCII username. Falling back to '$fallbackSeed'."
        $cleanName = $fallbackSeed
    }
    else {
        $cleanName = Remove-Diacritics -text $trimmedName
    }

    $cleanName = $cleanName.Trim()
    $parts = $cleanName -split '\s+' | Where-Object { $_ -ne '' }

    if ($parts.Count -eq 0) {
        $username = ($fallbackSeed -replace '[^a-zA-Z0-9]', '').ToLower()
    }
    elseif ($parts.Count -eq 1) {
        $username = ($parts[0] -replace '[^a-zA-Z0-9]', '').ToLower()
    }
    else {
        $familyName = $parts[0]
        $givenName  = $parts[-1]
        $username = "$($givenName[0])$familyName".ToLower() -replace '[^a-zA-Z0-9]', ''
    }

    if ([string]::IsNullOrWhiteSpace($username)) {
        # Last-resort fallback so we never emit an empty/garbage username
        $username = ($fallbackSeed -replace '[^a-zA-Z0-9]', '').ToLower()
    }

    return $username
}

# 1. Parse CSV and build execution list
$users = Import-Csv -Path $InputCsv
$commandsToRun = @()
$seenUsernames = @{}

foreach ($user in $users) {
    $userId = $user.'invitedUser.id'
    $email  = $user.email.Trim()
    $org    = $user.org.Trim()
    $name   = $user.name.Trim()

    if ([string]::IsNullOrWhiteSpace($userId)) {
        Write-Warning "Skipping '$email': Missing invitedUser.id"
        continue
    }

    $emailLocalPart = ($email -split '@')[0]
    $username = Get-TrakkaUsername -fullName $name -fallbackSeed $emailLocalPart

    # Guard against collisions (two different people folding to the same username,
    # which becomes much more likely once you're falling back for non-Latin names)
    if ($seenUsernames.ContainsKey($username)) {
        Write-Warning "Username '$username' for '$name' <$email> collides with an existing entry - appending userId suffix to disambiguate."
        $username = "$username$($userId.Substring(0, [Math]::Min(4, $userId.Length)))"
    }
    $seenUsernames[$username] = $true

    $cmdString = "trakka user add --user-id `"$userId`" --username `"$username`" --org `"$org`" --owner-group-roles `"Viewer`" --email `"$email`""
    $commandsToRun += [PSCustomObject]@{
        UserId   = $userId
        Username = $username
        Org      = $org
        Email    = $email
        Command  = $cmdString
    }
}

# 2. Display all plain string commands
Write-Host "`n=== COMMANDS TO BE EXECUTED ===" -ForegroundColor Cyan
foreach ($item in $commandsToRun) {
    Write-Host $item.Command -ForegroundColor Yellow
}
Write-Host "================================" -ForegroundColor Cyan
Write-Host "Total commands to execute: $($commandsToRun.Count)`n" -ForegroundColor Cyan

# 3. Prompt user for Y/N confirmation
$confirmation = Read-Host "Do you want to proceed with executing these commands? (y/n)"
if ($confirmation -notmatch '^[Yy]$') {
    Write-Host "Operation cancelled by user. No commands were executed." -ForegroundColor Red
    exit
}

Write-Host "`nExecuting commands..." -ForegroundColor Green
foreach ($item in $commandsToRun) {
    Write-Host "Running: $($item.Command)" -ForegroundColor Gray
    trakka user add `
        --user-id $item.UserId `
        --username $item.Username `
        --org $item.Org `
        --owner-group-roles "Viewer" `
        --email $item.Email
    if ($LASTEXITCODE -eq 0) {
        Write-Host " -> Success" -ForegroundColor Green
    } else {
        Write-Error " -> Failed (Exit code: $LASTEXITCODE)"
    }
}
