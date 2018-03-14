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
    '#cedaea',  # Periwinkle Gray
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


def messages_sent_labels(chat, start_date, end_date):
    """
    Return title and x/y labels associated with plot of messages sent by
    each member.
    """
    title = 'Messages sent in {subject} ({start_date} - {end_date})'.format(
        subject=chat.subject,
        start_date=start_date,
        # start_date=start_date.FormatDate(),
        # end_date=end_date.FormatDate())
        end_date=end_date)
    x_label = 'Name'
    y_label = 'Messages sent'
    return (title, x_label, y_label)


def show_bar_chart(data, labels):
    """
    Show bar chart of data with given labels, where data is list of
    tuples (x, y) and labels is tuple (title, x_label, y_label).
    """
    plot.figure('WhatStats - {title}'.format(title=labels[0]))
    plot.box(on=False)
    plot.title(labels[0])
    index = [i for i in range(len(data[0]))]
    colours = colour_list(len(data[0]))
    plot.bar(index, data[1], color=colours)
    plot.xlabel(labels[1])
    plot.ylabel(labels[2])
    plot.xticks(index, data[0], rotation=30)
    for i in index:
        plot.text(i, data[1][i], data[1][i], horizontalalignment='center')
    plot.tight_layout()
    plot.show()


def show_pie_chart(data, title):
    """Show pie chart of data tuple (labels, values)."""
    x = data[0]
    y = data[1]
    labels = ['{} ({})'.format(x[i], y[i]) for i in range(len(x))]
    colours = colour_list(len(x))
    explode = [0.05 for _ in range(len(x))]

    plot.figure('WhatStats - {title}'.format(title=title))
    plot.title(title, y=1.05)
    plot.pie(y, labels=labels, colors=colours, explode=explode)
    plot.gcf().gca().add_artist(plot.Circle((0, 0), 0.70, fc='white'))

    plot.axis('equal')
    plot.tight_layout()
    plot.show()
