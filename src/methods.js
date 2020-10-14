const CHEM055 = {
  name: "CHEM-055",
  description: "Metals in tissues",
  elements: [
    "Be",
    "B",
    "Mg",
    "V",
    "Cr",
    "Mn",
    "Fe",
    "Co",
    "Ni",
    "Cu",
    "Zn",
    "As",
    "Se",
    "Mo",
    "Cd",
    "Sn",
    "Sb",
    "Ba",
    "Hg",
    "Tl",
    "Pb"
  ],
  units: [
    "ppm",
    "ppm",
    "ppm",
    "ppm",
    "ppm",
    "ppm",
    "ppm",
    "ppm",
    "ppm",
    "ppm",
    "ppm",
    "ppm",
    "ppm",
    "ppm",
    "ppm",
    "ppm",
    "ppm",
    "ppm",
    "ppm",
    "ppm",
    "ppm"
  ],
  checkStdTolerance: 0.15,
  checkStds: [
    {
      name: "Calibration Check",
      expectedValues: [
        10,
        10,
        10,
        10,
        10,
        10,
        10,
        10,
        10,
        10,
        10,
        10,
        10,
        10,
        10,
        10,
        10,
        10,
        1,
        10,
        10
      ]
    }
  ],
  blanks: [
    {
      name: "Method Blank",
      type: "normal",
      LOQs: [
        0.008,
        0.16,
        4.1,
        0.04,
        0.12,
        0.52,
        8.6,
        0.03,
        0.38,
        0.46,
        2.1,
        0.02,
        0.07,
        0.02,
        0.02,
        0.5,
        0.02,
        0.03,
        0.003,
        0.005,
        0.016
      ]
    }
  ],
  duplicateTolerance: 20,
  calStandards: [0, 0.01, 0.05, 0.25, 0.5, 1, 5, 10, 0.25, 0.5, 1, 5, 10, 50],
  sigFigs: 3,
  referenceMaterials: [
    {
      name: "Bovine Liver",
      rangesLow: [
        null,
        null,
        459.33,
        null,
        null,
        4.46,
        122.62,
        0.14,
        null,
        105.9,
        84.68,
        null,
        0.99,
        3.42,
        0.0335,
        null,
        null,
        null,
        null,
        null,
        0.06
      ],
      rangesHigh: [
        null,
        null,
        558.39,
        null,
        null,
        5.9,
        177.16,
        0.2,
        null,
        149.82,
        110.78,
        null,
        1.53,
        4.68,
        0.06,
        null,
        null,
        null,
        null,
        null,
        0.42
      ]
    },
    {
      name: "TORT-3",
      rangesLow: [
        0.0062,
        2.74,
        942.22,
        7.62,
        1.09,
        13.01,
        148.29,
        0.87,
        4.34,
        416.01,
        114.4,
        55.86,
        9.09,
        2.93,
        35.34,
        null,
        0.0344,
        null,
        0.222,
        0.0076,
        0.17
      ],
      rangesHigh: [
        0.0134,
        3.7,
        1177.78,
        9.18,
        2.35,
        16.49,
        186.69,
        1.11,
        5.66,
        512.37,
        145.6,
        69.66,
        10.95,
        3.65,
        44.4,
        null,
        0.0776,
        null,
        0.34,
        0.0124,
        0.23
      ]
    }
  ]
};

const CHEM057 = {
  name: "CHEM-057",
  description: "Iodine in Milk, Tissue and Feeds",
  elements: ["I"],
  units: ["ppb"],
  checkStdTolerance: 0.15,
  checkStds: [
    {
      name: "500 ppb check",
      expectedValues: [500]
    }
  ],
  blanks: [
    {
      name: "Method Blank",
      type: "any",
      LOQs: [3]
    }
  ],
  duplicateTolerance: 20,
  calStandards: [0, 0.05, 0.1, 0.2, 0.5, 1],
  sigFigs: 3,
  referenceMaterials: [
    {
      name: "Skim Milk Powder",
      rangesLow: [2317],
      rangesHigh: [3229]
    }
  ]
};

