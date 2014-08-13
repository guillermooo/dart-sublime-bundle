# python builder.py
case `uname` in
  'Linux')
    # cp -f ../dist/Dart.sublime-package ~/.config/sublime-text-3/Installed\ Packages
    cp -rf * ~/.config/sublime-text-3/Packages/Dart
    ;;
  'Darwin')
    # cp -f ../dist/Dart.sublime-package ~/Library/Application\ Support/Sublime\ Text\ 3/Installed\ Packages
    cp -rf * ~/Library/Application\ Support/Sublime\ Text\ 3/Packages/Dart
    ;;
esac

killall sublime_text "Sublime Text" 2> /dev/null
sleep 0.2
subl
