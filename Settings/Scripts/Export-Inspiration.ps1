# Pulls art out of the game client into Settings\Inspiration, to look at when making new art.
#
#     powershell -ExecutionPolicy Bypass -File Settings\Scripts\Export-Inspiration.ps1
#     powershell -ExecutionPolicy Bypass -File Settings\Scripts\Export-Inspiration.ps1 -Only Places
#
# -Only is any of Monsters, Places, Backgrounds, Tiles, Objects; without it, all of them.
#
# Maps\Places        whole maps drawn as one picture, with their monsters: the towns and well-known hunting maps
# Maps\Backgrounds   the background layers of each set, and one overview sheet per set
# Maps\Tiles         the ground tiles of each set, and one overview sheet per set
# Maps\Objects       trees, houses and other decorations (first frame), and overview sheets per set
# Monsters\Sheets    every monster side by side, per ten levels, and the bosses on their own
# Monsters\All       one picture of every monster
# Monsters\Animations every frame of well-known monsters and bosses, one row per action
#
# Whole maps are an approximation: the game moves background layers with the camera, and here the camera
# stands in the middle of the map. For looking at only: Settings\Inspiration is in .gitignore, since the
# repository is public and the art is not ours.
param([string[]]$Only = @('Monsters', 'Places', 'Backgrounds', 'Tiles', 'Objects'))

$ErrorActionPreference = 'Stop'
$Only = @($Only | ForEach-Object { $_ -split ',' })      # -File hands over "Monsters,Tiles" as one word
$root = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
$out = Join-Path $root 'Settings\Inspiration'
Add-Type -AssemblyName System.Drawing
Add-Type -Path (Join-Path $root 'Tools\HaRepacker-4.1.0\AnyCPU\MapleLib.dll')

$towns = [ordered]@{
    'Amherst' = 1000000; 'Southperry' = 2000000; 'Henesys' = 100000000; 'Ellinia' = 101000000; 'Perion' = 102000000
    'Kerning City' = 103000000; 'Lith Harbor' = 104000000; 'Sleepywood' = 105040300; 'Florina Beach' = 110000000
    'Nautilus Harbor' = 120000000; 'Ereve' = 130000000; 'Rien' = 140000000; 'Orbis' = 200000000; 'El Nath' = 211000000
    'Ludibrium' = 220000000; 'Omega Sector' = 221000000; 'Korean Folk Town' = 222000000; 'Aquarium' = 230000000
    'Leafre' = 240000000; 'Mu Lung' = 250000000; 'Herb Town' = 251000000; 'Ariant' = 260000000; 'Magatia' = 261000000
    'Temple of Time' = 270000000; 'New Leaf City' = 600000000; 'Amoria' = 680000000; 'Mushroom Shrine' = 800000000
    'Free Market' = 910000000; 'Zakum Altar' = 280030000; 'Pink Bean' = 270050100; 'Papulatus' = 220080001
}
# Hunting maps, found by name in Settings\Reference\Maps.tsv
$fields = @('Snail Hunting Ground II', 'Forest West of Henesys', 'Monkey Forest I', 'The Forest of Wisdom', 'West Rocky Mountain I',
    'Ant Tunnel I', 'The Cave of Evil Eye I', 'Construction Site North of Kerning City', 'Line 1 <Area 1>', 'The Chilly Hill',
    'Dead Mine I', 'Razor Sharp Cliff', 'Eos Tower 1st Floor', 'Toy Factory <Process 1> Zone 1', 'Crossroad of Time',
    'Kulan Field I', 'Boswell Field I', 'Black Mountain <Corner>', 'Blue Seaweed Road', 'Deep Sea Gorge I', 'West Leafre Forest',
    'The Dragon Canyon', 'Red-Nose Pirate Den 1', 'The Desert of Red Sand', 'Road of Regrets1', 'Snow-covered Field 1',
    'Mushroom Forest Field', 'Jungle Clearing', 'Valley of Heroes 1', 'Bent Tree')
