# Makes the client's skill data (Client\MapleStory\Skill.wz) match the server's for every field listed in
# Skill-Changes.tsv. Run Apply-Skill-Changes.py first; the game must be closed.
#
#   powershell -ExecutionPolicy Bypass -File Settings\Scripts\Patch-Client-Skills.ps1
#   powershell -ExecutionPolicy Bypass -File Settings\Scripts\Patch-Client-Skills.ps1 -CheckOnly
#
# The untouched original is kept once as Skill.wz.original. The patched file is written to a temporary
# file, read back and checked, and only then put in place.
param([switch]$CheckOnly, [string[]]$Show = @(), [int]$ShowCount = 0)

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
$edits = New-Object System.Collections.ArrayList      # every value that differs from the original, for the tooltips
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
    $prop = $level.WzProperties | Where-Object { $_.Name -eq $row.field } | Select-Object -First 1
    if ($row.value -match ',') {
        # A corner of the skill's hit box, written as "x,y".
        $x, $y = $row.value.Split(',') | ForEach-Object { [int]$_ }
        if ($prop) {
            if ($prop.X.Value -eq $x -and $prop.Y.Value -eq $y) { $same++; continue }
            $prop.X.Value = $x; $prop.Y.Value = $y; $changed++
        } else {
            $level.AddProperty((New-Object MapleLib.WzLib.WzProperties.WzVectorProperty($row.field, [int]$x, [int]$y)))
            $added++
        }
        $img.Changed = $true
        continue
    }
    $value = [int]$row.value
    if ($prop) {
        $old = [int]$prop.WzValue
        if ($old -eq $value) { $same++; continue }
        if ($prop -is [MapleLib.WzLib.WzProperties.WzIntProperty]) { $prop.Value = $value }
        elseif ($prop -is [MapleLib.WzLib.WzProperties.WzShortProperty]) { $prop.Value = [int16]$value }
        else { throw "Skill $id level $($row.level) field $($row.field) has an unexpected type: $($prop.GetType().Name)" }
        $changed++
        [void]$edits.Add([pscustomobject]@{ id = $id; level = $row.level; field = $row.field; old = $old; new = $value })
    } else {
        $level.AddProperty((New-Object MapleLib.WzLib.WzProperties.WzIntProperty($row.field, $value)))
        $added++
        [void]$edits.Add([pscustomobject]@{ id = $id; level = $row.level; field = $row.field; old = $null; new = $value })
    }
    $img.Changed = $true
}
"Values: $changed changed, $added added, $same already matching. Skills not found in the client: $($missing.Keys.Count)"
if ($missing.Keys.Count) { '  ' + (($missing.Keys | Sort-Object) -join ', ') }

# ---- Tooltips: rewrite the per-level description texts in String.wz so they show the new numbers.
$textTarget = Join-Path $client 'String.wz'
$textOriginal = Join-Path $client 'String.wz.original'
if (-not (Test-Path $textOriginal)) { Copy-Item $textTarget $textOriginal }
$textSource = Join-Path $work 'String.source.wz'
$textPatched = Join-Path $work 'String.patched.wz'
Copy-Item $textOriginal $textSource -Force
Remove-Item $textPatched -ErrorAction SilentlyContinue
$textWz = Open-Wz $textSource
$skillText = $textWz.WzDirectory.WzImages | Where-Object { $_.Name -eq 'Skill.img' }
[void]$skillText.ParseImage()

# Where each kind of number sits in the original wording.
$patterns = @{
    time        = @('(?<=for )\d+(?= ?sec)')
    mpCon       = @('(?<=MP ?- ?)\d+')
    hpCon       = @('(?<=HP ?- ?)\d+')
    damage      = @('\d+(?=% damage)', '(?<=damage )\d+(?=%)', '\d+(?=% in damage)')
    attackCount = @('(?<=attack )\d+(?=x)')
    speed       = @('(?<=speed \+)\d+')
    pdd         = @('(?<=weapon def\. ?[+-])\d+')
    mdd         = @('(?<=magic def\. ?[+-])\d+')
    prop        = @('\d+(?=% success)')
}
# Wording to add when the original text has no place for the number.
$extras = @{ mobCount = 'hits up to {0} enemies'; mdd = 'magic def. +{0}'; speed = 'speed +{0}'; cooltime = 'cooldown {0} sec'
             pdd = 'weapon def. +{0}'; attackCount = '{0} hits' }
