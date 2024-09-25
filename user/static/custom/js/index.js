async function send_post(url, data, message) {
    let form_data = new FormData();
    for (let key in data) {
        form_data.append(key, data[key]);
    }
    console.log(message)
    if (message) {
        let confirmation = confirm(message)
        if (confirmation === true) {
            const response = await fetch(url, {
                method: "post",
                cache: 'no-cache',
                body: form_data
            })
                .then(response => {
                    console.log(response);
                    window.location = response['url']
                })
                .catch(response => {
                    alert('Error')
                })
        }
    } else {
        const response = await fetch(url, {
            method: "post",
            cache: 'no-cache',
            body: form_data
        })
            .then(response => {
                console.log(response);
                window.location = response['url']
            })
            .catch(response => {
                alert('Error')
            })
    }


}

async function fetch_post(url, data) {
    let form_data = new FormData();
    for (let key in data) {
        form_data.append(key, data[key]);
    }
    let response = await fetch(url,
        {
            method: 'POST',
            cache: "no-cache",
            body: form_data
        }
    )
    return response.json();
}

function number_mask(id) {
    const element = document.getElementById(id);
    return IMask(element, {
        mask: Number,
        min: 0,
        max: 1000000000,
        thousandsSeparator: ' '
    })
}

function phone_mask(id) {
    return IMask(document.querySelector(`#${id}`), {
        mask: '+{998}(00) 000-00-00',
        lazy: false,
        placeholderChar: '*'
    });
}