const CHEM114 = {
  name: "CHEM-114",
  description: "Metals in soils, biosolids and wastewaters",
  elements: ["Cr", "Co", "Ni", "Cu", "Zn", "As", "Se", "Mo", "Cd", "Hg", "Pb"],
  units: [
    "ppm",
    "ppm",
    "ppm",
    "ppm",
    "ppm",
    "ppm",
    "ppm",
    "ppm",
    "ppm",
    "ppm",
    "ppm"
  ],
  checkStdTolerance: 0.15,
  checkStds: [
    {
      name: "Calibration Check",
      expectedValues: [10, 10, 10, 50, 50, 10, 10, 10, 10, 1, 10]
    }
  ],
  blanks: [
    {
      name: "Solids Blank",
      type: "solids",
      LOQs: [null, null, null, null, null, null, null, null, null, null, null]
    },
    {
      name: "Water Blank",
      type: "waters",
      LOQs: [null, null, null, null, null, null, null, null, null, null, null]
    }
  ],
  duplicateTolerance: 15,
  calStandards: [0, 0.05, 0.1, 0.5, 1, 5, 10, 50],
  sigFigs: 3,
  referenceMaterials: [
    {
      name: "Ref 2b",
      rangesLow: [
        null,
        null,
        null,
        null,
        null,
        null,
        null,
        null,
        null,
        null,
        null
      ],
      rangesHigh: [
        null,
        null,
        null,
        null,
        null,
        null,
        null,
        null,
        null,
        null,
        null
      ]
    }
  ]
};

const CHEM162 = {
  name: "CHEM-162",
  description: "Metals in Blood and Serum",
  elements: ["Mn", "Fe", "Co", "Cu", "Zn", "Se", "Mo", "Pb"],
  units: ["ppb", "ppm", "ppb", "ppm", "ppm", "ppm", "ppb", "ppm"],
  checkStdTolerance: 0.1,
  checkStds: [
    {
      name: "5/50 ppb",
      expectedValues: [5, 50, 5, 50, 50, 5, 5, 5]
    }
  ],
  blanks: [
    {
      name: "Serum Blank",
      type: "serum",
      LOQs: [0.9, 0.013, 0.3, 0.0008, 0.0011, 0.007, 1, null]
    },
    {
      name: "Blood Blank",
      type: "blood",
      LOQs: [null, null, null, null, null, 0.029, null, 0.001]
    }
  ],
  duplicateTolerance: 15,
  calStandards: [0, 0.05, 0.1, 0.25, 0.5, 1, 5, 10, 50, 250],
  sigFigs: 3,
  referenceMaterials: [
    {
      name: "QM-S Q1807",
      rangesLow: [2.23, 0.747, 3.47, 1.03, 0.913, 0.119, 1.11, null],
      rangesHigh: [3.2, 0.851, 4.3, 1.22, 1.16, 0.152, 1.73, null]
    },
    {
      name: "QM-B Q1720",
      rangesLow: [null, null, null, null, null, 0.153, null, 0.102],
      rangesHigh: [null, null, null, null, null, 0.216, null, 0.143]
    }
  ]
};

const TOXI064 = {
  name: "TOXI-064",
  description: "Metals in Food",
  elements: [
    "Be",
    "B",
    "Mg",
    "Al",
    "Ti",
    "Cr",
    "Mn",
    "Fe",
    "Co",
    "Ni",
    "Cu",
    "Zn",
    "As",
    "Se",
    "Mo",
    "Cd",
    "Sn",
    "Sb",
    "Hg",
    "Pb"
  ],
  units: [
    "ppm",
    "ppm",
    "ppm",
    "ppm",
    "ppm",
    "ppm",
    "ppm",
    "ppm",
    "ppm",
    "ppm",
    "ppm",
    "ppm",
    "ppm",
    "ppm",
    "ppm",
    "ppm",
    "ppm",
    "ppm",
    "ppm",
    "ppm"
  ],
  checkStdTolerance: 0.15,
  checkStds: [
    {
      name: "Calibration Check",
      expectedValues: [
        10,
        10,
        10,
        10,
        10,
        10,
        10,
        10,
        10,
        10,
        10,
        10,
        10,
        10,
        10,
        10,
        10,
        10,
        0.5,
        10
      ]
    }
  ],
  blanks: [
    {
      name: "Method Blank",
      type: "any",
      LOQs: [
        0.001,
        0.01,
        0.07,
        0.2,
        0.2,
        0.007,
        0.003,
        0.08,
        0.0003,
        0.007,
        0.01,
        0.3,
        0.002,
        0.02,
        0.0007,
        0.001,
        0.01,
        0.002,
        0.0003,
        0.001
      ]
    },
    {
      name: "Sand Bath Blank",
      type: "sand bath",
      LOQs: [
        0.001,
        0.01,
        0.07,
        0.2,
        0.2,
        0.007,
        0.003,
        0.08,
        0.0003,
        0.007,
        0.01,
        0.3,
        0.002,
        0.02,
        0.0007,
        0.001,
        0.01,
        0.002,
        0.0003,
        0.001
      ]
    }
  ],
  duplicateTolerance: 20,
  calStandards: [
    0,
    0.0001,
    0.001,
    0.005,
    0.01,
    0.02,
    0.0001,
    0.001,
    0.005,
    0.01,
    0.02,
    0.05,
    0.1,
    0.2
  ],
  sigFigs: 3,
  referenceMaterials: [
    {
      name: "Wheat Flour",
      rangesLow: [
        null,
        0.62,
        769.6,
        0.77,
        0.058,
        -0.07,
        23.45,
        27.4,
        0.003,
        0.09,
        2.85,
        19.38,
        null,
        0.66,
        0.54,
        0.04,
        null,
        null,
        null,
        null
      ],
      rangesHigh: [
        null,
        1.58,
        1704,
        5.27,
        0.615,
        0.17,
        46.19,
        54.28,
        0.01,
        0.27,
        6.45,
        46.02,
        null,
        1.98,
        1.38,
        0.1,
        null,
        null,
        null,
        null
      ]
    },
    {
      name: "Dried Potato",
      rangesLow: [
        null,
        2.76,
        727,
        0.18,
        0.74,
        0.031,
        4.06,
        9.37,
        0.02,
        0.116,
        0.02,
        5.99,
        null,
        -0.06,
        -0.05,
        0.152,
        null,
        -0.0005,
        -0.0001,
        -0.0005
      ],
      rangesHigh: [
        null,
        4.02,
        841,
        1.14,
        2.18,
        0.127,
        5.8,
        13.93,
        0.026,
        0.164,
        3.62,
        9.83,
        null,
        0.117,
        0.452,
        0.188,
        null,
        0.0013,
        0.0005,
        0.0025
      ]
    }
  ]
};

