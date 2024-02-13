from libqtile import bar, layout, widget
from libqtile.config import Click, Drag, Group, Key, KeyChord, Match, Screen
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal
from typing import NamedTuple
from pathlib import Path

MOD_KEY = "mod4"
TERMINAL = guess_terminal()
INTRPR = "bash"
UTILS = Path.home().joinpath(".config/qtile/utils/")
MAIN_MONITOR = "eDP-1"

class Volume(NamedTuple):
    step: int = 5
    quick_increase: int = 100
    quick_decrease: int = 50

class Brightness(NamedTuple):
    step: int = 5
    quick_increase: int = 100
    quick_decrease: int = 50

keys = [
    # windows control
    Key([MOD_KEY], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([MOD_KEY], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([MOD_KEY], "j", lazy.layout.down(), desc="Move focus down"),
    Key([MOD_KEY], "k", lazy.layout.up(), desc="Move focus up"),
    Key([MOD_KEY, "shift"], "h", lazy.layout.swap_left(), desc="Move window to the left"),
    Key([MOD_KEY, "shift"], "l", lazy.layout.swap_right(), desc="Move window to the right"),
    Key([MOD_KEY, "shift"], "j", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([MOD_KEY, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),
    Key([MOD_KEY, "shift"], "q", lazy.window.kill(), desc="Kill focused window"),
    # layouts control
    Key([MOD_KEY], "o", lazy.layout.maximize(), desc="Layout context maximize"),
    Key([MOD_KEY, "shift"], "o", lazy.layout.normalize(), desc="Layout context normalize"),
    Key([MOD_KEY], "equal", lazy.layout.reset(), desc="Layout size reset"),
    Key([MOD_KEY], "i", lazy.layout.grow(), desc="Layout context window grow"),
    Key([MOD_KEY, "shift"], "i", lazy.layout.shrink(), desc="Layout context window shrink"),
    Key([MOD_KEY, "shift"], "minus", lazy.layout.flip(), desc="Layout context flip"),
    KeyChord(
        [MOD_KEY, "shift"], 'f', [
            Key([], 'f', lazy.group.setlayout('max'), desc=''),
            Key([], 'm', lazy.group.setlayout('monadtall'), desc='')
        ],
    ),
    # qtile quit/reload/restart
    Key([MOD_KEY, "shift"], "e", lazy.shutdown(), desc="Shutdown Qtile"),
    Key([MOD_KEY, "shift"], "c", lazy.reload_config(), desc="Reload Qtile config"),
    Key([MOD_KEY, "shift"], "r", lazy.restart(), desc="Restart Qtile"),
    # programs
    Key([MOD_KEY], "return", lazy.spawn(TERMINAL), desc="Launch terminal"),
    Key([MOD_KEY], "d", lazy.spawn("dmenu_run"), desc="Launch dmenu_run"),
    Key([MOD_KEY, "shift"], "d", lazy.spawn(f"{INTRPR} {UTILS.joinpath('dmenu_tools')}"), desc="Launch terminal"),
]

groups = [Group(i) for i in "1234567890"]
for group in groups:
    keys.extend(
        [
            # mod1 + letter of group = switch to group
            Key(
                [MOD_KEY],
                group.name,
                lazy.group[group.name].toscreen(),
                desc="Switch to group {}".format(group.name),
            ),
            # mod1 + shift + letter of group = switch to & move focused window to group
            Key(
                [MOD_KEY, "shift"],
                group.name,
                lazy.window.togroup(group.name, switch_group=True),
                desc="Switch to & move focused window to group {}".format(group.name),
            ),
            # Or, use below if you prefer not to switch to that group.
            # # mod1 + shift + letter of group = move focused window to group
            # Key([mod, "shift"], i.name, lazy.window.togroup(i.name),
            #     desc="move focused window to group {}".format(i.name)),
        ]
    )

layouts = [
    layout.MonadTall(),
    layout.Max(),
]

widget_defaults = dict(
    font="sans",
    fontsize=12,
    padding=3,
)
extension_defaults = widget_defaults.copy()

screens = [
    Screen(
        bottom=bar.Bar(
            [
                widget.CurrentLayout(),
                widget.GroupBox(hide_unused=True),
                widget.Prompt(),
                widget.WindowName(),
                widget.Chord(
                    chords_colors={
                        "launch": ("#ff0000", "#ffffff"),
                    },
                    name_transform=lambda name: name.upper(),
                ),
                widget.TextBox("default config", name="default"),
                widget.TextBox("Press &lt;M-r&gt; to spawn", foreground="#d75f5f"),
                # NB Systray is incompatible with Wayland, consider using StatusNotifier instead
                # widget.StatusNotifier(),
                widget.Systray(),
                widget.Clock(format="%Y-%m-%d %a %I:%M %p"),
                widget.QuickExit(),
            ],
            24,
            # border_width=[2, 0, 2, 0],  # Draw top and bottom borders
            # border_color=["ff00ff", "000000", "ff00ff", "000000"]  # Borders are magenta
        ),
    ),
]

# Drag floating layouts.
mouse = [
    Drag([MOD_KEY], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([MOD_KEY], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([MOD_KEY], "Button2", lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = False
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
    ]
)
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# When using the Wayland backend, this can be used to configure input devices.
wl_input_rules = None

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"
