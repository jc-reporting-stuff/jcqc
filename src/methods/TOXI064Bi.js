const TOXI064Bi = {
  name: 'TOXI-064 - Bismuth',
  description: 'Bismuth in Milk',
  elements: ['Bi'],
  units: ['ppb'],
  checkStdTolerance: 0.15,
  checkStds: [
    {
      name: 'Calibration Check',
      expectedValues: [10]
    }
  ],
  blanks: [
    {
      name: 'Method Blank',
      type: 'any',
      LOQs: [0.15]
    }
  ],
  duplicateTolerance: 20,
  calStandards: [0, 0.1, 1, 5, 10, 20],
  sigFigs: 3,
  referenceMaterials: [
    {
      name: 'Skim Milk Powder',
      rangesLow: [18.9],
      rangesHigh: [23.3]
    }
  ]
};

export default TOXI064Bi;
