----------------**TestRun**-----------------------------------

Backend logic add new Game

add new games from UI

add new Area
    update nuzlockeScreen areaChanged to show a new screen

catch pokemon
delete catched pokemon, seperate area called lost&found?
save encountered pokemon to savefiles and read them
add pokemon to area, add new encountertype to area

treat multiple floors as the same encounter - logic

fileretriever -> dictionary with settings

grab and save items
show items
add new items

add pokemon when name is entered, update pokemon after that
back button -> popup leave game, check if screen is a edit screen, message continue editing. else message save and exit or just exit
exit without saving -> save temporary, next startup ask to save with list of adjustments
update to kivyMD


---STEPS TO TAKE FOR BETA---
*******************************Logic*************************
save encountered pokemon, ~~defeated trainers~~ and ~~grabbed items~~ to savefiles and read them correctly ONLY READING LEFT, TEST WRITING
What to save to data and savefile from encounters

able to create new games
~~read trainerlist and can defeat trainers~~
~~read itemlist and can pickup items~~
How double battles?

export/import save data
add base stats, possible moves/abilities to base pokemon
update settings.py, also use settings.py for certain variables
export Trainer to showdown format
export route trainers to showdown format
export all trainers to showdown format
    optionmenu for single trainer, route, all
add / delete routes
rework saving
add game object inheritance to also allow http, keep it locally as well for crashes

removing pokemon automatically displays the first, update to show new position or 1 before??
error? if 1 or more pokemon caught same route (default on) "you have already caught pokemon x on this route"

ugly solution, change saves for different phone. export to folder/over wifi to other device?, import from folder


********************************UI*************************
implement swiping
TrainerScreen global view, picture buttons pressed -> defeat pokemon
Trainerscreen add images to buttons to change detailed view



****************************retropie**************************
Opencv to overlay on game



*************************Settings*******************************
settings button front page
    show available areas per badge - option on or off (default off)
    
    checkmark after route name if pokemon already caught that route (default on)
    duplicate clause and evolutionary clause (default on)
    shiny clause (on)
    option to change wallpaper
        check standard image(s) for copyright

*****************************extras***************************
show all available pokemon per route vanilla games
show all available trainer data vanilla games
show all available items per route vanilla games

use a movelist to validate moves used
basic logic for getting encounters from rom hack documentation
read encountertable data from rom
    import pkhex file to display caught pokemon and update caught pokemon in areas
add window to make adding games easier
figure out how to change typings/ base stats in showdown, probably create own showdown from base showdown
add map to display encounters, in correlation with number of badges, colour coding
add nickname, shiny, level etc from caught pokemon
add list of moves
check if moves are valid, option in settings
new run option, clears all data and starts with clean slate
popup message, x removed
generate catchable pokemon by reading old savestates, only for blind nuzlockes. settings option, add statistics which pokemon was caught at every route
add non-canon pokemon with name and use own sprite or ?.png
sort route list option, own choice
When selecting route, automatically center route chosen when choosing other route
When selecting areatype for encounters, use scrollview to teleport to correct position and have all pokemon visible in a large layout
export import saves, files on android will be saved to internal storage and windows will exclude /games/*
settings button on front page, settings page two tabs, general and game specific based on game chosen
read from internal storage instead of copying everything to the program at startup
Remove trainer from saveFile is trainer is defeated, saves space
1 function for searching for pokemon images

*****************************************Overhaul to KIVYMD**********************************************
start screen
    

info screen
    add next boss

trainerScreen
    tabs for global/detailed
    cogwheel for edit trainer?
    Button overlap for edit area
    MD divider between pokemon, global only

encounterScreen
    tabs for encounter types, grass, fish, surf
    static size and scroll?
    MDdivider between encounters

ItemScreen


General
    kivy swiper and/or Navigation bar for screens
    SnackBar for errors


