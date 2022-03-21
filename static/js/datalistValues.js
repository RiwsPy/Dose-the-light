var datalist = document.getElementById('postal_code_choice');

let request = new Request('http://127.0.0.1:8000/maps/api/city_choice', {
    method: 'GET',
    headers: new Headers(),
    })

fetch(request)
.then((resp) => resp.json())
.then((data) => {
    for (value of data.choices) {
        console.log("<option value=" + String(value) + ">")
        datalist.innerHTML += "<option value='" + String(value) + "'>"
    }
})
