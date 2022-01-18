const baseUrl = "/api"

export async function handleResponse(response) {
    if (response.ok) return response.json();
    if (response.status < 499 && response.status >= 400) {
        const error = await response.text();
        throw new Error(error);
    }
    throw new Error("Network response was not ok.");
}

export function handleError(error) {
    // eslint-disable-next-line no-console
    console.error("API call failed. " + error);
    throw error;
}



export function postDataColumns(datas, column, setResponse, setLoading) {
    if (datas == undefined || column == undefined) {
        console.log("undefined")
    }
    setLoading(true)

    console.log("api call");
    console.log(datas);
    console.log(column);
    let fetchUrl = 'Model/trainModel';

    return fetch(fetchUrl, {
        method: 'POST',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            data: datas,
            columns: column,
        })
    }).then(handleResponse)
        .then((res) => {
            setResponse(res)
            console.log(res)
            setLoading(false)

        })
        .catch(handleError);
}


const merge = (csv, newLabels) =>
    csv.map(function (itm, index) {
        const label = newLabels['label'][index];
        itm = { ...itm, label };
        return itm
    });
   

export function postUseModel(datas, column, selectedOption, setResponse, setLoading, setData, setColumns) {
    if (datas == undefined || column == undefined) {
        console.log("undefined")
    }
    setLoading(true)
    console.log("api call");
    let fetchUrl = 'Model/testModel';
    const column2 = JSON.parse(JSON.stringify(column)); 
    column2.push('label');
    console.log(typeof column2)
    console.log(column2)
    const columns = column2.map(c => ({
        name: c,
        selector: c,
    }));
    setColumns(columns)

    console.log(column)

    return fetch(fetchUrl, {
        method: 'POST',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            container_name: selectedOption,
            data: datas,
            columns: column,
        })
    }).then(handleResponse)
        .then((res) => {
            setLoading(false)
            return setData(merge(datas, JSON.parse(res)));
        })
        .catch(handleError);
}