$(document).ready(() => {
    refreshList();
});


function refreshList() {
    var tbody = document.getElementById("tbody");
    tbody.innerHTML = "";
    const url = "/pages?id=" + 

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
    })
}


function progress(id) {
    location.href = "/edit?id=" + id; 
}