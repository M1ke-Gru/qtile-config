# Copyright (c) 2010 Aldo Cortesi
# Copyright (c) 2010, 2014 dequis
# Copyright (c) 2012 Randall Ma
# Copyright (c) 2012-2014 Tycho Andersen
# Copyright (c) 2012 Craig Barnes
# Copyright (c) 2013 horsik
# Copyright (c) 2013 Tao Sauvage
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights# Copyright (c) 2010 Aldo Cortesi
# Copyright (c) 2010, 2014 dequis
# Copyright (c) 2012 Randall Ma
# Copyright (c) 2012-2014 Tycho Andersen
# Copyright (c) 2012 Craig Barnes
# Copyright (c) 2013 horsik
# Copyright (c) 2013 Tao Sauvage
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


import os
import re
import socket
import subprocess
from typing import List  # noqa: F401
from libqtile import layout, bar, widget, hook, qtile
from libqtile.config import (
    Click,
    Drag,
    Group,
    Key,
    Match,
    Screen,
    Rule,
    ScratchPad,
    DropDown,
)
from libqtile.command import lazy


# mod4 or mod = super key
mod = "mod4"
mod1 = "alt"
mod2 = "control"
home = os.path.expanduser("~")


@lazy.function
def window_to_prev_group(qtile):
    if qtile.currentWindow is not None:
        i = qtile.groups.index(qtile.currentGroup)
        qtile.currentWindow.togroup(qtile.groups[i - 1].name)


@lazy.function
def window_to_next_group(qtile):
    if qtile.currentWindow is not None:
        i = qtile.groups.index(qtile.currentGroup)
        qtile.currentWindow.togroup(qtile.groups[i + 1].name)


myTerm = "kitty"  # My terminal of choice

