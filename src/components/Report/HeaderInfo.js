import React from "react";

const HeaderInfo = ({ method, instrument }) => {
  return (
    <div>
      <h1>Sequence Information - {method.name}</h1>
      <div className="headerItem">Analyst: _________________________</div>
      <div className="headerItem">Analysis Date: _________________________</div>
      <div className="headerItem">
        Sequence ID: ______________________________________
      </div>
      <div className="headerItem">
        Software Version: {instrument.sw} - Version {instrument.swVersion} -
        Build {instrument.swBuild}
      </div>
      <div className="headerItem" style={{ marginTop: "-1rem" }}>
        Autosampler Info: {instrument.as} - Serial Number {instrument.asSerial}
      </div>
    </div>
  );
};

export default HeaderInfo;
