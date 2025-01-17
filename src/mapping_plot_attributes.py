##### Y-AXIS INTERVALS vs. PLOT HEIGHT #####

n_yintervals_map = {
    'min': {
        100: 3,
        150: 3,
        200: 4,
        250: 5,
        300: 5,
        350: 5,
        400: 5,        
        450: 5,
        500: 5,        
        550: 6,
        600: 6,
        650: 6,        
        700: 7,
        750: 7,
        800: 7,
        850: 7,        
        900: 8,
        950: 8,
        1000: 8        
    },
    'max': {
        100: 6,
        150: 7,
        200: 8,
        250: 10,
        300: 12,
        350: 12,
        400: 13,
        450: 14,
        500: 14,
        550: 15,
        600: 15,
        650: 15,
        700: 16,
        750: 16,
        800: 17,
        850: 17,        
        900: 18,
        950: 19,
        1000: 19        
    }
}

n_xticks_map = {
    'width_slope': 31
} 

##### LEGEND MAPS #####

tripledeck_legendtitle = {
    1: 'UPPER DECK',
    2: 'MIDDLE DECK',
    3: 'LOWER DECK'
} 

legend_gap = {
    # NOTE: The coefficients below come from linear regression analysis    
    'double': {
        'intercept': -118.3,
        'slope_upper': 0.94258,
        'slope_lower': 0.17954
    },   
    'triple': {
        'intercept': -177.0,
        'slope_upper': 1,
        'slope_lower': 2
    }
}

##### MAIN COLOR THEMES #####

