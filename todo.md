---STEPS TO TAKE FOR BETA---
*******************************Logic*************************
Create new games
save encountered pokemon, ~~defeated trainers~~ and ~~grabbed items~~ to savefiles and read them correctly ONLY READING LEFT, TEST WRITING

able to create new games
~~read trainerlist and can defeat trainers~~
~~read itemlist and can pickup items~~
How double battles?

update settings.py, also use settings.py for certain variables
export Trainer to showdown format
export route trainers to showdown format
export all trainers to showdown format
optionmenu for single trainer, route, all
add / delete routes


********************************Kivy*************************
implement logic



****************************retropie**************************
Opencv to overlay on game



*****************************extras***************************
show all available pokemon per route vanilla games
show all available trainer data vanilla games
show all available items per route vanilla games

settings button front page
    show available areas per badge - option on or off (default off)
    message if 2 or more pokemon caught same route (default on) "you have already caught pokemon x on this route"
    checkmark after route name if pokemon already caught that route (default on)
    duplicate clause and evolutionary clause (default on)
    remember all caught pokemon, collected items and defeated trainers (default on) each own setting
    use a movelist to validate moves used
    amount of saves kept.
    option to change wallpaper
        check image(s) for copyright
        option to change updateTime for wallpaper

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
generate catchable pokemon by reading old savestates, only for blind nuzlockes. settings option
add non-canon pokemon with name and use own sprite or ?.png
sort route list option, own choice
