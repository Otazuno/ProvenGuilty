# You can place the script of your game in this file.

# Declare images below this line, using the image statement.
# eg. image eileen happy = "eileen_happy.png"
image blackness = "images/locations/blackness.png"
image court_archives = "images/locations/court_archives.png"
image restaurant = "images/locations/restaurant.png"
image mall = "images/locations/mall.jpg"
image thinking = "images/locations/thinking.png"
image ctc_animation = Animation("images/UI/ctc01.png", 0.075, "images/UI/ctc02.png", 0.075, "images/UI/ctc03.png", 0.1, "images/UI/ctc02.png", 0.075, xpos=0.94, ypos=0.95, xanchor=1.0, yanchor=1.0)
image abacus_profile = "images/characters/croak/profile.png"
image present = "images/UI/present.png"
image evaloria = "images/characters/evaloria/base.png"

#define present = CropMove(0.9, "custom", startcrop=(0.9, 0.0, 0.1, 0.1), startpos=(0.9, 0.0), endcrop=(0.0, 0.0, 1.0, 1.0), endpos=(0.0, 0.0), topnew=True, old_widget=None, new_widget=None)
#define take = CropMove(0.9, "custom", startcrop=(0.0, 0.0, 1.0, 1.0), startpos=(0.0, 0.0), endcrop=(0.9, 0.0, 0.1, 0.1), endpos=(0.9, 0.0), topnew=False, old_widget=None, new_widget=None)

define present = CropMove(0.125, "custom", startcrop=(0.9, 0.0, 0.1, 0.1), startpos=(0.9, 0.0), endcrop=(0.58, 0.0, 0.42, 0.55), endpos=(0.58, 0.0), topnew=True, old_widget=None, new_widget=None)
define take = CropMove(0.125, "custom", startcrop=(0.58, 0.0, 0.42, 0.55), startpos=(0.58, 0.0), endcrop=(0.9, 0.0, 0.1, 0.1), endpos=(0.9, 0.0), topnew=False, old_widget=None, new_widget=None)


# Declare sounds
init python:
    #config.default_fullscreen = True
    config.window_icon = "images/icons/icon.png"
    renpy.music.register_channel("sfx", "sfx", False)
    renpy.music.register_channel("test_six", "sfx", False)
    renpy.music.register_channel("test_seven", "sfx", False)
    renpy.music.register_channel("test_eight", "sfx", False)
    
    # This is set to the name of the character that is speaking, or
    # None if no character is currently speaking.
    speaking = None
  
    # This returns speaking if the character is speaking, and done if the
    # character is not.
    def while_speaking(name, speak_d, done_d, st, at):
        if speaking == name:
            return speak_d, .1
        else:
            return done_d, None
  
    # Curried form of the above.
    curried_while_speaking = renpy.curry(while_speaking)
  
    # Displays speaking when the named character is speaking, and done otherwise.
    def WhileSpeaking(name, speaking_d, done_d=Null()):
        return DynamicDisplayable(curried_while_speaking(name, speaking_d, done_d))
  
    # This callback maintains the speaking variable.
    def speaker_callback(name, event, **kwargs):
        global speaking  
        
        if event == "show":
            speaking = name
            
            if (speaking == 'male'):
                renpy.music.play("sfx/male_talking.ogg", channel="sound", loop=True)
            elif (speaking == 'croak'):
                renpy.music.play("sfx/male_talking.ogg", channel="sound", loop=True)
            elif (speaking == 'godwin'):
                renpy.music.play("sfx/male_talking.ogg", channel="sound", loop=True)
            elif (speaking == 'media'):
                renpy.music.set_volume(0.25, delay=0, channel="sound")
                renpy.music.play("sfx/sfx-blipfemale.ogg", channel="sound", loop=True)
            elif (speaking == 'typewriter'):
                renpy.music.play("sfx/sfx-typewriter.ogg", channel="sound", loop=True)
            print speaking
        elif event == "slow_done":
            renpy.music.stop(channel="sound")
            speaking = None
        elif event == "end":
            renpy.music.stop(channel="sound")
            speaking = None
  
    # Curried form of the same.
    speaker = renpy.curry(speaker_callback)
    
    import math

    class Shaker(object):
        
        anchors = {
            'top' : 0.0,
            'center' : 0.5,
            'bottom' : 1.0,
            'left' : 0.0,
            'right' : 1.0,
            }
        
        def __init__(self, start, child, dist):
            if start is None:
                start = child.get_placement()
            #
            self.start = [ self.anchors.get(i, i) for i in start ]  # central position
            self.dist = dist    # maximum distance, in pixels, from the starting point
            self.child = child
                
        def __call__(self, t, sizes):
            # Float to integer... turns floating point numbers to
            # integers.                
            def fti(x, r):
                if x is None:
                    x = 0
                if isinstance(x, float):
                    return int(x * r)
                else:
                    return x

            xpos, ypos, xanchor, yanchor = [ fti(a, b) for a, b in zip(self.start, sizes) ]

            xpos = xpos - xanchor
            ypos = ypos - yanchor
                
            nx = xpos + (1.0-t) * self.dist * (renpy.random.random()*2-1)
            ny = ypos + (1.0-t) * self.dist * (renpy.random.random()*2-1)

            return (int(nx), int(ny), 0, 0)
        
    def _Shake(start, time, child=None, dist=100.0, **properties):

        move = Shaker(start, child, dist=dist)
        
        return renpy.display.layout.Motion(move,
                        time,
                        child,
                        add_sizes=True,
                        **properties)

    Shake = renpy.curry(_Shake)
        
