<#
.SYNOPSIS
  Install skills from this library into Claude Code and Codex.

.DESCRIPTION
  With no options, installs the core set into Claude Code (%USERPROFILE%\.claude\skills)
  and Codex (%USERPROFILE%\.agents\skills).

  Only skills this script installed are ever replaced or removed: it keeps a list of
  them in each skills folder (.agent-skills-managed), so your own skills are left alone.

.EXAMPLE
  .\install.ps1                        # core set into Claude Code and Codex
  .\install.ps1 -Profile all           # everything
  .\install.ps1 -Add motion,seo        # add categories or skill names
  .\install.ps1 -Remove gsap-timeline  # remove skills this script installed
  .\install.ps1 -Reset                 # remove every skill this script installed
  .\install.ps1 -List design           # list skills (* = core)

  If Windows blocks the script, run it with:
  powershell -ExecutionPolicy Bypass -File .\install.ps1

  Categories: design motion html frontend backend tokens workflow testing
              security marketing seo ads research learning automation writing agents
#>
[CmdletBinding()]
param(
  # Named -Preset because $Profile is a built-in PowerShell variable; -Profile still works
  [Alias('Profile')][ValidateSet('core', 'all')][string]$Preset,
  [string[]]$Add = @(),
  [string[]]$Remove = @(),
  [switch]$Reset,
  [ValidateSet('claude', 'codex', 'both')][string]$Target = 'both',
  [switch]$List,
  [Parameter(Position = 0)][string]$Category = '',
  [switch]$DryRun
)
$ErrorActionPreference = 'Stop'

$Root = $PSScriptRoot
$Index = Import-Csv -Path (Join-Path $Root 'index.tsv') -Delimiter "`t"
$ByName = @{}; foreach ($row in $Index) { $ByName[$row.name] = $row }
$Core = Get-Content (Join-Path $Root 'profiles/core.txt') | Where-Object { $_ -and -not $_.StartsWith('#') }
$Manifest = '.agent-skills-managed'

$claudeHome = if ($env:CLAUDE_CONFIG_DIR) { $env:CLAUDE_CONFIG_DIR } else { Join-Path $HOME '.claude' }
$Dirs = switch ($Target) {
  'claude' { @(Join-Path $claudeHome 'skills') }
  'codex' { @(Join-Path $HOME '.agents/skills') }
  default { @((Join-Path $claudeHome 'skills'), (Join-Path $HOME '.agents/skills')) }
}

if ($List) {
  $Index | Where-Object { -not $Category -or $_.category -eq $Category } | ForEach-Object {
    $mark = if ($Core -contains $_.name) { '*' } else { ' ' }
    '{0} {1,-40} {2}' -f $mark, $_.name, $_.category
  }
  return
}

# Comma-separated values passed as one string still work: -Add "motion,seo"
function Split-Names([string[]]$values) { $values | ForEach-Object { $_ -split ',' } | Where-Object { $_ } }

# Turn names, categories and profiles into a list of skill names
function Expand-Names([string[]]$tokens) {
  $out = [System.Collections.Generic.List[string]]::new()
  foreach ($token in $tokens) {
    $names = switch ($token) {
      'core' { $Core }
      'all' { $Index.name }
      default {
        $inCategory = @($Index | Where-Object { $_.category -eq $token } | ForEach-Object { $_.name })
        if ($inCategory.Count) { $inCategory }
        elseif ($ByName.ContainsKey($token)) { $token }
        else { Write-Warning "No skill or category called '$token' (see .\install.ps1 -List)"; @() }
      }
    }
    foreach ($n in $names) { if (-not $out.Contains($n)) { $out.Add($n) } }
  }
  return $out
}

function Get-Managed($dir) {
  $file = Join-Path $dir $Manifest
  if (Test-Path $file) { @(Get-Content $file | Where-Object { $_ }) } else { @() }
}

function Set-Managed($dir, [string[]]$names) {
  Set-Content -Path (Join-Path $dir $Manifest) -Value ($names | Sort-Object -Unique) -Encoding utf8
}

# Skills without a licence that allows copying them here are downloaded from their
# own repository, pinned to the commit that was reviewed.
function Get-RemoteSkill($row) {
  $cache = Join-Path $Root (".cache/{0}@{1}" -f ($row.repo -replace '/', '_'), $row.commit)
  $source = Join-Path $cache $row.path
  if (-not (Test-Path $source)) {
    if (-not (Get-Command git -ErrorAction SilentlyContinue)) { throw "git is needed to install $($row.repo) skills" }
    New-Item -ItemType Directory -Force -Path $cache | Out-Null
    if (-not (Test-Path (Join-Path $cache '.git'))) {
      git -c gc.auto=0 -C $cache init -q
      git -c gc.auto=0 -C $cache remote add origin "https://github.com/$($row.repo)"
      git -c gc.auto=0 -C $cache fetch -q --depth 1 --filter=blob:none origin $row.commit
      if ($LASTEXITCODE -ne 0) { Remove-Item -Recurse -Force $cache; throw "Could not download $($row.name) from $($row.repo)" }
    }
    git -c gc.auto=0 -C $cache checkout -q FETCH_HEAD -- $row.path
    if ($LASTEXITCODE -ne 0) { throw "Could not download $($row.name) from $($row.repo)" }
  }
  return $source
}

$wantTokens = @(Split-Names $Add)
if ($Preset) { $wantTokens = @($Preset) + $wantTokens }
$dropTokens = @(Split-Names $Remove)
if (-not $Reset -and -not $dropTokens.Count -and -not $wantTokens.Count) { $wantTokens = @('core') }

foreach ($dir in $Dirs) {
  Write-Host $dir
  if (-not $DryRun) { New-Item -ItemType Directory -Force -Path $dir | Out-Null }
  $managed = [System.Collections.Generic.List[string]]::new()
  foreach ($n in (Get-Managed $dir)) { $managed.Add($n) }

  $toRemove = @()
  if ($Reset) { $toRemove += $managed.ToArray() }
  if ($dropTokens.Count) { $toRemove += Expand-Names $dropTokens }
  foreach ($name in ($toRemove | Select-Object -Unique)) {
    if (-not $managed.Contains($name)) { continue }
    Write-Host "  - $name"
    if (-not $DryRun) {
      Remove-Item -Recurse -Force (Join-Path $dir $name) -ErrorAction SilentlyContinue
      [void]$managed.Remove($name)
    }
  }

  if ($wantTokens.Count) {
    foreach ($name in (Expand-Names $wantTokens)) {
      $row = $ByName[$name]
      $dest = Join-Path $dir $name
      if ((Test-Path $dest) -and -not $managed.Contains($name)) {
        Write-Host "  - ${name}: skipped, you already have your own skill with this name"
        continue
      }
      if ($DryRun) { Write-Host "  + $name ($($row.kind))"; continue }
      try {
        $source = if ($row.kind -eq 'remote') { Get-RemoteSkill $row } else { Join-Path $Root "library/$name" }
      } catch { Write-Warning $_; continue }
      if (Test-Path $dest) { Remove-Item -Recurse -Force $dest }
      Copy-Item -Recurse -Path $source -Destination $dest
      if (-not $managed.Contains($name)) { $managed.Add($name) }
      Write-Host "  + $name"
    }
  }
  if (-not $DryRun) { Set-Managed $dir $managed.ToArray() }
  Write-Host "  $($managed.Count) skills from this library installed here"
}

Write-Host ''
Write-Host 'Done. Restart Claude Code / Codex to pick up the changes.'
Write-Host 'Every installed skill adds its description to each session, so keep the active set lean.'
