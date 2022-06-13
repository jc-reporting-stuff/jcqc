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
      rangesLow: [0.402],
      rangesHigh: [0.525]
    }
  ]
};

export default TOXI064Pb;
