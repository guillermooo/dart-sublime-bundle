param([switch]$Release)

function abort_if_failure {
	if ($LASTEXITCODE -ne 0) {
		"aborting build process"
		exit 1	
	}
}

if ($Release) {
	& dart -c $PSScriptRoot\bin\deployment_tool\bin\perform_checks.dart
	abort_if_failure
}

# Deploy files.
& dart -c $PSScriptRoot\bin\deployment_tool\bin\main.dart

# TODO(guillermooo):
# Restart Sublime Text
# & $PSScriptRoot\bin\Restart-SublimeText.ps1
