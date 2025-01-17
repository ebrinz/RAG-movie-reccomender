import React from "react";

const ResponseList = ({ responses }) => {
    return (
        <div>
            {/* <h2>Responses</h2> */}
            {responses.length === 0 && ""}
            {responses.map((entry, index) => (
                <div
                    key={index}
                    style={{
                        marginBottom: "20px",
                        padding: "10px",
                        border: "1px solid #ddd",
                        borderRadius: "4px",
                    }}
                >
                    <p><strong>Prompt:</strong> {entry.prompt}</p>
                    <div style={{ whiteSpace: "pre-wrap" }}>
                        <strong>Response:</strong> {entry.response}
                    </div>
                </div>
            ))}
        </div>
    );
};

export default ResponseList;