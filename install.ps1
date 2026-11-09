<#
.SYNOPSIS
  Install skills and agents from this library into Claude Code and Codex.

.DESCRIPTION
  With no options, installs the core skills into Claude Code (%USERPROFILE%\.claude\skills)
  and Codex (%USERPROFILE%\.agents\skills), and the core agents into
  %USERPROFILE%\.claude\agents and %USERPROFILE%\.codex\agents. Everything else stays in
  this folder, and the library-router skill reads the best skill or agent from it when a
  task needs one.

  Only skills and agents this script installed are ever replaced or removed: it keeps a
  list of them in each folder (.agent-skills-managed), so your own are left alone.

.EXAMPLE
  .\install.ps1                        # core skills + core agents into Claude Code and Codex
  .\install.ps1 -Profile all           # every skill (+ all agents)
  .\install.ps1 -Add motion,seo        # add categories or skill names
  .\install.ps1 -Remove gsap-timeline  # remove skills this script installed
  .\install.ps1 -List design           # list skills (* = core)
  .\install.ps1 -Agents engineering,design   # add agents by division or name
  .\install.ps1 -Agents all            # every agent (core and all also remove other agents it installed)
  .\install.ps1 -NoAgents              # core skills only, no agents
  .\install.ps1 -RemoveAgents all      # remove the agents this script installed (or name divisions)
  .\install.ps1 -ListAgents marketing  # list agents in a division
  .\install.ps1 -SetupRea              # also run REA's own setup (needs Node.js 22.23.4+)
  .\install.ps1 -SetupGraphify         # also install the graphifyy Python package for the graphify skill
  .\install.ps1 -Reset                 # remove every skill and agent this script installed

  If Windows blocks the script, run it with:
  powershell -ExecutionPolicy Bypass -File .\install.ps1

  Skill categories: design motion html frontend backend tokens workflow testing
                    security marketing sales seo ads research learning automation writing agents
  Agent divisions:  academic design engineering finance game-development gis healthcare
                    marketing paid-media product project-management research sales
                    security spatial-computing specialized support testing ads
