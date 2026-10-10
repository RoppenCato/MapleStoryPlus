# Makes the client's skill data (Client\MapleStory\Skill.wz) match the server's for every field listed in
# Skill-Changes.tsv. Run Apply-Skill-Changes.py first; the game must be closed.
#
#   powershell -ExecutionPolicy Bypass -File Settings\Scripts\Patch-Client-Skills.ps1
#   powershell -ExecutionPolicy Bypass -File Settings\Scripts\Patch-Client-Skills.ps1 -CheckOnly
#
# The untouched original is kept once as Skill.wz.original. The patched file is written to a temporary
# file, read back and checked, and only then put in place.
param([switch]$CheckOnly)

$ErrorActionPreference = 'Stop'
$root = Split-Path (Split-Path $PSScriptRoot -Parent) -Parent
$client = Join-Path $root 'Client\MapleStory'
$target = Join-Path $client 'Skill.wz'
$original = Join-Path $client 'Skill.wz.original'
$work = Join-Path $env:TEMP 'MapleStoryPlus-ClientPatch'
$python = 'python'

Add-Type -Path (Join-Path $root 'Tools\HaRepacker-4.1.0\AnyCPU\MapleLib.dll')

function Open-Wz($path) {
    $wz = New-Object MapleLib.WzLib.WzFile($path, [int16]83, [MapleLib.WzLib.WzMapleVersion]::GMS)
    $message = ''
    if (-not $wz.ParseWzFile([ref]$message, $null)) { throw "Could not read $path : $message" }
    return $wz
}

if (-not $CheckOnly -and (Get-Process MapleStory -ErrorAction SilentlyContinue)) {
    throw 'MapleStory is running. Close the game first.'
}

New-Item -ItemType Directory -Force $work | Out-Null
$values = Join-Path $work 'values.tsv'
& $python (Join-Path $PSScriptRoot 'Apply-Skill-Changes.py') --export $values | Out-Null
$rows = Import-Csv $values -Delimiter "`t"

# Always patch from the untouched original, so the result never depends on earlier patches.
if (-not (Test-Path $original)) { Copy-Item $target $original }
$source = Join-Path $work 'Skill.source.wz'
$patched = Join-Path $work 'Skill.patched.wz'
Copy-Item $original $source -Force
Remove-Item $patched -ErrorAction SilentlyContinue

$wz = Open-Wz $source
$images = @{}
$changed = 0; $added = 0; $same = 0; $missing = @{}
foreach ($row in $rows) {
    $id = [int]$row.skill_id
    $name = ('{0:000}.img' -f [int][math]::Floor($id / 10000))
    if (-not $images.ContainsKey($name)) {
        $img = $wz.WzDirectory.WzImages | Where-Object { $_.Name -eq $name }
        if ($img) { [void]$img.ParseImage() }
        $images[$name] = $img
    }
    $img = $images[$name]
    $level = if ($img) { $img.GetFromPath(('skill/{0:0000000}/level/{1}' -f $id, $row.level)) } else { $null }
    if (-not $level) { $missing["$id"] = $true; continue }
    $value = [int]$row.value
    $prop = $level.WzProperties | Where-Object { $_.Name -eq $row.field } | Select-Object -First 1
    if ($prop) {
        if ([int]$prop.WzValue -eq $value) { $same++; continue }
        if ($prop -is [MapleLib.WzLib.WzProperties.WzIntProperty]) { $prop.Value = $value }
        elseif ($prop -is [MapleLib.WzLib.WzProperties.WzShortProperty]) { $prop.Value = [int16]$value }
        else { throw "Skill $id level $($row.level) field $($row.field) has an unexpected type: $($prop.GetType().Name)" }
        $changed++
    } else {
        $level.AddProperty((New-Object MapleLib.WzLib.WzProperties.WzIntProperty($row.field, $value)))
        $added++
    }
    $img.Changed = $true
}
"Values: $changed changed, $added added, $same already matching. Skills not found in the client: $($missing.Keys.Count)"
if ($missing.Keys.Count) { '  ' + (($missing.Keys | Sort-Object) -join ', ') }

if ($CheckOnly) { $wz.Dispose(); 'Check only: nothing written.'; return }

$wz.SaveToDisk($patched, [MapleLib.WzLib.WzMapleVersion]::GMS)
$wz.Dispose()

# Read the result back: same number of files inside, and every value in place.
$before = Open-Wz $source; $countBefore = $before.WzDirectory.WzImages.Count; $before.Dispose()
$check = Open-Wz $patched
if ($check.WzDirectory.WzImages.Count -ne $countBefore) { throw 'The patched file lost data. Nothing was installed.' }
$bad = 0; $loaded = @{}
foreach ($row in $rows) {
    $id = [int]$row.skill_id
    if ($missing.ContainsKey("$id")) { continue }
    $name = ('{0:000}.img' -f [int][math]::Floor($id / 10000))
    if (-not $loaded.ContainsKey($name)) { $i = $check.WzDirectory.WzImages | Where-Object { $_.Name -eq $name }; [void]$i.ParseImage(); $loaded[$name] = $i }
    $p = $loaded[$name].GetFromPath(('skill/{0:0000000}/level/{1}/{2}' -f $id, $row.level, $row.field))
    if (-not $p -or [int]$p.WzValue -ne [int]$row.value) { $bad++ }
}
$check.Dispose()
if ($bad) { throw "$bad values did not read back correctly. Nothing was installed." }

Copy-Item $patched $target -Force
"Installed. Original kept as Skill.wz.original. Size {0:N0} bytes (original {1:N0})." -f (Get-Item $target).Length, (Get-Item $original).Length
