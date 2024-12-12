document.addEventListener('DOMContentLoaded',function(){
    const username= document.getElementById('id_username')
    const password= document.getElementById('id_password')
    const button= document.getElementById('visibility')

    username.placeholder="Nom d'utilisateur"
    password.placeholder="mots de passe"

    button.onclick= function(){
        if(password.type == 'password'){
            password.type = 'text'
        }
        else {
            password.type = 'password'
        }
    }
})
// nouveau
document.addEventListener('DOMContentLoaded',function(){
    localStorage.clear()
    const set_none= document.getElementById('set_style')
    const pop_up= document.getElementById('pop-up')

    if(localStorage.getItem('pop_state') === 'true'){
        pop_up.style.display='none'
    }

    set_none.onclick = function(){
        pop_up.style.display='none'
        localStorage.setItem('pop_state','true')
    }
})
// fin nouveau
document.addEventListener('DOMContentLoaded',function(){
    const username= document.getElementById('id_username')
    const password1= document.getElementById('id_password1')
    const password2= document.getElementById('id_password2')
    const code= document.getElementById('id_code')
    const button= document.getElementById('visibility-sigin')

    username.placeholder= "Nom d'utilisateur"
    password1.placeholder="mots de passe"
    password2.placeholder="confirmation du mots de passe"
    code.placeholder= "Saissisez le code"

    button.onclick= function(){
        if(password1.type == 'password'){
            password1.type ='text'
            password2.type = 'text'
        }
        else {
            password1.type = 'password'
            password2.type = 'password'
        }
    }
})
document.addEventListener('DOMContentLoaded',function(){
    var button= document.getElementById('input3')
    var password1= document.getElementById('id_new_password1')
    var password2= document.getElementById('id_new_password2')

    password1.placeholder="Nouveau mots de passe"
    password2.placeholder="confirmation du mots de passe"

    button.onclick= function(){
        if(password1.type == 'password'){
            password1.type ='text'
            password2.type = 'text'
            button.value = 'Masquer'
        }
        else {
            password1.type = 'password'
            password2.type = 'password'
            button.value = 'Afficher'
        }
    }
})