keys = [
    # SUPER + FUNCTION KEYS
    Key([mod], "f", lazy.window.toggle_fullscreen()),
    Key([mod], "x", lazy.window.kill()),
    Key([mod], "t", lazy.spawn("xterm")),
    Key([mod], "p", lazy.spawn("pavucontrol")),
    Key([mod], "space", lazy.spawn("rofi -show drun")),
    Key([mod], "Escape", lazy.spawn("xkill")),
    Key([mod], "Return", lazy.spawn(myTerm)),
    Key([mod], "KP_Enter", lazy.spawn("alacritty")),
    Key([mod, "control"], "q", lazy.shutdown()),
    # SUPER + SHIFT KEYS
    Key([mod, "shift"], "Return", lazy.spawn("pcmanfm")),
    Key(
        [mod, "shift"],
        "d",
        lazy.spawn(
            "dmenu_run -i -nb '#191919' -nf '#ff1493' -sb '#ff1493' -sf '#191919' -fn 'NotoMonoRegular:bold:pixelsize=15'"
        ),
    ),
    #    Key([mod, "shift"], "d", lazy.spawn(home + '/.config/qtile/scripts/dmenu.sh')),
    Key([mod, "shift"], "q", lazy.window.kill()),
    Key([mod, "shift"], "r", lazy.restart()),
    Key([mod, "control"], "r", lazy.restart()),
    Key([mod, "shift"], "x", lazy.shutdown()),
    # CONTROL + ALT KEYS
    Key(
        ["mod1", "control"],
        "o",
        lazy.spawn(home + "/.config/qtile/scripts/picom-toggle.sh"),
    ),
    Key(["mod1", "control"], "t", lazy.spawn("xterm")),
    Key(["mod1", "control"], "u", lazy.spawn("pavucontrol")),
    # ALT + ... KEYS
    Key([mod, "mod1"], "p", lazy.spawn("pamac-manager")),
    Key([mod, "mod1"], "f", lazy.spawn("thunar")),
    Key([mod, "mod1"], "w", lazy.spawn("garuda-welcome")),
    Key([mod, "mod1"], "b", lazy.spawn("brave")),
    Key([mod, "mod1"], "l", lazy.spawn("flatpak run com.logseq.Logseq")),
    Key([mod, "mod1"], "t", lazy.spawn("flatpak run org.telegram.desktop")),
    Key([mod, "mod1"], "v", lazy.spawn("codium")),
    # CONTROL + SHIFT KEYS
    Key([mod2, "shift"], "Escape", lazy.spawn("lxtask")),
    # SCREENSHOTS
    Key([], "Print", lazy.spawn("flameshot full -p " + home + "/Pictures")),
    Key([mod2], "Print", lazy.spawn("flameshot full -p " + home + "/Pictures")),
    #    Key([mod2, "shift"], "Print", lazy.spawn('gnome-screenshot -i')),
    # MULTIMEDIA KEYS
    # INCREASE/DECREASE BRIGHTNESS
    Key([], "F6", lazy.spawn("brightnessctl s +5%")),
    Key([], "F5", lazy.spawn("brightnessctl s 5%-")),
    # INCREASE/DECREASE/MUTE VOLUME
    Key([], "F4", lazy.spawn("amixer -q set Master toggle")),
    Key([], "F2", lazy.spawn("amixer -q set Master 5%-")),
    Key([], "F3", lazy.spawn("amixer -M set Master 5%+")),
    Key([], "F9", lazy.spawn("playerctl play-pause")),
    Key([], "XF86AudioNext", lazy.spawn("playerctl next")),
    Key([], "XF86AudioPrev", lazy.spawn("playerctl previous")),
    Key([], "XF86AudioStop", lazy.spawn("playerctl stop")),
    #    Key([], "XF86AudioPlay", lazy.spawn("mpc toggle")),
    #    Key([], "XF86AudioNext", lazy.spawn("mpc next")),
    #    Key([], "XF86AudioPrev", lazy.spawn("mpc prev")),
    #    Key([], "XF86AudioStop", lazy.spawn("mpc stop")),
    # QTILE LAYOUT KEYS
    Key([mod], "n", lazy.layout.normalize()),
    Key([mod], "s", lazy.next_layout()),
    # CHANGE FOCUS
    Key([mod], "Up", lazy.layout.up()),
    Key([mod], "Down", lazy.layout.down()),
    Key([mod], "Left", lazy.layout.left()),
    Key([mod], "Right", lazy.layout.right()),
    Key([mod], "k", lazy.layout.up()),
    Key([mod], "j", lazy.layout.down()),
    Key([mod], "h", lazy.layout.left()),
    Key([mod], "l", lazy.layout.right()),
    # RESIZE UP, DOWN, LEFT, RIGHT
    Key(
        [mod, "control"],
        "l",
        lazy.layout.grow_right(),
        lazy.layout.grow(),
        lazy.layout.increase_ratio(),
        lazy.layout.delete(),
    ),
    Key(
        [mod, "control"],
        "Right",
        lazy.layout.grow_right(),
        lazy.layout.grow(),
        lazy.layout.increase_ratio(),
        lazy.layout.delete(),
    ),
    Key(
        [mod, "control"],
        "h",
        lazy.layout.grow_left(),
        lazy.layout.shrink(),
        lazy.layout.decrease_ratio(),
        lazy.layout.add(),
    ),
    Key(
        [mod, "control"],
        "Left",
        lazy.layout.grow_left(),
        lazy.layout.shrink(),
        lazy.layout.decrease_ratio(),
        lazy.layout.add(),
    ),
    Key(
        [mod, "control"],
        "k",
        lazy.layout.grow_up(),
        lazy.layout.grow(),
        lazy.layout.decrease_nmaster(),
    ),
    Key(
        [mod, "control"],
        "Up",
        lazy.layout.grow_up(),
    ),
    Key(
        [mod, "control"],
        "j",
        lazy.layout.grow_down(),
    ),
    Key(
        [mod, "control"],
        "Down",
        lazy.layout.grow_down(),
        lazy.layout.shrink(),
        lazy.layout.increase_nmaster(),
    ),
    # FLIP LAYOUT FOR MONADTALL/MONADWIDE
    Key([mod, "shift"], "f", lazy.layout.flip()),
    # FLIP LAYOUT FOR BSP
    Key([mod, "mod1"], "k", lazy.layout.flip_up()),
    Key([mod, "mod1"], "j", lazy.layout.flip_down()),
    Key([mod, "mod1"], "l", lazy.layout.flip_right()),
    Key([mod, "mod1"], "h", lazy.layout.flip_left()),
    # MOVE WINDOWS UP OR DOWN BSP LAYOUT
    Key([mod, "shift"], "k", lazy.layout.shuffle_up()),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down()),
    Key([mod, "shift"], "h", lazy.layout.shuffle_left()),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right()),
    ### Treetab controls
    Key(
        [mod, "control"],
        "k",
        lazy.layout.section_up(),
        desc="Move up a section in treetab",
    ),
    Key(
        [mod, "control"],
        "j",
        lazy.layout.section_down(),
        desc="Move down a section in treetab",
    ),
    # MOVE WINDOWS UP OR DOWN MONADTALL/MONADWIDE LAYOUT
    Key([mod, "shift"], "Up", lazy.layout.shuffle_up()),
    Key([mod, "shift"], "Down", lazy.layout.shuffle_down()),
    Key([mod, "shift"], "Left", lazy.layout.swap_left()),
    Key([mod, "shift"], "Right", lazy.layout.swap_right()),
    # TOGGLE FLOATING LAYOUT
    Key([mod, "shift"], "space", lazy.window.toggle_floating()),
]

