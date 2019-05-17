# mk_config.py
#
# Translate default FF.CFG into a C header.
# 
# Written & released by Keir Fraser <keir.xen@gmail.com>
# 
# This is free and unencumbered software released into the public domain.
# See the file COPYING for more details, or visit <http://unlicense.org>.

import re, sys

def main(argv):
    in_f = open(argv[1], "r")
    out_f = open(argv[2], "w")
    out_f.write("/* Autogenerated by " + argv[0] + " */\n")
    for line in in_f:
        match = re.match("[ \t]*([A-Za-z0-9-]+)[ \t]*=[ \t]*"
                         "([A-Za-z0-9-]+|\".*\")", line)
        if match:
            opt = match.group(1)            
            val = match.group(2)
            if opt == "interface":
                val = "FINTF_" + val.upper().replace("-","_")
            elif opt == "pin02" or opt == "pin34":
                val = "PIN_" + val
            elif opt == "track-change":
                val = "TRKCHG_" + val
            elif opt == "host":
                val = "HOST_" + val
            elif opt == "oled-font":
                val = "FONT_" + val
            elif opt == "display-type":
                opts = []
                for x in val.split("-"):
                    size = re.match("([0-9]+)x([0-9]+)", x)
                    if size:
                        w = int(size.group(1))
                        h = int(size.group(2))
                        if w == 128 and h == 64:
                            opts += ['DISPLAY_oled_64']
                        elif h == 2 and w >= 16 and w <= 40:
                            opts += ['DISPLAY_lcd_columns(%d)' % w]
                    else:
                        opts += ['DISPLAY_' + x]
                val = '|'.join(opts)
            elif opt == "image-on-startup":
                val = "IMGS_" + val
            elif opt == "rotary":
                opts = []
                for x in val.split(","):
                    opts += ['ROT_' + x]
                val = '|'.join(opts)
            elif opt == "twobutton-action":
                opts = []
                for x in val.split(","):
                    opts += ['TWOBUTTON_' + x.replace("-","_")]
                val = '|'.join(opts)
            elif opt == "nav-mode":
                val = "NAVMODE_" + val
            elif opt == "folder-sort":
                val = "SORT_" + val
            elif opt == "motor-delay":
                if val == 'ignore':
                    val = "MOTOR_" + val
                else:
                    val = (int(val) + 9) // 10
            else:
                val = {
                    'no': 'FALSE',
                    'yes': 'TRUE'
                }.get(val,val)
            out_f.write("x(%s, %s, %s)\n" % (opt, re.sub('-','_',opt), val))

if __name__ == "__main__":
    main(sys.argv)
