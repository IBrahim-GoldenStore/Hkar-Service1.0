document.addEventListener('DOMContentLoaded',function(){
    const btn= document.querySelector('.form_btn')
    const form= document.querySelector('.form')
    btn.onclick= function(){
        form.classList.toggle('active_form')
    }
    const address_holder= document.getElementById('id_adresse')
    const number_holder= document.getElementById('id_number')
    address_holder.placeholder="Vôtre résidence"
    number_holder.placeholder="Numéro"
})
document.addEventListener('DOMContentLoaded',function(){
    const btn2= document.querySelector('.form_btn2')
    const form2= document.querySelector('.form2')
    btn2.onclick= function(){
        form2.classList.toggle('active_form2')
    }
    const address_holder= document.getElementById('id_adresse')
    const number_holder= document.getElementById('id_number')
    address_holder.placeholder="Vôtre résidence"
    number_holder.placeholder="Numéro"
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
document.addEventListener('DOMContentLoaded',function() {
    let lastScrollTop= 0
    const header = document.querySelector('header')

    window.addEventListener('scroll', function(){
        const scrollTop= window.scrollY || this.document.documentElement.scrollTop
        if (scrollTop > lastScrollTop){
            header.classList.add('header-hidden')
        }
        else{
            header.classList.remove('header-hidden')
        }
        lastScrollTop = scrollTop <= 0 ? 0 : scrollTop
    })
})
document.addEventListener('DOMContentLoaded',function(){
    const btn2= document.querySelector('.form_btn2')
    const form2= document.querySelector('.form2')
    btn2.onclick= function(){
        form2.classList.toggle('active_form2')
    }
    const name_holder= document.getElementById('id_name')
    const email_holder= document.getElementById('id_email')
    const address_holder= document.getElementById('id_adresse')
    const number_holder= document.getElementById('id_number')
    address_holder.placeholder="Votre residence"
    number_holder.placeholder="Numero"
    name_holder.placeholder="Votre Nom"
    email_holder.placeholder="Email"
})
//const image= document.querySelectorAll('.produit-img')

//image.forEach(function(element){
   //element.addEventListener('mouseover',function(){
       //element.classList.add('hover-effect')
   //})
   //element.addEventListener('mouseout',function(){
       //element.classList.remove('hover-effect')
   //})
//});

//const imageArticle= document.querySelectorAll('.produit-article-img')

//imageArticle.forEach(function(element){
   //element.addEventListener('mouseover',function(){
       //element.classList.add('hover-effect')
   //})
   //element.addEventListener('mouseout',function(){
       //element.classList.remove('hover-effect')
   //})
//});
