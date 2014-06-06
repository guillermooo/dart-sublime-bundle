# Dart – Sublime Text Package


## Overview

Basic Dart support for Sublime Text 3. These are the current features at a
glance:

* Syntax highlighting
* Comment/uncomment lines and text blocks.
* Snippets
* JavaScript translation through `dart2js` using ST3's build system
* Pub support to manage Dart packages
* Code linting using `dartanalyzer`
* Basic symbol navigation using ST3's built-in symbol indexing
* Works on **OS X**, **Linux** and **Windows**

Most features are only active in files with a `.dart` extension.

Check out or [introductory video][6] for a short tutorial on using this pacakge.


## Getting Started

Things to do before you can take full advantage of this package.

1. [Download and install the Dart SDK][sdk]
2. Make sure the SDK's `bin` directory is on your PATH.


## Installation

You can install the Dart package in two ways.

### Using Package Control

Installing through the [Package Control][1] plugin is the easiest way:

- Open the command palette (<kbd>Ctrl+Shift+P</kbd> or <kbd>⌘+Shift+P</kbd>)
- Type 'install'
- Select **Package Control: Install Package** from the list
- Type 'Dart'
- Select Dart package from the list

You may need to restart ST3 before you can start using all the features in the
package.

### Manually

- Clone this repository
- Copy its content to a new *Dart* directory inside *Packages*

To quicklu open your *Packages* folder, select **Preferences → Browse Packages**
from the ST3 menu or use the command palette.

---

For an optimal experience:

- Add Dart's SDK *bin* directory to your path
- Add the `dartsdk_path` variable to your ST3 user settings

```json
    {
      "dartsdk_path" : "/Users/foo/dart-sdk"
    }
```

---

Looking for an IDE experience? Try [Dart Editor][2], the
[Dart plugin for Eclipse][3], or the [Dart plugin for IntelliJ/WebStorm][4].

## Using the Build System

<kbd>Ctrl+B</kbd> or <kbd>⌘+B</kbd> will run the `dart2js` compiler on
the active file.

Browse other Dart commands via ST3's command pallete: `Run`, `Analyzer`,
`pub install`, `pub update`...


## Using the Linter

### Getting Started

The `dartanalyzer` is deactivated by default. To use this feature you must
set the `dartlint_active` setting to `true`.

You may need to make this change in `Packages/User/Preferences.sublime-settings`
or in a `Dart.sublime-settings` file within your `Packages/User` folder.

```json
{
  "dartlint_active" : true,
}
```

### Configuration

The linter will run when Dart scripts are loaded or saved. You can change this
behavior through the `dartlint_on_load` and `dartlint_on_save` settings.


### Customizing Highlight Colors

Use the following settings:

- `dartlint_underline_color_error`,
- `dartlint_underline_color_warning`
- `dartlint_underline_color_info`

To customize gutter icons:

`dartlint_gutter_icon_error`
`dartlint_gutter_icon_warning`
`dartlint_gutter_icon_info`

Paths to icons must start at the *Packages* directory.

#### Example

```json
{
  `"dartlint_gutter_icon_error" : "Packages/Users/Icons/error.png"`
}
```

### Linter Popup Configuration

Use `dartlint_show_popup_level` setting to control when the pop up should
show. Valid values are:

- `ERROR`
- `WARNING`
- `INFO`


## DEVELOPMENT

Please ensure that all .tmPreferences, .tmLanguage, .tmSnippets, etc. files
stay in sync with the related [Dart TextMate repository][5].


## LICENSE

    Copyright 2012, the Dart project authors. All rights reserved.
    Redistribution and use in source and binary forms, with or without
    modification, are permitted provided that the following conditions are
    met:
        * Redistributions of source code must retain the above copyright
          notice, this list of conditions and the following disclaimer.
        * Redistributions in binary form must reproduce the above
          copyright notice, this list of conditions and the following
          disclaimer in the documentation and/or other materials provided
          with the distribution.
        * Neither the name of Google Inc. nor the names of its
          contributors may be used to endorse or promote products derived
          from this software without specific prior written permission.
    THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
    "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
    LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
    A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
    OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
    SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
    LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
    DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
    THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
    (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
    OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

[1]: http://wbond.net/sublime_packages/package_control
[2]: http://www.dartlang.org/editor
[3]: http://news.dartlang.org/2012/08/dart-plugin-for-eclipse-is-ready-for.html
[4]: http://plugins.intellij.net/plugin/?id=6351
[5]: http://github.com/dart-lang/dart-textmate-bundle
[6]: http://news.dartlang.org/2013/02/using-dart-with-sublime-text.html
[sdk]: http://www.dartlang.org/tools/sdk/
