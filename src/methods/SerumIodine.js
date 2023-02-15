const SerumIodine = {
  name: "Serum Iodine",
  description: "Iodine in Serum",
  elements: ["I"],
  units: ["ppb"],
  checkStdTolerance: 0.15,
  checkStds: [
    {
      name: "5 ppb check",
      expectedValues: [5]
    }
  ],
  blanks: [
    {
      name: "Method Blank",
      type: "any",
      LOQs: [0.8]
    }
  ],
  duplicateTolerance: 20,
  calStandards: [0, 0.1, 0.2, 0.5, 2, 10],
  sigFigs: 3,
  referenceMaterials: [
    {
      name: "QM-S Q1807",
      rangesLow: [102],
      rangesHigh: [141]
    },
    {
      name: "QM-S Q2116",
      rangesLow: [107],
      rangesHigh: [135]
    }
  ]
};

export default SerumIodine;