init:
    $ sshake = Shake((0, 0, 0, 0), 1.0, dist=15)

# Declare characters used by this game.            
define croak = Character('CROAK', 
    color = "#ffffff",
    size = 23,
    bold = 0,
    line_leading = 0,
    kerning = 0,
    first_indent = -2,
    callback = speaker("croak"),
    show_who_window_style = "say_who_window_red",
    show_two_window = True,
    ctc = "ctc_animation",
    ctc_position = "fixed")

image silent croak base = LiveComposite(
    (600, 534),
    (0, 0), "images/characters/croak/base.png",
    (0, 0), "croak base blinking"
    )

image croak base = LiveComposite(
    (600, 534),
    (0, 0), "images/characters/croak/base.png",
    (0, 0), "croak base blinking",
    (0, 0), WhileSpeaking("croak", "croak base talking")
    )

image croak base blinking:
    "images/characters/croak/base.png"
    choice:
        4.5
    choice:
        3.5
    choice:
        1.5
    # This randomizes the time between blinking.
    "images/characters/croak/base_blink_1.png"
    .1
    "images/characters/croak/base_blink_2.png"
    .2
    "images/characters/croak/base_blink_1.png"
    .1
    repeat

image croak base talking:
    choice:
        "images/characters/croak/base.png"
        .15
        "images/characters/croak/base_talk_1.png.png"
        .1
        "images/characters/croak/base_talk_2.png"
        .2
        "images/characters/croak/base_talk_1.png.png"
        .1
        "images/characters/croak/base.png"
        .15
        "images/characters/croak/base_talk_1.png.png"
        .1
        "images/characters/croak/base_talk_2.png"
        .2
        "images/characters/croak/base_talk_1.png.png"
        .1
        "images/characters/croak/base_talk_2.png"
        .2
        "images/characters/croak/base_talk_1.png.png"
        .1
    repeat

define godwin = Character('GODWIN', 
    color = "#ffffff",
    size = 23,
    bold = 0,
    line_leading = 0,
    kerning = 0,
    first_indent = -3,
    callback = speaker("godwin"),
    show_who_window_style = "say_who_window_blue",
    show_two_window = True,
    ctc = "ctc_animation",
    ctc_position = "fixed")

image silent godwin base = LiveComposite(
    (600, 554), #534
    (0, 0), "images/characters/godwin/base.png",
    (0, 0), "godwin base blinking"
    )

