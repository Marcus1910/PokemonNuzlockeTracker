***************************************TestRun*******************************
!switch to db file
webscrape all pokemon info gen 1-10 -> only update if different -> add stats
    check if db file present if not popup -> create new db
    On startup check if database is up to date with python objects -> upgrade if not -> popup
    convert all read json to database entries -> game filepath encounters
    Game needs filepaths, movesets, abilities, pokemonchanges, encounters -> json format
    other application that reads txt or excel and converts it into json -> use existing data to smartly do it (potion, known pokemon)
    New game -> idparentgame not null -> copy trainers,items,location,pokemon inidivdual checkmarks. insert select where x=x
    database phone storage ipv in data
    encountertypes -> static, walking, gift, surfing
    

Catch wild pokemon
grab items
display caught pokemon

get all pokemoninfo gen 1 - 9
save in different folders
Start pokemon changes documentation

add error message popups before game has 'started'

GAME
    Overhaul backend object to include easier way to add observers, quite a cluster now
        base object with addobserver?    
    give game gen attribute to read
    AREA
        Treat multiple floors as singular object or new Area object with multiple areas
            db - parentArea
    TRAINERS
        How double battles
    ITEMS
        grab items, add items, dropdown for items
    POKEMON
        get possible moves from db -> input with automatic dropdown
        get possible abilities from db -> input with automatic dropdown

KIVY
    change when screen are added to manager
    edit area
    remove area's
    change area spinner so dropdown is entire screen
    update new area popup to dialog
    change removed items location to lost&found
    back button -> popup leave game, check if screen is a edit screen, message continue editing. else message save and exit or just exit
    exit without saving -> save temporary, next startup ask to save with list of adjustments
    snackbar errors / info
    tabs for multiple floors
    badges to display if can catch pokemon, color coded background?
    navigationbar different screens
    MAINSCREEN
        edit game
        remove game
        set direction to Settings screen
    ATTEMPTINFOSCREEN
        read arena and retirement and place images
        tabs for info, arena, retirement and lost & found (sub tabs trainerpokemon encounterpokemon and items)
        show amount of encounters catchable
        show badges
        show next boss trainer  
    TRAINERSCREEN
        ~~Add observers for trainer detail screen~~
        ~~edit trainerPOkemon detailed view to show possible abilities and moves, dummy data~~
        add bossTrainer to edit trainer box
        ~~popup delete trainer~~
        kivy bubble move accuracy and power + secondary effect
        kivy bubble ability information
        adjust size of detailedpokemonbox so it is visible, self.trainerbox.height = x if not x
    ENCOUNTERSCREEN
        catch pokemon -> create playerpokemon -> arena
        release pokemon -> retirement
        remove pokemon from area
        give headers standard size and use expandable box
        edit encounter pokemon
        see possible moves the pokemon has as well as abilities
        add new areatype
    ITEMSCREEN
        grab items
        remove item
        edit item
        add new items
        show more info about item, read from json
    POKEMONINFOSCREEN
        search for specific pokemon
        display everything from pokemon
        where it is caught
        which trainers have it so far
        levelup moves
        tm/hm
        basestats
        evolution line + method
    SETTINGSCREEN
        edit trainer header and content height
        edit trainerpokemon header and content height
        edit pokemonEncounter header and content height
        edit item header and content height
        x and y sensitivity for scrolling
        ~~amount of mb gameObject is~~
        ~~amount of mb app consumes~~
        Trust game data, remove all inputs for pokemon abilities
    Statistics screen
        Kills per pokemon
        crits per pokemon
        items used / gathered
        Crits dealt
        Crits taken
        Graph when pokemon died


---STEPS TO TAKE FOR BETA---
*******************************Further development*************************
look at threading to gather mutiple widgets in a for loop for optimization
create file that displays all changes made, in case saving corrupts or undo's
export/import save data
add base stats graph, possible moves/abilities to base pokemon
export Trainer to showdown format
export route trainers to showdown format
export all trainers to showdown format
    optionmenu for single trainer, route, all
add / delete routes
add game object inheritance to also allow http, keep it locally as well for crashes
error? if 1 or more pokemon caught same route (default on) "you have already caught pokemon x on this route"
ugly solution, change saves for different phone. export to folder/over wifi to other device?, import from folder


****************************retropie**************************
Opencv to overlay on game
create sdm image


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
read encountertable data from rom -> check if it is possible
    import pkhex file to display caught pokemon and update caught pokemon in areas
add window to make adding games easier
figure out how to change typings/ base stats in showdown, probably create own showdown from base showdown
add map to display encounters, in correlation with number of badges, colour coding
add nickname, shiny, level etc from caught pokemon
add list of moves
check if moves are valid, option in settings
generate catchable pokemon by reading old savestates, only for blind nuzlockes. settings option, add statistics which pokemon was caught at every route
add non-canon pokemon with name and use own sprite or ?.png
sort route list option, own choice
When selecting route, automatically center route chosen when choosing other route
When selecting areatype for encounters, use scrollview to teleport to correct position and have all pokemon visible in a large layout
export import saves, files on android will be saved to internal storage and windows will exclude /games/*
settings button on front page, settings page two tabs, general and game specific based on game chosen
read from internal storage instead of copying everything to the program at startup
1 function for searching for pokemon images

trainerscreen add quick view to headerbutton, sprites of pokemon / pokeball empty is less than 6
overhaul db performance? - 2 versions for comparison
class data importer -> import data from files
bubble arena graveyard pokemon
uitvogelen hoe met screen capture software - > redis kafka etc
