import React from "react";
import "../styles/terminal.css";

const ResponseList = ({ responses }) => {
    return (
        <div>
            {responses.length === 0 && ""}
            {responses.map((entry, index) => (
                <div
                    key={index}
                    style={{
                        marginBottom: "20px",
                        padding: "10px",
                    }}
                >
                    {console.log('sdfsdfsd', entry)}
                    {/* <p>{entry.prompt}</p> */}
                    <div style={{ whiteSpace: "pre-wrap" }}>
                        {entry.response || ""}
                        {index === responses.length - 1 && (
                            <span className="blinking-cursor" style={{ fontSize: "1em" }}></span>
                        )}
                    </div>
                </div>
            ))}
        </div>
    );
};

export default ResponseList;
