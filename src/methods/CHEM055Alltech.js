const CHEM055Alltech = {
  name: "CHEM-055 - Alltech",
  description: "Animal Nutrition Project - Alltech",
  elements: ["Mn", "Fe", "Co", "Cu", "Zn", "Se", "Mo"],
  units: ["ppm", "ppm", "ppm", "ppm", "ppm", "ppm", "ppm"],
  checkStdTolerance: 0.15,
  checkStds: [
    {
      name: "Calibration Check",
      expectedValues: [100, 100, 10, 100, 100, 10, 10]
    }
  ],
  blanks: [
    {
      name: "Method Blank",
      type: "methoblank",
      LOQs: [0.52, 8.6, 0.03, 0.46, 2.1, 0.07, 0.02]
    },
    {
      name: "Undiluted Blank",
      type: "undilblank",
      LOQs: [0.052, 0.86, 0.003, 0.046, 0.21, 0.007, 0.002]
    }
  ],
  duplicateTolerance: 20,
  calStandards: [0, 0.25, 0.5, 1, 5, 10, 50, 200, 500, 1000],
  sigFigs: 3,
  referenceMaterials: [
    {
      name: "Wheat Flour",
      rangesLow: [31.6, 36.8, 0.0045, 4.14, 30.1, 0.92, 0.77],
      rangesHigh: [48.1, 55.4, 0.0077, 5.68, 40.8, 1.43, 1.08]
    }
  ]
};

export default CHEM055Alltech;
