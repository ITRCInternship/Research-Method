
document.addEventListener("DOMContentLoaded", () => {
  const members = document.querySelectorAll(".team-member");
  members.forEach((member, index) => {
    setTimeout(() => {
      member.classList.add("visible");
    }, index * 200); 
  });
});
