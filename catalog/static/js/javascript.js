function renderTable(tableData, BaseUrl, helpBaseUrl, element_id, help_row, lens_id) {
    console.log(lens_id)
    console.log("whyy")
    let fragment = document.createDocumentFragment();
    let table = document.createElement('table');
    

    tableData.forEach((rowData, rowIndex) => {
        let row = document.createElement('tr');

        rowData.forEach((cellData, colIndex) => {
            let cell;
            if (rowIndex === 0) {
                cell = document.createElement('th');
                console.log(help_row[cellData])
                cell.innerHTML = `<a href="${helpBaseUrl}#${cellData}">${help_row[cellData]}</a>`;
            } else {
                cell = document.createElement('td');
                if(tableData[0][colIndex] == "Name"){
                    cell.innerHTML = `<a id="a${rowIndex}" data-index="${rowIndex}" href="${BaseUrl}${lens_id[rowIndex-1]}">${cellData}</a>`;
                } 
                else if(tableData[0][colIndex] == "BibCode" || tableData[0][colIndex] == "z_bibcode"){
                    if(cellData.includes(" / ")){
                        console.log(cellData);
                        let break_index = cellData.indexOf(" / ");
                        let str1 = cellData.slice(0, break_index);
                        let str2 = cellData.slice(break_index + 3);
                        console.log(str1);
                        console.log(str2);
                        cell.innerHTML = table_bibcode_links(str1) + `\n`;
                        cell.innerHTML += table_bibcode_links(str2)
                        cell.style.setProperty("line-height", "16px")
                    }
                    else{
                        cell.innerHTML = table_bibcode_links(cellData);
                    }
                }
                else {
                    cell.textContent = cellData;
                }
            }
            row.appendChild(cell);
        });

        table.appendChild(row);
    });

    fragment.appendChild(table);

    const container = document.getElementById(element_id);
    container.innerHTML = ''; // Clear previous content
    container.appendChild(fragment);
}

function table_bibcode_links(bibcode){
    let html = ""
    if(bibcode.includes("https")){
        html = `<a href="${bibcode}">${bibcode}</a>`;
    }
    else{
        html = `<a href="https://ui.adsabs.harvard.edu/abs/${bibcode}/abstract">${bibcode}</a>`
    }
    return html
}

function clickboxes(checkbox){
    var defaultcheckboxes = document.getElementsByName('defaultform');
    var filtercheckboxes = document.getElementsByName('typeform');
    var defaultvalue = ""
    var filtervalue = ""
    if(checkbox.name === 'defaultform'){
        defaultcheckboxes.forEach((item) => {
            if (item !== checkbox) item.checked = false
            else if(item.checked == true){
                defaultvalue = item.value
            }
        })
       filtervalue = get_filter_value()
    }
    else{
        filtercheckboxes.forEach((item) => {
            if (item !== checkbox) item.checked = false
            else if(item.checked == true){
                filtervalue = item.value
            }
        })
        defaultcheckboxes.forEach((item) => {
            if(item.checked == true){
                defaultvalue = item.value
            }
        })
    }
    updateTableDefault(defaultvalue, filtervalue)
}

function containsObject(obj, list) {
    var i;
    for (i = 0; i < list.length; i++) {
        if (list[i] === obj) {
            return true;
        }
    }

    return false;
}

function get_filter_value(){
    var filtercheckboxes = document.getElementsByName('typeform');
    var filtervalue = ""
    filtercheckboxes.forEach((item) => {
        if(item.checked == true){
            filtervalue = item.value;
        }
    })
    return filtervalue;

}

window.renderTable = renderTable;
window.clickboxes = clickboxes;
window.containsObject = containsObject;
window.get_filter_value = get_filter_value;