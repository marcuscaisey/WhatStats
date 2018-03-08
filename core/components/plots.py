import matplotlib.pyplot as plot
from random import randrange

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
    '#818fa0',  # Regent Gray
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


def show_bar_chart(data, x_label='', y_label='', title=''):
    """Show bar chart of data."""
    plot.figure('WhatsApp Statistics')
    plot.box(on=False)
    plot.title(title)
    index = [i for i in range(len(data[0]))]
    plot.bar(index, data[1], color=colour_list(len(data[0])))
    plot.xlabel(x_label)
    plot.ylabel(y_label)
    plot.xticks(index, data[0], rotation=30)
    for i in index:
        plot.text(i, data[1][i], data[1][i], horizontalalignment='center')
    plot.show()
