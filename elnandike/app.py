#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, absolute_import, division
import urwid
from .game import Game
from .ui import CardWidget, CardPileWidget, SpacerWidget, EmptyCardWidget, PALETTE


def exit_on_q(key):
    if key in ('q', 'Q', 'esc'):
        raise urwid.ExitMainLoop()


def main(args):
    game = Game()
    statusbar = urwid.Text(u'Ready')

    def onclick(card_widget):
        # XXX: code below is meant just for testing the UI,
        # it's not related to actual game logic
        card_widget.face_up = not card_widget.face_up
        card_widget.highlighted = not card_widget.highlighted

        text = 'Clicked: {}\nCard: {}\nHighlighted: {}'.format(
            card_widget,
            card_widget.card,
            card_widget.highlighted,
        )
        statusbar.set_text(text)
        card_widget.redraw()

    main_layout = urwid.Pile([
        urwid.Columns([
            CardWidget(game.stock[-1]),
            EmptyCardWidget(),
            SpacerWidget(),
            EmptyCardWidget(),
            EmptyCardWidget(),
            EmptyCardWidget(),
            EmptyCardWidget(),
        ]),
        urwid.Divider(),
        urwid.Columns([
            CardPileWidget(pile, onclick=onclick)
            for pile in game.tableau
        ]),
        urwid.Divider(),
        statusbar,
    ])

    if args.shell:
        from IPython import embed
        embed()
    else:
        loop = urwid.MainLoop(
            urwid.Filler(main_layout, valign='top'),
            PALETTE,
            unhandled_input=exit_on_q,
        )
        loop.run()


if '__main__' == __name__:
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--shell', action='store_true')

    args = parser.parse_args()
    main(args)
