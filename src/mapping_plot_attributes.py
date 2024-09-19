theme_style = {

    'dark': {

        'template':                 'plotly_dark',
        'basecolor':                'deepskyblue',
        'green_color':              'limegreen',        # rgb(50, 205, 50)
        'red_color':                'red',              # rgb(255, 0, 0)
        'signal_color':             'gold',
        'diff_green_linecolor':     'green',
        'diff_red_linecolor':       'darkred',
        'diff_green_fillcolor':     'rgba(50, 205, 50, 0.75)',  # limegreen
        'diff_red_fillcolor':       'rgba(255, 0, 0, 0.7)',    # red
        'rsi_30_linecolor':         'saddlebrown',
        'rsi_30_fillcolor':         'rgba(255, 255, 200, 0.3)',
        'rsi_70_linecolor':         'firebrick',
        'rsi_70_fillcolor':         'rgba(255, 192, 203, 0.4)',
        'x_gridcolor':              '#283442',
        'y_gridcolor':              '#283442',
        'x_linecolor':              '#506784',
        'y_linecolor':              '#506784',

        'overlay_color_theme': {
            'gold': [
                'darkgoldenrod',
                'goldenrod',
                'gold',
                'khaki',
                'palegoldenrod',
                'lemonchiffon'
            ],
            'turquoise': [
                # NEEDS ADJUSTMENT - expand the color scale
                'lightseagreen',
                'mediumturquoise',
                'turquoise',
                'aquamarine',
                'paleturquoise',
                'lightcyan'
            ],
            'seagreen': [
                'rgb(36, 119, 70)',
                'rgb(66, 134, 79)',
                'rgb(98, 150, 98)',
                'rgb(158, 250, 158)',
                'rgb(182, 251, 182)',
                'rgb(204, 253, 204)'
            ],
            # https://www.schemecolor.com/clean-blues.php
            'sapphire': [
                'rgb(16, 84, 190)',     # sapphire
                'rgb(41, 117, 217)',    # lightened sapphire
                'rgb(65, 149, 244)',    # brilliant azure
                'rgb(106, 195, 244)',   # maya blue
                'rgb(153, 225, 249)',   # winter wizard
                'rgb(204, 248, 254)'    # water
            ],            
            # https://www.schemecolor.com/dreamy-light-coral.php
            'coral': [
                'indianred',
                'rgb(234, 121, 121)',   # light coral
                'rgb(250, 161, 155)',   # light salmon pink
                'rgb(245, 188, 184)',   # Spanish pink
                'rgb(245, 206, 184)',   # apricot
                'rgb(245, 226, 204)'    # apricot lightened
            ],
            # https://www.schemecolor.com/deep-peach-brown.php
            'sienna': [
                'rgb(102, 66, 40)',     # cologne earth brown
                'rgb(156, 108, 75)',    # dirt
                'rgb(193, 146, 107)',   # camel
                'rgb(255, 228, 180)',   # peach
                'rgb(210, 120, 100)',   # deep peach
                'rgb(175, 89, 62)'      # crayola's brown
            ],
            # https://www.schemecolor.com/pastel-lavender-gradient.php
            'lavender': [
                # NEEDS ADJUSTING
                'rgb(115, 79, 150)',    # dark lavender
                'rgb(190, 148, 230)',   # bright lavender
                'rgb(204, 167, 236)',   # bright ube
                'rgb(225, 197, 252)',   # pale lavender
                'rgb(230, 213, 255)',   # paler lavender
                'rgb(233, 225, 252)'    # lavender
            ],
            # https://www.schemecolor.com/love-gradient.php
            'magenta': [
                'rgb(170, 14, 87)',     # jazzbery jam
                'rgb(209, 40, 122)',    # magenta dye
                'rgb(249, 66, 158)',    # rose bonbon
                'rgb(253, 100, 194)',   # lightened rose bonbon
                'rgb(255, 130, 206)',   # double lightened rose bonbon
                'rgb(255, 165, 220)'    # triple lightened rose bonbon                
            ],
            'rainbow': [
                'red',
                'orange',
                'yellow',
                # 'lime',
                'forestgreen',
                # 'deepskyblue',
                'dodgerblue',
                'darkviolet'
            ],
            'tableau': [
                'rgb(255, 187, 120)',  # light orange
                'rgb(197, 176, 213)',  # light purple
                'rgb(196, 156, 148)',  # light brown
                'rgb(199, 199, 199)',  # light grey
                'rgb(219, 219, 141)',  # light olive
                'rgb(158, 218, 229)'   # light cyan
            ]
        },
        
        'overlay_color_selection': {
        # for each color_theme, keys = number of overlays, values = list of corresponding colors
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
            }
        }
    },

    'light': {

        'template':                 'plotly',
        'basecolor':                '#1f77b4',
        'green_color':              'green',            # rgb(0, 255, 0)
        'red_color':                'firebrick',        # rgb(178, 34, 34)
        'signal_color':             'orange',
        'diff_green_linecolor':     'darkgreen',
        'diff_red_linecolor':       'darkred',
        #'diff_green_fillcolor':     'rgba(50, 205, 50, 0.75)',  # limegreen
        'diff_green_fillcolor':     'rgba(0, 155, 0, 0.85)',     # green
        # 'diff_red_fillcolor':       'rgba(255, 0, 0, 0.75)',     # red
        'diff_red_fillcolor':       'rgba(178, 34, 34, 0.85)',     # firebrick
        'rsi_30_linecolor':         'rgb(125, 75, 25)',
        'rsi_30_fillcolor':         'rgba(255, 225, 100, 0.3)',
        'rsi_70_linecolor':         'rgb(138, 34, 54)',
        'rsi_70_fillcolor':         'rgba(225, 142, 153, 0.3)',
        'x_gridcolor':              'grey',
        'y_gridcolor':              'grey',
        'x_linecolor':              'black',
        'y_linecolor':              'black',

        'overlay_color_theme': {
            'gold': [
                'sienna',
                'darkgoldenrod',
                'goldenrod',
                'gold',
                'khaki',
                'palegoldenrod'
            ],
            'turquoise': [
                # NEEDS MINOR ADJUSTMENTS: 
                #   - slightly darken 'paleturquoise'
                #   - slightly shift to green and/or lighten 'turquoise'
                'teal',
                'lightseagreen',
                'mediumturquoise',
                'turquoise',
                'aquamarine',
                'paleturquoise'
            ],
            'seagreen': [
                'darkgreen',
                'seagreen',
                'mediumseagreen',
                'darkseagreen',
                'lightgreen',
                'rgb(164, 244, 164)'  # lightgreen lightened
                #'palegreen'
            ],
            # https://www.schemecolor.com/clean-blues.php
            'sapphire': [
                'rgb(8, 42, 95)',  # darkened sapphire
                'rgb(12, 65, 153)',  # slightly darkened sapphire
                'rgb(18, 88, 198)',  # sapphire
                'rgb(65, 149, 244)',  # brilliant azure
                'rgb(106, 195, 244)',  # maya blue
                'rgb(153, 225, 249)'  # winter wizard
            ],
            # https://www.schemecolor.com/coral-roses.php
            'coral': [
                'rgb(184, 92, 102)',  # twilight lavender
                'rgb(202, 112, 121)',  # china rose
                'rgb(240, 136, 132)',  # light coral
                'rgb(245, 167, 152)',  # light salmon pink
                'rgb(255, 191, 168)',  # melon
                'rgb(245, 206, 184)'  # apricot
            ],
            # https://www.schemecolor.com/deep-peach-brown.php
            'sienna': [
                'rgb(102, 66, 40)',  # cologne earth brown
                'rgb(156, 108, 75)',  # dirt
                'rgb(193, 146, 107)',  # camel
                'rgb(235, 202, 150)',  # darkened peach
                'rgb(210, 120, 100)',  # deep peach
                'rgb(175, 89, 62)'   # crayola's brown
            ],
            # https://www.schemecolor.com/dark-lavender-monochromatic.php
            'lavender': [
                # NEEDS ADJUSTING                
                'rgb(98, 68, 128)',  # cyber grape
                'rgb(113, 78, 147)', # dark lavender
                'rgb(134, 93, 175)', # royal purple
                'rgb(169, 109, 209)',  # rich lavender
                'rgb(181, 126, 228)',  # floral lavender
                'rgb(204, 167, 236)'  # bright ube 
            ],
            # https://www.schemecolor.com/love-gradient.php
            'magenta': [
                'rgb(170, 14, 87)', # jazzbery jam
                'rgb(199, 30, 110)',  # darkened magenta dye
                'rgb(219, 50, 152)',  # lightened magenta dye
                'rgb(249, 66, 158)',  # rose bonbon
                'rgb(253, 100, 194)',  # lightened rose bonbon
                'rgb(255, 130, 206)'  # double lightened rose bonbon
            ],
            'rainbow': [
                'firebrick',
                'darkorange',
                'gold',
                'limegreen',
                'royalblue',
                'purple'
            ],
            'tableau': [
                'rgb(255, 127, 14)',   # orange
                'rgb(148, 103, 189)',  # purple
                'rgb(140, 86, 75)',    # brown
                'rgb(127, 127, 127)',  # grey
                'rgb(188, 189, 34)',   # olive
                'rgb(23, 190, 207)'    # cyan
            ]

        },

        'overlay_color_selection': {
        # for each color_theme, keys = number of overlays, values = list of corresponding colors
            'gold': {
                1: [2],
                2: [5, 2],
                3: [5, 2, 0],
                4: [5, 3, 2, 0],
                5: [5, 3, 2, 1, 0],
                6: [5, 4, 3, 2, 1, 0]
            },
                'turquoise': {
                1: [2],                 # 
                2: [4, 2],              # 
                3: [4, 2, 0],           # 
                4: [4, 2, 1, 0],        # 
                5: [4, 3, 2, 1, 0],     # 
                6: [5, 4, 3, 2, 1, 0]   # 
            },
            'seagreen': {
                1: [2],                 # 
                2: [4, 2],              # 
                3: [4, 2, 0],           # 
                4: [4, 2, 1, 0],        # 
                5: [4, 3, 2, 1, 0],     # 
                6: [5, 4, 3, 2, 1, 0]   # 
            },
            'sapphire': {
                1: [2],                 # 
                2: [4, 2],              # 
                3: [4, 2, 0],           # 
                4: [4, 3, 2, 0],        # 
                5: [4, 3, 2, 1, 0],     # 
                6: [5, 4, 3, 2, 1, 0]   # 
            },
            'coral': {
                1: [2],                 # 
                2: [4, 1],              # 
                3: [4, 2, 0],           # 
                4: [4, 2, 1, 0],        # 
                5: [4, 3, 2, 1, 0],     # 
                6: [5, 4, 3, 2, 1, 0]   # 
            },
            'sienna': {
                1: [1],                 #
                2: [3, 1],              #
                3: [3, 1, 0],           #
                4: [3, 2, 1, 0],        #
                5: [4, 3, 2, 1, 0],     #
                6: [5, 4, 3, 2, 1, 0]   #
            },
            'lavender': {
                1: [2],                 # 
                2: [4, 1],              # 
                3: [4, 2, 0],           # 
                4: [4, 2, 1, 0],        # 
                5: [4, 3, 2, 1, 0],     # 
                6: [5, 4, 3, 2, 1, 0]   # 
            },
            'magenta': {
                1: [1],                 # 
                2: [4, 1],              # 
                3: [4, 2, 0],           # 
                4: [4, 2, 1, 0],        # 
                5: [4, 3, 2, 1, 0],     # 
                6: [5, 4, 3, 2, 1, 0]   # 
            },
            'rainbow': {
                1: [1],                 #
                2: [1, 3],              #
                3: [1, 3, 4],           #
                4: [1, 2, 3, 4],        #
                5: [1, 2, 3, 4, 5],     #
                6: [0, 1, 2, 3, 4, 5]   #
            },
            'tableau': {
                1: [5],                 # cyan
                2: [5, 4],              # olive
                3: [5, 4, 3],           # grey
                4: [5, 4, 3, 2],        # brown
                5: [5, 4, 3, 2, 1],     # purple
                6: [5, 4, 3, 2, 1, 0]   # orange
            }
        }
    }
}