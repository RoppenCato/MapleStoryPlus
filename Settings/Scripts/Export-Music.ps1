# Copies the best-loved music out of the game client's Sound.wz into Settings\Music, named by place.
#
#     powershell -ExecutionPolicy Bypass -File Settings\Scripts\Export-Music.ps1
#
# The list is below: the track's place in Sound.wz, then the file name. Which track plays where was
# looked up in the maps (the "bgm" of each map in Server\wz\Map.wz). The files are for listening
# locally: Settings\Music is in .gitignore, since the repository is public and the music is not ours.
$root = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
$tracks = @(
    @('BgmUI.img/Title', '01 Login Screen'),
    @('Bgm00.img/GoPicnic', '02 Maple Island - Southperry and Maple Road'),
    @('Bgm00.img/RestNPeace', '03 Snail Hunting Ground and Dangerous Forest'),
    @('Bgm00.img/FloralLife', '04 Henesys'),
    @('Bgm01.img/CavaBien', '05 Henesys Fields'),
    @('Bgm02.img/WhenTheMorningComes', '06 Ellinia'),
    @('Bgm01.img/MoonlightShadow', '07 Ellinia Forest'),
    @('Bgm00.img/Nightmare', '08 Perion'),
    @('Bgm01.img/BadGuys', '09 Kerning City'),
    @('Bgm03.img/Subway', '10 Kerning City Subway'),
    @('Bgm02.img/AboveTheTreetops', '11 Lith Harbor'),
    @('Bgm00.img/SleepyWood', '12 Sleepywood'),
    @('Bgm01.img/AncientMove', '13 Ant Tunnel'),
    @('Bgm15.img/Nautilus', '14 Nautilus Harbor'),
    @('Bgm03.img/Beachway', '15 Florina Beach'),
    @('Bgm04.img/UponTheSky', '16 Ship to Orbis'),
    @("Bgm04.img/Shinin'Harbor", '17 Orbis'),
    @('Bgm03.img/SnowyVillage', '18 El Nath'),
    @('Bgm04.img/WarmRegard', '19 El Nath Mountains'),
    @('Bgm06.img/FantasticThinking', '20 Ludibrium'),
    @('Bgm07.img/FunnyTimeMaker', '21 Eos Tower'),
    @('Bgm07.img/WhereverYouAre', '22 Path of Time'),
    @('Bgm08.img/LetsMarch', '23 Omega Sector'),
    @('Bgm11.img/DownTown', '24 Korean Folk Town'),
    @('Bgm11.img/Aquarium', '25 Aquarium'),
    @('Bgm11.img/BlueWorld', '26 Aqua Road'),
    @('Bgm13.img/Leafre', '27 Leafre'),
    @("Bgm13.img/Minar'sDream", '28 Minar Forest'),
    @('Bgm15.img/MureungHill', '29 Mu Lung'),
    @('Bgm15.img/WhiteHerb', '30 Herb Town'),
    @('Bgm14.img/Ariant', '31 Ariant'),
    @('Bgm12.img/Dispute', '32 Magatia'),
    @('Bgm16.img/TimeTemple', '33 Temple of Time'),
    @('Bgm18.img/QueensGarden', '34 Ereve'),
    @('Bgm19.img/RienVillage', '35 Rien'),
    @('BgmGL.img/NLCtown', '36 New Leaf City'),
    @('BgmGL.img/amoria', '37 Amoria'),
    @('BgmJp.img/Feeling', '38 Mushroom Shrine'),
    @('Bgm06.img/WelcomeToTheHell', '39 Zakum'),
    @('Bgm16.img/FightingPinkBeen', '40 Pink Bean'),
    @('BgmUI.img/ShopBgm', '41 Cash Shop')
)

Add-Type -Path (Join-Path $root 'Tools\HaRepacker-4.1.0\AnyCPU\MapleLib.dll')
$out = Join-Path $root 'Settings\Music'
New-Item -ItemType Directory -Force $out | Out-Null
$wz = New-Object MapleLib.WzLib.WzFile((Join-Path $root 'Client\MapleStory\Sound.wz'), [int16]83, [MapleLib.WzLib.WzMapleVersion]::GMS)
$message = $null
if (-not $wz.ParseWzFile([ref]$message, $null)) { throw "Could not read Sound.wz : $message" }
try {
    foreach ($t in $tracks) {
        $imgName, $trackName = $t[0].Split('/')
        $img = $wz.WzDirectory.GetImageByName($imgName)
        if ($img -eq $null) { Write-Warning "$($t[0]) not found"; continue }
        $img.ParseImage() | Out-Null
        $sound = $img.WzProperties | Where-Object { $_.Name -eq $trackName } | Select-Object -First 1
        if ($sound -eq $null) { Write-Warning "$($t[0]) not found"; continue }
        $file = Join-Path $out ($t[1] + '.mp3')
        $sound.SaveToFile($file)
        "{0,-48} {1,4} s  from {2}" -f ($t[1] + '.mp3'), [int]($sound.Length / 1000), $t[0]
    }
} finally {
    $wz.Dispose()
}
