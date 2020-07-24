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
  calStandards: [0.05, 0.1, 0.25, 0.5, 1, 5, 10, 50, 250],
  sigFigs: 3,
  referenceMaterials: [
    {
      name: "QM-S Q1807",
      rangesLow: [2.6, 0.7, 3.7, 0.9, 0.9, 0.1, 1.0, null],
      rangesHigh: [3.1, 1.0, 4.2, 1.2, 1.2, 0.15, 1.7, null]
    },
    {
      name: "QM-B Q1720",
      rangesLow: [null, null, null, null, null, 0.15, null, 0.1],
      rangesHigh: [null, null, null, null, null, 0.2, null, 0.14]
    }
  ]
};

const CHEM055 = {
  name: "CHEM-055",
  description: "Metals in Tissues",
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
  calStandards: [0.05, 0.1, 0.25, 0.5, 1, 5, 10, 50, 250],
  sigFigs: 3,
  referenceMaterials: [
    {
      name: "QM-S Q1807",
      rangesLow: [2.6, 0.7, 3.7, 0.9, 0.9, 0.1, 1.0, null],
      rangesHigh: [3.1, 1.0, 4.2, 1.2, 1.2, 0.15, 1.7, null]
    },
    {
      name: "QM-B Q1720",
      rangesLow: [null, null, null, null, null, 0.15, null, 0.1],
      rangesHigh: [null, null, null, null, null, 0.2, null, 0.14]
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
      name: "0.5 ppm check",
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
      rangesLow: [2501],
      rangesHigh: [3200]
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
  checkStdTolerance: 0.1,
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
        0.64,
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
        3.4,
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

const methods = [CHEM162, CHEM057, TOXI064, CHEM055];

module.exports = methods;
