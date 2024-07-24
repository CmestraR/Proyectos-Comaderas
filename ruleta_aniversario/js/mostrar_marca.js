function mostrarMarca(ganador) {

    const argos = document.querySelector('.argos');
    const brilla = document.querySelector('.brilla');
    const corona = document.querySelector('.corona');
    const firplak = document.querySelector('.firplak');
    const mazter = document.querySelector('.mazter');
    const pavco = document.querySelector('.pavco');
    const pintuco = document.querySelector('.pintuco');
    const raspaYgana = document.querySelector('.raspaYgana');
    const rotoplas = document.querySelector('.rotoplas');
    const sigma = document.querySelector('.sigma');
    const sige = document.querySelector('.sige');
    const sika = document.querySelector('.sika');

    // Ocultar todas las imágenes inicialmente
    const todasLasImagenes = [argos, brilla, corona, firplak, mazter, pavco, pintuco, raspaYgana, rotoplas, sigma, sige, sika];
    todasLasImagenes.forEach(img => img.style.display = 'none');

    // Mostrar la imagen correspondiente según el ganador
    if (ganador === "Ganador patrocinado por Argos") {
        argos.style.display = 'block';
    } else if (ganador === "Ganador patrocinado por Brilla") {
        brilla.style.display = 'block';
    } else if (ganador === "Ganador patrocinado por Corona") {
        corona.style.display = 'block';
    } else if (ganador === "Ganador patrocinado por Firplak") {
        firplak.style.display = 'block';
    } else if (ganador === "Ganador patrocinado por Mazter") {
        mazter.style.display = 'block';
    } else if (ganador === "Ganador patrocinado por Pavco") {
        pavco.style.display = 'block';
    } else if (ganador === "Ganador patrocinado por Pintuco") {
        pintuco.style.display = 'block';
    } else if (ganador === "Raspa y Gana") {
        raspaYgana.style.display = 'block';
    } else if (ganador === "Ganador patrocinado por Rotoplas") {
        rotoplas.style.display = 'block';
    } else if (ganador === "Ganador patrocinado por Sigma") {
        sigma.style.display = 'block';
    } else if (ganador === "Sigue intentando") {
        sige.style.display = 'block';
    } else if (ganador === "Ganador patrocinado por Sika") {
        sika.style.display = 'block';
    }
    
    console.log('Mostrar marca', ganador);
}
        