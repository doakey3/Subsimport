def hexcode_to_color(value):
    """
    Return [float_red, float_green, float_blue]
    for the color given as #rrggbb.
    """
    color = []
    value = value.lstrip('#')

    for i in range(0, len(value), 2):
        color.append(int(value[i:i + 2], 16))

    for i in range(len(color)):
        if color[i] == 255:
            color[i] = 256

        color[i] = color[i] / 256

    return color

if __name__ == '__main__':

    print(hexcode_to_color('#FF0000'))