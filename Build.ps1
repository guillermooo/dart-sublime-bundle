param([switch]$Release)

function abort_if_failure {
	if ($LASTEXITCODE -ne 0) {
		"aborting build process ($(split-path $MyInvocation.ScriptName -leaf))"
		exit 1	
	}
}

if ($Release) {
	& pub global run grinder release
	abort_if_failure
}

push-location "$PSScriptRoot\bin\deployment_tool\"
	# Deploy files.
	& pub global run grinder deploy
pop-location
abort_if_failure

# TODO(guillermooo):
# Restart Sublime Text
# & $PSScriptRoot\bin\Restart-SublimeText.ps1
