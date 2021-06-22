function submit() {
    let data = document.getElementById("editArea").value.trim();
    
    const package = {
        "data": data
    }

    let url = "/edit"

    $.post(url, package, (response) => {
        location.href = response;
    });
}