# Monsters drawn frame by frame
$animated = @('Snail', 'Blue Snail', 'Red Snail', 'Slime', 'Orange Mushroom', 'Green Mushroom', 'Horny Mushroom', 'Zombie Mushroom', 'Stump',
    'Pig', 'Ribbon Pig', 'Octopus', 'Evil Eye', 'Curse Eye', 'Lupin', 'Jr. Necki', 'Ligator', 'Fire Boar', 'Wraith', 'Stone Golem', 'Drake',
    'Yeti', 'Pepe', 'Sentinel', 'Hector', 'Tauromacis', 'Taurospear', 'Mano', 'Stumpy', 'King Slime', 'Mushmom', 'Crimson Balrog', 'Papulatus',
    'Pianus', 'Pink Bean')
$actionOrder = 'stand', 'move', 'fly', 'jump', 'hit1', 'attack1', 'attack2', 'attack3', 'skill1', 'skill2', 'die1', 'die2'

function Open-Wz($name) {
    $wz = New-Object MapleLib.WzLib.WzFile((Join-Path $root "Client\MapleStory\$name"), [int16]83, [MapleLib.WzLib.WzMapleVersion]::GMS)
    $message = $null
    if (-not $wz.ParseWzFile([ref]$message, $null)) { throw "Could not read $name : $message" }
    return , $wz
}

function Safe($name) { return ($name -replace '[\\/:*?"<>|]', '').Trim() }

function Parsed($img) {
    if ($img -and -not $img.Parsed) { $img.ParseImage() | Out-Null }
    return $img
}

function Num($p, $name, $default) {
    $v = $p[$name]
    if ($null -eq $v) { return $default }
    return [int]$v.Value
}

function Text($p, $name) {
    $v = $p[$name]
    if ($null -eq $v) { return '' }
    return [string]$v.Value
}

# A canvas, following a link to another one if that is what is stored there
function Canvas($p) {
    for ($i = 0; $i -lt 5 -and $p -is [MapleLib.WzLib.WzProperties.WzUOLProperty]; $i++) { $p = $p.LinkValue }
    if ($p -is [MapleLib.WzLib.WzProperties.WzCanvasProperty]) { return $p }
    return $null
}

function Release($img) {
    $img.UnparseImage()
    [GC]::Collect()
}

function Numbered($p) {
    if (-not $p -or -not $p.WzProperties) { return @() }
    return @($p.WzProperties | Where-Object { $_.Name -match '^\d+$' } | Sort-Object { [int]$_.Name })
}

function Save-Canvas($canvas, $file) {
    New-Item -ItemType Directory -Force (Split-Path -Parent $file) | Out-Null
    # Not disposed: the library keeps this bitmap and hands out the same one next time
    $bitmap = $canvas.GetBitmap()
    if ($bitmap) { $bitmap.Save($file, [System.Drawing.Imaging.ImageFormat]::Png) }
}

# Overview pictures: the given files side by side with their names, largest ones scaled down to fit a cell
function Save-Sheet($items, $file, $cellW, $cellH, $columns) {
    if ($items.Count -eq 0) { return }
    New-Item -ItemType Directory -Force (Split-Path -Parent $file) | Out-Null
    $perSheet = $columns * 25
    $part = 0
    for ($start = 0; $start -lt $items.Count; $start += $perSheet) {
        $part++
        $slice = @($items | Select-Object -Skip $start -First $perSheet)
        $rows = [math]::Ceiling($slice.Count / $columns)
        $labelH = 30
        $sheet = New-Object System.Drawing.Bitmap(($columns * $cellW), ($rows * ($cellH + $labelH)))
        $g = [System.Drawing.Graphics]::FromImage($sheet)
        $g.Clear([System.Drawing.Color]::FromArgb(58, 66, 78))
        $g.InterpolationMode = 'NearestNeighbor'
        $g.PixelOffsetMode = 'Half'
        $font = New-Object System.Drawing.Font('Segoe UI', 8)
        for ($i = 0; $i -lt $slice.Count; $i++) {
            $x = ($i % $columns) * $cellW
            $y = [math]::Floor($i / $columns) * ($cellH + $labelH)
            $img = [System.Drawing.Image]::FromFile($slice[$i].File)
            $scale = [math]::Min(1.0, [math]::Min(($cellW - 8) / $img.Width, ($cellH - 8) / $img.Height))
            $w = [int][math]::Max(1, $img.Width * $scale)
            $h = [int][math]::Max(1, $img.Height * $scale)
            $g.DrawImage($img, [int]($x + ($cellW - $w) / 2), [int]($y + $cellH - $h - 4), $w, $h)
            $img.Dispose()
            $rect = New-Object System.Drawing.RectangleF($x, ($y + $cellH), $cellW, $labelH)
            $format = New-Object System.Drawing.StringFormat
            $format.Alignment = 'Center'
            $g.DrawString($slice[$i].Label, $font, [System.Drawing.Brushes]::White, $rect, $format)
        }
        $g.Dispose()
        $target = if ($items.Count -gt $perSheet) { $file -replace '\.png$', " part $part.png" } else { $file }
        $sheet.Save($target, [System.Drawing.Imaging.ImageFormat]::Png)
        $sheet.Dispose()
    }
}