image godwin base = LiveComposite(
    (600, 554),
    (0, 0), "images/characters/godwin/base.png",
    (0, 0), "godwin base blinking",
    (0, 0), WhileSpeaking("godwin", "godwin base talking")
    )

image godwin base blinking:
    "images/characters/godwin/base.png"
    choice:
        4.5
    choice:
        3.5
    choice:
        1.5
    # This randomizes the time between blinking.
    "images/characters/godwin/base_blink_1.png"
    .1
    "images/characters/godwin/base_blink_2.png"
    .2
    "images/characters/godwin/base_blink_1.png"
    .1
    repeat

image godwin base talking:
    choice:
        "images/characters/godwin/base.png"
        .15
        "images/characters/godwin/base_talk_1.png"
        .1
        "images/characters/godwin/base_talk_2.png"
        .2
        "images/characters/godwin/base_talk_1.png"
        .1
        "images/characters/godwin/base.png"
        .15
        "images/characters/godwin/base_talk_1.png"
        .1
        "images/characters/godwin/base_talk_2.png"
        .2
        "images/characters/godwin/base_talk_1.png"
        .1
        "images/characters/godwin/base_talk_2.png"
        .2
        "images/characters/godwin/base_talk_1.png"
        .1
    repeat

define news = Character('NEWS',
    color = "#ffffff",
    size = 23,
    bold = 0,
    line_leading = 0,
    kerning = 0,
    first_indent = 12,
    callback = speaker("media"),
    show_who_window_style = "say_who_window_green",
    show_two_window = True,
    ctc = "ctc_animation",
    ctc_position = "fixed")

define dutch = Character('DUTCH',
    color = "#ffffff",
    size = 23,
    bold = 0,
    line_leading = 0,
    kerning = 0,
    first_indent = 4,
    callback = speaker("male"),
    show_who_window_style = "say_who_window_purple",
    show_two_window = True,
    ctc = "ctc_animation",
    ctc_position = "fixed")

define sahwit = Character('SAHWIT',
    color = "#ffffff",
    size = 23,
    bold = 0,
    line_leading = 0,
    kerning = 0,
    first_indent = 4,
    callback = speaker("male"),
    show_who_window_style = "say_who_window_green",
    show_two_window = True,
    ctc = "ctc_animation",
    ctc_position = "fixed")

define gency = Character('GENCY',
    color = "#ffffff",
    size = 23,
    bold = 0,
    line_leading = 0,
    kerning = 0,
    first_indent = 4,
    callback = speaker("male"),
    show_who_window_style = "say_who_window_brown",
    show_two_window = True,
    ctc = "ctc_animation",
    ctc_position = "fixed")

define juri = Character('JUDGE',
    color = "#ffffff",
    size = 23,
    bold = 0,
    line_leading = 0,
    kerning = 0,
    first_indent = 4,
    callback = speaker("male"),
    show_who_window_style = "say_who_window_black",
    show_two_window = True,
    ctc = "ctc_animation",
    ctc_position = "fixed")

define typewriter = Character('',
    color = "#54fe54",
    size = 23,
    bold = 0,
    line_leading = 0,
    kerning = 0,
    first_indent = 4,
    callback = speaker("typewriter"),
    ctc = "ctc_animation",
    ctc_position = "fixed")
    

