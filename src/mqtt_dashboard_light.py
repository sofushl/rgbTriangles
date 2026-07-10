#mqtt dashboard Light tile color-command and brightness-command parser

def parse_color_command(message):
    mode="MONO_COLOR"
    hexstring = message.replace("#","0x")
    decimal = int(hexstring, 16)
    b = decimal % 256
    decimal //= 256
    g = decimal % 256
    r = decimal // 256
    return (r, g, b)

def parse_brightness_command(message):
    return(int(round(int(message)*255/100,0)))