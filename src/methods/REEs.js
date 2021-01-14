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

export default REEs;
