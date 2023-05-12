let add_to_cart_buttons = document.getElementsByClassName("add_to_cart");

for (let i = 0; i < add_to_cart_buttons.length; i++) {
    let add_to_cart_button = add_to_cart_buttons[i];
    add_to_cart_button.addEventListener("click", function () {
        // get product id from this a href
        product_id = this.getAttribute("data-product_id");
        let quantity = 1;
        console.log(product_id);
        // send xhr request to server, to check if user is logged in
        const xhr = new XMLHttpRequest();
        xhr.open("POST", "/add_to_cart", true);
        xhr.setRequestHeader("Content-Type", "application/json");
        xhr.send(JSON.stringify({ "product_id": product_id, "quantity": quantity }));
        xhr.onload = function () {
            if (xhr.status == 200) {
                // if user is logged in, add item to cart
                add_to_cart_button.innerHTML = "Added to cart";
                add_to_cart_button.disabled = true;
                alert("Added to cart");
                // update cart count
                update_cart_count();
            }
            else {
                // if user is not logged in, redirect to login page
                window.location.href = "/login";
            }
        }
    });
}

//function to update cart count
function update_cart_count() {
    const xhr = new XMLHttpRequest();
    xhr.open("GET", "/get_cart_count", true);
    xhr.send();
    xhr.onload = function () {
        if (xhr.status == 200) {
            let response = JSON.parse(xhr.responseText);
            let cart_count = document.getElementById("cart_count");
            cart_count.innerHTML = response.cart_count;
        }

    }
}

// run update_cart_count() on page load
update_cart_count();

// fade out success and danger alerts after 5 seconds if they exist
let success_alert = document.getElementsByClassName("success");
let danger_alert = document.getElementsByClassName("danger");

if (success_alert.length > 0) {
    setTimeout(function () {
        success_alert[0].style.display = "none";
    }, 5000);
}

if (danger_alert.length > 0) {
    setTimeout(function () {
        danger_alert[0].style.display = "none";
    }, 5000);
}

// remove_item_from_cart
let remove_item_from_cart_buttons = document.getElementsByClassName("remove_item_from_cart");

for (let i = 0; i < remove_item_from_cart_buttons.length; i++) {
    let remove_item_from_cart_button = remove_item_from_cart_buttons[i];
    remove_item_from_cart_button.addEventListener("click", function () {
        // get product id from this a href
        product_id = this.getAttribute("data-id");
        // send xhr request to server, to check if user is logged in
        // confirm if user wants to remove item from cart
        if (confirm("Are you sure you want to remove this item from cart?")) {
            const xhr = new XMLHttpRequest();
            xhr.open("POST", "/remove_item_from_cart", true);
            xhr.setRequestHeader("Content-Type", "application/json");
            xhr.send(JSON.stringify({ "product_id": product_id }));
            xhr.onload = function () {
                if (xhr.status == 200) {
                    // if user is logged in, add item to cart
                    alert("Item removed from cart");
                    // update cart count
                    update_cart_count();
                    // reload page
                    window.location.reload();
                }
            }
        }
    });
}