function Item($file, $label) { return [pscustomobject]@{ File = $file; Label = $label } }

# ---------- Monsters ----------

function Mob-Image($mobWz, $id) {
    $img = Parsed $mobWz.WzDirectory.GetImageByName(('{0:D7}.img' -f $id))
    if (-not $img) { return $null }
    $info = $img['info']
    if ($info -and $info['link']) {
        $linked = Parsed $mobWz.WzDirectory.GetImageByName(('{0:D7}.img' -f [int]$info['link'].Value))
        if ($linked) { return $linked }
    }
    return $img
}

function First-Frame($img) {
    foreach ($action in 'stand', 'fly', 'move') {
        $p = $img[$action]
        if ($p) {
            foreach ($f in Numbered $p) {
                $c = Canvas $f
                if ($c) { return $c }
            }
        }
    }
    return $null
}

function Save-Animation($img, $file) {
    $rows = @()
    $actions = @($actionOrder | Where-Object { $img[$_] })
    foreach ($action in $actions) {
        $frames = @()
        foreach ($f in (Numbered $img[$action] | Select-Object -First 14)) {
            $c = Canvas $f
            if ($c) {
                $b = $c.GetBitmap()
                if ($b) { $frames += $b }
            }
        }
        if ($frames.Count) { $rows += [pscustomobject]@{ Action = $action; Frames = $frames } }
    }
    if (-not $rows.Count) { return }
    $labelW = 70
    $width = 0; $height = 0
    foreach ($r in $rows) {
        $w = ($r.Frames | ForEach-Object { $_.Width } | Measure-Object -Maximum).Maximum + 6
        $h = ($r.Frames | ForEach-Object { $_.Height } | Measure-Object -Maximum).Maximum + 6
        $r | Add-Member CellW $w; $r | Add-Member CellH $h
        $width = [math]::Max($width, $labelW + $w * $r.Frames.Count)
        $height += $h
    }
    $sheet = New-Object System.Drawing.Bitmap([int]$width, [int]$height)
    $g = [System.Drawing.Graphics]::FromImage($sheet)
    $g.Clear([System.Drawing.Color]::FromArgb(58, 66, 78))
    $font = New-Object System.Drawing.Font('Segoe UI', 9)
    $y = 0
    foreach ($r in $rows) {
        $g.DrawString($r.Action, $font, [System.Drawing.Brushes]::White, 4, ($y + 4))
        $x = $labelW
        foreach ($b in $r.Frames) {
            $g.DrawImage($b, [int]($x + ($r.CellW - $b.Width) / 2), [int]($y + $r.CellH - $b.Height - 3), $b.Width, $b.Height)
            $x += $r.CellW
        }
        $y += $r.CellH
    }
    $g.Dispose()
    New-Item -ItemType Directory -Force (Split-Path -Parent $file) | Out-Null
    $sheet.Save($file, [System.Drawing.Imaging.ImageFormat]::Png)
    $sheet.Dispose()
}

