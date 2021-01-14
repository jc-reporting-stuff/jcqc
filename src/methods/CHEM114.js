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
  duplicateTolerance: 20,
  checkStdTolerance: 0.15,
  calStandards: [0, 0.05, 0.1, 0.5, 1, 5, 10, 50],
  sigFigs: 4,
  checkStds: [
    {
      name: "Calibration Check",
      expectedValues: [10, 10, 10, 10, 10, 10, 10, 10, 10, 1, 10]
    }
  ],
  blanks: [
    {
      name: "Solids Blank",
      type: "solids",
      LOQs: [1.9, 0.04, 0.6, 0.4, 3.3, 2.2, 0.3, 0.2, 0.04, 0.04, 0.3]
    },
    {
      name: "Liquids Blank",
      type: "waters",
      LOQs: [
        0.0082,
        0.0004,
        0.0037,
        0.009,
        0.04,
        0.035,
        0.0009,
        0.0006,
        0.0002,
        0.0002,
        0.0011
      ]
    }
  ],
  referenceMaterials: [
    {
      name: "EnviroMAT BE-1",
      rangesLow: [
        34.6,
        5.05,
        17.7,
        233,
        378,
        2.63,
        0.935,
        3.03,
        0.191,
        0.404,
        17.8
      ],
      rangesHigh: [
        81.4,
        7.38,
        32.5,
        367,
        555,
        5.99,
        4.8,
        6.83,
        1.56,
        0.956,
        35.5
      ]
    },
    {
      name: "EnviroMAT CP-1",
      rangesLow: [
        7.66,
        1.78,
        6.42,
        51.7,
        196,
        1.46,
        0.39,
        0.645,
        0.313,
        0.027,
        10.1
      ],
      rangesHigh: [
        24.5,
        4.22,
        15.9,
        100.7,
        300,
        3.02,
        1.408,
        1.78,
        1.124,
        0.257,
        21.1
      ]
    },
    {
      name: "EnviroMAT ES-H",
      rangesLow: [
        0.37,
        0.103,
        0.71,
        0.72,
        0.683,
        0.345,
        0.0259,
        0.347,
        0.19,
        null,
        0.0943
      ],
      rangesHigh: [
        0.498,
        0.144,
        0.96,
        0.909,
        1.014,
        0.502,
        0.039,
        0.461,
        0.252,
        null,
        0.125
      ]
    },
    {
      name: "EnviroMAT SS-1",
      rangesLow: [66.6, 10.2, 50.4, 334, 860, 14.0, 0.02, 4.7, 1.8, 0.29, 665],
      rangesHigh: [140, 15.7, 68, 472, 1369, 27.5, 1.54, 9, 4.7, 0.53, 863]
    }
  ]
};

export default CHEM114;
