function renderTable(tableData, element_id, help_row, lens_id) {
    //console.log(lens_id)
    const baseUrl = window.myApp.lensesUrl
    const helpBaseUrl = window.myApp.helpUrl
    try {
        const counter = document.getElementById("counter")
        let current_length = document.getElementById("current_length").textContent
        let length = parseInt(document.getElementById("total_length").textContent)
        let n_rows = parseInt(document.getElementById("n_rows").textContent)
        current_length = current_length.slice(1, -1)
        counter.innerHTML = "Showing " + current_length + " rows of " + length
    } catch(error){
        console.log("nothing")
    }
    let table = document.createElement('table');
    const fragment = document.createDocumentFragment();

    tableData.forEach((rowData, rowIndex) => {
        let row = document.createElement('tr')

        rowData.forEach((cellData, colIndex) => {
            let cell;
            if (rowIndex === 0) {
                cell = document.createElement('th');
                //cell.classList.add("form-label")
                //cell.id = cellData
                //console.log(cell.id)
                //console.log(help_row[cellData])
                //cell.innerHTML = `<a href="${helpBaseUrl}#${cellData}">${help_row[cellData]}</a><div class="form-label"><span id=${cellData} class=labelpopup style="display: none">text</span></div>`;
                cell.innerHTML = `<a href="${helpBaseUrl}#${cellData}">${help_row[cellData]}</a>`;
            } else {
                cell = document.createElement('td');
                if(tableData[0][colIndex] == "Name"){
                    cell.innerHTML = `<a id="a${rowIndex}" data-index="${rowIndex}" href="${baseUrl}${lens_id[rowIndex-1]}">${cellData}</a>`;
                } 
                else if((tableData[0][colIndex] == "BibCode" || tableData[0][colIndex] == "z_bibcode") || tableData[0][colIndex] == 'BibCode_TD'){
                    if(cellData.includes(" / ")){
                        //console.log(cellData);
                        let break_index = cellData.indexOf(" / ");
                        let str1 = cellData.slice(0, break_index);
                        let str2 = cellData.slice(break_index + 3);
                        //console.log(str1);
                        //console.log(str2);
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
        fragment.appendChild(row)
    });
    table.appendChild(fragment);

    const container = document.getElementById(element_id);
    container.innerHTML = ''; // Clear previous content
    container.appendChild(table);
    //area_info()
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

function toggleColumns()
    {
        //var html=document.getElementById("form-columns").innerHTML;
        if (status == "less") {
            console.log(status)
            document.getElementById("form-columns-id").style.display="flex";
            document.getElementById("toggleButton").innerText = "Hide columns";
            status = "more";
        } else if (status == "more") {
            console.log(status)
            document.getElementById("form-columns-id").style.display="none";
            document.getElementById("toggleButton").innerText = "Show all columns";
            status = "less"
        }
    }

class objectsClass{
    constructor(){
        this.dict = {
            checkboxes: [],
            buttons: []
        }
    }
    add_object(key, name){
        this.dict[key].push(name)
    }
    get_objects(key){
        return this.dict[key]
    }
}

class checkboxClass {
    constructor(name, url, strict) {
        this.name = name
        this.url = url
        this.strict = strict
        this.items = document.querySelectorAll(`input[name=${this.name}]`);
        if (window?.myApp?.holder) {
            window.myApp.holder.add_object("checkboxes", this);
        } else {
            console.warn("Holder not found on window.myApp");
        }
        this.items.forEach(checkbox => {
            checkbox.addEventListener('change', () => {
                if(strict == "very"){
                    this.check_one(checkbox.value)
                }
                if(strict == "yes"){
                    if(checkbox.checked == true){
                        this.check_one(checkbox.value)
                    }
                }
                newTable(this.name, lens_id)
            });
        });
    }
    get_name(){
        return this.name
    }
    get_url(){
        return this.url
    }
    get_checked(){
        var value = ""
        this.items.forEach((item) => {
            if(item.checked == true){
                value += item.value;
            }
        });
        return value;
        }
    get_checks_url(){
        var value = ""
        this.items.forEach((item) => {
            if(item.checked == true){
                value += `${this.url}=${item.value}&`;
            }
        });
        return value;
        }
    check_one(value){
        this.items.forEach((item) => {
            if(item.value == value){
                item.checked = true;
            }
            else{
                item.checked = false;
            }
        });
    }
    check_list(values){
        this.items.forEach((item) => {
            if(values.includes(item.value)){
                item.checked = true;
            }
            else{
                item.checked = false;
            }
        });
    }
}

class downloadClass{
    constructor(id){
        this.id = id
        const downloader = document.getElementById(this.id)
        downloader.addEventListener('click', function(event){
            event.preventDefault(); // Prevent default anchor action
            let url_str = window.myApp.exportUrl + "?";
            const objects = window.myApp.holder.get_objects("checkboxes");
            objects.forEach((object) => {
                url_str += object.get_checks_url();
            });
            url_str = url_str.slice(0, -1);
            window.location.href = url_str;
        });
    }
}

class buttonPaginationClass{
    constructor(id, value){
        this.id = id;
        console.log(this.id)
        this.value = value;
        console.log(this.value)
        window.myApp.holder.add_object("buttons", this);
        this.button = document.getElementById(this.id);
        this.button.addEventListener('click', () => {
            console.log(this.value)
            newTable(value, lens_id)
        });
    }
    hide(){
        this.button.style.display = 'none';
    }
    display(){
        this.button.style.display = '';
    }
    get_value(){
        return this.value
    }
}

function newTable(name,lens_id) {
    const xhr = new XMLHttpRequest();
    const request = window.myApp.requestUrl;
    const objects = window.myApp.holder.get_objects("checkboxes");
    const tableContainer = document.getElementById('table-container');
    let url_str = `${request}?`;
    //url_str += `$changeform=${name}&`;
    objects.forEach((object) => {
        url_str += object.get_checks_url();
    });
    //url_str = url_str.slice(0, -1);
    let start_row = document.getElementById("start_row").textContent
    console.log(start_row)
    url_str += `start_row=${start_row}`
    console.log(url_str)
    console.log(name)
    xhr.open('GET', url_str, true);
    xhr.setRequestHeader('X-Requested-With', name);
    xhr.onreadystatechange = function () {
        if (xhr.readyState === XMLHttpRequest.DONE && xhr.status === 200) {
            tableContainer.innerHTML = xhr.responseText;
            const startTime = performance.now()
            let fields = JSON.parse(document.getElementById('fields_json').textContent);
            let defaultlist = JSON.parse(document.getElementById('default_json').textContent);
            objects.forEach((object) => {
                if(object.get_name() == "fieldsform"){
                    object.check_list(fields)
                }
                if(object.get_name() == "defaultform"){
                    object.check_list(defaultlist)
                }
            });
            let tableData = JSON.parse(document.getElementById('table_json').textContent);
            let lens_id = JSON.parse(document.getElementById('id_json').textContent);
            renderTable(tableData, 'partial-table-container', help_row, lens_id);
            const endTime = performance.now()
            console.log(`Call to render took ${endTime - startTime} milliseconds`)
        }
    }
    xhr.send();
}

function get_help_text(field, id){
    const url = window.myApp.textUrl
    fetch(url)
    .then((response) => {
        if (!response.ok) {
          throw new Error(`HTTP error: ${response.status}`);
        }
        return response.json();
      })
      .then((json) => help_text(field, json[field], id))
      .catch((err) => console.error(`Fetch problem: ${err.message}`));
}

function help_text(field, text, id){
    let helpBaseUrl = window.myApp.helpUrl;
    let html = `<a href="${helpBaseUrl}#${field}">`
    html += help_row[field] + `</a>` + ": " + text
    document.getElementById(id).innerHTML = html
}

function area_info(){
    const labelArray = document.querySelectorAll('.form-label');

    labelArray.forEach(label => {
        //console.log(label.tagName)
        //console.log(label.querySelector('span'))
        const textareaId = label.querySelector('span').id;
        //console.log(textareaId)
        get_help_text(label.id, textareaId);

        label.addEventListener('mouseover', function () {
            const popup = document.getElementById(textareaId);
            popup.style.display = 'block';
        });

        label.addEventListener('mouseout', function () {
            const popup = document.getElementById(textareaId);
            popup.style.display = 'none';
        });
    });
}

window.renderTable = renderTable;
window.containsObject = containsObject;
window.get_filter_value = get_filter_value;
window.toggleColumns = toggleColumns;
window.get_help_text = get_help_text;
window.help_text = help_text;
window.area_info = area_info;