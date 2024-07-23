
// document.addEventListener('DOMContentLoaded', () => {
//     const button = document.getElementById('sortear');
//     let isRed = true; // Variable para alternar colores

//     // Función para alternar colores
//     const intervalId = setInterval(() => {
//         button.style.backgroundColor = isRed ? 'red' : 'white';
//         isRed = !isRed; // Alterna entre true y false
//     }, 600); // Cambia de color cada medio segundo

//     button.addEventListener('click', () => {
//         // Detiene el destello
//         clearInterval(intervalId);
        
//         // Oculta el botón
//         button.style.display = 'none';

//         // Reaparece el botón después de 20 segundos
//         setTimeout(() => {
//             button.style.display = 'block';
//             // Reinicia el destello al reaparecer
//             const newIntervalId = setInterval(() => {
//                 button.style.backgroundColor = isRed ? 'red' : 'white';
//                 isRed = !isRed; // Alterna entre true y false
//             }, 500); // Cambia de color cada medio segundo
//         }, 20000); // 20,000 ms = 20 segundos
//     });
// });

const ruleta = document.getElementById("ruleta");

let ganador = "";

document.getElementById("sortear").addEventListener("click", () => sortear());

const sigueIntentando1 = { 
    nombre: "Sigue intentando", 
    probabilidad: 6.25 
};
const argos = { 
    nombre: "Argos", 
    probabilidad: 6.25 
};
const firplak = { 
    nombre: "firplak", 
    probabilidad: 6.25 
};
const sika = { 
    nombre: "Sika", 
    probabilidad: 6.25 
};
const sigueIntentando2 = { 
    nombre: "Sigue intentando", 
    probabilidad: 6.25 
};
const pavco = { 
    nombre: "Pavco", 
    probabilidad: 6.25 
};
const raspaYGana1 = { 
    nombre: "Raspa y Gana", 
    probabilidad: 6.25 
};
const rotoPlas = { 
    nombre: "Roto plas", 
    probabilidad: 6.25 
};
const sigueIntentando3 = { 
    nombre: "Sigue intentando", 
    probabilidad: 6.25 
};
const sigma = { 
    nombre: "Sigma", 
    probabilidad: 6.25 
};
const brilla = { 
    nombre: "Brilla", 
    probabilidad: 6.25 
};
const corona = { 
    nombre: "Corona", 
    probabilidad: 6.25 
};
const sigueIntentando4 = { 
    nombre: "Sigue intentando", 
    probabilidad: 6.25 
};
const pintuco = { 
    nombre: "Pintuco", 
    probabilidad: 6.25 
};
const raspaYGana2 = { 
    nombre: "Raspa y Gana", 
    probabilidad: 6.25 
};
const mazter = { 
    nombre: "Mazter", 
    probabilidad: 6.25 
};
const sigeIntentando = { 
    nombre: "Sige intentando", 
    probabilidad: 6.25 
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
    opcionesContainer.id = "opcionesContainer"
    ruleta.appendChild(opcionesContainer);
    let pAcumulada = 0;
    //Crear contenido dinamico dentro de la ruleta
    conceptos.forEach((concepto, i) => {
        const opcionElement = document.createElement("div");
        opcionElement.classList.add("opcion");
        opcionesContainer.appendChild(opcionElement);
        opcionElement.style = `
            background-color: ${colores[i]};
            transform: rotate(${probabilidadAGrados(pAcumulada)}deg);
            ${getPosicionParaProbabilidad(concepto.probabilidad)}
        `
        pAcumulada += concepto.probabilidad
        const separador = document.createElement("div");
        separador.classList.add("separador");
        ruleta.appendChild(separador);
        separador.style = `
            transform: rotate(${probabilidadAGrados(pAcumulada)}deg);
        `
        ruleta.appendChild(separador);
    })

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
    let pAcumulada = 0;
    nSorteo = Math.random();
    conceptos.forEach(concepto => {
        if (nSorteo*100 > pAcumulada && nSorteo*100 < pAcumulada+concepto.probabilidad) {
            ganador = concepto.nombre;
            console.log("Ganador", nSorteo*100, concepto.nombre, "porque está entre ",pAcumulada, "y",pAcumulada+concepto.probabilidad)
        }
        pAcumulada += concepto.probabilidad;
    })
}


ajustarRuleta(); //Llamado a la función