#>
[CmdletBinding()]
param(
  # Named -Preset because $Profile is a built-in PowerShell variable; -Profile still works
  [Alias('Profile')][ValidateSet('core', 'all')][string]$Preset,
  [string[]]$Add = @(),
  [string[]]$Remove = @(),
  [string[]]$Agents = @(),
  [switch]$NoAgents,
  [string[]]$RemoveAgents = @(),
  [switch]$ListAgents,
  [switch]$SetupRea,
  [switch]$SetupGraphify,
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
$AgentIndex = Import-Csv -Path (Join-Path $Root 'agents/index.tsv') -Delimiter "`t" -Encoding UTF8
$AgentCore = Get-Content (Join-Path $Root 'profiles/agents-core.txt') | Where-Object { $_ -and -not $_.StartsWith('#') }
$Manifest = '.agent-skills-managed'
# REA (Reverse Engineer Anything) version that -SetupRea runs; it matches
# library/reverse-engineer-anything. Official package: npm rea-agents (github.com/morluto/rea).
$ReaVersion = '6.8.0'

$claudeHome = if ($env:CLAUDE_CONFIG_DIR) { $env:CLAUDE_CONFIG_DIR } else { Join-Path $HOME '.claude' }
$codexHome = if ($env:CODEX_HOME) { $env:CODEX_HOME } else { Join-Path $HOME '.codex' }
$ClaudeAgents = Join-Path $claudeHome 'agents'
$CodexAgents = Join-Path $codexHome 'agents'
$Dirs = switch ($Target) {
  'claude' { @(Join-Path $claudeHome 'skills') }
  'codex' { @(Join-Path $HOME '.agents/skills') }
  default { @((Join-Path $claudeHome 'skills'), (Join-Path $HOME '.agents/skills')) }
}
$AgentDirs = switch ($Target) {
  'claude' { @($ClaudeAgents) }
  'codex' { @($CodexAgents) }
  default { @($ClaudeAgents, $CodexAgents) }
}

if ($List) {
  $Index | Where-Object { -not $Category -or $_.category -eq $Category } | ForEach-Object {
    $mark = if ($Core -contains $_.name) { '*' } else { ' ' }
    '{0} {1,-40} {2}' -f $mark, $_.name, $_.category
  }
  return
}

if ($ListAgents) {
  $shown = @($AgentIndex | Where-Object { -not $Category -or $_.division -eq $Category })
  $shown | ForEach-Object { '{0} {1,-48} {2,-20} {3}' -f $(if ($AgentCore -contains $_.id) { '*' } else { ' ' }), $_.id, $_.division, $_.name }
  ''
  "$($shown.Count) agents (* = core)"
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

# Turn divisions and agent names into agent index rows
function Expand-Agents([string[]]$tokens) {
  $out = [System.Collections.Generic.List[object]]::new()
  $seen = @{}
  foreach ($token in $tokens) {
    $rows = if ($token -eq 'core') { @($AgentIndex | Where-Object { $AgentCore -contains $_.id }) }
            else { @($AgentIndex | Where-Object { $token -eq 'all' -or $_.id -eq $token -or $_.division -eq $token -or $_.codex -eq $token }) }
    if (-not $rows.Count) { Write-Warning "No agent or division called '$token' (see .\install.ps1 -ListAgents)" }
    foreach ($r in $rows) { if (-not $seen.ContainsKey($r.id)) { $seen[$r.id] = 1; $out.Add($r) } }
  }
  return $out
}

function Get-Managed($dir) {
  $file = Join-Path $dir $Manifest
  if (Test-Path $file) { @(Get-Content $file | Where-Object { $_ }) } else { @() }
}

function Set-Managed($dir, [string[]]$names) {
  $file = Join-Path $dir $Manifest
  if ($names.Count) { Set-Content -Path $file -Value ($names | Sort-Object -Unique) -Encoding utf8 }
  elseif (Test-Path $file) { Remove-Item -Force $file }
}

# Agents are single files: <id>.md for Claude Code, <codex name>.toml for Codex
function Get-AgentFile($dir, $row) { if ($dir -eq $CodexAgents) { "$($row.codex).toml" } else { "$($row.id).md" } }
function Get-AgentSource($dir, $row) {
  if ($dir -eq $CodexAgents) { Join-Path $Root "agents/codex/$($row.codex).toml" }
  else { Join-Path $Root "agents/claude/$($row.division)/$($row.id).md" }
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
$agentWant = @(Split-Names $Agents)
$agentDrop = @(Split-Names $RemoveAgents)
$defaultRun = -not $Reset -and -not $dropTokens.Count -and -not $wantTokens.Count -and -not $agentWant.Count -and -not $agentDrop.Count
if ($defaultRun) { $wantTokens = @('core') }
if ($NoAgents) { $agentWant = @() }
elseif (-not $agentWant.Count -and $Preset -eq 'all') { $agentWant = @('all') }
elseif (-not $agentWant.Count -and ($defaultRun -or $Preset)) { $agentWant = @('core') }

if ($DryRun) { Write-Host 'Dry run: nothing will be changed.' }
$skillDirs = if ($Reset -or $dropTokens.Count -or $wantTokens.Count) { $Dirs } else { @() }
foreach ($dir in $skillDirs) {
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
      # Some skills ship a Windows version of SKILL.md: use it on Windows, drop it elsewhere
      $winSkill = Join-Path $dest 'SKILL.windows.md'
      if (Test-Path $winSkill) {
        if ([System.Environment]::OSVersion.Platform -eq 'Win32NT') { Move-Item -Force $winSkill (Join-Path $dest 'SKILL.md') }
        else { Remove-Item -Force $winSkill }
      }
      # Skills that need to know where this library is (library-router)
      $skillFile = Join-Path $dest 'SKILL.md'
      $skillText = [System.IO.File]::ReadAllText($skillFile)
      if ($skillText.Contains('{{AGENT_SKILLS_ROOT}}')) {
        [System.IO.File]::WriteAllText($skillFile, $skillText.Replace('{{AGENT_SKILLS_ROOT}}', $Root), (New-Object System.Text.UTF8Encoding $false))
      }
      if (-not $managed.Contains($name)) { $managed.Add($name) }
      Write-Host "  + $name"
    }
  }
  if (-not $DryRun) { Set-Managed $dir $managed.ToArray() }
  Write-Host "  $($managed.Count) skills from this library installed here"
}

if ($Reset -or $agentWant.Count -or $agentDrop.Count) {
  foreach ($dir in $AgentDirs) {
    Write-Host $dir
    $managed = [System.Collections.Generic.List[string]]::new()
    foreach ($n in (Get-Managed $dir)) { $managed.Add($n) }
    $added = 0; $updated = 0; $removed = 0

    $dropFiles = @()
    if ($Reset -or $agentDrop -contains 'all') { $dropFiles = $managed.ToArray() }
    elseif ($agentDrop.Count) { $dropFiles = @(Expand-Agents $agentDrop | ForEach-Object { Get-AgentFile $dir $_ }) }
    foreach ($file in $dropFiles) {
      if (-not $managed.Contains($file)) { continue }
      if (-not $DryRun) { Remove-Item -Force (Join-Path $dir $file) -ErrorAction SilentlyContinue; [void]$managed.Remove($file) }
      $removed++
    }

    if ($agentWant.Count) {
      if (-not $DryRun) { New-Item -ItemType Directory -Force -Path $dir | Out-Null }
      $wanted = @(Expand-Agents $agentWant)
      foreach ($row in $wanted) {
        $file = Get-AgentFile $dir $row
        $dest = Join-Path $dir $file
        if ((Test-Path $dest) -and -not $managed.Contains($file)) {
          Write-Host "  - ${file}: skipped, you already have your own agent with this name"
          continue
        }
        if (Test-Path $dest) { $updated++ } else { $added++ }
        if ($DryRun) { continue }
        Copy-Item -Force -Path (Get-AgentSource $dir $row) -Destination $dest
        if (-not $managed.Contains($file)) { $managed.Add($file) }
      }
      # core and all are whole sets: drop agents this script installed that are not in them
      if ($agentWant -contains 'all' -or $agentWant -contains 'core') {
        $current = @{}; foreach ($row in $wanted) { $current[(Get-AgentFile $dir $row)] = 1 }
        foreach ($file in @($managed.ToArray())) {
          if ($current.ContainsKey($file)) { continue }
          if (-not $DryRun) { Remove-Item -Force (Join-Path $dir $file) -ErrorAction SilentlyContinue; [void]$managed.Remove($file) }
          $removed++
        }
      }
    }
    if ($added -or $updated -or $removed) { Write-Host "  agents: +$added new, $updated refreshed, -$removed removed" }
    if (-not $DryRun -and (Test-Path $dir)) { Set-Managed $dir $managed.ToArray() }
    Write-Host "  $($managed.Count) agents installed here"
  }
}

if ($SetupRea) {
  $reaArgs = @('--yes', "rea-agents@$ReaVersion", 'setup', '--skill=false')
  Write-Host ''
  Write-Host "REA setup: npx $($reaArgs -join ' ')"
  Write-Host '  (registers the REA MCP server; the reverse-engineer-anything skill comes from this library)'
  if ($DryRun) {
    Write-Host '  dry run: not running it'
  } elseif (-not (Get-Command node -ErrorAction SilentlyContinue) -or -not (Get-Command npx -ErrorAction SilentlyContinue)) {
    Write-Warning 'REA needs Node.js 22.23.4+, 24.22.1+ or 26.12.1+ (https://nodejs.org). Install it, then run .\install.ps1 -SetupRea again.'
  } else {
    $v = [version]((node -p 'process.versions.node').Trim())
    $ok = ($v.Major -eq 22 -and $v -ge [version]'22.23.4') -or ($v.Major -eq 24 -and $v -ge [version]'24.22.1') -or ($v -ge [version]'26.12.1')
    if (-not $ok) {
      Write-Warning "REA needs Node.js 22.23.4+, 24.22.1+ or 26.12.1+; you have $v. Update Node, then run .\install.ps1 -SetupRea again."
    } else {
      & npx @reaArgs
    }
  }
  $hasSkill = $false
  foreach ($dir in $Dirs) { if ((Get-Managed $dir) -contains 'reverse-engineer-anything') { $hasSkill = $true } }
  if (-not $hasSkill -and -not $DryRun) { Write-Host '  Note: the REA skill isn''t installed. Add it with .\install.ps1 -Add reverse-engineer-anything' }
}

if ($SetupGraphify) {
  Write-Host ''
  Write-Host 'Graphify setup: installing the graphifyy package (the graphify skill runs it)'
  if ($DryRun) {
    Write-Host '  dry run: not installing'
  } elseif (Get-Command uv -ErrorAction SilentlyContinue) {
    & uv tool install --upgrade graphifyy
  } elseif (Get-Command pipx -ErrorAction SilentlyContinue) {
    & pipx install --force graphifyy
  } elseif (Get-Command py -ErrorAction SilentlyContinue) {
    & py -m pip install --user --upgrade graphifyy
  } elseif (Get-Command python -ErrorAction SilentlyContinue) {
    & python -m pip install --user --upgrade graphifyy
  } else {
    Write-Warning 'Graphify needs Python 3.10+ (https://www.python.org/downloads/). Install it, then run .\install.ps1 -SetupGraphify again.'
  }
}

Write-Host ''
Write-Host 'Done. Restart Claude Code / Codex to pick up the changes.'
Write-Host 'Every installed skill and agent adds its description to each session, so keep the active set lean.'
