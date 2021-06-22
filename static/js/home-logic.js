var _application;
var _page;
var _element;

$(document).ready(() => {
    refreshList(0);
    
});


function refreshList(mode, id) {
    var tbody = document.getElementById("tbody");
    tbody.innerHTML = "";
    let url = "";

    if(mode == 0) {
        url = "/apps";
        $.get(url, (data) => {
            let row = "";
            let index = 1;
            for(let i in data) {
                row = `
                    <tr onclick="progress(${index});">
                    <td >${index}</td>
                    <td>${data[i]}</td>
                    </tr>
                `;
                tbody.innerHTML += row;
                row = "";
                index++;
            }
        });
    } else if (mode == 1) {
        url = "/pages?id=" + id;
        $.get(url, (data) => {
            let row = "";
            let index = 1;
            for(let i in data) {
                row = `
                    <tr onclick="progressElements(${index});">
                    <td >${index}</td>
                    <td>${data[i]}</td>
                    </tr>
                `;
                tbody.innerHTML += row;
                row = "";
                index++;
            }
        });
    } else if (mode == 2) {
        url = "/elements?id="+id;
        $.get(url, (data) => {
            let row = "";
            let index = 1;
            for(let i in data) {
                row = `
                    <tr onclick="edit(${index});">
                    <td >${index}</td>
                    <td>${data[i]}</td>
                    </tr>
                `;
                tbody.innerHTML += row;
                row = "";
                index++;
            }
        });
    } else {
        url = "/apps";
        $.get(url, (data) => {
            let row = "";
            let index = 1;
            for(let i in data) {
                row = `
                    <tr onclick="progress(${index});">
                    <td >${index}</td>
                    <td>${data[i]}</td>
                    </tr>
                `;
                tbody.innerHTML += row;
                row = "";
                index++;
            }
        });
    }
    
    
}

function progress(id) {
    _application = id;
    refreshList(1, id);
}

function progressElements(id) {
    _page = id;
    refreshList(2, id);
}

function edit(id) {
    _element = id;
    console.log("Application: " + _application + " | Page: " + _page);
    console.log(_application);
    console.log(_page);
    console.log(_element);

    location.href = "/edit?application=" + _application + "&page=" + _page + "&element=" + _element
}