$textsChanged = 0; $unplaced = 0
$samples = New-Object System.Collections.ArrayList     # before and after, shown with -CheckOnly -ShowCount N
foreach ($group in ($edits | Group-Object id, level)) {
    $id = $group.Group[0].id; $lv = $group.Group[0].level
    $node = $skillText.GetFromPath(('{0:0000000}/h{1}' -f $id, $lv))
    if (-not $node) { $node = $skillText.GetFromPath(('{0}/h{1}' -f $id, $lv)) }
    if (-not $node) { $unplaced += $group.Count; continue }
    $text = [string]$node.Value; $before = $text
    foreach ($e in $group.Group) {
        $new = [string][math]::Abs($e.new); $done = $false
        foreach ($p in @($patterns[$e.field])) {
            if ($p -and [regex]::IsMatch($text, $p)) { $text = ([regex]$p).Replace($text, $new, 1); $done = $true; break }
        }
        if (-not $done -and $null -ne $e.old) {
            $whole = '(?<![\d.])' + [math]::Abs($e.old) + '(?![\d.])'
            if ([regex]::Matches($text, $whole).Count -eq 1) { $text = ([regex]$whole).Replace($text, $new, 1); $done = $true }
        }
        if (-not $done -and $extras.ContainsKey($e.field) -and $e.new -ne 0) {
            $text = $text.TrimEnd().TrimEnd('.') + '; ' + ($extras[$e.field] -f $new) + '.'; $done = $true
        }
        if (-not $done) { $unplaced++ }
    }
    if ($text -ne $before) {
        $node.Value = $text; $textsChanged++; $skillText.Changed = $true
        if ($lv -eq '1' -or $Show -contains "$id") { [void]$samples.Add(("{0} h{1}: {2}  =>  {3}" -f $id, $lv, $before, $text)) }
    }
}
"Tooltips: $textsChanged level texts updated. $unplaced values have no place in their text and were left out."
if ($CheckOnly -and $ShowCount -gt 0) { $samples | Select-Object -First $ShowCount }

if ($CheckOnly) { $wz.Dispose(); $textWz.Dispose(); 'Check only: nothing written.'; return }

$wz.SaveToDisk($patched, [MapleLib.WzLib.WzMapleVersion]::GMS)
$wz.Dispose()
$textWz.SaveToDisk($textPatched, [MapleLib.WzLib.WzMapleVersion]::GMS)
$textWz.Dispose()
$textCheck = Open-Wz $textPatched
$textCheckImg = $textCheck.WzDirectory.WzImages | Where-Object { $_.Name -eq 'Skill.img' }
[void]$textCheckImg.ParseImage()
$textImages = $textCheck.WzDirectory.WzImages.Count
$sample = $textCheckImg.GetFromPath('4201005/h30')
$textCheck.Dispose()
$textBefore = Open-Wz $textSource; $textImagesBefore = $textBefore.WzDirectory.WzImages.Count; $textBefore.Dispose()
if ($textImages -ne $textImagesBefore -or -not $sample) { throw 'The patched text file did not read back correctly. Nothing was installed.' }

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
    if (-not $p) { $bad++ }
    elseif ($row.value -match ',') { if (('{0},{1}' -f $p.X.Value, $p.Y.Value) -ne $row.value) { $bad++ } }
    elseif ([int]$p.WzValue -ne [int]$row.value) { $bad++ }
}
$check.Dispose()
if ($bad) { throw "$bad values did not read back correctly. Nothing was installed." }

Copy-Item $patched $target -Force
Copy-Item $textPatched $textTarget -Force
"Installed. Originals kept as Skill.wz.original and String.wz.original."
"Skill.wz {0:N0} bytes (original {1:N0}). String.wz {2:N0} bytes (original {3:N0})." -f (Get-Item $target).Length, (Get-Item $original).Length, (Get-Item $textTarget).Length, (Get-Item $textOriginal).Length