function Export-Monsters {
    $mobWz = Open-Wz 'Mob.wz'
    $bands = @{}; $bosses = @(); $seen = @{}; $count = 0
    $rows = Import-Csv (Join-Path $root 'Settings\Reference\Mobs.tsv') -Delimiter "`t" | Sort-Object { [int]$_.id }
    foreach ($row in $rows) {
        $name = Safe $row.name
        if (-not $name -or $name -like 'MISSING*' -or $seen.ContainsKey($name)) { continue }
        $img = Mob-Image $mobWz ([int]$row.id)
        if (-not $img) { continue }
        $frame = First-Frame $img
        if (-not $frame) { continue }
        $seen[$name] = 1
        $level = 0; [void][int]::TryParse($row.level, [ref]$level)
        $file = Join-Path $out "Monsters\All\$name.png"
        try { Save-Canvas $frame $file } catch { Write-Warning "$name : $_"; continue }
        $count++
        $label = "$name ($level)"
        if ($row.boss) { $bosses += Item $file $label }
        else {
            $band = [int]([math]::Floor([math]::Max(0, $level - 1) / 10) * 10 + 1)
            if (-not $bands.ContainsKey($band)) { $bands[$band] = @() }
            $bands[$band] += Item $file $label
        }
    }
    "Monsters: $count pictures"
    foreach ($band in $bands.Keys) {
        Save-Sheet $bands[$band] (Join-Path $out ('Monsters\Sheets\Level {0:D3} to {1:D3}.png' -f $band, ($band + 9))) 170 150 8
    }
    Save-Sheet $bosses (Join-Path $out 'Monsters\Sheets\Bosses.png') 320 300 5
    foreach ($name in $animated) {
        $row = $rows | Where-Object { $_.name.Trim() -eq $name } | Select-Object -First 1
        if (-not $row) { Write-Warning "No monster called $name"; continue }
        $img = Mob-Image $mobWz ([int]$row.id)
        if ($img) { Save-Animation $img (Join-Path $out "Monsters\Animations\$(Safe $name).png") }
    }
    "Monsters: animations done"
    $mobWz.Dispose()
}

# ---------- Sets of map art ----------

function Export-Backgrounds($mapWz) {
    foreach ($img in $mapWz.WzDirectory.GetDirectoryByName('Back').WzImages) {
        Parsed $img | Out-Null
        $set = $img.Name -replace '\.img$', ''
        $items = @()
        foreach ($f in Numbered $img['back']) {
            $c = Canvas $f
            if (-not $c) { continue }
            $file = Join-Path $out "Maps\Backgrounds\$set\$($f.Name).png"
            Save-Canvas $c $file
            if (Test-Path $file) { $items += Item $file $f.Name }
        }
        foreach ($a in Numbered $img['ani']) {
            $f = Numbered $a | Select-Object -First 1
            $c = if ($f) { Canvas $f } else { $null }
            if (-not $c) { continue }
            $file = Join-Path $out "Maps\Backgrounds\$set\animated $($a.Name).png"
            Save-Canvas $c $file
            if (Test-Path $file) { $items += Item $file "animated $($a.Name)" }
        }
        Save-Sheet $items (Join-Path $out "Maps\Backgrounds\_Overview\$set.png") 320 240 4
        Release $img
    }
    "Backgrounds done"
}

function Export-Tiles($mapWz) {
    foreach ($img in $mapWz.WzDirectory.GetDirectoryByName('Tile').WzImages) {
        Parsed $img | Out-Null
        $set = $img.Name -replace '\.img$', ''
        $items = @()
        foreach ($kind in $img.WzProperties) {
            if ($kind.Name -eq 'info') { continue }
            foreach ($f in Numbered $kind) {
                $c = Canvas $f
                if (-not $c) { continue }
                $file = Join-Path $out "Maps\Tiles\$set\$($kind.Name) $($f.Name).png"
                Save-Canvas $c $file
                if (Test-Path $file) { $items += Item $file "$($kind.Name) $($f.Name)" }
            }
        }
        Save-Sheet $items (Join-Path $out "Maps\Tiles\_Overview\$set.png") 110 90 10
        Release $img
    }
    "Tiles done"
}

function Export-Objects($mapWz) {
    foreach ($img in $mapWz.WzDirectory.GetDirectoryByName('Obj').WzImages) {
        Parsed $img | Out-Null
        $set = $img.Name -replace '\.img$', ''
        $items = @()
        foreach ($l0 in $img.WzProperties) {
            if (-not $l0.WzProperties) { continue }
            foreach ($l1 in $l0.WzProperties) {
                if (-not $l1.WzProperties) { continue }
                foreach ($l2 in $l1.WzProperties) {
                    $f = Numbered $l2 | Select-Object -First 1
                    $c = if ($f) { Canvas $f } else { $null }
                    if (-not $c) { continue }
                    $label = Safe "$($l0.Name) $($l1.Name) $($l2.Name)"
                    $file = Join-Path $out "Maps\Objects\$set\$label.png"
                    try { Save-Canvas $c $file } catch { continue }
                    if (Test-Path $file) { $items += Item $file $label }
                }
            }
        }
        Save-Sheet $items (Join-Path $out "Maps\Objects\_Overview\$set.png") 180 170 8
        Release $img
    }
    "Objects done"
}

