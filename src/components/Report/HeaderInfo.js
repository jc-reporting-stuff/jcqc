import React from "react";

const HeaderInfo = ({ method }) => {
  return (
    <div>
      <h1>Sequence Information - {method.name}</h1>
      <div className="headerItem">Analyst: _________________________</div>
      <div className="headerItem">Analysis Date: _________________________</div>
      <div className="headerItem">
        Sequence ID: ______________________________________
      </div>
      <div className="headerItem">
        Software Version: MassHunter v4.6 Build 621.8 Patch 1
      </div>
      <div className="headerItem">Autosampler Info: ESI prepFAST SC4</div>
    </div>
  );
};

export default HeaderInfo;