groups = []

# FOR QWERTY KEYBOARDS
group_names = [
    "1",
    "2",
    "3",
    "4",
    "5",
    "6",
    "7",
    "8",
    "9",
    "0",
]

# FOR AZERTY KEYBOARDS
# group_names = ["ampersand", "eacute", "quotedbl", "apostrophe", "parenleft", "section", "egrave", "exclam", "ccedilla", "agrave",]

group_labels = [
    "1 ",
    "2 ",
    "3 ",
    "4 ",
    "5 ",
    "6 ",
    "7 ",
    "8 ",
    "9 ",
    "0",
]
# group_labels = ["α", "β", "γ", "δ", "ε", "ζ", "η", "θ", "ι", "κ",]
# group_labels = ["", "", "", "", "",]
# group_labels = ["Web", "Edit/chat", "Image", "Gimp", "Meld", "Video", "Vb", "Files", "Mail", "Music",]

group_layouts = [
    "columns",
    "monadtall",
    "monadtall",
    "monadtall",
    "monadtall",
    "monadtall",
    "monadtall",
    "monadtall",
    "treetab",
    "floating",
]
# group_layouts = ["monadtall", "matrix", "monadtall", "bsp", "monadtall", "matrix", "monadtall", "bsp", "monadtall", "monadtall",]

for i in range(len(group_names)):
    groups.append(
        Group(
            name=group_names[i],
            layout=group_layouts[i].lower(),
            label=group_labels[i],
        )
    )

for i in groups:
    keys.extend(
        [
            # CHANGE WORKSPACES
            Key([mod], i.name, lazy.group[i.name].toscreen()),
            Key([mod], "Tab", lazy.screen.next_group()),
            Key([mod, "shift"], "Tab", lazy.screen.prev_group()),
            Key(["mod1"], "Tab", lazy.screen.next_group()),
            Key(["mod1", "shift"], "Tab", lazy.screen.prev_group()),
            # MOVE WINDOW TO SELECTED WORKSPACE 1-10 AND STAY ON WORKSPACE
            # Key([mod, "shift"], i.name, lazy.window.togroup(i.name)),
            # MOVE WINDOW TO SELECTED WORKSPACE 1-10 AND FOLLOW MOVED WINDOW TO WORKSPACE
            Key(
                [mod, "shift"],
                i.name,
                lazy.window.togroup(i.name),
                lazy.group[i.name].toscreen(),
            ),
        ]
    )