# ---------- Whole maps ----------

$bitmapCache = @{}

function Cached($key, $getCanvas) {
    if ($bitmapCache.ContainsKey($key)) { return $bitmapCache[$key] }
    $entry = $null
    try {
        $c = & $getCanvas
        if ($c) {
            $b = $c.GetBitmap()
            $o = $c['origin']
            $entry = [pscustomobject]@{
                Bitmap = $b
                OX = if ($o) { [int]$o.X.Value } else { 0 }
                OY = if ($o) { [int]$o.Y.Value } else { 0 }
                Z = Num $c 'z' 0
            }
        }
    } catch { }
    $bitmapCache[$key] = $entry
    return $entry
}

function Draw($g, $entry, $x, $y, $flip, $alpha) {
    $b = $entry.Bitmap
    if ($flip) { $rect = New-Object System.Drawing.Rectangle(($x + $b.Width), $y, (-$b.Width), $b.Height) }
    else { $rect = New-Object System.Drawing.Rectangle($x, $y, $b.Width, $b.Height) }
    if ($alpha -lt 255) {
        $matrix = New-Object System.Drawing.Imaging.ColorMatrix
        $matrix.Matrix33 = $alpha / 255.0
        $attr = New-Object System.Drawing.Imaging.ImageAttributes
        $attr.SetColorMatrix($matrix)
        $points = [System.Drawing.Point[]]@(
            (New-Object System.Drawing.Point($rect.Left, $y)),
            (New-Object System.Drawing.Point($rect.Right, $y)),
            (New-Object System.Drawing.Point($rect.Left, ($y + $b.Height))))
        $source = New-Object System.Drawing.Rectangle(0, 0, $b.Width, $b.Height)
        $g.DrawImage($b, $points, $source, [System.Drawing.GraphicsUnit]::Pixel, $attr)
        $attr.Dispose()
    } else {
        $g.DrawImage($b, $rect)
    }
}

function Map-Bounds($map) {
    $info = $map['info']
    if ($info -and $info['VRLeft'] -and $info['VRRight']) {
        return @((Num $info 'VRLeft' 0), (Num $info 'VRTop' 0), (Num $info 'VRRight' 800), (Num $info 'VRBottom' 600))
    }
    $l = 100000; $t = 100000; $r = -100000; $b = -100000
    $foothold = $map['foothold']
    if ($foothold) {
        foreach ($layer in $foothold.WzProperties) { foreach ($group in $layer.WzProperties) { foreach ($fh in $group.WzProperties) {
            $l = [math]::Min($l, [math]::Min((Num $fh 'x1' 0), (Num $fh 'x2' 0)))
            $r = [math]::Max($r, [math]::Max((Num $fh 'x1' 0), (Num $fh 'x2' 0)))
            $t = [math]::Min($t, [math]::Min((Num $fh 'y1' 0), (Num $fh 'y2' 0)))
            $b = [math]::Max($b, [math]::Max((Num $fh 'y1' 0), (Num $fh 'y2' 0)))
        } } }
    }
    if ($r -lt $l) { return @(-400, -300, 400, 300) }
    return @(($l - 50), ($t - 300), ($r + 50), ($b + 150))
}

