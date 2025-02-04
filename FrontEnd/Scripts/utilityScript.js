// JavaScript for navbar functionality

// Select elements
const menuButton = document.getElementById('menu');
const crossButton = document.getElementById('cross');
const menuList = document.querySelector('.menu-list');

// Function to show the menu
function showMenu() {
    menuList.style.display = 'flex'; // Make the menu visible
    menuList.classList.add('menu-visible'); // Optional: Add a class for additional styling (e.g., animations)
    menuButton.style.display = 'none'; // Hide the menu icon
}

// Function to hide the menu
function hideMenu() {
    menuList.style.display = 'none'; // Hide the menu
    menuList.classList.remove('menu-visible'); // Remove the styling class
    menuButton.style.display = 'block'; // Show the menu icon
}

// Add event listeners
menuButton.addEventListener('click', showMenu);
crossButton.addEventListener('click', hideMenu);

// Optional: Close the menu when clicking outside it
document.addEventListener('click', (event) => {
    if (!menuList.contains(event.target) && !menuButton.contains(event.target)) {
        hideMenu();
    }
});