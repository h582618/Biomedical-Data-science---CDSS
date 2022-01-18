import React, { Component } from 'react';
import CSVupload from "./CSVupload";
import postDataColumns from "../Utils/ApiUtils"
import { ClientPage } from './ClientPage';

export class UseModel extends Component {

    constructor(props) {
        super(props);
    }


    render() {
        let contents = <ClientPage />

            ;

        return (
            <div>
                <h1 id="tabelLabel">Run on model</h1>
                <p>Upload file to test the model</p>
                <ClientPage />
            </div>
        );
    }

}
