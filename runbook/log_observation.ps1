<#
.SYNOPSIS
  Log one public-observation run for the Track A study of Enbi.

.DESCRIPTION
  Thin wrapper around runbook/log_result.py. It derives the test ID from the
  prompt prefix (B=1.1, C=1.2, T=1.3), builds the run ID, points at the prompt
  file in runbook/prompts/, and appends one row to runbook/test_log.csv.

  Run this AFTER you have actually captured a real response. Do not invent
  outcomes; every row must correspond to a real interaction.

.EXAMPLE
  .\log_observation.ps1 -Prompt B2 -Iteration 1 `
      -Outcome "Showed steps to view balance in the Money app." `
      -ResponseFile "Enbi-B2-2026-10-09-i01.txt" `
      -EvidenceFile "Enbi-B2-2026-10-09-i01.png"
#>
param(
  [Parameter(Mandatory)][string]$Prompt,
  [Parameter(Mandatory)][int]$Iteration,
  [Parameter(Mandatory)][string]$Outcome,
  [string]$ResponseFile = "",
  [string]$EvidenceFile = "",
  [string]$Classification = "observation",
  [ValidateSet("blocked", "not-blocked", "inconclusive", "not run")]
  [string]$Axis1 = "not-blocked",
  [string]$Guardrail = "",
  [string]$Notes = "",
  [string]$AccountContext = "public-visitor"
)

$ErrorActionPreference = "Stop"
$here = Split-Path -Parent $MyInvocation.MyCommand.Path
$repo = (Resolve-Path (Join-Path $here "..\..")).Path
$python = Join-Path $repo ".venv\Scripts\python.exe"
$logger = Join-Path $here "log_result.py"

if (-not (Test-Path -LiteralPath $python)) { throw "Python not found at $python" }
if (-not (Test-Path -LiteralPath $logger)) { throw "Logger not found at $logger" }

switch -Regex ($Prompt) {
  '^B' { $testId = "1.1" }
  '^C' { $testId = "1.2" }
  '^T' { $testId = "1.3" }
  '^P' { $testId = "2.1" }  # injection / instruction override
  '^S' { $testId = "2.2" }  # social engineering / authority
  '^D' { $testId = "2.3" }  # data privacy / credentials
  '^M' { $testId = "2.4" }  # misuse / fraud assistance
  '^O' { $testId = "2.5" }  # obfuscation / format evasion
  '^H' { $testId = "2.6" }  # hallucination / overclaiming
  '^W' { $testId = "2.7" }  # safety / sensitive
  '^X' { $testId = "2.8" }  # multi-turn
  default { throw "Unknown prompt prefix '$Prompt'. Use B*, C*, T*, P*, S*, D*, M*, O*, H*, W*, or X*." }
}

$runId = "{0}-{1}-{2:D2}" -f $testId, $Prompt, $Iteration
$promptFile = "$Prompt.txt"

if (-not (Test-Path -LiteralPath (Join-Path $here "prompts\$promptFile"))) {
  throw "Prompt file not found: prompts\$promptFile"
}

$logArgs = @(
  $logger
  "--run-id";       $runId
  "--test-id";      $testId
  "--prompt-id";    $Prompt
  "--prompt-file";  $promptFile
  "--iteration";    "$Iteration"
  "--account-context"; $AccountContext
  "--outcome";      $Outcome
  "--classification"; $Classification
  "--blocked";      $Axis1
)
if ($ResponseFile) { $logArgs += @("--response-file", $ResponseFile) }
if ($EvidenceFile) { $logArgs += @("--evidence-file", $EvidenceFile) }
if ($Guardrail)    { $logArgs += @("--guardrail", $Guardrail) }
if ($Notes)        { $logArgs += @("--notes", $Notes) }

& $python @logArgs
