document.addEventListener("DOMContentLoaded", function () {
  const app = new Vue({
    el: "#app",
    data: {},
    methods: {
      confirmDelete(vehicleId) {
        const confirmation = window.confirm(
          "Voulez-vous vraiment supprimer ce véhicule ? Cela entraînera la perte totale des données de suivi."
        );
        if (confirmation) {
          this.deleteVehicle(vehicleId);
        }
      },
      deleteVehicle(vehicleId) {
        const formData = {
          vehicle_id: vehicleId,
        };

        $.ajax({
          url: "/delete_vehicle",
          type: "POST",
          data: formData,
          dataType: "json",
          success: (data) => {
            window.location.href = window.location.href;
            console.log("succes JS");
            console.log(formData);
            console.log(data);
            // Gérer la réponse après la suppression du véhicule
            // window.location.href = "/dashboard/";
          },
          error: (error) => {
            console.log(JSON.parse(error.responseText).error);
            console.log("error JS");
            // Gérer les erreurs
          },
        });
      },

      createTracking(vehicleId) {
        window.location.href = `/vehicle/${vehicleId}/create_tracking`;
      },

      listTrackings(vehicleId) {
        window.location.href = `/vehicle/${vehicleId}/list_trackings`;
      },
    },
  });
});
