document.addEventListener('DOMContentLoaded', () => {
    const button = document.getElementById('sortear');
    let isRed = true; // Variable para alternar colores

    // Función para alternar colores
    const intervalId = setInterval(() => {
        button.style.backgroundColor = isRed ? 'red' : 'white';
        isRed = !isRed; // Alterna entre true y false
    }, 600); // Cambia de color cada medio segundo

    button.addEventListener('click', () => {
        // Detiene el destello
        clearInterval(intervalId);
        
        // Oculta el botón
        button.style.display = 'none';

        // Reaparece el botón después de 20 segundos
        setTimeout(() => {
            button.style.display = 'block';
            // Reinicia el destello al reaparecer
            const newIntervalId = setInterval(() => {
                button.style.backgroundColor = isRed ? 'red' : 'white';
                isRed = !isRed; // Alterna entre true y false
            }, 500); // Cambia de color cada medio segundo
        }, 20000); // 20,000 ms = 20 segundos
    });
});









const ruleta = document.getElementById("ruleta");


const blanco = { nombre: "Blanco", probabilidad: 6.25 };
const amarillo = { nombre: "Amarillo", probabilidad: 6.25 };
const naranja = { nombre: "Naranja", probabilidad: 6.25 };
const blanco4 = { nombre: "Blanco", probabilidad: 6.25 };
const negro = { nombre: "Negro", probabilidad: 6.25 };
const azul = { nombre: "Azul", probabilidad: 6.25 };
const verde = { nombre: "Verde", probabilidad: 6.25 };
const azulClaro2 = { nombre: "Azul Claro", probabilidad: 6.25 };
const blanco2 = { nombre: "Blanco", probabilidad: 6.25 };
const amarillo2 = { nombre: "Amarillo", probabilidad: 6.25 };
const naranja2 = { nombre: "Naranja", probabilidad: 6.25 };
const blanco3 = { nombre: "Blanco", probabilidad: 6.25 };
const negro2 = { nombre: "Negro", probabilidad: 6.25 };
const azul2 = { nombre: "Azul", probabilidad: 6.25 };
const verde2 = { nombre: "Verde", probabilidad: 6.25 };
const azulClaro = { nombre: "Azul Claro", probabilidad: 6.25 };
const blanco5 = { nombre: "Blanco", probabilidad: 6.25 };

let conceptos = [
    blanco, 
    amarillo, 
    naranja, 
    azulClaro, 
    negro, 
    verde, 
    azul, 
    blanco2, 
    amarillo2, 
    naranja2, 
    azulClaro2, 
    negro2, 
    verde2, 
    azul2, 
    blanco3, 
    blanco4
];

const colores = [
    "#FFFFFF", // Blanco
    "#FFFF00", // Amarillo
    "#FFA500", // Naranja
    "#FFFFFF", // Blanco
    "#000000", // Negro
    "#0000FF", // Azul
    "#008000", // Verde
    "#ADD8E6", // Azul claro
    "#FFFFFF", // Blanco
    "#FFFF00", // Amarillo
    "#FFA500", // Naranja
    "#FFFFFF", // Blanco
    "#000000", // Negro
    "#0000FF", // Azul
    "#008000", // Verde
    "#ADD8E6", // Azul claro
    "#FFFFFF"  // Blanco
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



ajustarRuleta();