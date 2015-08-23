<#
    .SYNOPSIS
    Publishes the final files that users will receive via Package Control.

    .DESCRIPTION
    Publishes the final files that users will receive via Package Control.
#>
[CmdletBinding()]
param(
    [parameter( Mandatory=$true, Position=0)]
    [String]
    $Tag
    )

$script:scriptDir = split-path $myinvocation.mycommand.path -parent

push-location "$script:scriptDir\.."
    & git checkout master
    & git tag $Tag
    & git push bigdeal master --tags

    remove-item -force -recurse 'dist' -erroraction silentlycontinue
    new-item -force -itemtype directory 'dist'

    push-location 'dist'
        & git clone "https://github.com/guillermooo/dart-sublime-bundle" "dart-sublime-bundle-releases-tmp"
        & git clone "https://github.com/guillermooo/dart-sublime-bundle-releases" "dart-sublime-bundle-releases"

        push-location "dart-sublime-bundle-releases-tmp"
            & git checkout master
            remove-item -recurse -force ".git" -erroraction silentlycontinue
            remove-item -recurse -force "repository" -erroraction silentlycontinue
            remove-item -recurse -force "scripts" -erroraction silentlycontinue
            remove-item -recurse -force "bin" -erroraction silentlycontinue
            remove-item -recurse -force "tests" -erroraction silentlycontinue
            remove-item -recurse -force "dist" -erroraction silentlycontinue
            remove-item "travis.sh" -erroraction silentlycontinue
            remove-item "test_runner.py" -erroraction silentlycontinue
            remove-item "manifest.json" -erroraction silentlycontinue
            remove-item "*.sublime-workspace" -erroraction silentlycontinue
            remove-item "*.sublime-project" -erroraction silentlycontinue
            remove-item "*.YAML-*" -erroraction silentlycontinue
            remove-item "appveyor.yml" -erroraction silentlycontinue
            remove-item ".travis.yml" -erroraction silentlycontinue
            remove-item ".gitignore" -erroraction silentlycontinue
            remove-item ".gitattributes" -erroraction silentlycontinue

            copy-item -recurse -force * "..\dart-sublime-bundle-releases"
        pop-location

        push-location "dart-sublime-bundle-releases"
            & git checkout master
            & git add .
            & git commit -m "release: $Tag"
            & git tag "$Tag"
            & git push origin master --tags
        pop-location
    pop-location
pop-location