function Draw-Backgrounds($g, $map, $dirBack, $left, $top, $width, $height, $front) {
    $back = $map['back']
    if (-not $back) { return }
    $cx = $left + $width / 2
    $cy = $top + $height / 2
    foreach ($bg in Numbered $back) {
        if ((Num $bg 'front' 0) -ne $front) { continue }
        $set = Text $bg 'bS'
        if (-not $set) { continue }
        $no = Num $bg 'no' 0
        $isAni = (Num $bg 'ani' 0) -eq 1
        $entry = Cached "back/$set/$isAni/$no" {
            $img = Parsed $dirBack.GetImageByName("$set.img")
            if (-not $img) { return $null }
            if ($isAni) { $a = $img['ani']; if ($a -and $a["$no"]) { return Canvas $a["$no"]['0'] } ; return $null }
            $k = $img['back']; if ($k -and $k["$no"]) { return Canvas $k["$no"] }
            return $null
        }
        if (-not $entry -or -not $entry.Bitmap) { continue }
        $b = $entry.Bitmap
        $type = Num $bg 'type' 0
        $rx = Num $bg 'rx' 0; $ry = Num $bg 'ry' 0
        # Where the layer lies with the camera in the middle of the map
        # rx 0 stays on the screen, rx -100 stays on the map. In moving types (4 to 7) rx or ry is a speed instead.
        $shiftX = if ($type -in 4, 6) { 0 } else { $cx * (100 + $rx) / 100 }
        $shiftY = if ($type -in 5, 7) { 0 } else { $cy * (100 + $ry) / 100 }
        $x = (Num $bg 'x' 0) + $shiftX - $entry.OX - $left
        $y = (Num $bg 'y' 0) + $shiftY - $entry.OY - $top
        $stepX = Num $bg 'cx' 0; if ($stepX -le 0) { $stepX = $b.Width }
        $stepY = Num $bg 'cy' 0; if ($stepY -le 0) { $stepY = $b.Height }
        $tileX = $type -in 1, 3, 4, 6, 7
        $tileY = $type -in 2, 3, 5, 6, 7
        $x0 = [int]$x; $y0 = [int]$y
        if ($tileX) { $x0 = [int]($x - [math]::Ceiling(($x + $b.Width) / $stepX) * $stepX) }
        if ($tileY) { $y0 = [int]($y - [math]::Ceiling(($y + $b.Height) / $stepY) * $stepY) }
        $alpha = Num $bg 'a' 255
        $flip = (Num $bg 'f' 0) -eq 1
        for ($py = $y0; $py -lt $height; $py += $stepY) {
            for ($px = $x0; $px -lt $width; $px += $stepX) {
                Draw $g $entry $px $py $flip $alpha
                if (-not $tileX) { break }
            }
            if (-not $tileY) { break }
        }
    }
}

