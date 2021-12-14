const CHEM162 = {
  name: 'CHEM-162',
  description: 'Metals in Blood and Serum',
  elements: ['Mn', 'Fe', 'Co', 'Cu', 'Zn', 'Se', 'Mo', 'Pb'],
  units: ['ppb', 'ppm', 'ppb', 'ppm', 'ppm', 'ppm', 'ppb', 'ppm'],
  checkStdTolerance: 0.1,
  checkStds: [
    {
      name: '5/50 ppb',
      expectedValues: [5, 50, 5, 50, 50, 5, 5, 5]
    }
  ],
  blanks: [
    {
      name: 'Serum Blank',
      type: 'serum',
      LOQs: [0.9, 0.013, 0.3, 0.0008, 0.011, 0.007, 1, null]
    },
    {
      name: 'Blood Blank',
      type: 'blood',
      LOQs: [null, null, null, null, null, 0.029, null, 0.001]
    }
  ],
  duplicateTolerance: 15,
  calStandards: [0, 0.05, 0.1, 0.25, 0.5, 1, 5, 10, 50, 250],
  sigFigs: 3,
  referenceMaterials: [
    {
      name: 'QM-S Q2007',
      rangesLow: [4.69, 0.494, 0.558, 2.191, 1.04, 0.117, 1.59, null],
      rangesHigh: [6.99, 0.579, 0.77, 2.572, 1.21, 0.141, 2.6, null]
    },
    {
      name: 'QM-B Q1720',
      rangesLow: [null, null, null, null, null, 0.169, null, 0.109],
      rangesHigh: [null, null, null, null, null, 0.238, null, 0.134]
    }
  ]
};

export default CHEM162;
