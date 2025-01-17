__TestRun__
    __NuzlockeScreen__
    __trainerscreen__
        ~~add Trainers~~
            ~~NuzlockeSpinner -> NLS -> app.get_running_app.manager.getLUValues(NLSType, param 2, param3)~~
        ~~edit trainers~~
            ~~add editdialog~~
            ~~AddTrainerBox -> 2 states add and edit ->~~ picture functions as button defeated. ~~only edit has remove trainer button~~
        add trainerpokemon to trainers -> empty boxlayout -> check before you can swipe
        edit trainerpokemon
            change box(header) to editBox 
            more info -> pokemonInfoScreen -> give trainerPokemonID to Box. Show all data 
            list of levelup moves with level -> onpress add to learnset -> learnset textfields allow all moves
    __encounter screen__
        catch encounters
        add new encounters
        edit encounters
        add new locationTypes (dark grass, surfing) per location
        more info -> pokemonInfoScreen
        dbcompLocation -> canCatch -> trigger?
    __attemptInfoScreen__
        continue graveyard
        continue arena
        continue lost and found
    __ITEMSCREEN__
        add items
        remove items
        edit items
    __basedata screen__
        Add all basedate -> new pokemon, new trainertype, new typing, alter typechart. all options in nuzlockespinner
        Basedata screen -> addNewBaseData -> items, moves etc
    __location__
        Remove locations
        update new location popup to dialog
        Getlocation -> returns dictionary {name: canCatch} -> display green/ red
        tabs for multiple floors
    __general__
        add error message popups before game has 'started'
        ~~Class NuzlockeSpinner -> textfield + dropdown already in nuzlockescreen~~
        Rethink scrollview
        exit game popup

__nice to have__
    Own eventDispatcher -> can integrate APi calls to screen software
    optimize lookup -> more characters added, filter memory instead of new query
    when adding new games -> "selects" game, only sets text
    How handle editing rights, screen capture -> mistake -> manual edit -> at same time?
    __screenCapture__
        Script that records gameplay -> saves it to folder
        Convert recorded gameplay to database records -> ai?
        Keep track of changes -> replay battles using pokemonShowdown?
        redis kafka for database
        autosave game every x minutes -> needed?
    __general__
        __database__
            check if db file present if not popup -> create new db -> no databse detected -> first time (tutorial)
            On startup check if database is up to date with python objects -> upgrade if not -> popup
            database phone storage ipv in data
            DB how real time update without polling, if needed?
            Database location outside phone
        __settings__ 
            settings per game / global settings
            settings -> read from outside
            duplicate clause and evolutionary clause (default on)
            shiny clause (on)
            option to change wallpaper
                check standard image(s) for copyright
            check if moves are valid, option in settings
            sort route list option, own choice
        __pokemonData__
            add trainertype data
            webscrape all pokemon info gen 1-10 -> only update if different -> add stats
            Other application that reads txt or excel and converts it into json which inserts it into database -> use existing data to smartly do it (potion, known pokemon) 
        __layout__
            every screen has its own spinner for area -> one central spinner
            change nuzlockespinner so dropdown is entire screen 
            navigationbar different screens
            When selecting route, automatically center route chosen when choosing other route  
        Lost&Found
        back button -> popup leave game, check if screen is a edit screen, message continue editing. else message save and exit or just exit
        kivy bubbles
        create file that displays all changes made, in case saving corrupts or undo's
        export/import save data -> game data
        export showdown
    __game__
        New game -> idparentgame not null -> copy trainers,items,location,pokemon inidivdual checkmarks. insert select where x=x
        Option remove / edit game
    __trainerscreen__
        add all database fields -> trainer dialogs -> boxes
        How double battles?
        pokeballs / sprites to quickly show how many pokemon
        dialog -> add nuzlockespinner -> images (popup)
    __atemptInfoScreen__
        show amount of encounters catchable
        show next boss trainer 
        click on pokemon -> pokemonInfo -> display where caught and where died if applicable
    __pokemonInfoScreen__
        pokemonInfo (standard readonly)
            Types -> Base, trainer, location, player
            name, image, dexno, parentPokemon (base), level(not base),  learnedmoves (not Base/ add/remove), levelupmoves (add/remove), typing (add/remove), origin (trainer, location, player), 
            helditem (not base), abilities (active ability bold/green whatever), gender (trainer, player), defeated (trainer), nickname (player), encounterRate(encounter), tms hms (Base, encounter, player)    
        edit pokemon -> editbutton
        add non-canon pokemon with name and use own sprite or ?.png
    __Statistics screen__
        Kills per pokemon
        crits per pokemon
        items used / gathered
        Crits dealt
        Crits taken
        Graph when pokemon died

__Finishingtouches__(2026)
    read encountertable data from rom -> check if it is possible
    figure out how to change typings/ base stats in showdown, probably create own showdown from base showdown -> custom calculator
    add map to display encounters, in correlation with number of badges, colour coding
    generate catchable pokemon by reading old savestates, only for blind nuzlockes. settings option, add statistics which pokemon was caught at every route