def init_layout_theme():
    return {
        "margin": 0,
        "border_width": 2,
        "border_focus": "#89b4fa",
        "border_normal": "#1e1e2e",
    }


layout_theme = init_layout_theme()


layouts = [
    #   layout.MonadTall(**layout_theme),
    #   layout.MonadWide(margin=8, border_width=2, border_focus="#ff00ff", border_normal="#f4c2c2"),
    #   layout.MonadWide(**layout_theme),
    #   layout.Matrix(**layout_theme),
    #   layout.Bsp(**layout_theme),
    #   layout.Floating(**layout_theme),
    #   layout.RatioTile(**layout_theme),
    layout.Columns(**layout_theme),
    layout.Max(border_width=0),
    #   layout.Stack(**layout_theme),
    #   layout.Tile(**layout_theme),
    #   layout.TreeTab(
    #       sections=['FIRST', 'SECOND'],
    #       bg_color = '#141414',
    #       active_bg = '#0000ff',
    #       inactive_bg = '#1e90ff',
    #       padding_y =5,
    #       section_top =10,
    #       panel_width = 280),
    #   layout.VerticalTile(**layout_theme),
    #   layout.Zoomy(**layout_theme)
]

# ScratchPads
groups.append(
    ScratchPad(
        "scratchpad",
        [
            DropDown(
                "term", "alacritty", width=0.8, height=0.7, x=0.1, y=0.1, opacity=1
            ),
            DropDown("fm", "pcmanfm", width=0.4, height=0.5, x=0.3, y=0.1, opacity=1),
        ],
    )
)

# Extend keys for scratchPad
keys.extend(
    [
        Key(["control"], "Return", lazy.group["scratchpad"].dropdown_toggle("term")),
        # Key(["control"], "s", lazy.group['scratchpad'].dropdown_toggle('fm')),
    ]
)


# COLORS FOR THE BAR


def init_colors():
    return [
        # Catpuchinn colors are used
        ["#11111b", "#11111b"],  # almost black
        ["#7777aa", "#7777aa"],
        ["#cdd6f4", "#cdd6f4"],
        ["ffff00", "ffff00"],
        ["89b4fa", "89b4fa"],  # blue
        ["#313255", "#313255"],  # some dark color
    ]


colors = init_colors()


def base(fg="text", bg="dark"):
    return {"foreground": colors[2], "background": colors[0]}


# WIDGETS FOR THE BAR


def init_widgets_defaults():
    return dict(font="Noto Sans", fontsize=9, padding=2, background=colors[0])


widget_defaults = init_widgets_defaults()


