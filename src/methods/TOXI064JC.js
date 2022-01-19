const TOXI064JC = {
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
        0.014,
        0.07,
        0.2,
        0.17,
        0.007,
        0.004,
        0.07,
        0.0007,
        0.007,
        0.01,
        0.23,
        0.0017,
        0.017,
        0.0014,
        0.0014,
        0.014,
        0.002,
        0.0003,
        0.001
      ]
    }
  ],
  duplicateTolerance: 20,
  calStandards: [0, 0.1, 1, 5, 10, 20, 50, 100, 200],
  sigFigs: 3,
  referenceMaterials: [
    {
      name: "Wheat Flour",
      rangesLow: [
        null,
        0.65,
        1233,
        1.48,
        null,
        0.0001,
        31.6,
        35.9,
        0.0046,
        0.138,
        4.02,
        30.6,
        0.0046,
        1.1,
        0.89,
        0.069,
        null,
        null,
        null,
        0.0001
      ],
      rangesHigh: [
        null,
        1.36,
        1671,
        6.28,
        null,
        0.041,
        44.9,
        48.7,
        0.0076,
        0.245,
        5.15,
        40.5,
        0.0084,
        1.33,
        1.0,
        0.082,
        null,
        null,
        null,
        0.0057
      ]
    },
    {
      name: "Dried Potato",
      rangesLow: [
        null,
        1.51,
        744,
        0.449,
        0.015,
        -0.04,
        4.93,
        10.6,
        0.021,
        0.119,
        1.59,
        8.43,
        null,
        null,
        0.159,
        0.162,
        null,
        null,
        null,
        null
      ],
      rangesHigh: [
        null,
        5.73,
        1012,
        0.996,
        0.447,
        0.107,
        7.88,
        14.8,
        0.026,
        0.188,
        2.05,
        12.7,
        null,
        null,
        0.195,
        0.204,
        null,
        null,
        null,
        null
      ]
    },
    {
      name: "Dried Soup",
      rangesLow: [
        null,
        4.49,
        1063,
        5.1,
        0.37,
        0.01,
        9.95,
        26.31,
        0.037,
        0.29,
        3.98,
        22.0,
        0.007,
        0.064,
        0.524,
        0.046,
        null,
        null,
        null,
        0.017
      ],
      rangesHigh: [
        null,
        14.61,
        1605,
        9.79,
        0.83,
        0.24,
        17.94,
        39.37,
        0.046,
        0.47,
        5.59,
        34.3,
        0.01,
        0.13,
        0.638,
        0.061,
        null,
        null,
        null,
        0.025
      ]
    }
  ]
};

export default TOXI064JC;
