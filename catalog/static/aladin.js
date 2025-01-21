let aladin;
let aladinData = window.aladinData;
html = `<p>${aladinData.name} (${aladinData.type}): ${aladinData.ra} ${aladinData.dec}</p>`
document.getElementById("text").innerHTML = html
let surveyname;
if(aladinData.dec < -31.5){
    surveyname = 'CDS/P/DSS2/color'
}
else{
    surveyname = 'CDS/P/PanSTARRS/DR1/color-i-r-g'
}
A.init.then(() => {
    aladin = A.aladin('#aladin-lite-div', {survey: surveyname, fov:aladinData.fovValue, target: aladinData.loc});
});