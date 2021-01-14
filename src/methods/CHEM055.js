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

export default CHEM055;
