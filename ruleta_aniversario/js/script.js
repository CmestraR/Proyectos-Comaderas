
const ruleta = document.getElementById("ruleta");
let ganador = "";
const root = document.documentElement;
let sorteando = false;
let animacionCarga;
let animacionMostrarMarcas;
const ganadorTexto = document.getElementById("ganadorTexto");
const ganadorTextoElement = document.getElementById("ganadorTexto");
const audioFondo = document.getElementById('audioFondo'); // Elemento de audio de fondo


function iniciarAudioFondo() {
    if (audioFondo) {
        audioFondo.play().catch(error => {
            console.error('Error al reproducir el audio de fondo:', error);
        });
    }
}


function ocultarImagenes() {
    const imagenesEspecificas = [
        '.brilla',
        '.corona',
        '.firplak',
        '.mazter',
        '.pavco',
        '.pintuco',
        '.raspaYgana',
        '.sika',
        '.rotoplas',
        '.sigma',
        '.sige',
        '.argos'
    ].map(selector => document.querySelector(selector));
    imagenesEspecificas.forEach(img => img.style.display = 'none');
}

function detenerAudioFondo() {
    if (audioFondo) {
        audioFondo.pause();
        audioFondo.currentTime = 0; // Reiniciar el tiempo de reproducción
    }

}



document.getElementById("sortear").addEventListener("click", () => {
    ocultarImagenes();
    sortear();
    detenerAudioFondo();
    setTimeout(() => {
        mostrarMarca(ganador);
        iniciarAudioFondo();
    }, 5280);

    // Reproducir el audio
    if (audioReproduccion) {
        audioReproduccion.play().catch(error => {
            console.error('Error al reproducir el audio:', error);
        });
    }

    setTimeout(() => {
        ganadorTexto.textContent = '¡Presiona en "Girar" para iniciar!';
        ocultarImagenes(); // Ocultar imágenes cuando el texto cambia
    }, 15000);

});

const sigueIntentando1 = {
    nombre: "Sigue intentando",
    probabilidad: 6.25,
};
const argos = {
    nombre: "Ganador patrocinado por Argos",
    probabilidad: 6.25,
};
const firplak = {
    nombre: "Ganador patrocinado por Firplak",
    probabilidad: 6.25,
};
const sika = {
    nombre: "Ganador patrocinado por Sika",
    probabilidad: 6.25,
};
const sigueIntentando2 = {
    nombre: "Sigue intentando",
    probabilidad: 6.25,
};
const pavco = {
    nombre: "Ganador patrocinado por Pavco",
    probabilidad: 6.25,
};
const raspaYGana1 = {
    nombre: "Raspa y Gana",
    probabilidad: 6.25,
};
const rotoPlas = {
    nombre: "Ganador patrocinado por Rotoplas",
    probabilidad: 6.25,
};
const sigueIntentando3 = {
    nombre: "Sigue intentando",
    probabilidad: 6.25,
};
const sigma = {
    nombre: "Ganador patrocinado por Sigma",
    probabilidad: 6.25,
};
const brilla = {
    nombre: "Ganador patrocinado por Brilla",
    probabilidad: 6.25,
};
const corona = {
    nombre: "Ganador patrocinado por Corona",
    probabilidad: 6.25,
};
const sigueIntentando4 = {
    nombre: "Sigue intentando",
    probabilidad: 6.25,
};
const pintuco = {
    nombre: "Ganador patrocinado por Pintuco",
    probabilidad: 6.25,

};
const raspaYGana2 = {
    nombre: "Raspa y Gana",
    probabilidad: 6.25,
};
const mazter = {
    nombre: "Ganador patrocinado por Mazter",
    probabilidad: 6.25,
};
const sigeIntentando = {
    nombre: "Sige intentando",
    probabilidad: 6.25,
};


const conceptos = [
    sigueIntentando1,
    argos,
    firplak,
    sika,
    sigueIntentando2,
    pavco,
    raspaYGana1,
    rotoPlas,
    sigueIntentando3,
    sigma,
    brilla,
    corona,
    sigueIntentando4,
    pintuco,
    raspaYGana2,
    mazter,
    sigeIntentando
];


const colores = [
    "#FFFFFF", // Sigue intentando 
    "#D9E021", // Argos
    "#009FE3", // firplak
    "#FBC600", // Sika
    "#FFFFFF", // Sigue intentando
    "#2B2C82", // Pavco
    "#E52539", // Raspa y Gana
    "#8DC53E", // Roto plas
    "#FFFFFF", // Sigue intendando 
    "#B3EAFF", // Sigma 
    "#E10B17", // Brilla
    "#0069B3", // Corona
    "#FFFFFF", // Sigue intentando
    "#002C6A", // Pintuco 
    "#E31E24", // Raspa y Gana
    "#3C64AC", // Mazter
    "#FFFFFF"  // Sige intentando
];


