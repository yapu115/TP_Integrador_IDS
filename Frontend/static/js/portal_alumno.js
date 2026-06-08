document.addEventListener("DOMContentLoaded", () => {
  const portal = document.querySelector("[data-student-portal]");
  if (!portal) return;

  const studentName = document.querySelector("[data-student-display-name]");
  const studentPadron = document.querySelector("[data-student-display-padron]");

  const updateStudentIdentity = (button) => {
    if (studentName && button.dataset.studentName) {
      studentName.textContent = button.dataset.studentName;
    }

    if (studentPadron && button.dataset.studentPadron) {
      studentPadron.textContent = button.dataset.studentPadron;
    }
  };

  portal.querySelectorAll("[data-course-target]").forEach((button) => {
    button.addEventListener("click", () => {
      portal.querySelectorAll("[data-course-target]").forEach((item) => {
        item.classList.toggle("is-active", item === button);
      });

      portal.querySelectorAll(".course-panel").forEach((panel) => {
        panel.classList.toggle("is-active", panel.id === button.dataset.courseTarget);
      });

      updateStudentIdentity(button);
    });
  });

  portal.querySelectorAll(".student-tab").forEach((button) => {
    button.addEventListener("click", () => {
      const coursePanel = button.closest(".course-panel");
      if (!coursePanel) return;

      coursePanel.querySelectorAll(".student-tab").forEach((tab) => {
        tab.classList.toggle("is-active", tab === button);
      });

      coursePanel.querySelectorAll(".tab-panel").forEach((panel) => {
        panel.classList.toggle("is-active", panel.id === button.dataset.tabTarget);
      });
    });
  });
});
