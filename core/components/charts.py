from random import randrange

import matplotlib.pyplot as plot

COLOUR_PALETTE = [
    '#cee8eb',  # Jagged Ice
    '#d2eade',  # Skeptic
    '#b7d7c9',  # Gum Leaf
    '#b3dad8',  # Ziggurat
    '#83d3d8',  # Bermuda
    '#81c1d1',  # Half Baked
    '#8cc8aa',  # Vista Blue
    '#86c48b',  # De York
    '#e6e281',  # Wild Rice
    '#f8d2ad',  # Maize
    '#eed6e0',  # Melanie
    '#d7d3e8',  # Snuff
    '#dfc3e6',  # Prelude
    '#f4ccd3',  # We Peep
    '#f3abaa',  # Wewak
    '#f0908f',  # Sea Pink
    '#e46b5e',  # Terracotta
    '#ee6679',  # Froly
    '#ce7459',  # Chestnut Rose
    '#45344a',  # Voodoo
    '#7a79cf',  # Moody Blue
    '#375b9e',  # Azure
    '#4b9dd1',  # Shakespeare
    '#2093a3',  # Eastern Blue
]


def colour_list(n):
    """Return list of n colours from COLOUR_PALETTE."""
    colours = [*COLOUR_PALETTE]
    colour_list = []
    while len(colour_list) < n:
        colour_list.append(colours.pop(randrange(len(colours))))
        if not colours:
            colours[:] = COLOUR_PALETTE
    return colour_list


def chart_title(statistic, chat, start_date, end_date):
    """Return title for chart displaying statistic (given as string)."""
    return '{statistic} in "{subject}" ({start_date} - {end_date})'.format(
        statistic=statistic,
        subject=chat.subject,
        start_date=start_date.Format('%d/%m/%Y'),
        end_date=end_date.Format('%d/%m/%Y'))


def bar_chart(data, title):
    """Show bar chart of data tuple (labels, values)."""
    labels = data[0]
    values = data[1]
    index = [i for i in range(len(labels))]
    colours = colour_list(len(labels))

    plot.figure('WhatStats - {title}'.format(title=title))
    plot.title(title, y=1.08)
    plot.bar(index, values, color=colours)
    plot.xticks(index, labels, rotation=30)
    for i in index:
        value = '{:,}'.format(values[i])
        plot.text(i, values[i], value, horizontalalignment='center')

    plot.box(on=False)
    plot.tight_layout()
    plot.show()


def doughnut_chart(data, title):
    """Show doughnut chart of data tuple (labels, values)."""
    labels = data[0]
    values = data[1]
    slice_labels = ['{} ({:,})'.format(l, v) for l, v in zip(labels, values)]
    colours = colour_list(len(labels))
    explode = [0.05 for _ in range(len(labels))]

    plot.figure('WhatStats - {title}'.format(title=title))
    plot.title(title, y=1.08)
    plot.pie(values, labels=slice_labels, colors=colours, explode=explode)
    plot.gcf().gca().add_artist(plot.Circle((0, 0), 0.70, fc='white'))

    plot.axis('equal')
    plot.tight_layout()
    plot.show()
