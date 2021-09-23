// Position footer at bottom of viewport if it is floating
// If there is enough content pushing it off the screen leave it as is
function setFooter()
{
    let footer = document.querySelector("footer");
    let rect = footer.getBoundingClientRect();

    // If the footer is higher than the height of the viewport, move it down
    if (rect.bottom < window.innerHeight)
    {
        footer.style.position = "absolute";
        footer.style.bottom = "0";
    }
}

// Wait until DOM is loaded
document.addEventListener("DOMContentLoaded", () =>
{
    setFooter();
});