function ajustarRuleta() {
    const opcionesContainer = document.createElement("div");
    opcionesContainer.id = "opcionesContainer";
    ruleta.appendChild(opcionesContainer);
    let pAcumulada = 0;

    conceptos.forEach((concepto, i) => {
        const opcionElement = document.createElement("div");
        opcionElement.classList.add("opcion");
        opcionesContainer.appendChild(opcionElement);
        opcionElement.style = `
            background-color: ${colores[i]};
            transform: rotate(${probabilidadAGrados(pAcumulada)}deg);
            ${getPosicionParaProbabilidad(concepto.probabilidad)}
        `;

        const imagen = document.createElement("img");
        //imagen.src = concepto.imagen;
        // Añadir una clase específica basada en el nombre
        imagen.classList.add(`imagen-${concepto.nombre.toLowerCase().replace(/\s+/g, '-')}`);
        opcionElement.appendChild(imagen);
        pAcumulada += concepto.probabilidad;
        const separador = document.createElement("div");
        separador.classList.add("separador");
        ruleta.appendChild(separador);
        separador.style = `
            transform: rotate(${probabilidadAGrados(pAcumulada)}deg);
        `;
    });
}



function getPosicionParaProbabilidad(probabilidad) {
    if (probabilidad === 100) {
        return ''
    }
    if (probabilidad >= 87.5) {
        const x5 = Math.tan(probabilidadARadianes(probabilidad)) * 50 + 50;
        return `clip-path: polygon(50% 0%, 100% 0, 100% 100%, 0 100%, 0 0, ${x5}% 0, 50% 50%)`
    }
    if (probabilidad >= 75) {
        const y5 = 100 - (Math.tan(probabilidadARadianes(probabilidad - 75)) * 50 + 50);
        return `clip-path: polygon(50% 0%, 100% 0, 100% 100%, 0 100%, 0% ${y5}%, 50% 50%)`
    }
    if (probabilidad >= 62.5) {
        const y5 = 100 - (0.5 - (0.5 / Math.tan(probabilidadARadianes(probabilidad)))) * 100;
        return `clip-path: polygon(50% 0%, 100% 0, 100% 100%, 0 100%, 0% ${y5}%, 50% 50%)`
    }
    if (probabilidad >= 50) {
        const x4 = 100 - (Math.tan(probabilidadARadianes(probabilidad)) * 50 + 50);
        return `clip-path: polygon(50% 0, 100% 0, 100% 100%, ${x4}% 100%, 50% 50%)`
    }
    if (probabilidad >= 37.5) {
        const x4 = 100 - (Math.tan(probabilidadARadianes(probabilidad)) * 50 + 50);
        return `clip-path: polygon(50% 0, 100% 0, 100% 100%, ${x4}% 100%, 50% 50%)`
    }
    if (probabilidad >= 25) {
        const y3 = Math.tan(probabilidadARadianes(probabilidad - 25)) * 50 + 50;
        return `clip-path: polygon(50% 0, 100% 0, 100% ${y3}%, 50% 50%)`
    }
    if (probabilidad >= 12.5) {
        const y3 = (0.5 - (0.5 / Math.tan(probabilidadARadianes(probabilidad)))) * 100;
        return `clip-path: polygon(50% 0, 100% 0, 100% ${y3}%, 50% 50%)`
    }
    if (probabilidad >= 0) {
        const x2 = Math.tan(probabilidadARadianes(probabilidad)) * 50 + 50;
        return `clip-path: polygon(50% 0, ${x2}% 0, 50% 50%)`
    }
}


function sortear() {
    if (sorteando) return;
    sorteando = true;
    ganadorTextoElement.textContent = ".";
    animacionCarga = setInterval(() => {
        switch (ganadorTextoElement.textContent) {
            case ".":
                ganadorTextoElement.textContent = ".."
                break;
            case "..":
                ganadorTextoElement.textContent = "..."
                break;
            default:
                ganadorTextoElement.textContent = "."
                break;
        }
    }, 500)
    let pAcumulada = 0;
    nSorteo = Math.random();
    ruleta.classList.toggle("girar", true);
    conceptos.forEach((concepto, i) => {
        if (nSorteo * 100 >= pAcumulada && nSorteo * 100 < pAcumulada + concepto.probabilidad) {
            ganador = concepto.nombre;
            ganador = ganador;
            // 5280 milisegundos = 5.28 segundos 
            //console.log("Ganador", nSorteo*100, concepto.nombre, "porque está entre ",pAcumulada, "y",pAcumulada+concepto.probabilidad)
        }
        pAcumulada += concepto.probabilidad;
        console.log(ganador);
    })
    const giroRuleta = 10 * 360 + (1 - nSorteo * 360)
    root.style.setProperty("--giroRuleta", giroRuleta + "deg")
}

ruleta.addEventListener("animationend", () => {
    ruleta.style.transform = "rotate(" + getCurrentRotation(ruleta) + "deg)";
    ruleta.classList.toggle("girar", false);
    sorteando = false;
    ganadorTexto.textContent = ganador;
    clearInterval(animacionCarga);
    clearInterval(animacionMostrarMarcas);
})


iniciarAudioFondo();
//compararYMostrarImagen(); //Ejecutar la función para comparar y mostrar la imagen
ajustarRuleta(); //Llamado a la función


