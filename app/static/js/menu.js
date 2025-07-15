const toggle = document.querySelector('.toggle');
const menu = document.querySelector('.menu');

toggle.onclick = () => {
    toggle.classList.toggle('active');
    menu.classList.toggle('active');
}

const list = document.querySelectorAll('li')
function SetActiveLink(){
    list.forEach( (item) => 
        item.classList.remove('active')
    );
    this.classList.add('active')
}

list.forEach( (item) => 
item.addEventListener('click',SetActiveLink));