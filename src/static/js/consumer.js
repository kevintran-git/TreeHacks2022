var container = document.getElementById('card-group');
var docFrag = document.createDocumentFragment();

function createElementFromHTML(htmlString) {
    var div = document.createElement('div');
    div.innerHTML = htmlString.trim();

    // Change this to div.childNodes to support multiple top-level nodes.
    return div.firstChild;
}


for (var i=0; i < posts.length; i++) {
    var cardWrapper = `
        <div class="card"><img class="card-img-top w-100 d-block">
            <div class="card-body">
                <h4 class="card-title" style="font-family: Montserrat, sans-serif;font-weight: bold;">${posts[i].title}</h4>
                <p class="card-text" style="font-family: Montserrat, sans-serif;">Organization Name: ${posts[i].org_name}<br></p>
                <p class="card-text" style="font-family: Montserrat, sans-serif;">Food Name: ${posts[i].food_name}<br></p>
                <p class="card-text" style="font-family: Montserrat, sans-serif;">Location: ${posts[i].address}<br></p>
                <p class="card-text" style="font-family: Montserrat, sans-serif;">Date: ${posts[i].date}<br></p>
                <p class="card-text" style="font-family: Montserrat, sans-serif;">Allergens: ${posts[i].allergens}<br></p>
                <button class="btn btn-primary" type="button" style="font-family: Montserrat, sans-serif;">accept event</button>
            </div>
        </div>
    `;

    docFrag.appendChild(createElementFromHTML(cardWrapper));
}

container.appendChild(docFrag);