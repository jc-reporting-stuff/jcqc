import React from "react";

import dataUtils from "../utils/dataUtils";
import csvParse from "../utils/csvParse";

import { useHistory } from "react-router-dom";

const FileSelector = ({ setError, setData, method }) => {
  const history = useHistory();
  const fileHandler = (event) => {
    event.preventDefault();
    const inputFile = event.target.files[0];
    if (inputFile.type !== "text/plain") {
      setError("Please use a text file");
      return;
    }
    history.push("/report");

    const reader = new FileReader();
    reader.readAsText(inputFile);
    reader.onloadend = () => {
      const jsonData = csvParse(reader.result);
      const parsedData = dataUtils.parseJsonData(jsonData);
      setData(parsedData);
    };
  };
  return (
    <div
      className="centeredContainerParent"
      style={{ height: "60px", padding: "5px" }}
    >
      <div className="centeredContainerChild">
        {method.name && (
          <input
            type="file"
            id="inputFile"
            className="custom-file-input"
            name="inputFile"
            onChange={fileHandler}
          />
        )}
      </div>
    </div>
  );
};

export default FileSelector;
