document.addEventListener("DOMContentLoaded", function () {
  const app = new Vue({
    el: "#app",
    data: {},
    methods: {
      confirmDelete(trackingId) {
        const confirmation = window.confirm(
          "Voulez-vous vraiment supprimer ce suivi ?"
        );
        if (confirmation) {
          this.deleteTracking(trackingId);
        }
      },
      deleteTracking(trackingId) {
        const formData = {
          tracking_id: trackingId,
        };

        $.ajax({
          url: "/delete_tracking",
          type: "POST",
          data: formData,
          dataType: "json",
          success: (data) => {
            window.location.href = window.location.href;
            console.log("succes JS");
            console.log(formData);
            console.log(data);
          },
          error: (error) => {
            console.log(JSON.parse(error.responseText).error);
            console.log("error JS");
            // Gérer les erreurs
          },
        });
      },
      showTracking(trackingId) {
        window.location.href = `/tracking/${trackingId}/show_tracking`;
      },
    },
  });
  const formattedDateElements = document.querySelectorAll(".formatted-date");
  formattedDateElements.forEach((element) => {
    const isoDate = element.textContent;
    const dateToFormat = new Date(isoDate);
    element.textContent = dateToFormat.toLocaleDateString("fr-FR");
  });
});
