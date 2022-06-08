from .error_collection_level import ErrorCollectionLevel


# ISO/IEC 23941:2022 Table 6
data_capacities = {
    'R7x43': {
        'height': 7,
        'width': 43,
        'capacity': {
            'Byte': {
                ErrorCollectionLevel.M: 5,
                ErrorCollectionLevel.H: 2,
            },
        },
    },
    'R7x59': {
        'height': 7,
        'width': 59,
        'capacity': {
            'Byte': {
                ErrorCollectionLevel.M: 11,
                ErrorCollectionLevel.H: 6,
            },
        },
    },
    'R7x77': {
        'height': 7,
        'width': 77,
        'capacity': {
            'Byte': {
                ErrorCollectionLevel.M: 19,
                ErrorCollectionLevel.H: 9,
            },
        },
    },
    'R7x99': {
        'height': 7,
        'width': 99,
        'capacity': {
            'Byte': {
                ErrorCollectionLevel.M: 27,
                ErrorCollectionLevel.H: 13,
            },
        },
    },
    'R7x139': {
        'height': 7,
        'width': 139,
        'capacity': {
            'Byte': {
                ErrorCollectionLevel.M: 42,
                ErrorCollectionLevel.H: 22,
            },
        },
    },
    'R9x43': {
        'height': 9,
        'width': 43,
        'capacity': {
            'Byte': {
                ErrorCollectionLevel.M: 11,
                ErrorCollectionLevel.H: 6,
            },
        },
    },
    'R9x59': {
        'height': 9,
        'width': 59,
        'capacity': {
            'Byte': {
                ErrorCollectionLevel.M: 20,
                ErrorCollectionLevel.H: 10,
            },
        },
    },
    'R9x77': {
        'height': 9,
        'width': 77,
        'capacity': {
            'Byte': {
                ErrorCollectionLevel.M: 30,
                ErrorCollectionLevel.H: 16,
            },
        },
    },
    'R9x99': {
        'height': 9,
        'width': 99,
        'capacity': {
            'Byte': {
                ErrorCollectionLevel.M: 40,
                ErrorCollectionLevel.H: 20,
            },
        },
    },
    'R9x139': {
        'height': 9,
        'width': 139,
        'capacity': {
            'Byte': {
                ErrorCollectionLevel.M: 61,
                ErrorCollectionLevel.H: 31,
            },
        },
    },
    'R11x27': {
        'height': 11,
        'width': 27,
        'capacity': {
            'Byte': {
                ErrorCollectionLevel.M: 6,
                ErrorCollectionLevel.H: 4,
            },
        },
    },
    'R11x43': {
        'height': 11,
        'width': 43,
        'capacity': {
            'Byte': {
                ErrorCollectionLevel.M: 18,
                ErrorCollectionLevel.H: 10,
            },
        },
    },
    'R11x59': {
        'height': 11,
        'width': 59,
        'capacity': {
            'Byte': {
                ErrorCollectionLevel.M: 30,
                ErrorCollectionLevel.H: 14,
            },
        },
    },
    'R11x77': {
        'height': 11,
        'width': 77,
        'capacity': {
            'Byte': {
                ErrorCollectionLevel.M: 41,
                ErrorCollectionLevel.H: 21,
            },
        },
    },
    'R11x99': {
        'height': 11,
        'width': 99,
        'capacity': {
            'Byte': {
                ErrorCollectionLevel.M: 55,
                ErrorCollectionLevel.H: 27,
            },
        },
    },
    'R11x139': {
        'height': 11,
        'width': 139,
        'capacity': {
            'Byte': {
                ErrorCollectionLevel.M: 82,
                ErrorCollectionLevel.H: 40,
            },
        },
    },
    'R13x27': {
        'height': 13,
        'width': 27,
        'capacity': {
            'Byte': {
                ErrorCollectionLevel.M: 11,
                ErrorCollectionLevel.H: 6,
            },
        },
    },
    'R13x43': {
        'height': 13,
        'width': 43,
        'capacity': {
            'Byte': {
                ErrorCollectionLevel.M: 26,
                ErrorCollectionLevel.H: 12,
            },
        },
    },
    'R13x59': {
        'height': 13,
        'width': 59,
        'capacity': {
            'Byte': {
                ErrorCollectionLevel.M: 36,
                ErrorCollectionLevel.H: 18,
            },
        },
    },
    'R13x77': {
        'height': 13,
        'width': 77,
        'capacity': {
            'Byte': {
                ErrorCollectionLevel.M: 51,
                ErrorCollectionLevel.H: 27,
            },
        },
    },
    'R13x99': {
        'height': 13,
        'width': 99,
        'capacity': {
            'Byte': {
                ErrorCollectionLevel.M: 71,
                ErrorCollectionLevel.H: 33,
            },
        },
    },
    'R13x139': {
        'height': 13,
        'width': 139,
        'capacity': {
            'Byte': {
                ErrorCollectionLevel.M: 104,
                ErrorCollectionLevel.H: 52,
            },
        },
    },
    'R15x43': {
        'height': 15,
        'width': 43,
        'capacity': {
            'Byte': {
                ErrorCollectionLevel.M: 31,
                ErrorCollectionLevel.H: 13,
            },
        },
    },
    'R15x59': {
        'height': 15,
        'width': 59,
        'capacity': {
            'Byte': {
                ErrorCollectionLevel.M: 46,
                ErrorCollectionLevel.H: 24,
            },
        },
    },
    'R15x77': {
        'height': 15,
        'width': 77,
        'capacity': {
            'Byte': {
                ErrorCollectionLevel.M: 65,
                ErrorCollectionLevel.H: 29,
            },
        },
    },
    'R15x99': {
        'height': 15,
        'width': 99,
        'capacity': {
            'Byte': {
                ErrorCollectionLevel.M: 86,
                ErrorCollectionLevel.H: 46,
            },
        },
    },
    'R15x139': {
        'height': 15,
        'width': 139,
        'capacity': {
            'Byte': {
                ErrorCollectionLevel.M: 125,
                ErrorCollectionLevel.H: 67,
            },
        },
    },
    'R17x43': {
        'height': 17,
        'width': 43,
        'capacity': {
            'Byte': {
                ErrorCollectionLevel.M: 37,
                ErrorCollectionLevel.H: 19,
            },
        },
    },
    'R17x59': {
        'height': 17,
        'width': 59,
        'capacity': {
            'Byte': {
                ErrorCollectionLevel.M: 54,
                ErrorCollectionLevel.H: 26,
            },
        },
    },
    'R17x77': {
        'height': 17,
        'width': 77,
        'capacity': {
            'Byte': {
                ErrorCollectionLevel.M: 76,
                ErrorCollectionLevel.H: 36,
            },
        },
    },
    'R17x99': {
        'height': 17,
        'width': 99,
        'capacity': {
            'Byte': {
                ErrorCollectionLevel.M: 98,
                ErrorCollectionLevel.H: 54,
            },
        },
    },
    'R17x139': {
        'height': 17,
        'width': 139,
        'capacity': {
            'Byte': {
                ErrorCollectionLevel.M: 150,
                ErrorCollectionLevel.H: 74,
            },
        },
    },
}