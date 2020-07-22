const csvParser = input => {
  const fileData = input;

  const splitFileData = fileData.split("\n");

  const fieldNames = splitFileData[0].trim().split(",");

  // modify field names to not allow spaces -> replace with underscore
  for (let i = 0; i < fieldNames.length; i++) {
    let currentFieldName = fieldNames[i];
    currentFieldName = fieldNames[i].toLowerCase();
    const isMultipleWords = fieldNames[i].split(" ").length > 1;
    if (isMultipleWords) {
      currentFieldName = currentFieldName.split(" ").join("_");
    }
    fieldNames[i] = currentFieldName;
  }

  let parsedData = [];

  for (let i = 1; i < splitFileData.length; i++) {
    const currentLine = splitFileData[i];
    const lineItems = currentLine.split(",");
    let currentLineObject = {};

    for (let j = 0; j < lineItems.length; j++) {
      currentLineObject[fieldNames[j]] = lineItems[j];
    }

    if (currentLineObject[fieldNames[0]].length > 0) {
      parsedData.push(currentLineObject);
    }
  }

  return parsedData;
};

module.exports = csvParser;
