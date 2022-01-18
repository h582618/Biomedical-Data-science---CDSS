import React, { useEffect, useState } from "react";
import FileSaver from 'file-saver';
import DataTable from 'react-data-table-component';
import * as XLSX from 'xlsx';
import { postDataColumns } from "../Utils/ApiUtils"
import { postUseModel } from "../Utils/ApiUtils"
import { TailSpin } from 'react-loader-spinner'


export function ClientPage({ }) {

    const options = [
        {
            label: "Random Forest",
            value: "28f926e1-0437-4738-97c7-12dac1efb3fe",
        },
        {
            label: "Logistic Regression",
            value: "98237317-64ce-48aa-9df9-5693d181b222",
        },
        {
            label: "Gradient Boosting",
            value: "b987b56d-0bc3-42bb-b770-8e8279a8ebf3",
        },
    ]

    const [columns, setColumns] = useState([]);
    const [column, setColumn] = useState([]);
    const [data, setData] = useState([]);
    const [dataResponse, setDataResponse] = useState([])
    const [response, setResponse] = useState("");
    const [isLoading, setLoading] = useState(false)
    const [selectedOption, setSelectedOption] = useState(options[0].value);

    // handle file upload
    const processData = dataString => {
        const dataStringLines = dataString.split(/\r\n|\n/);
        const headers = dataStringLines[0].split(/,(?![^"]*"(?:(?:[^"]*"){2})*[^"]*$)/);

        const list = [];
        for (let i = 1; i < dataStringLines.length; i++) {
            const row = dataStringLines[i].split(/,(?![^"]*"(?:(?:[^"]*"){2})*[^"]*$)/);
            if (headers && row.length == headers.length) {
                const obj = {};
                for (let j = 0; j < headers.length; j++) {
                    let d = row[j];
                    if (d.length > 0) {
                        if (d[0] == '"')
                            d = d.substring(1, d.length - 1);
                        if (d[d.length - 1] == '"')
                            d = d.substring(d.length - 2, 1);
                    }
                    if (headers[j]) {
                        obj[headers[j]] = d;
                    }
                }

                // remove the blank rows
                if (Object.values(obj).filter(x => x).length > 0) {
                    list.push(obj);
                }
            }
        }

        // prepare columns list from headers
        const columns = headers.map(c => ({
            name: c,
            selector: c,
        }));





        setData(list);
        setColumns(columns);

        setColumn(headers);
        console.log("IGJEN");
    }



 


   
    const Dropdown = () => {
        
        console.log(options)
        console.log(options[0].value)
        return (
            <select
                value={selectedOption}
                onChange={e => setSelectedOption(e.target.value)}>
                {options.map(o => (
                    <option key={o.value} value={o.value}>{o.label}</option>
                ))}
            </select>
        );
    };

    // handle file upload
    const handleFileUpload = e => {
        const file = e.target.files[0];
        const reader = new FileReader();
        reader.onload = (evt) => {
            /* Parse data */
            const bstr = evt.target.result;
            const wb = XLSX.read(bstr, { type: 'binary' });
            /* Get first worksheet */
            const wsname = wb.SheetNames[0];
            const ws = wb.Sheets[wsname];
            /* Convert array of arrays */
            const data = XLSX.utils.sheet_to_csv(ws, { header: 1 });
            processData(data);
        };
        reader.readAsBinaryString(file);
    }

    let final = isLoading ? <TailSpin
        heigth="80"
        width="80"
        color="#00BFFF"
        arialLabel='loading'
    /> : <DataTable
            pagination
            highlightOnHover
            columns={columns}
            data={dataResponse}
        />


    let content = dataResponse.length != 0 || isLoading ? final : <DataTable
        pagination
        highlightOnHover
        columns={columns}
        data={data}
    />

    const saveFile = () => {
        FileSaver.saveAs(
            process.env.PUBLIC_URL + "template.csv",
            "inadvance_synth_template.csv"
        );
    };

    return (
        <div>
            <div> 
            <button className="cv" onClick={saveFile}>
                    Download Template
                </button>
             </div>
            <input  style={{ marginTop: '5px' }}
                type="file"
                accept=".csv,.xlsx,.xls"
                onChange={handleFileUpload}
            />
            <div style={{ marginTop: '5px' }}>

                {Dropdown()}
            
                <button type="button" class="btn btn-primary" style={{ marginLeft: '5px' }} onClick={() => postUseModel(data, column, selectedOption, setResponse, setLoading, setDataResponse, setColumns)}>
                    Run on model
                </button>
            </div>
            {content}
            
            
        </div>
    );
}

export default ClientPage;