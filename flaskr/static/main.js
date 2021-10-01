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

// Use bootstrap navbar to make the active page in the header bold
function setActivePage()
{
    url = window.location.href
    url_suffix = url.substring(url.indexOf('.com') + 5)
    end = url_suffix.indexOf('/')
    end === -1 ? cur_page = url_suffix : cur_page = url_suffix.substring(0, end)
    console.log(cur_page)
    page = document.getElementById(cur_page)
    if (page !== null) page.setAttribute('class', 'nav-link active')
}

// Wait until DOM is loaded
document.addEventListener("DOMContentLoaded", () =>
{
    setFooter();
    setActivePage();
});