def init_widgets_list():
    prompt = "{0}@{1}: ".format(os.environ["USER"], socket.gethostname())
    widgets_list = [
        widget.Sep(linewidth=1, padding=10, foreground=colors[0], background=colors[0]),
        widget.Image(
            filename="~/.config/qtile/icons/garuda-white.png",
            iconsize=8,
            mouse_callbacks={"Button1": lambda: qtile.cmd_spawn("jgmenu_run")},
        ),
        widget.Sep(linewidth=0, padding=7, foreground=colors[1], background=colors[0]),
        widget.GroupBox(
            **base(bg=colors[0]),
            font="UbuntuMono Nerd Font",
            fontsize=15,
            margin_y=3,
            margin_x=2,
            padding_y=5,
            padding_x=4,
            borderwidth=3,
            active=colors[2],
            inactive=colors[4],
            highlight_method="block",
            this_current_screen_border=colors[5],
            this_screen_border=colors[5],
            urgent_alert_method="block",
            disable_drag=True,
            rounded=True,
        ),
        widget.Sep(linewidth=0, padding=7, foreground=colors[1], background=colors[0]),
        widget.TaskList(
            highlight_method="block",
            icon_size=20,
            max_title_width=150,
            rounded=True,
            padding_x=0,
            padding_y=0,
            margin_y=0,
            fontsize=17,
            margin=2,
            txt_floating="🗗",
            txt_minimized=">_ ",
            borderwidth=1,
            border=colors[5],
            # background=colors[0],
            # unfocused_border = 'border'
        ),
        widget.CurrentLayoutIcon(
            custom_icon_paths=[os.path.expanduser("~/.config/qtile/icons")],
            background=colors[0],
            padding=5,
            scale=0.7,
        ),
        widget.Sep(linewidth=2, padding=10, foreground=colors[1], background=colors[0]),
        widget.KeyboardLayout(
            padding=4,
            configured_keyboards=["us intl", "ua"],
            fontsize=16,
            background=colors[0],
        ),
        widget.Sep(linewidth=2, padding=10, foreground=colors[1], background=colors[0]),
        widget.Battery(
            padding=4,
            fontsize=16,
            background=colors[0],
        ),
        widget.Sep(linewidth=2, padding=10, foreground=colors[1], background=colors[0]),
        #                widget.CPU(
        #                        font="Noto Sans",
        #                        #format = '{MemUsed}M/{MemTotal}M',
        #                        update_interval = 1,
        #                        fontsize = 16,
        #                        foreground = colors[5],
        #                        background = colors[22],
        #                        mouse_callbacks = {'Button1': lambda : qtile.cmd_spawn(myTerm + ' -e htop')},
        #                       ),
        #
        #               widget.Memory(
        #                        font="Noto Sans",
        #                        format = '{MemUsed: .0f}M/{MemTotal: .0f}M',
        #                        update_interval = 1,
        #                        fontsize = 16,
        #                        measure_mem = 'M',
        #                        foreground = colors[5],
        #                        background = colors[16],
        #                        mouse_callbacks = {'Button1': lambda : qtile.cmd_spawn(myTerm + ' -e htop')},
        #                       ),
        widget.Systray(
            background=colors[0],
            icon_size=20,
            padding=4,
        ),
        widget.Sep(
            linewidth=2,
            padding=10,
            foreground=colors[1],
            background=colors[0],
        ),
        widget.Clock(padding=4, fontsize=18, rounded=True, format="%H:%M"),
    ]
    return widgets_list


widgets_list = init_widgets_list()


def init_widgets_screen1():
    widgets_screen1 = init_widgets_list()
    return widgets_screen1


def init_widgets_screen2():
    widgets_screen2 = init_widgets_list()
    return widgets_screen2


widgets_screen1 = init_widgets_screen1()
widgets_screen2 = init_widgets_screen2()


def init_screens():
    return [
        Screen(
            top=bar.Bar(
                widgets=init_widgets_screen1(), size=25, opacity=1, background="000000"
            )
        ),
        Screen(
            top=bar.Bar(
                widgets=init_widgets_screen2(), size=25, opacity=1, background="000000"
            )
        ),
    ]


screens = init_screens()


