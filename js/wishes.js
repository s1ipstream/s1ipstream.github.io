const wishes = [
  "Pause & Breathe",
  "Name the Boundary",
  "Ask for a Chest-Feel Rating",
  "State the Clock",
  "Timed Exit Clause"
];
document.getElementById("wish-btn")?.addEventListener("click", () => {
  const ul = document.getElementById("wish-list");
  ul.innerHTML = "";
  wishes
    .sort(() => 0.5 - Math.random())
    .slice(0, 3)
    .forEach(w => ul.insertAdjacentHTML("beforeend", `<li>${w}</li>`));
}); 