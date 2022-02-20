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
            </div>
        </div>
    `;

    docFrag.appendChild(createElementFromHTML(cardWrapper));
}

container.appendChild(docFrag);

var container = document.getElementById('accepted-posts');
var docFrag = document.createDocumentFragment();

for (var i=0; i < accepted_posts.length; i++) {
    var cardWrapper = `
    <form method="post" action="/publish_event/">
        <div class="card"><img class="card-img-top w-100 d-block">
            <div class="card-body">
                <input type="hidden" name="id" value=${accepted_posts[i].post_id}>
                <h4 class="card-title" style="font-family: Montserrat, sans-serif;font-weight: bold;">${accepted_posts[i].title}</h4>
                <p class="card-text" style="font-family: Montserrat, sans-serif;">Organization Name: ${accepted_posts[i].org_name}<br></p>
                <p class="card-text" style="font-family: Montserrat, sans-serif;">Food Name: ${accepted_posts[i].food_name}<br></p>
                <p class="card-text" style="font-family: Montserrat, sans-serif;">Location: ${accepted_posts[i].address}<br></p>
                <p class="card-text" style="font-family: Montserrat, sans-serif;">Date: ${accepted_posts[i].date}<br></p>
                <p class="card-text" style="font-family: Montserrat, sans-serif;">Allergens: ${accepted_posts[i].allergens}<br></p>
                <button class="btn btn-primary" type="submit" style="font-family: Montserrat, sans-serif;">publish</button>
            </div>
        </div>
    </form>
    `;

    docFrag.appendChild(createElementFromHTML(cardWrapper));
}

container.appendChild(docFrag);