const TOXI064Pb = {
  name: "TOXI-064 - Pb only",
  description: "Metals in Food",
  elements: ["Pb"],
  units: ["ppm"],
  checkStdTolerance: 0.15,
  checkStds: [
    {
      name: "Calibration Check",
      expectedValues: [10]
    }
  ],
  blanks: [
    {
      name: "Method Blank",
      type: "any",
      LOQs: [0.004]
    }
  ],
  duplicateTolerance: 20,
  calStandards: [0, 0.0001, 0.001, 0.005, 0.01, 0.02],
  sigFigs: 3,
  referenceMaterials: [
    {
      name: "Control MS",
      rangesLow: [0.324],
      rangesHigh: [0.526]
    }
  ]
};

const CHEM055Alltech = {
  name: "CHEM-055 - Alltech",
  description: "Animal Nutrition Project - Alltech",
  elements: ["Mn", "Fe", "Co", "Cu", "Zn", "Se", "Mo"],
  units: ["ppm", "ppm", "ppm", "ppm", "ppm", "ppm", "ppm"],
  checkStdTolerance: 0.15,
  checkStds: [
    {
      name: "Calibration Check",
      expectedValues: [10, 10, 10, 10, 10, 10, 10]
    }
  ],
  blanks: [
    {
      name: "Method Blank",
      type: "serum",
      LOQs: [0.52, 8.6, 0.03, 0.46, 2.1, 0.07, 0.02]
    }
  ],
  duplicateTolerance: 20,
  calStandards: [0, 0.25, 0.5, 1, 5, 10, 50, 200, 500, 1000],
  sigFigs: 3,
  referenceMaterials: [
    {
      name: "Wheat Flour",
      rangesLow: [23.45, 27.4, 0.003, 2.85, 19.38, 0.66, 0.54],
      rangesHigh: [46.19, 54.28, 0.01, 6.45, 46.02, 1.98, 1.38]
    }
  ]
};

const REEs = {
  name: "REEs",
  description: "Rare Earth Elements in plant extracts and digests",
  elements: ["Ce", "Nd", "Eu"],
  units: ["ppb", "ppb", "ppb"],
  checkStdTolerance: 0.15,
  checkStds: [
    {
      name: "Calibration Check",
      expectedValues: [50, 50, 50]
    }
  ],
  blanks: [
    {
      name: "Method Blank",
      type: "any",
      LOQs: [1, 1, 1]
    }
  ],
  duplicateTolerance: 20,
  calStandards: [0, 0.05, 0.25, 1, 5, 25, 100, 200],
  sigFigs: 3,
  referenceMaterials: []
};

const methods = [
  CHEM055,
  CHEM057,
  CHEM114,
  CHEM162,
  TOXI064,
  TOXI064Pb,
  CHEM055Alltech,
  REEs
];

module.exports = methods;
