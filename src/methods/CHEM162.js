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
      LOQs: [0.9, 0.013, 0.3, 0.0008, 0.0011, 0.007, 1, null]
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
      name: 'QM-S Q1807',
      rangesLow: [2.23, 0.747, 3.47, 1.03, 0.913, 0.119, 1.11, null],
      rangesHigh: [3.2, 0.851, 4.3, 1.22, 1.16, 0.152, 1.73, null]
    },
    {
      name: 'QM-S Q2007',
      rangesLow: [4.69, 0.459, 0.558, 2.057, 0.986, 0.115, 1.74, null],
      rangesHigh: [6.99, 0.621, 0.77, 2.783, 1.33, 0.155, 2.36, null]
    },
    {
      name: 'QM-B Q1720',
      rangesLow: [null, null, null, null, null, 0.169, null, 0.109],
      rangesHigh: [null, null, null, null, null, 0.238, null, 0.134]
    }
  ]
};

export default CHEM162;
