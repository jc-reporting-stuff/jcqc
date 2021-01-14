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
      LOQs: [4]
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

export default CHEM057;
