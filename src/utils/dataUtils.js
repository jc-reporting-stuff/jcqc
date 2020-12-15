const parseJsonData = (output) => {
  const data = [];

  const firstElementMass = output[0].mass;
  let i = 1;
  let massesPresent = [Number(output[0].mass)];
  while (output[i].mass !== firstElementMass) {
    massesPresent.push(Number(output[i].mass));
    i++;
  }
  const elementCount = i;
  massesPresent.sort((a, b) => a - b);

  for (let i = 0; i < output.length; i += elementCount) {
    let values = new Array(elementCount);
    let units = [];

    for (let j = 0; j < elementCount; j++) {
      const findMassIndex = massesPresent.findIndex(
        (m) => m === Number(output[i + j].mass)
      );
      values[findMassIndex] = Number(output[i + j].concentration);
      units.push(output[i + j].units);
    }

    const dupRegEx = new RegExp("(.*) (d|dup)$", "i");
    if (data.length > 1 && output[i].sample_name.match(dupRegEx)) {
      const sampleId = output[i].sample_name.match(dupRegEx)[1].trim();
      const refSample = () => {
        for (let count = data.length - 1; count > 0; count--) {
          if (data[count].id === sampleId) {
            console.log(data[count].id === sampleId);
            return data[count];
          }
        }
      };
      //const refSample = data.find((datum) => datum.id === sampleId);
      try {
        refSample().dupValues = values;
      } catch (e) {
        alert(
          `Error: Couldn't find Reference for duplicate with sample ID ${sampleId}`
        );
      }
    } else {
      const sampleObject = {
        id: output[i].sample_name,
        values,
        dupValues: null,
        units
      };
      data.push(sampleObject);
    }
  }
  return data;
};

const roundToSigFigs = (number, sigFigs) => {
  let oom = 0;
  let result = Number(number);

  if (number > 10) {
    while (result > 10) {
      result /= 10;
      oom += 1;
    }
  } else if (number < 0.0001 && number > 0) {
    return "0.00";
  } else if (number < 10) {
    while (result < 1 && result > 0) {
      if (result < 0) {
        result = result * -1;
      }
      result = result * 10;
      oom += 1;
    }
  }
  if (number > 10) {
    result = number / Math.pow(10, oom);
    result = result * Math.pow(10, sigFigs - 1);
    result = Math.round(result);
    result = result / Math.pow(10, sigFigs - oom - 1);
    result = result.toPrecision(sigFigs);
  } else if (number < 0) {
    result = number * Math.pow(10, sigFigs + 1);
    result = Math.round(result);
    result = result / Math.pow(10, sigFigs + 1);
    result.toPrecision(sigFigs);
  } else if (number < 1) {
    result = number * Math.pow(10, oom);
    result = result * Math.pow(10, sigFigs - 1);
    result = Math.round(result);
    result = result / Math.pow(10, sigFigs + oom - 1);
    result = result.toPrecision(sigFigs);
  } else {
    result = number.toPrecision(sigFigs);
  }

  return result;
};

export default { parseJsonData, roundToSigFigs };
