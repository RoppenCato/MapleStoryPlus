# Copies the game's sound effects out of the client's Sound.wz into Settings\Sounds, named so they can be found.
#
#     powershell -ExecutionPolicy Bypass -File Settings\Scripts\Export-Sounds.ps1
#
# Settings\Sounds\Weapons   every weapon swing and shot (17)
# Settings\Sounds\Game      level up, job change, portal, pick up, quest done, scroll pass and fail ... (27)
# Settings\Sounds\Interface buttons, windows, the character select and shop sounds (31)
# Settings\Sounds\Monsters  each monster's hit and death sound, once per distinct sound
#
# Most are MP3; the few stored as WAV keep that. For local listening only: Settings\Sounds is in
# .gitignore, since the repository is public and the sounds are not ours.
$root = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)

# Weapon.img: the kind of weapon, and what its two sounds are
$weapons = @{
    # Which weapon uses which sound is its "sfx" in Character.wz: each sword, axe and dagger has one of the two swings
    'swordL'    = 'Sword, axe or dagger, heavy swing';
    'swordS'    = 'Sword, axe or dagger, light swing';
    'mace'      = 'Blunt weapon, wand or staff';
    'poleArm'   = 'Polearm';
    'spear'     = 'Spear';
    'bow'       = 'Bow';
    'cBow'      = 'Crossbow';
    'tGlove'    = 'Claw';
    'knuckle'   = 'Knuckle';
    'barehands' = 'Bare hands';
    'gun'       = 'Gun'
}

Add-Type -Path (Join-Path $root 'Tools\HaRepacker-4.1.0\AnyCPU\MapleLib.dll')
$wz = New-Object MapleLib.WzLib.WzFile((Join-Path $root 'Client\MapleStory\Sound.wz'), [int16]83, [MapleLib.WzLib.WzMapleVersion]::GMS)
$message = $null
if (-not $wz.ParseWzFile([ref]$message, $null)) { throw "Could not read Sound.wz : $message" }

# "PickUpItem" -> "Pick Up Item"
function Words($name) {
    return (($name -creplace '_', ' ') -creplace '(?<=[a-z])(?=[A-Z])', ' ').Trim()
}

function Save($sound, $folder, $name) {
    $dir = Join-Path $root "Settings\Sounds\$folder"
    New-Item -ItemType Directory -Force $dir | Out-Null
    $bytes = $sound.GetBytes($false)
    $ext = if ($bytes.Length -ge 4 -and [System.Text.Encoding]::ASCII.GetString($bytes, 0, 4) -eq 'RIFF') { '.wav' } else { '.mp3' }
    $file = Join-Path $dir ($name + $ext)
    $sound.SaveToFile($file)
    $script:saved++
}

$saved = 0
try {
    $img = $wz.WzDirectory.GetImageByName('Weapon.img'); $img.ParseImage() | Out-Null
    foreach ($kind in $img.WzProperties) {
        $label = $weapons[$kind.Name]; if (-not $label) { $label = $kind.Name }
        foreach ($s in $kind.WzProperties) {
            $which = if ($s.Name -eq 'Attack') { 'attack' } else { 'attack ' + $s.Name.Substring(6) }
            Save $s 'Weapons' "$label - $which"
        }
    }
    foreach ($pair in @(@('Game.img', 'Game'), @('UI.img', 'Interface'))) {
        $img = $wz.WzDirectory.GetImageByName($pair[0]); $img.ParseImage() | Out-Null
        foreach ($s in $img.WzProperties) {
            if ($s -is [MapleLib.WzLib.WzProperties.WzBinaryProperty]) { Save $s $pair[1] (Words $s.Name) }
        }
    }

    # Mob.img: each monster's own sound when it is hit ("Damage") and when it dies ("Die"). That hit sound
    # is the impact you hear, whatever the weapon. Many monsters have a silent placeholder (1 ms) or share
    # the very same sound; each sound is written once, under the first monster that has it.
    $mobNames = @{}
    Import-Csv (Join-Path $root 'Settings\Reference\Mobs.tsv') -Delimiter "`t" | ForEach-Object { $mobNames[[int]$_.id] = $_.name.Trim() }
    $sha = [System.Security.Cryptography.SHA1]::Create()
    $seen = @{}
    $img = $wz.WzDirectory.GetImageByName('Mob.img'); $img.ParseImage() | Out-Null
    foreach ($mob in $img.WzProperties) {
        $id = 0
        if (-not [int]::TryParse($mob.Name, [ref]$id)) { continue }
        $name = $mobNames[$id]
        if (-not $name) { continue }
        $name = $name -replace '[\\/:*?"<>|]', ''
        foreach ($pair in @(@('Damage', 'hit'), @('Die', 'dies'))) {
            $s = $mob.WzProperties | Where-Object { $_.Name -eq $pair[0] -and $_ -is [MapleLib.WzLib.WzProperties.WzBinaryProperty] } | Select-Object -First 1
            if (-not $s -or $s.Length -lt 50) { continue }
            $hash = [BitConverter]::ToString($sha.ComputeHash($s.GetBytes($false)))
            if ($seen.ContainsKey($hash)) { continue }
            $seen[$hash] = 1
            $file = "$name - $($pair[1])"
            if (Test-Path (Join-Path $root "Settings\Sounds\Monsters\$file.mp3")) { $file = "$file ($id)" }
            Save $s 'Monsters' $file
        }
    }
} finally {
    $wz.Dispose()
}
"$saved sounds written to Settings\Sounds"