# MOUSE CONFIGURATION
mouse = [
    Drag(
        [mod],
        "Button1",
        lazy.window.set_position_floating(),
        start=lazy.window.get_position(),
    ),
    Drag(
        [mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()
    ),
]

dgroups_key_binder = None
dgroups_app_rules = []

# ASSIGN APPLICATIONS TO A SPECIFIC GROUPNAME
# BEGIN

#########################################################
################ assgin apps to groups ##################
#########################################################
# @hook.subscribe.client_new
# def assign_app_group(client):
#     d = {}
#     #########################################################
#     ################ assgin apps to groups ##################
#     #########################################################
#     d["1"] = ["Navigator", "Firefox", "Vivaldi-stable", "Vivaldi-snapshot", "Chromium", "Google-chrome", "Brave", "Brave-browser",
#               "navigator", "firefox", "vivaldi-stable", "vivaldi-snapshot", "chromium", "google-chrome", "brave", "brave-browser", ]
#     d["2"] = [ "Atom", "Subl3", "Geany", "Brackets", "Code-oss", "Code", "TelegramDesktop", "Discord",
#                "atom", "subl3", "geany", "brackets", "code-oss", "code", "telegramDesktop", "discord", ]
#     d["3"] = ["Inkscape", "Nomacs", "Ristretto", "Nitrogen", "Feh",
#               "inkscape", "nomacs", "ristretto", "nitrogen", "feh", ]
#     d["4"] = ["Gimp", "gimp" ]
#     d["5"] = ["Meld", "meld", "org.gnome.meld" "org.gnome.Meld" ]
#     d["6"] = ["Vlc","vlc", "Mpv", "mpv" ]
#     d["7"] = ["VirtualBox Manager", "VirtualBox Machine", "Vmplayer",
#               "virtualbox manager", "virtualbox machine", "vmplayer", ]
#     d["8"] = ["pcmanfm", "Nemo", "Caja", "Nautilus", "org.gnome.Nautilus", "Pcmanfm", "Pcmanfm-qt",
#               "pcmanfm", "nemo", "caja", "nautilus", "org.gnome.nautilus", "pcmanfm", "pcmanfm-qt", ]
#     d["9"] = ["Evolution", "Geary", "Mail", "Thunderbird",
#               "evolution", "geary", "mail", "thunderbird" ]
#     d["0"] = ["Spotify", "Pragha", "Clementine", "Deadbeef", "Audacious",
#               "spotify", "pragha", "clementine", "deadbeef", "audacious" ]
#     ##########################################################
#     wm_class = client.window.get_wm_class()[0]
#
#     for i in range(len(d)):
#         if wm_class in list(d.values())[i]:
#             group = list(d.keys())[i]
#             client.togroup(group)
#             client.group.cmd_toscreen()

# END
# ASSIGN APPLICATIONS TO A SPECIFIC GROUPNAME


main = None


# Define a function to set the wallpaper using feh
def set_wallpaper():
    wallpaper_path = "~/Bilder/nord-theme-city-lights-building-night-street-light-hd-wallpaper-preview.jpg"  # Replace with the actual path to your wallpaper image
    subprocess.Popen(["feh", "--bg-fill", wallpaper_path])


# Define a keybinding to change the wallpaper
keys.append(Key([mod], "w", lazy.function(set_wallpaper)))


@hook.subscribe.startup_once
def autostart():
    home = os.path.expanduser("~")
    subprocess.call([home + "/.config/qtile/scripts/autostart.sh"])


@hook.subscribe.startup
def start_always():
    # Set the cursor to something sane in X
    subprocess.Popen(["xsetroot", "-cursor_name", "left_ptr"])


@hook.subscribe.client_new
def set_floating(window):
    if (
        window.window.get_wm_transient_for()
        or window.window.get_wm_type() in floating_types
    ):
        window.floating = True


floating_types = ["notification", "toolbar", "splash", "dialog"]


follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(
    float_rules=[
        *layout.Floating.default_float_rules,
        Match(wm_class="confirm"),
        Match(wm_class="dialog"),
        Match(wm_class="download"),
        Match(wm_class="error"),
        Match(wm_class="file_progress"),
        Match(wm_class="notification"),
        Match(wm_class="splash"),
        Match(wm_class="toolbar"),
        Match(wm_class="confirmreset"),
        Match(wm_class="makebranch"),
        Match(wm_class="maketag"),
        Match(wm_class="Arandr"),
        Match(wm_class="feh"),
        Match(wm_class="Galculator"),
        Match(title="branchdialog"),
        Match(title="Open File"),
        Match(title="pinentry"),
        Match(wm_class="ssh-askpass"),
        Match(wm_class="lxpolkit"),
        Match(wm_class="Lxpolkit"),
        Match(wm_class="yad"),
        Match(wm_class="Yad"),
        Match(wm_class="Cairo-dock"),
        Match(wm_class="cairo-dock"),
    ],
    fullscreen_border_width=0,
    border_width=0,
)
auto_fullscreen = True

focus_on_window_activation = "focus"  # or smart

wmname = "LG3D"
