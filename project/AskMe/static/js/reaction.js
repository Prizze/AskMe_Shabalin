 function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const cards = document.getElementsByClassName('card')

for (const card of cards){
    const likeButton = card.querySelector('.like')
    const dislikeButton = card.querySelector('.dislike')

    let id = card.dataset.questionId
    let is_question = 'true'

    if (id === undefined){
        id = card.dataset.answerId
        is_question = 'false'
    }

    fetch(`/question/${id}/get_likes_status/`, {
        method: "POST",
        headers: {'X-CSRFToken': getCookie('csrftoken')},
        mode: 'same-origin',
        body: JSON.stringify({ 'is_question': is_question })
    })
    .then(response => response.json())
    .then(data => {
        if (data.is_liked) {
            likeButton.disabled = true;
            dislikeButton.disabled = true;
        } else {
            likeButton.disabled = false;
            dislikeButton.disabled = false;
        }
    });
}

for (const card of cards){
    const likeButton = card.querySelector('.like')
    const dislikeButton = card.querySelector('.dislike')
    const likesCounter = card.querySelector('.likes_counter')

    let id = card.dataset.questionId
    let is_question = 'true'

    if (id === undefined){
        id = card.dataset.answerId
        is_question = 'false'
    }

    likeButton.addEventListener('click', () => {
        url = `/question/${id}/like_async/`
        const request = new Request(url, {
            method:"POST",
            headers: {'X-CSRFToken': getCookie('csrftoken')},
            mode: 'same-origin',
            body: JSON.stringify({'type': 'like', 'is_question': is_question}),
        });
        
        fetch(request).then((response) => {
            response.json().then((data) => {
                console.log({data})
                likesCounter.innerHTML = data.like_count
                likeButton.disabled = true
                dislikeButton.disabled = true
            });
        });
    });

    dislikeButton.addEventListener('click', () => {
        url = `/question/${id}/like_async/`
        const request = new Request(url, {
            method:"POST",
            headers: {'X-CSRFToken': getCookie('csrftoken')},
            mode: 'same-origin',
            body: JSON.stringify({'type': 'dislike', 'is_question': is_question}),
        });
        
        fetch(request).then((response) => {
            response.json().then((data) => {
                console.log({data})
                likesCounter.innerHTML = data.like_count
                likeButton.disabled = true
                dislikeButton.disabled = true
            });
        });
    });
}