theme_style = {

    'dark': {

        'template':                 'plotly_dark',
        'basecolor':                'rgba(0, 191, 255, 1)',  # deepskyblue
        'green_color':              'rgba(50, 205, 50, 1)',  # limegreen
        'red_color':                'rgba(255, 0, 0, 1)',    # red
        'signal_color':             'gold',
        'diff_green_linecolor':     'green',
        'diff_red_linecolor':       'darkred',
        'diff_green_fillcolor':     'rgba(50, 205, 50, 0.75)',  # limegreen
        'diff_red_fillcolor':       'rgba(255, 0, 0, 0.7)',     # red
        'rsi_linecolor':            'gold',
        'kline_linecolor':          'orange',
        'dline_linecolor':          'darkorchid',
        'oversold_linecolor':       'saddlebrown',
        'oversold_fillcolor':       'rgba(255, 225, 150, 0.3)',
        'overbought_linecolor':     'firebrick',
        'overbought_fillcolor':     'rgba(255, 192, 203, 0.4)',
        'x_gridcolor':              '#283442',
        'y_gridcolor':              '#283442',
        'x_linecolor':              '#506784',
        'y_linecolor':              '#506784',

        'drawdown_colors': {
            'red': {
                'fill':     'rgba(255, 0, 0, 1)',     # red
                'border':   'rgba(165, 42, 42, 1)'    # brown
            },
            'green': {
                'fill':     'rgba(50, 205, 50, 1)',   # limegreen
                'border':   'rgba(0, 100, 0, 1)'      # darkgreen
            },
            'yellow': {
                'fill':     'rgba(255, 215, 0, 1)',   # gold
                'border':   'rgba(184, 134, 11, 1)'   # darkgoldenrod
            },
            'blue': {
                'fill':     'rgba(0, 191, 255, 1)',   # deepskyblue
                'border':   'rgba(0, 50, 160, 1)'     #
            },
            'purple': {
                'fill':     'rgba(205, 35, 230, 1)',  # 
                'border':   'rgba(90, 0, 130, 1)'     #
            },
            'orange': {
                'fill':     'rgba(255, 150, 0, 1)',   # 
                'border':   'rgba(115, 55, 0, 1)'     #
            },
            'silver': {
                'fill':     'rgba(200, 230, 240, 1)', # 
                'border':   'rgba(80, 80, 80, 1)'     #
            }
        },

        'overlay_color_theme': {
            'base': [
                'rgba(0, 191, 255, 1)',     # deepskyblue
                'rgba(255, 0, 0, 1)',       # red
                'rgba(50, 205, 50, 1)',     # limegreen
                'rgba(255, 165, 0, 1)',     # orange
                'rgba(153, 50, 204, 1)',    # darkorchid
                'rgba(139, 69, 19, 1)'      # saddlebrown
            ],
            'gold': [
                'rgba(184, 134, 11, 1)',   # darkgoldenrod
                'rgba(218, 165, 32, 1)',   # goldenrod
                'rgba(255, 215, 0, 1)',    # gold
                'rgba(240, 230, 140, 1)',  # khaki
                'rgba(238, 232, 170, 1)',  # palegoldenrod
                'rgba(255, 250, 205, 1)'   # lemonchiffon
            ],
            'turquoise': [
                # NEEDS ADJUSTMENT - expand the color scale
                'rgba(32, 178, 170, 1)',   # lightseagreen
                'rgba(72, 209, 204, 1)',   # mediumturquoise
                # 'rgba(64, 224, 208, 1)',   # turquoise
                'rgba(64, 224, 228, 1)',   # turquoise
                'rgba(117, 255, 222, 1)',  # aquamarine
                'rgba(175, 238, 238, 1)',  # paleturquoise
                'rgba(224, 255, 255, 1)'   # lightcyan
            ],
            'seagreen': [
                'rgba(36, 119, 70, 1)',
                'rgba(66, 134, 79, 1)',
                'rgba(98, 150, 98, 1)',
                'rgba(158, 250, 158, 1)',
                'rgba(182, 251, 182, 1)',
                'rgba(204, 253, 204, 1)'
            ],
            # https://www.schemecolor.com/everything-green.php
            'grasslands': [
                'rgba(13, 91, 17, 1)',      # Royal Green
                'rgba(24, 124, 25, 1)',     # Verse Green
                'rgba(105, 180, 30, 1)',    # RYB Green
                'rgba(141, 199, 30, 1)',    # Dark Lemon Green
                'rgba(174, 203, 51, 1)',    # Android Green darkened
                'rgba(202, 236, 128, 1)'    # Crayola Yellow Green darkened
            ],
            # https://www.schemecolor.com/clean-blues.php
            'sapphire': [
                'rgba(16, 84, 190, 1)',     # sapphire
                'rgba(41, 117, 217, 1)',    # lightened sapphire
                'rgba(65, 149, 244, 1)',    # brilliant azure
                'rgba(106, 195, 244, 1)',   # maya blue
                'rgba(153, 225, 249, 1)',   # winter wizard
                'rgba(204, 248, 254, 1)'    # water
            ],     
            # https://www.schemecolor.com/dreamy-light-coral.php
            'coral': [
                'rgba(205, 92, 92, 1)',     # indianred
                'rgba(234, 121, 121, 1)',   # light coral
                'rgba(250, 161, 155, 1)',   # light salmon pink
                'rgba(245, 188, 184, 1)',   # Spanish pink
                'rgba(245, 206, 184, 1)',   # apricot
                'rgba(245, 226, 204, 1)'    # apricot lightened
            ],
            # https://www.schemecolor.com/deep-peach-brown.php
            'sienna': [
                'rgba(102, 66, 40, 1)',     # cologne earth brown
                'rgba(156, 108, 75, 1)',    # dirt
                'rgba(193, 146, 107, 1)',   # camel
                'rgba(255, 228, 180, 1)',   # peach
                'rgba(210, 120, 100, 1)',   # deep peach
                'rgba(175, 89, 62, 1)'      # crayola's brown
            ],
            # https://www.schemecolor.com/pastel-lavender-gradient.php
            'lavender': [
                # NEEDS ADJUSTING
                'rgba(115, 79, 150, 1)',    # dark lavender
                'rgba(190, 148, 230, 1)',   # bright lavender
                'rgba(204, 167, 236, 1)',   # bright ube
                'rgba(225, 197, 252, 1)',   # pale lavender
                'rgba(230, 213, 255, 1)',   # paler lavender
                'rgba(233, 225, 252, 1)'    # lavender
            ],
            # https://www.schemecolor.com/love-gradient.php
            'magenta': [
                'rgba(170, 14, 87, 1)',     # jazzbery jam
                'rgba(209, 40, 122, 1)',    # magenta dye
                'rgba(249, 66, 158, 1)',    # rose bonbon
                'rgba(253, 100, 194, 1)',   # lightened rose bonbon
                'rgba(255, 130, 206, 1)',   # double lightened rose bonbon
                'rgba(255, 165, 220, 1)'    # triple lightened rose bonbon                
            ],
            'rainbow': [
                'rgba(255, 0, 0, 1)',     # red
                'rgba(255, 165, 0, 1)',   # orange
                'rgba(255, 255, 0, 1)',   # yellow
                # 'rgba(0, 255, 0, 1)',   # lime
                'rgba(34, 139, 34, 1)',   # forestgreen
                # 'rgba(0, 191, 255, 1)', # deepskyblue
                'rgba(30, 144, 255, 1)',  # dodgerblue
                'rgba(148, 0, 211, 1)'    # darkviolet
            ],
            'tableau': [
                'rgba(255, 187, 120, 1)',  # light orange
                'rgba(197, 176, 213, 1)',  # light purple
                'rgba(196, 156, 148, 1)',  # light brown
                'rgba(199, 199, 199, 1)',  # light grey
                'rgba(219, 219, 141, 1)',  # light olive
                'rgba(158, 218, 229, 1)'   # light cyan
            ],
            # 'silver': [
            #     'rgba(55, 55, 55, 1)',  #
            #     'rgba(95, 95, 95, 1)',  #
            #     'rgba(135, 135, 135, 1)',  # 
            #     'rgba(175, 175, 175, 1)',  #
            #     'rgba(215, 215, 215, 1)',  # 
            #     'rgba(255, 255, 255, 1)'   #
            # ]
            'silver': [
                'rgba(50, 50, 75, 1)',  #
                'rgba(90, 90, 110, 1)',  #
                'rgba(130, 130, 145, 1)',  # 
                'rgba(170, 170, 195 1)',  #
                'rgba(210, 210, 235, 1)',  # 
                'rgba(240, 240, 255, 1)'   #
            ]
        },
        
        'overlay_color_selection': {
        # for each color_theme, keys = number of overlays, values = list of corresponding colors
            'base': {
                1: [0],
                2: [0, 3],
                3: [0, 3, 4],
                4: [0, 2, 3, 4],
                5: [0, 1, 2, 3, 4],
                6: [0, 1, 2, 3, 4, 5]
            },        
            'gold': {
                1: [2],                 # goldenrod
                2: [5, 2],              # palegoldenrod, goldenrod
                3: [5, 2, 0],           # palegoldenrod, goldenrod, sienna
                4: [5, 3, 2, 0],        # palegoldenrod, gold, goldenrod, sienna                
                5: [5, 3, 2, 1, 0],     # palegoldenrod, gold, goldenrod, darkgoldenrod, sienna
                6: [5, 4, 3, 2, 1, 0]   # palegoldenrod, palegoldenrod, gold, goldenrod, darkgoldenrod, sienna
            },
            'turquoise': {
                1: [2],                 # mediumturquoise
                2: [5, 2],              # paleturquoise, mediumturquoise
                3: [5, 2, 0],           # paleturquoise, mediumturquoise, teal
                4: [5, 3, 2, 0],        # paleturquoise, turquoise, mediumturquoise, teal
                5: [5, 3, 2, 1, 0],     # paleturquoise, turquoise, mediumturquoise, lightseagreen, teal
                6: [5, 4, 3, 2, 1, 0]   # paleturquoise, aquamarine, turquoise, mediumturquoise, lightseagreen, teal
            },
            'seagreen': {
                1: [3],                 # darkseagreen
                2: [5, 2],              # lightgreen lightened, mediumseagreen
                3: [5, 2, 0],           # lightgreen lightened, mediumseagreen, darkgreen
                4: [5, 3, 2, 0],        # lightgreen lightened, darkseagreen, mediumseagreen, darkgreen
                5: [5, 3, 2, 1, 0],     # lightgreen lightened, darkseagreen, mediumseagreen, seagreen, darkgreen
                6: [5, 4, 3, 2, 1, 0]   # lightgreen lightened, lightgreen, darkseagreen, mediumseagreen, seagreen, darkgreen
            },
            'grasslands': {
                1: [3],                 # 
                2: [5, 2],              # 
                3: [5, 2, 0],           # 
                4: [5, 3, 2, 0],        # 
                5: [5, 3, 2, 1, 0],     # 
                6: [5, 4, 3, 2, 1, 0]   # 
            },
            'sapphire': {
                1: [2],                 # sapphire
                2: [5, 2],              # winter wizard, sapphire
                3: [5, 2, 0],           # winter wizard, sapphire, darkened sapphire
                4: [5, 3, 2, 0],        # winter wizard, brilliant azure, sapphire, darkened sapphire
                5: [5, 4, 3, 2, 0],     # winter wizard, maya blue, brilliant azure, sapphire, darkened sapphire
                6: [5, 4, 3, 2, 1, 0]   # winter wizard, maya blue, brilliant azure, sapphire, slightly darkened sapphire, darkened sapphire
            },
            'coral': {
                1: [2],                 # light salmon pink 
                2: [5, 2],              # apricot lightened, light salmon pink
                3: [5, 2, 0],           # apricot lightened, light salmon pink, indianred
                4: [5, 2, 1, 0],        # apricot lightened, light coral, light salmon pink, indianred
                5: [5, 3, 2, 1, 0],     # apricot lightened, Spanish pink, light coral, light salmon pink, indianred
                6: [5, 4, 3, 2, 1, 0]   # apricot lightened, apricot, Spanish pink, light coral, light salmon pink, indianred
            },
            'sienna': {
                1: [2],                 # camel
                2: [3, 1],              # darkened peach, dirt
                3: [3, 1, 0],           # darkened peach, dirt, cologne earth brown
                4: [3, 2, 1, 0],        # darkened peach, camel, dirt, cologne earth brown
                5: [4, 3, 2, 1, 0],     # darkened peach, camel, dirt, cologne earth brown, deep peach
                6: [5, 4, 3, 2, 1, 0]   # darkened peach, camel, dirt, cologne earth brown, deep peach, crayola's brown
            },
            'lavender': {
                1: [2],                 # royal purple
                2: [5, 2],              # bright ube, royal purple
                3: [5, 2, 0],           # bright ube, royal purple, cyber grape
                4: [5, 2, 1, 0],        # bright ube, royal purple, dark lavender, cyber grape
                5: [5, 3, 2, 1, 0],     # bright ube, rich lavender, royal purple, dark lavender, cyber grape
                6: [5, 4, 3, 2, 1, 0]   # bright ube, floral lavender, rich lavender, royal purple, dark lavender, cyber grape
            },
            'magenta': {
                1: [2],                 # lightened magenta dye
                2: [5, 2],              # double lightened rose bonbon, lightened magenta dye
                3: [5, 2, 0],           # double lightened rose bonbon, lightened magenta dye, jazzbery jam
                4: [5, 3, 2, 0],        # double lightened rose bonbon, rose bonbon, lightened magenta dye, jazzbery jam
                5: [5, 3, 2, 1, 0],     # double lightened rose bonbon, rose bonbon, lightened magenta dye, darkened magenta dye, jazzbery jam
                6: [5, 4, 3, 2, 1, 0]   # double lightened rose bonbon, lightened rose bonbon, rose bonbon, lightened magenta dye, darkened magenta dye, jazzbery jam
            },
            'rainbow': {
                1: [2],                 # gold
                2: [2, 5],              # gold, purple
                3: [2, 3, 5],           # gold, limegreen, purple
                4: [0, 2, 3, 5],        # red, gold, limegreen, purple
                5: [0, 2, 3, 4, 5],     # red, gold, limegreen, royalblue, purple
                6: [0, 1, 2, 3, 4, 5]   # red, darkorange, gold, limegreen, royalblue, purple
            },
            'tableau': {
                1: [5],                 # light cyan
                2: [5, 4],              # light olive
                3: [5, 4, 3],           # light grey
                4: [5, 4, 3, 2],        # light brown
                5: [5, 4, 3, 2, 1],     # light purple
                6: [5, 4, 3, 2, 1, 0]   # light orange
            },
            'silver': {
                1: [2],                 # 
                2: [5, 2],              # 
                3: [5, 2, 0],           # 
                4: [5, 3, 2, 0],        #
                5: [5, 3, 2, 1, 0],     #
                6: [5, 4, 3, 2, 1, 0]   #
            }
        }
    },

    'light': {

        'template':                 'plotly',
        'basecolor':                'rgba(31, 119, 180, 1)',  # '#1f77b4'
        'green_color':              'rgba(0, 128, 0, 1)',     # green
        'red_color':                'rgba(178, 34, 34, 1)',   # firebrick
        'signal_color':             'orange',
        'diff_green_linecolor':     'darkgreen',
        'diff_red_linecolor':       'darkred',
        'diff_green_fillcolor':     'rgba(0, 155, 0, 0.85)',     # green
        'diff_red_fillcolor':       'rgba(178, 34, 34, 0.85)',   # firebrick
        'rsi_linecolor':            'goldenrod',
        'kline_linecolor':          'darkorange',
        'dline_linecolor':          'purple',
        'oversold_linecolor':       'rgba(125, 75, 25, 1)',
        'oversold_fillcolor':       'rgba(205, 165, 75, 0.3)',
        'overbought_linecolor':     'rgba(138, 34, 54, 1)',
        'overbought_fillcolor':     'rgba(225, 142, 153, 0.3)',
        'x_gridcolor':              'grey',
        'y_gridcolor':              'grey',
        'x_linecolor':              'black',
        'y_linecolor':              'black',

        'drawdown_colors': {
            'red': {
                'fill':     'rgba(178, 34, 34, 1)',   # firebrick
                'border':   'rgba(165, 42, 42, 1)'    # brown
            },
            'green': {
                'fill':     'rgba(25, 185, 25, 1)',   # limegreen
                'border':   'rgba(0, 100, 0, 1)'      # darkgreen
            },
            'yellow': {
                'fill':     'rgba(205, 180, 0, 1)',   # gold
                'border':   'rgba(180, 124, 8, 1)'    # darkgoldenrod
            },
            'blue': {
                'fill':     'rgba(0, 175, 235, 1)',   # deepskyblue
                'border':   'rgba(0, 50, 160, 1)'     #
            },
            'purple': {
                'fill':     'rgba(190, 30, 220, 1)',  # 
                'border':   'rgba(90, 0, 130, 1)'     #
            },
            'orange': {
                'fill':     'rgba(225, 100, 0, 1)',   # 
                'border':   'rgba(115, 55, 0, 1)'     #
            },
            'silver': {
                'fill':     'rgba(65, 85, 105, 1)', # 
                'border':   'rgba(10, 10, 10, 1)'     #
            }
        },

        'overlay_color_theme': {
            'base': [
                'rgba(31, 119, 180, 1)',    # '#1f77b4', base blue
                'rgba(178, 34, 34, 1)',     # firebrick
                'rgba(0, 128, 0, 1)',       # green
                'rgba(255, 140, 0, 1)',     # darkorange
                'rgba(102, 51, 153, 1)',    # rebecca purple
                'rgba(125, 75, 25, 1)'      # oversold line color
            ],
            'gold': [                
                'rgba(160, 92, 45, 1)',   # sienna modified
                'rgba(180, 124, 8, 1)',   # darkgoldenrod modified
                'rgba(210, 155, 12, 1)',  # goldenrod modified
                'rgba(226, 190, 0, 1)',   # gold modified
                'rgba(238, 210, 90, 1)',  # khaki modified
                'rgba(245, 218, 140, 1)'  # palegoldenrod modified
            ],
            'turquoise': [
                'rgba(0, 128, 138, 1)',    # teal modified
                'rgba(30, 172, 168, 1)',   # lightseagreen modified
                'rgba(64, 202, 200, 1)',   # mediumturquoise modified
                'rgba(60, 227, 205, 1)',   # turquoise modified
                'rgba(122, 245, 207, 1)',  # aquamarine modified
                'rgba(160, 237, 222, 1)'   # paleturquoise modified
            ],
            'seagreen': [
                'rgba(0, 100, 0, 1)',      # darkgreen modified
                'rgba(46, 139, 87, 1)',    # seagreen modified
                'rgba(60, 179, 113, 1)',   # mediumseagreen modified
                'rgba(110, 200, 140, 1)',  # darkseagreen modified
                'rgba(142, 228, 138, 1)',  # lightgreen modified
                'rgba(164, 244, 164, 1)'   # lightgreen lightened modified
            ],
            # https://www.schemecolor.com/everything-green.php
            'grasslands': [
                'rgba(10, 70, 13, 1)',       # Royal Green darkened
                'rgba(13, 91, 17, 1)',      # Royal Green
                'rgba(24, 124, 25, 1)',     # Verse Green
                'rgba(105, 180, 30, 1)',    # RYB Green
                'rgba(141, 199, 30, 1)',    # Dark Lemon Green
                'rgba(184, 213, 61, 1)'     # Android Green
            ],
            # https://www.schemecolor.com/clean-blues.php
            'sapphire': [
                'rgba(8, 42, 95, 1)',      # darkened sapphire
                'rgba(12, 65, 153, 1)',    # slightly darkened sapphire
                'rgba(18, 88, 198, 1)',    # sapphire
                'rgba(65, 149, 244, 1)',   # brilliant azure
                'rgba(106, 195, 244, 1)',  # maya blue
                'rgba(153, 225, 249, 1)'   # winter wizard
            ],
            # https://www.schemecolor.com/coral-roses.php
            'coral': [
                'rgba(184, 92, 102, 1)',   # twilight lavender modified
                'rgba(202, 112, 121, 1)',  # china rose modified
                'rgba(240, 136, 132, 1)',  # light coral modified
                'rgba(245, 167, 152, 1)',  # light salmon pink modified
                'rgba(255, 191, 168, 1)',  # melon modified
                'rgba(245, 206, 184, 1)'   # apricot modified
            ],
            # https://www.schemecolor.com/deep-peach-brown.php
            'sienna': [
                'rgba(118, 80, 45, 1)',    # cologne earth brown modified
                'rgba(155, 105, 70, 1)',   # dirt modified
                'rgba(193, 146, 107, 1)',  # camel modified
                'rgba(240, 182, 130, 1)',  # darkened peach modified
                'rgba(210, 130, 100, 1)',  # deep peach modified
                'rgba(175, 89, 62, 1)'     # crayola's brown modified
            ],
            # https://www.schemecolor.com/dark-lavender-monochromatic.php
            'lavender': [
                'rgba(95, 60, 122, 1)',    # cyber grape modified
                'rgba(113, 78, 147, 1)',   # dark lavender modified
                'rgba(134, 93, 175, 1)',   # royal purple modified
                'rgba(169, 109, 209, 1)',  # rich lavender modified
                'rgba(181, 126, 228, 1)',  # floral lavender modified
                'rgba(204, 167, 236, 1)'   # bright ube modified
            ],
            # https://www.schemecolor.com/love-gradient.php
            'magenta': [
                'rgba(170, 14, 87, 1)',    # jazzbery jam
                'rgba(199, 30, 110, 1)',   # darkened magenta dye
                'rgba(219, 50, 152, 1)',   # lightened magenta dye
                'rgba(249, 66, 158, 1)',   # rose bonbon
                'rgba(253, 100, 194, 1)',  # lightened rose bonbon
                'rgba(255, 130, 206, 1)'   # double lightened rose bonbon
            ],
            'rainbow': [
                'rgba(178, 34, 34, 1)',    # firebrick
                'rgba(255, 140, 0, 1)',    # darkorange
                'rgba(255, 215, 0, 1)',    # gold
                'rgba(50, 205, 50, 1)',    # limegreen
                'rgba(65, 105, 225, 1)',   # royalblue
                'rgba(128, 0, 128, 1)'     # purple
            ],
            'tableau': [
                'rgba(255, 127, 14, 1)',   # orange
                'rgba(148, 103, 189, 1)',  # purple
                'rgba(140, 86, 75, 1)',    # brown
                'rgba(127, 127, 127, 1)',  # grey
                'rgba(188, 189, 34, 1)',   # olive
                'rgba(23, 190, 207, 1)'    # cyan
            ],
            'silver': [
                'rgba(70, 70, 70, 1)'      #
                'rgba(100, 100, 100, 1)',  #
                'rgba(130, 130, 130, 1)',  #
                'rgba(160, 160, 160, 1)',  # 
                'rgba(190, 190, 190, 1)',  #
                'rgba(220, 220, 220, 1)',  # 
            ]
        },

        'overlay_color_selection': {
        # for each color_theme, keys = number of overlays, values = list of corresponding colors
            'base': {
                1: [0],
                2: [0, 3],
                3: [0, 3, 4],
                4: [0, 2, 3, 4],
                5: [0, 1, 2, 3, 4],
                6: [0, 1, 2, 3, 4, 5]
            },
            'gold': {
                1: [3],
                2: [0, 3],
                3: [0, 2, 4],
                4: [0, 2, 3, 4],
                5: [0, 1, 2, 3, 4],
                6: [0, 1, 2, 3, 4, 5]
            },
            'turquoise': {
                1: [0],                 # 
                2: [0, 2],              # 
                3: [0, 2, 4],           # 
                4: [0, 2, 3, 4],        # 
                5: [0, 1, 2, 3, 4],     # 
                6: [0, 1, 2, 3, 4, 5]   # 
            },
            'seagreen': {
                1: [1],                 # 
                2: [1, 3],              # 
                3: [0, 2, 4],           # 
                4: [0, 2, 3, 4],        # 
                5: [0, 1, 2, 3, 4],     # 
                6: [0, 1, 2, 3, 4, 5]   # 
            },
            'grasslands': {
                1: [1],                 # 
                2: [1, 3],              # 
                3: [0, 2, 4],           # 
                4: [0, 2, 3, 4],        # 
                5: [0, 1, 2, 3, 4],     # 
                6: [0, 1, 2, 3, 4, 5]   # 
            },
            'sapphire': {
                1: [1],                 # 
                2: [1, 3],              # 
                3: [1, 3, 5],           # 
                4: [1, 2, 3, 5],        # 
                5: [1, 2, 3, 4, 5],     # 
                6: [0, 1, 2, 3, 4, 5]   # 
            },
            'coral': {
                1: [0],                 # 
                2: [0, 3],              # 
                3: [0, 2, 4],           # 
                4: [0, 1, 2, 4],        # 
                5: [0, 1, 2, 3, 4],     # 
                6: [0, 1, 2, 3, 4, 5]   # 
            },
            'sienna': {
                1: [0],                 #
                2: [0, 3],              #
                3: [0, 2, 4],           #
                4: [0, 1, 2, 4],        #
                5: [0, 1, 2, 3, 4],     #
                6: [0, 1, 2, 3, 4, 5]   #
            },
            'lavender': {
                1: [1],                 # 
                2: [1, 4],              # 
                3: [0, 2, 4],           # 
                4: [0, 2, 3, 4],        # 
                5: [0, 1, 2, 3, 4],     # 
                6: [0, 1, 2, 3, 4, 5]   # 
            },
            'magenta': {
                1: [0],                 # 
                2: [0, 3],              # 
                3: [0, 2, 4],           # 
                4: [0, 1, 3, 4],        # 
                5: [0, 1, 2, 3, 4],     # 
                6: [0, 1, 2, 3, 4, 5]   # 
            },
            'rainbow': {
                1: [0],                 #
                2: [4, 2],              #
                3: [4, 2, 1],           #
                4: [4, 3, 2, 1],        #
                5: [4, 3, 2, 1, 0],     #
                6: [0, 1, 2, 3, 4, 5]   #
            },
            'tableau': {
                1: [0],                 # cyan
                2: [0, 1],              # olive
                3: [0, 1, 2],           # grey
                4: [0, 1, 2, 3],        # brown
                5: [0, 1, 2, 3, 4],     # purple
                6: [0, 1, 2, 3, 4, 5]   # orange
            },
            'silver': {
                1: [1],                 # 
                2: [3, 1],              # 
                3: [3, 1, 0],           # 
                4: [3, 2, 1, 0],        #
                5: [4, 3, 2, 1, 0],     #
                6: [5, 4, 3, 2, 1, 0]   #
            }

        }
    }
}