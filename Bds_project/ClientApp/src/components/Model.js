import React, { Component } from 'react';
import CSVupload from "./CSVupload";
import postDataColumns from "../Utils/ApiUtils"

export class Model extends Component {
  
    constructor(props) {
        super(props);
    }

    render() {
        return (
            <div>
                <h1 id="tabelLabel">Model</h1>
                <p>Upload csv file to train the model</p>
                <CSVupload />
            </div>
        );
    }

}
