const blogsPerPage = 3;
let currentIndex = 0;
const blogCards = Array.from(document.getElementsByClassName("blog-card"));

function renderBlogs() {
    blogCards.forEach((card, index) => {
        card.style.display = (index >= currentIndex && index < currentIndex + blogsPerPage)
            ? "block"
            : "none";
    });

    // Toggle arrow visibility
    document.getElementById("arrow-left").style.display = currentIndex > 0 ? "block" : "none";
    document.getElementById("arrow").style.display = currentIndex + blogsPerPage < blogCards.length ? "block" : "none";
}

document.getElementById("arrow").onclick = () => {
    if (currentIndex + blogsPerPage < blogCards.length) {
        currentIndex += blogsPerPage;
        renderBlogs();
    }
};

document.getElementById("arrow-left").onclick = () => {
    if (currentIndex - blogsPerPage >= 0) {
        currentIndex -= blogsPerPage;
        renderBlogs();
    }
};

blogCards.forEach(card => {
    card.onclick = () => {
        const title = card.dataset.title;
        const content = card.dataset.content;
        const body = card.dataset.body;
        document.getElementById("expanded-title").innerText = title;
        document.getElementById("expanded-content").innerText = content;
        document.getElementById("expanded-body").innerText = body;
        document.getElementById("expanded-blog").style.display = "block";
        document.getElementById("main-content").classList.add("blur");
    };
});

document.getElementById("close-btn").onclick = () => {
    document.getElementById("expanded-blog").style.display = "none";
    document.getElementById("main-content").classList.remove("blur");


};

// Initial render
renderBlogs();