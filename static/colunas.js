const logout = document.getElementById("logout");

//evento de click para fazer logout
logout.addEventListener('click', (event) => {
    event.preventDefault()
    window.location.href = '/index';
});

// Colunas evt drag on drop
const columns = document.querySelectorAll(".column_cards");
let draggedCard;

const dragStart = (event) => {
    draggedCard = event.target;
    console.log(draggedCard);
    event.dataTransfer.effectAllowed = "move";
};

const dragOver = (event) => {
    event.preventDefault();
};

const dragEnter = ({ target }) => {
    if (target.classList.contains("column_cards")) {
        target.classList.add("column--highlight");
    }
};

const dragLeave = ({ target }) => {
    target.classList.remove("column--highlight");
};

const drop = ({ target }) => {
    if (target.classList.contains("column_cards")) {
        target.classList.remove("column--highlight");
        target.append(draggedCard);  
    }
};

const createCard = ({ target }) => {
    const card = document.createElement("section")
    card.className = "card";
    if (target.classList.contains("column_cards")) {
        target.classList.remove("column--highlight");
        target.append(card);  
    }
    card.draggable = "true";
    card.contentEditable = "true";
    card.focus();

    card.addEventListener("focusout", () => {
        card.contentEditable = "false";
        if(!card.textContent) card.remove();
    });
    card.addEventListener("dragstart", dragStart);
}; 

columns.forEach((column) => {
    column.addEventListener("dragover", dragOver);
    column.addEventListener("dragenter", dragEnter);
    column.addEventListener("dragleave", dragLeave);
    column.addEventListener("drop", drop);
    column.addEventListener("dblclick", createCard);
});

