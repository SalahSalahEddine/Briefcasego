function toggleMode() {
    const html = document.documentElement;
    const current = html.getAttribute("data-theme");
    html.setAttribute("data-theme", current === "light" ? "dark" : "light");
}
function toggleBusinessForm() {
    const form = document.getElementById("businessSignup");
    form.style.display = form.style.display === "none" || form.style.display === "" ? "block" : "none";
    form.scrollIntoView({ behavior: "smooth" });
}
function toggleLoginForm() {
    const section = document.getElementById("login-section");
    section.style.display = section.style.display === "none" ? "block" : "none";
}
function showForm() {
      document.getElementById("contractForm").style.display = "block";
      document.getElementById("overlay").style.display = "block";
}
function showAnnounceForm(){
    document.getElementById("AnnounceForm").style.display = "block";
    document.getElementById("overlay").style.display = "block";
}
function showUpContractDetailsForIpfsandDownload(){
    document.getElementById("contract_details_for_download").style.display = "block";
}
document.getElementById('price').disabled = true;
