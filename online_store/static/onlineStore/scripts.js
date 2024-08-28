document.addEventListener('DOMContentLoaded',function(){
    const btn= document.querySelector('.form_btn')
    const form= document.querySelector('.form')
    btn.onclick= function(){
        form.classList.toggle('active_form')
    }
})
document.addEventListener('DOMContentLoaded',function(){
    const btn2= document.querySelector('.form_btn2')
    const form2= document.querySelector('.form2')
    btn2.onclick= function(){
        form2.classList.toggle('active_form2')
    }     
})
document.addEventListener('DOMContentLoaded',function() {
    // menu deroulant
    const links= document.querySelector('header nav')
    const menu_list= document.querySelector('.menu-bar') //  selection de "menu_list"
    menu_list.onclick = function(){    // on ajoute a menu_list un ajouteur d'un evenement ".onclick" ensuite on definie une fonction pour reagir dondc tout les scripts suivant n'agisse que si l'evenement se produit 
        menu_list.classList.toggle("active")  // ".classList.toggle("nom_selecteur_css") ajoute la classe  specifie comme argument si elle est presente sinon elle l'enleve"
        links.classList.toggle('menu')
    }
})
