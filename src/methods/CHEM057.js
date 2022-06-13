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
      LOQs: [6]
    }
  ],
  duplicateTolerance: 20,
  calStandards: [0, 1, 2, 4, 10, 20],
  sigFigs: 3,
  referenceMaterials: [
    {
      name: "Skim Milk Powder",
      rangesLow: [2627],
      rangesHigh: [3103]
    }
  ]
};

export default CHEM057;
