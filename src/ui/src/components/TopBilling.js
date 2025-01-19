import React from "react";
import "../styles/TopBilling.css";

const TopBilling = () => {
    return (
        <div className="top-billing">
            <div className="ascii-banner">
                <pre className="ascii-art">
                    {`
>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
`}
                </pre>
                <h1 className="title">Movie Recco</h1>
                <pre className="ascii-art">
                    {`
<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
`}
                </pre>
            </div>
        </div>
    );
};

export default TopBilling;
