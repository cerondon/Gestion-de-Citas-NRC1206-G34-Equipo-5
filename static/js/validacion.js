function validar_registro(){
    vNombre=document.getElementById("nombre").value;
    vApellido=document.getElementById("apellido").value;
    vUsuario=document.getElementById("usuario").value;
    vEmail=document.getElementById("email").value;
    //expresión regular para validar el correo eléctrónico correcto
    var expReg= /^[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?$/;
    vContraseña=document.getElementById("password").value;
    vC_Contraseña=document.getElementById("c_password").value;
    vConfirmar=document.getElementById("confirmar");


    if (vNombre==""){
        alert("El campo Nombres no puede estar vacío");
        return false
    }else if(vApellido==""){
        alert("El campo Apellidos no puede estar vacío");
        return false   
    }else if(vUsuario==""){
        alert("El campo Usuario no debe estar vacío");
        return false
    }else if(vUsuario.length<8){
        alert("El campo Usuario debe tener mínimo 8 caracteres");
        return false
    }else if(vEmail==""){
        alert("El campo Correo no debe estar vacío");
        return false
    }else if ( expReg.test( vEmail ) == false ){
        alert("Correo no válido.")
        return false;
    }else if(vContraseña==""){
        alert("El campo Contraseña no debe estar vacío");
        return false
    }else if(vContraseña.length<8){
        alert("El campo Contraseña debe tener mínimo 8 caracteres");
        return false
    }else if(vC_Contraseña!=vContraseña){
        alert("La constraseñas no coinciden");
        return false
    }else if(!vConfirmar.checked){
        alert("Debe aceptar las condiciones generales y la normativa de protección de datos");
        return false
    }
}

function validar_login(){
    vUsuario=document.getElementById("usuario").value;
    vContraseña=document.getElementById("password").value;

    if(vUsuario==""){
        alert("El campo Usuario no debe estar vacío");
        return false
    }else if(vUsuario.length<8){
        alert("El campo Usuario debe tener mínimo 8 caracteres");
        return false
    }else if(vContraseña==""){
        alert("El campo Contraseña no debe estar vacío");
        return false
    }else if(vContraseña.length<8){
        alert("El campo Contraseña debe tener mínimo 8 caracteres");
        return false
    }
}

function mostrarPassword(){
    var obj = document.getElementById("password");
    obj.type = "text";
}

function ocultarPassword(){
    var obj = document.getElementById("password");
    obj.type = "password";
}
function limpiarFormulario() {
    document.getElementById("miForm").reset();
  }