function Render-Map($mapWz, $mobWz, $id, $name) {
    $s = '{0:D9}' -f $id
    $dirMap = $mapWz.WzDirectory.GetDirectoryByName('Map').GetDirectoryByName('Map' + $s[0])
    $map = if ($dirMap) { Parsed $dirMap.GetImageByName("$s.img") } else { $null }
    if (-not $map) { Write-Warning "No map $id ($name)"; return }
    $dirBack = $mapWz.WzDirectory.GetDirectoryByName('Back')
    $dirTile = $mapWz.WzDirectory.GetDirectoryByName('Tile')
    $dirObj = $mapWz.WzDirectory.GetDirectoryByName('Obj')
    $bounds = Map-Bounds $map
    $left = $bounds[0]; $top = $bounds[1]
    $width = [math]::Min(12000, $bounds[2] - $bounds[0]); $height = [math]::Min(6000, $bounds[3] - $bounds[1])
    if ($width -le 0 -or $height -le 0) { Write-Warning "Empty map $name"; return }
    $picture = New-Object System.Drawing.Bitmap([int]$width, [int]$height)
    $g = [System.Drawing.Graphics]::FromImage($picture)
    $g.Clear([System.Drawing.Color]::Black)
    $g.InterpolationMode = 'NearestNeighbor'
    $g.PixelOffsetMode = 'Half'

    Draw-Backgrounds $g $map $dirBack $left $top $width $height 0

    foreach ($layer in 0..7) {
        $l = $map["$layer"]
        if (-not $l) { continue }
        $drawables = New-Object System.Collections.ArrayList
        $objs = $l['obj']
        if ($objs) {
            foreach ($o in $objs.WzProperties) {
                $path = "$(Text $o 'oS')/$(Text $o 'l0')/$(Text $o 'l1')/$(Text $o 'l2')"
                $entry = Cached "obj/$path" {
                    $img = Parsed $dirObj.GetImageByName("$(Text $o 'oS').img")
                    if (-not $img) { return $null }
                    $p = $img[(Text $o 'l0')]; if ($p) { $p = $p[(Text $o 'l1')] }; if ($p) { $p = $p[(Text $o 'l2')] }
                    if ($p -and $p['0']) { return Canvas $p['0'] }
                    return $null
                }
                if ($entry -and $entry.Bitmap) {
                    [void]$drawables.Add([pscustomobject]@{ Kind = 0; Z = (Num $o 'z' 0); E = $entry; X = (Num $o 'x' 0); Y = (Num $o 'y' 0); F = ((Num $o 'f' 0) -eq 1) })
                }
            }
        }
        $tiles = $l['tile']
        $info = $l['info']
        $tS = if ($info) { Text $info 'tS' } else { '' }
        if ($tiles -and $tS) {
            foreach ($t in $tiles.WzProperties) {
                $u = Text $t 'u'; $no = Num $t 'no' 0
                $entry = Cached "tile/$tS/$u/$no" {
                    $img = Parsed $dirTile.GetImageByName("$tS.img")
                    if (-not $img) { return $null }
                    $k = $img[$u]
                    if ($k -and $k["$no"]) { return Canvas $k["$no"] }
                    return $null
                }
                if ($entry -and $entry.Bitmap) {
                    [void]$drawables.Add([pscustomobject]@{ Kind = 1; Z = ($entry.Z + (Num $t 'zM' 0)); E = $entry; X = (Num $t 'x' 0); Y = (Num $t 'y' 0); F = $false })
                }
            }
        }
        foreach ($d in ($drawables | Sort-Object Kind, Z)) {
            Draw $g $d.E ([int]($d.X - $d.E.OX - $left)) ([int]($d.Y - $d.E.OY - $top)) $d.F 255
        }
    }

    # The monsters that live here
    $life = $map['life']
    if ($life) {
        foreach ($m in $life.WzProperties) {
            if ((Text $m 'type') -ne 'm') { continue }
            $mobId = [int](Text $m 'id')
            $entry = Cached "mob/$mobId" {
                $img = Mob-Image $mobWz $mobId
                if ($img) { return First-Frame $img }
                return $null
            }
            if ($entry -and $entry.Bitmap) {
                # In the game a monster that is not flipped faces left, as it is drawn
                Draw $g $entry ([int]((Num $m 'x' 0) - $entry.OX - $left)) ([int]((Num $m 'cy' 0) - $entry.OY - $top)) ((Num $m 'f' 0) -eq 1) 255
            }
        }
    }

    Draw-Backgrounds $g $map $dirBack $left $top $width $height 1
    $g.Dispose()
    $folder = Join-Path $out 'Maps\Places'
    New-Item -ItemType Directory -Force $folder | Out-Null
    $picture.Save((Join-Path $folder "$(Safe $name).png"), [System.Drawing.Imaging.ImageFormat]::Png)
    $picture.Dispose()
    "  $name"
}

function Export-Places($mapWz) {
    $mobWz = Open-Wz 'Mob.wz'
    $byName = @{}
    Import-Csv (Join-Path $root 'Settings\Reference\Maps.tsv') -Delimiter "`t" | ForEach-Object {
        $n = $_.name.Trim()
        if ($n -and -not $byName.ContainsKey($n)) { $byName[$n] = [int]$_.id }
    }
    foreach ($name in $towns.Keys) {
        try { Render-Map $mapWz $mobWz $towns[$name] $name } catch { Write-Warning "$name : $_" }
    }
    foreach ($name in $fields) {
        if (-not $byName.ContainsKey($name)) { Write-Warning "No map called $name"; continue }
        try { Render-Map $mapWz $mobWz $byName[$name] $name } catch { Write-Warning "$name : $_" }
    }
    $bitmapCache.Clear()
    $mobWz.Dispose()
    "Places done"
}

if ($Only -contains 'Monsters') { Export-Monsters }
if ($Only | Where-Object { $_ -in 'Places', 'Backgrounds', 'Tiles', 'Objects' }) {
    $mapWz = Open-Wz 'Map.wz'
    if ($Only -contains 'Places') { Export-Places $mapWz }
    if ($Only -contains 'Backgrounds') { Export-Backgrounds $mapWz }
    if ($Only -contains 'Tiles') { Export-Tiles $mapWz }
    if ($Only -contains 'Objects') { Export-Objects $mapWz }
    $mapWz.Dispose()
}
$files = Get-ChildItem $out -Recurse -File
"{0} files, {1} MB in Settings\Inspiration" -f $files.Count, [int](($files | Measure-Object Length -Sum).Sum / 1MB)
