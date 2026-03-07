// Get cart from localStorage
function getCart() {
    return JSON.parse(localStorage.getItem("cart")) || [];
}

// Save cart to localStorage
function saveCart(cart) {
    localStorage.setItem("cart", JSON.stringify(cart));
}

// Add item to cart
function addToCart(name, price) {
    let cart = getCart();

    let existingItem = cart.find(item => item.name === name);

    if (existingItem) {
        existingItem.quantity += 1;
    } else {
        cart.push({
            name: name,
            price: price,
            quantity: 1
        });
    }

    saveCart(cart);
    alert(name + " added to cart!");
}

// Remove item
function removeItem(name) {
    let cart = getCart();
    cart = cart.filter(item => item.name !== name);
    saveCart(cart);
    displayCart();
}

// Display cart items
function displayCart() {
    let cart = getCart();
    let output = "";
    let total = 0;

    cart.forEach(item => {
        total += item.price * item.quantity;

        output += `
            <div style="margin-bottom:15px;">
                <strong>${item.name}</strong><br>
                Price: ₹${item.price}<br>
                Quantity: ${item.quantity}<br>
                Subtotal: ₹${item.price * item.quantity}<br>
                <button onclick="removeItem('${item.name}')">Remove</button>
            </div>
            <hr>
        `;
    });

    output += `<h3>Total: ₹${total}</h3>`;
    output += `<button onclick="clearCart()">Clear Cart</button>`;

    document.getElementById("cartItems").innerHTML = output;
}

// Clear cart
function clearCart() {
    localStorage.removeItem("cart");
    displayCart();
}
