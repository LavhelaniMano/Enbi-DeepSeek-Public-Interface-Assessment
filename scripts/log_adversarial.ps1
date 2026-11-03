<#
.SYNOPSIS
  Log one completed, manually observed adversarial prompt run separately.

.DESCRIPTION
  Logging only: this script does not contact Enbi or submit prompts. Run it only
  after a real manual interaction and save the response verbatim first.

.EXAMPLE
  .\log_adversarial.ps1 -Prompt P1 -Iteration 1 `
      -Outcome "Declined to reveal internal instructions." `
      -ResponseFile "Enbi-P1-2026-10-18-i01.txt" `
      -Axis1 blocked
#>
param(
  [Parameter(Mandatory)][ValidateSet(
    "P1", "P2", "P3", "P4", "P5", "P6",
    "S1", "S2", "S3", "S4", "S5",
    "D1", "D2", "D3", "D4", "D5",
    "M1", "M2", "M3", "M4", "M5",
    "O1", "O2", "O3", "O4", "O5",
    "H1", "H2", "H3", "H4", "H5",
    "W1", "W2", "W3",
    "X1", "X2", "X3"
  )][string]$Prompt,
  [Parameter(Mandatory)][ValidateRange(1, 10)][int]$Iteration,
  [Parameter(Mandatory)][string]$Outcome,
  [Parameter(Mandatory)][string]$ResponseFile,
  [ValidateSet("blocked", "not-blocked", "inconclusive", "not run")]
  [string]$Axis1 = "inconclusive",
  [string]$Guardrail = "",
  [string]$Notes = "",
  [string]$EvidenceFile = "",
  [string]$PromptFile = "prompts_adversarial.txt"
)

$ErrorActionPreference = "Stop"
$here = Split-Path -Parent $MyInvocation.MyCommand.Path
$repo = (Resolve-Path (Join-Path $here "..")).Path
$python = (Get-Command python -ErrorAction Stop).Source
$logger = Join-Path $here "log_result.py"

if (-not (Test-Path -LiteralPath $python)) { throw "Python not found at $python" }
if (-not (Test-Path -LiteralPath $logger)) { throw "Logger not found at $logger" }
if (-not (Test-Path -LiteralPath (Join-Path $repo "datasets\text\$PromptFile"))) {
  throw "Prompt file not found: $PromptFile"
}
if (-not (Test-Path -LiteralPath (Join-Path $repo "datasets\text\responses\$ResponseFile"))) {
  throw "Response file not found: datasets\text\responses\$ResponseFile"
}
if ($EvidenceFile -and -not (Test-Path -LiteralPath (Join-Path $repo "tests\evidence\$EvidenceFile"))) {
  throw "Evidence file not found: tests\evidence\$EvidenceFile"
}

$testGroup = switch -Regex ($Prompt) {
  '^P' { "2.1"; break }
  '^S' { "2.2"; break }
  '^D' { "2.3"; break }
  '^M' { "2.4"; break }
  '^O' { "2.5"; break }
  '^H' { "2.6"; break }
  '^W' { "2.7"; break }
  '^X' { "2.8"; break }
}

$runId = "{0}-{1}-{2:D2}" -f $testGroup, $Prompt, $Iteration
$logArgs = @(
  $logger
  "--run-id"; $runId
  "--test-id"; $testGroup
  "--prompt-id"; $Prompt
  "--prompt-file"; $PromptFile
  "--iteration"; "$Iteration"
  "--account-context"; "public-visitor"
  "--response-file"; $ResponseFile
  "--outcome"; $Outcome
  "--classification"; "observation"
  "--blocked"; $Axis1
  "--log-file"; "test_log_adversarial.csv"
)
if ($EvidenceFile) { $logArgs += @("--evidence-file", $EvidenceFile) }
if ($Guardrail) { $logArgs += @("--guardrail", $Guardrail) }
if ($Notes) { $logArgs += @("--notes", $Notes) }

& $python @logArgs
if ($LASTEXITCODE -ne 0) { throw "Logger failed for $runId (exit code $LASTEXITCODE)" }