# The game starts here.
label start:
    
    scene blackness
    typewriter "{cps=10}Molto Buona{w=0.25} \nSaturday{cps=5},{/cps} June 12{w=0.25} \n1:35pm{/cps}{w=0.25}"
    $ renpy.music.play("sfx/sfx-pichoop.ogg", channel="sfx", loop=False)
    
    #scene court_archives with Dissolve(2.0)
    scene restaurant with Dissolve(2.0)
    #scene mall with Dissolve(2.0)
    pause(1.0)
    show godwin base with Dissolve(0.75)
    #show croak base with Dissolve(0.75)
    $ renpy.music.play("sfx/sfx-realization.ogg", channel="sfx", loop=False)
    pause(2.0)
    
    #play sound "sfx/sfx-objection.ogg"
    
    play music "music/Investigation ~ Opening 2001.mp3"
    $ renpy.music.set_volume(0.45, delay=0, channel="music")
    pause(0.5)
    
    #play music "music/Cross Examination ~ Moderate 2001.mp3"
    
    #godwin      "Well, well! If it isn't my old drinking buddy!"
    #croak       "Cut that out. You know I don't drink."
    #godwin      "Small talk Croaky. It's called small talk."
    #croak       "I'm in a hurry. What did you want to tell me?"
    #godwin      "Right down to business is it? And here I wanted to catch up with some small talk."
    #croak       "Dorian..."
    #godwin      "Fine. Fine. All work and no play huh? Must be pretty boring."
    #godwin      "Let me guess, you're investigating the murder on the Nerodian right?"
    #croak       "..."
    #croak       "Is it everyone's business to know what my business is?"
    #godwin      "Nope, just us defense attorneys."
    #godwin      "Can't really blame 'em though. You ARE the rising star of the Vanguard after all."
    #godwin      "Too many questions come up when you start waltzing around unchecked."
    #croak       "{color=#77c0c6}(I don't know whether I should feel flattered or annoyed...){/color}"
    #godwin      "Anyways, I just called to give you a friendly warning about your competition this time around."
    #croak       "A warning? About what?"
    #godwin      "The Phalanx is putting up one of our oldest veterans. You might've heard of him before."
    #godwin      "His name is Praval Kochhar."
    #croak       "Praval..
    #croak       "And you couldn't just tell me this over the phone?"
    #godwin      "And miss out on a free meal in exchange? What kind of person do you think I am?"
    #croak       "{color=#77c0c6}(This guy...){/color}"
    #croak       ""
    
    
    croak      "If that is what you {color=#fe5162}truly believe{/color}...{w=0.25} then far be it from me to try and convince you otherwise."
    hide godwin base
    show evaloria
    croak      ""
    hide evaloria
    show godwin base
    croak      "But there will be but one truth made known in court tomorrow,{w=0.2} and it will be mine."
    godwin      "Yeah, yeah.{w=0.2} I get it."
    $ renpy.music.play("sfx/sfx-evidenceshoop.ogg", channel="sfx", loop=False)
    show present at Position(xpos = 0.934, xanchor = 0.934, ypos = 0.035, yanchor = 0.035) with present
    show abacus_profile at Position(xpos = 0.934, xanchor = 0.934, ypos = 0.035, yanchor = 0.035) with present
    pause(0.25)
    godwin      "But y'know, this is just dev text{w=0.2} so try not to look so {color=#fe5162}serious{/color} when you say that."
    $ renpy.music.play("sfx/sfx-evidenceshoop.ogg", channel="sfx", loop=False)
    hide abacus_profile with take
    hide present with take
    croak      "You never know when they'll call for some dramatic dialogue."
    hide godwin base
    show silent godwin base
    godwin      "{color=#77c0c6}( D{w=0.25}...Dramatic dialogue? ){/color}"
    hide silent godwin base
    show godwin base
    croak      "That and the author only has one working sprite at the moment,{w=0.2} and it just happens to be this one."
    croak      "So...{w=0.5} deal."
    godwin      "{w=0.25}Wow."
    godwin      "Never thought I'd hear a fourth wall break coming from you."
    godwin      "The least you can do is try and stay in character,{w=0.2} even if this is non-canon."
    croak      "Well,{w=0.2} someone DID just tell me this was only dev text."
    $ renpy.music.play("sfx/sfx-smack.ogg", channel="sfx", loop=False)
    godwin      "Ouch.{w=0.75} Touché." with Shake((0, 0, 0, 0), 0.2, dist=30)
    godwin      "Anyway! Let's see here...{w=0.25}it says we have to test the dialog formatting."
    croak      "Talking. Finally something you're good at."
    godwin      "Awww yeah! \nTime to bust out some lines!"
    croak      "Try not to pull a muscle."
    $ renpy.music.set_volume(0.50, delay=0, channel="sfx")
    $ renpy.music.play("sfx/sfx-objection.ogg", channel="sfx", loop=False)
    godwin      "\"That testimony contradicts {color=#fe5162}this evidence{/color}!\""
    $ renpy.music.play("sfx/sfx-objection.ogg", channel="sfx", loop=False)
    godwin      "\"There's a {color=#fe5162}fatal flaw{/color} in her argument, Your Honor!\""
    $ renpy.music.play("sfx/sfx-objection.ogg", channel="sfx", loop=False)
    godwin      "\"He shot the victim {color=#fe5162}before{/color} my client even got there!\""
    $ renpy.music.set_volume(0, delay=0, channel="music")
    $ renpy.music.set_volume(1.0, delay=0, channel="sfx")
    $ renpy.music.play("sfx/sfx-objection.ogg", channel="sfx", loop=False)
    godwin      "\"O...OBJECTIONNNNNNN!\"" with Shake((0, 0, 0, 0), 0.75, dist=30)
    #show silent croak base
    croak       "{cps=5}...{/cps}"
    #hide silent croak base
    hide godwin base
    show silent godwin base
    godwin      "{cps=5}...{/cps}"
    hide silent godwin base
    show godwin base
    $ renpy.music.set_volume(0.45, delay=1.5, channel="music")
    croak       "Proud of yourself?"
    godwin      "I'd feel a lot better if I had more than one talking sprite,{w=0.5} but other than that I'm okay." 
    godwin      "In any case,{w=0.2} I think that's all they needed us for so I think we're done for now."
    godwin      "Let's go grab some coffee."
    
    $ back_once = False
    $ silver_coin = 0
    $ small_talk = 0
    
    label call_screen:
        call screen game_menu
        show godwin base with Dissolve(0.5)
        $ result = _return
    
        if result == "examine":
            $ renpy.music.play("sfx/button-new.ogg", channel="sfx", loop=False)
            hide godwin base with Dissolve(0.5)
            $ config.mouse = { 'default' : [ ('images/UI/cursor_arrow.png', 0, 0)] , 'examine' : [('images/UI/cursor_examine.png', 77, 452)]}
            
            label examine_screen:
                call screen examine_restaurant
                $ result = _return
                
                if result == "Second Floor Left":
                    #$ config.mouse = {"default" : [("cursor_examine_hover.png", 19, 19)]}
                    $ renpy.music.play("sfx/button-new3.ogg", channel="sfx", loop=False)
                    croak "Second floor left."
                elif result == "Chandelier":
                    #$ config.mouse = {"default" : [("cursor_examine_hover.png", 19, 19)]}
                    $ renpy.music.play("sfx/button-new3.ogg", channel="sfx", loop=False)
                    croak "{color=#77c0c6}(An elegant decorative chandelier.{/color}"
                    croak "{color=#77c0c6}(Despite it's traditional appearance, it runs on electricity like everything else.{/color}"
                elif result == "Second Floor Right":
                    #$ config.mouse = {"default" : [("cursor_examine_hover.png", 19, 19)]}
                    $ renpy.music.play("sfx/button-new3.ogg", channel="sfx", loop=False)
                    croak "Second floor right."
                elif result == "Shelves Left":
                    #$ config.mouse = {"default" : [("cursor_examine_hover.png", 19, 19)]}
                    $ renpy.music.play("sfx/button-new3.ogg", channel="sfx", loop=False)
                    croak "Shelves left."
                elif result == "Door Left":
                    #$ config.mouse = {"default" : [("cursor_examine_hover.png", 19, 19)]}
                    $ renpy.music.play("sfx/button-new3.ogg", channel="sfx", loop=False)
                    croak "{color=#77c0c6}(The door leading to the defense lobby.){/color}"
                    croak "{color=#77c0c6}(I've been to this courthouse countless times in my career.){/color}"
                    croak "{color=#77c0c6}(But I've never actually been inside.){/color}"
                elif result == "Window":
                    #$ config.mouse = {"default" : [("cursor_examine_hover.png", 19, 19)]}
                    $ renpy.music.play("sfx/button-new3.ogg", channel="sfx", loop=False)
                    croak "{color=#77c0c6}(They designed it to look like a window, but it's really a stainless glass mural.){/color}"
                    croak "{color=#77c0c6}(I can't see through it, but like I said - it's only for decoration.){/color}"
                elif result == "Door Right":
                    #$ config.mouse = {"default" : [("cursor_examine_hover.png", 19, 19)]}
                    $ renpy.music.play("sfx/button-new3.ogg", channel="sfx", loop=False)
                    croak "{color=#77c0c6}(The door leading to the prosecuting lobby.){/color}"
                    croak "{color=#77c0c6}(I've walked through it many times before and after a case.){/color}"
                    croak "{color=#77c0c6}(Each crack and imperfection is its own memory in my mind.){/color}"
                elif result == "Shelves Right":
                    #$ config.mouse = {"default" : [("cursor_examine_hover.png", 19, 19)]}
                    $ renpy.music.play("sfx/button-new3.ogg", channel="sfx", loop=False)
                    croak "{color=#77c0c6}(These shelves are filled with information from recently closed cases.){/color}"
                    croak "{color=#77c0c6}(The theory was that associated crimes usually occur within 2 months of each other.){/color}"
                    croak "{color=#77c0c6}(These files are meant to be readily available to prosecutors for that purpose.){/color}"
                elif result == "Back":
                    $ renpy.music.play("sfx/button-new.ogg", channel="sfx", loop=False)
                    $ config.mouse = {"default" :[("images/UI/cursor_arrow.png", 0, 0)]}
                    show godwin base with Dissolve(0.5)
                    jump call_screen
                
                jump examine_screen
        
            # with Dissolve(0.5)
            #jump call_screen
            
        elif result == "move":
            $ renpy.music.play("sfx/button-new.ogg", channel="test_six", loop=False)
            #pause(0.25)
            show thinking with Dissolve(0.5)
            typewriter "Moving from Molto Buona..." 
            hide thinking with Dissolve(0.5)
            jump call_screen
            #jump move_restaurant
        elif result == "talk":
            $ renpy.music.play("sfx/button-new.ogg", channel="test_seven", loop=False)
            #pause(0.25)
            show thinking with Dissolve(0.5)
            jump talk_restaurant
        elif result == "present":
            $ renpy.music.play("sfx/button-new.ogg", channel="test_eight", loop=False)
            typewriter "Presenting in Molto Buona..."
            jump continue_dialog
            
    label talk_restaurant:
        $ renpy.music.set_volume(0.5, delay=0.25, channel="music")
        
        if silver_coin == 5 and small_talk != 1:
            call screen dialog_options_check_one
            $ result = _return
        elif silver_coin == 5 and small_talk == 1:
            call screen dialog_options_check_two
            $ result = _return
        elif silver_coin !=5 and small_talk == 1:
            call screen dialog_options_check_three
            $ result = _return
        else:
            call screen dialog_options
            $ result = _return
        
        if result == "Silver Coin":
            $ renpy.music.play("sfx/button-new3.ogg", channel="sfx", loop=False)
            $ renpy.music.set_volume(1, channel="music")
            hide thinking with Dissolve(0.4)
            if silver_coin == 0:
                croak "About that {color=f0567c}silver coin{/color}..."
                croak "How did you find it?"                
                godwin "You're not going to believe this but..."
                godwin "Well...a metal detector."                
                croak "A...{w=0.5}A metal detector?"                
                godwin "Yeah. I had to go down to the precint and borrow a makeshift metal detector from one of the detectives."
                godwin "Pretty ridiculous right?"                
                croak "No,{w=0.25} I believe you...{w=0.25}it's just..."
                croak "...isn't that a bit {w=0.5}archaic?"                
                godwin "Well, your fancy police budget didn't help you guys find this thing in the first place right?"
                godwin "So I don't think the means really matter as much that I found it."                
                croak "{color=#77c0c6}(I hate to admit it, but he has a point.){/color}"
                croak "{color=#77c0c6}(Perhaps I should start supervising detective work in person.){/color}"
            elif silver_coin == 1:
                croak "Are there any unique marks or features on that {color=f0567c}coin{/color}?"                
                godwin "Yes. There aren't."                
                croak "\'Yes\' there are? Or \'yes\' there aren't?"                
                godwin "Just what I said."
                godwin "The strange thing about this coin is..."
                godwin "There are absolutely no marks or features on it at all."                
                croak "No features? Care to elaborate?"                
                godwin "What I mean is, there's no print signature anywhere on its faces."
                godwin "Forget signature, there's not even a date of manufacture anywhere on this thing."                
                croak "Suspicious. What else?"                
                godwin "Well, it doesn't really have any design as far as I can tell. And it doesn't look like any form of currency I know either."                
                croak "A foreign coin?"                
                godwin "Maybe."
                godwin "The metal doesn't look normal though. I guess I'll start with that."                
                croak "A small lead is better than nothing."
                godwin "But I'll need more than just a small lead if I want to convince the court of anything tomorrow."
            elif silver_coin == 2:                
                godwin "I still haven't found anything out about that {color=f0567c}silver coin{/color}."                
                croak "If you give it to me I can run it to forensics for a look."
                godwin "And spoil all the fun of the investigation? Where's your sense of adventure?"                
                croak "{color=#77c0c6}(We're attorneys here, not detectives...){/color}"
            elif silver_coin == 3:
                croak "What are you expecting to find about that {color=f0567c}coin{/color} here in the first place?"                
                godwin "Nothing really. I'm going to the archives later to see what else I can dig up."                
                croak "In that case, wasn't it pointless to come here?"                
                godwin "Well, it's on the way out of the courthouse so I might as well right?"
                godwin "I don't want to have to leave and then come back because of something I might have missed when I was already here."
                godwin "That'd just be a big waste of time, don't you think?"                
                croak "{color=#77c0c6}(...what is this strange feeling of defeat?){/color}"
            else:
                godwin "Sorry, but I'm not handing over the {color=f0567c}coin{/color} yet."
                godwin "I'll let you know if I find anything on it...{w=0.5}maybe."
                
            if silver_coin < 5:
                $ silver_coin = silver_coin + 1
            show thinking with Dissolve(0.4)
            jump talk_restaurant
        elif result == "Gates":
            $ renpy.music.play("sfx/button-new3.ogg", channel="sfx", loop=False)
            $ renpy.music.set_volume(1, channel="music")
            hide thinking with Dissolve(0.4)
            pause(0.25)
            typewriter "Talking about Gates..."
            show thinking with Dissolve(0.4)
            jump talk_restaurant
        elif result == "Basalwood":
            $ renpy.music.play("sfx/button-new3.ogg", channel="sfx", loop=False)
            $ renpy.music.set_volume(1, channel="music")
            hide thinking with Dissolve(0.4)
            typewriter "Talking about Basalwood..."
            show thinking with Dissolve(0.4)
            jump talk_restaurant
        elif result == "Small Talk":
            $ renpy.music.play("sfx/button-new3.ogg", channel="sfx", loop=False)
            $ renpy.music.set_volume(1, channel="music")
            hide thinking with Dissolve(0.4)
            godwin "Oh, I just remembered..."
            godwin "That story you mentioned the other day...the one about the debtor's tournament?"
            croak "The Liar Game? What about it?"
            godwin "It sounded pretty interesting, so yesterday I went and found a digital copy."
            croak "I'm impressed. I didn't think you were actually listening to me."
            croak "So? What are your impressions?"
            godwin "I haven't had the time to start reading yet..."
            godwin "But you didn't mention that it was a comic book series."
            godwin "Or that it was in Japanese."
            croak "Something wrong with it being a Japanese comic?"
            croak "Just because we're lawyers doesn't mean we should limit our practice to lawbooks."
            croak "Ideas are ideas. Where they come from is just the source."
            croak "Don't you agree?"
            godwin "No, I get what you're saying. It's just..."
            godwin "You never struck me as the comic book reading type."
            croak "Interesting."
            croak "What type do I strike you as then?"
            godwin "Er...y'know...well..."
            godwin "The classy novella type."
            godwin "With a cup of tea on a coaster next to you and everything."
            croak "...I see."
            croak "Well a lot of things about people will surprise you...once you get to know them."
            godwin "Yeah. I guess you're right."
            show silent croak base
            croak "{color=#77c0c6}(...){/color}"
            hide silent croak base
            croak "(I think it may be time to change my reading beverage.)"
            if small_talk < 1:
                $ small_talk = small_talk + 1
            show thinking with Dissolve(0.4)
            jump talk_restaurant
        elif result == "Back":
            $ renpy.music.play("sfx/button-new3.ogg", channel="sfx", loop=False)
            $ renpy.music.set_volume(1, channel="music")
            hide thinking with Dissolve(0.4)
            if silver_coin > 4:
                hide dialog_options_check_one
            jump call_screen
    
    label examine_restaurant:
        typewriter "Examining Molto Buona..."
        jump menu_restaurant
        
    label move_restaurant:
        typewriter "Moving from Molto Buona..."
        jump menu_restaurant
        
    label present_restaurant:
        typewriter "Presenting in Molto Buona..."
        jump menu_restaurant
    
    label continue_dialog:
        godwin       "Exit stage left."    
        pause(0.5)
        hide godwin base with Dissolve(1.25)
        $ renpy.music.set_volume(0, delay=1.25, channel="music")
        pause(2.0)
        play music "music/Investigation ~ Core 2001.mp3"
        pause(1.0)
        $ renpy.music.set_volume(0.45, delay=1.0, channel="music")
        news        "{color=#54fe54}The victim's body was found in the river early yesterday morning.{/color}"
        news        "{color=#54fe54}A patrol unit responded to a call from a cruise ship passing through the harbor the night of the twelfth.{/color}"
        news        "{color=#54fe54}According to reports,{w=0.2} the cruise ship was hosting an end of the year party for local celebrities.{/color}"
        news        "{color=#54fe54}There's no word yet on the identity of the victim,{w=0.2} but we have information suggesting police have already arrested a suspect."
        news        "{color=#54fe54}Stay tuned,{w=0.2} and we'll keep you updated on this breaking story as more news develops.{/color}"
        news        "{color=#54fe54}This is Abigail Arrowny for News Channel 8,{w=0.5} signing off.{/color}"
        $ renpy.music.set_volume(1.0, delay=0, channel="sound")
        pause(1.0)
        $ renpy.music.set_volume(0, delay=1.5, channel="music")
        scene blackness with Fade(1.5, 0, 0)
        pause(2.5)
        play music "music/Cross Examination ~ Moderate 2001.mp3"
        $ renpy.music.set_volume(0.45, delay=1.0, channel="music")
        dutch       "I'm the detective here, right?{w=0.2} So let's agree to leave the detective work to me."
        dutch       "If you've got a problem with the way I do things,{w=0.2} then take it up with the chief."
        dutch       "But right now,{w=0.2} I'm the authority on what happened at the crime scene,{w=0.2} get me?"
        play music "music/Cross Examination ~ Allegro 2001.mp3"
        sahwit      "I didn't see nothin', I swear!"
        sahwit      "Yeah,{w=0.2} well...{w=0.2}maybe I saw a little bit...{w=0.5} maybe..."
        sahwit      "Okay!{w=0.2} Okay!{w=0.25} I admit it!{w=0.25} I saw everything!"
        play music "music/Confess the Truth 2001.mp3"
        juri        "Witness!"
        juri        "We are not here to listen to you air your personal grievances against the defendant!"
        juri        "Restrain yourself to the cold, hard facts,{w=0.5} or I will be forced to hold you in contempt!"
        juri        "Have I made myself clear?"
        play music "music/Won the Case! ~ First Victory.mp3"
        gency       "I can't believe it..."
        gency       "We won...{w=0.5} we actually won!"
        gency       "Thank you so much!"
        gency       "Thank you so much for everything!"
        $ renpy.music.set_volume(0, delay=2.0, channel="music")
        pause(2.0)
    
    return
