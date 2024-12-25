const checkboxs = document.getElementsByClassName('form-check-input')

for (const checkbox of checkboxs){
    const id = checkbox.dataset.answerId
    fetch( `/question/${id}/is_correct/`)
    .then(response => response.json())
    .then(data => {
        if (data.is_correct){
            checkbox.checked = true
        }
    });
}

for (const checkbox of checkboxs){
    
    const id = checkbox.dataset.answerId

    checkbox.addEventListener('change', () => {
        const is_correct = checkbox.checked
        console.log({is_correct})
        url = `/question/${id}/set_correct/`

        const request = new Request(url, {
            method:"POST",
            headers: {'X-CSRFToken': getCookie('csrftoken')},
            mode: 'same-origin',
            body: JSON.stringify({'is_correct': is_correct}),
        });
        
        fetch(request).then((response) => {
            response.json().then((data) => {

            });
        });
    })
}