# Changelog
## Framework
### Gui
- Added Buttons with animations
- Added Sliders with animations
- Added Line Edits with animations
- Added Progress Bars
### Window
- Added fullscreen
- Added resizing with aspect ratio
### BaseFunctions
- Added debug output, that can be changed through the environment variable LOG_LEVEL. It can be set on "info", "debug" and "complete".
### Render
- Added text rendering
## Level
- Added level opening and saving
- Added data opening and saving
- Added region opening and saving
- Added block rendering
- Added grid rendering
- Added animation for level opening
- Added Camera delay in level
## Levels
- Added some test levels
- Added negative coordinates in Level1
## Key Bindings Menu
- Added a gui for changing the key bindings in the settings
## Level Selection
- Added colored Graphics, that can come in and out of the screen.
- Added a scroll menu to select and open levels
- Added an animated level preview
- Added key controls
- Added delete level and create level buttons in the level selection for the editor
- Added delete level and create level menus
## Menus
- Added the main menu's gui elements
- Added the level selection's gui elements
- Added the settings's gui elements
- Added the key bindings's gui elements
- Added the video setting's gui elements
- Added a reset window size button
- Added a level quit menu
- Added Level Options
- Added Fullscreen option
## Resources
- Added json files that are defining the blocks
- Added freesansbold.ttf
- Added block textures
- Added gui sounds
- Added animation system
## Player
- Added a system that doesn't allow the player to go through walls
- Added the ability to die
- Added jumping
- Added falling with fall multiplier
- Added menu to access settings while playing and for quitting
- Added go in / out animation for the player
- Added lifes
- Can now see important changed block attributes
- Added chat
- Added animated block overlay
- Added block event system
- Added climbing
## Editor
- Added a grid
- Added go in / out animation for the grid
- Added level create / delete buttons
- Added menu to access settings while editing and for quitting
- Added block setting with automatic level resizing
- Added block selection
- Added block attributes
- Added spawn setting
- Added marking of blocks that are solid or cause the player to die
- Added jump walk fall and description value changes in level options
- Added save asking when quitting
- Added level renaming
- The level border is now shown
- Added selecting and region selecting
- Added filling, cloning and removingf of selection
- Added movement using mouse
- Added name of block in block selection
## Main
- Added block loading
- Added a configuration file
- Added a debug screen
- Added a screen shots function
- Added a menu handling system
- Added an exit animation
- Added config saving when exiting
- Added pygame_sdl2 support
- Added Loading screen at startup
