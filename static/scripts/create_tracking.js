document.addEventListener("DOMContentLoaded", function () {
  const app = new Vue({
    el: "#app",
    data: {
      date: new Date()
        .toLocaleDateString("fr-FR")
        .split("/")
        .reverse()
        .join("-"),
      mileage: "",

      tireFrontLeft: false,
      tireFrontRight: false,
      refTiresFront: "",
      tireRearLeft: false,
      tireRearRight: false,
      refTiresRear: "",

      brakePadsFront: false,
      refBrakePadsFront: "",
      brakePadsRear: false,
      refBrakePadsRear: "",

      brakeDisksFront: false,
      refBrakeDisksFront: "",
      brakeDisksRear: false,
      refBrakeDisksRear: "",

      oilChange: false,
      refOilChange: "",

      oilFilter: false,
      refOilFilter: "",

      airFilter: false,
      refAirFilter: "",

      fuelFilter: false,
      refFuelFilter: "",

      cabinFilter: false,
      refCabinFilter: "",

      isDateValid: true,
      isMileageValid: true,

      errorMessage: "",
      successMessage: "",
      showSuccessMessage: false,
    },
    methods: {
      validateMileage() {
        // Remplacez tous les caractères non numériques par une chaîne vide
        this.mileage = this.mileage.replace(/[^0-9]/g, "");
        // Formate le nombre avec des espaces tous les 3 chiffres
        this.mileage = Number(this.mileage).toLocaleString("fr-FR");
      },
      validateForm() {
        this.isDateValid = this.date.length > 0;
        this.isMileageValid = this.mileage.length > 0;

        return this.isDateValid && this.isMileageValid;
      },
      toggleTireFrontLeft() {
        this.TireFrontLeft = !this.TireFrontLeft;
      },
      toggleTireFrontRight() {
        this.TireFrontRight = !this.TireFrontRight;
      },
      toggleTireRearLeft() {
        this.TireRearLeft = !this.TireRearLeft;
      },
      toggleTireRearRight() {
        this.TireRearRight = !this.TireRearRight;
      },
      toggleBrakePadsFront() {
        this.brakePadsFront = !this.brakePadsFront;
      },
      toggleBrakePadsRear() {
        this.brakePadsRear = !this.brakePadsRear;
      },
      toggleBrakeDisksFront() {
        this.brakeDisksFront = !this.brakeDisksFront;
      },
      toggleBrakeDisksRear() {
        this.brakeDisksRear = !this.brakeDisksRear;
      },
      toggleOilChange() {
        this.oilChange = !this.oilChange;
      },
      toggleOilFilter() {
        this.oilFilter = !this.oilFilter;
      },
      toggleAirFilter() {
        this.airFilter = !this.airFilter;
      },
      toggleFuelFilter() {
        this.fuelFilter = !this.fuelFilter;
      },
      toggleCabinFilter() {
        this.cabinFilter = !this.cabinFilter;
      },
      createTracking() {
        if (this.validateForm()) {
          const formData = {
            date: this.date,
            mileage: this.mileage,

            tireFrontLeft: this.tireFrontLeft,
            tireFrontRight: this.tireFrontRight,
            refTiresFront: this.refTiresFront,
            tireRearLeft: this.tireRearLeft,
            tireRearRight: this.tireRearRight,
            refTiresRear: this.refBrakePadsRear,

            brakePadsFront: this.brakePadsFront,
            refBrakePadsFront: this.refBrakePadsFront,
            brakePadsRear: this.brakePadsRear,
            refBrakePadsRear: this.refBrakePadsRear,

            brakeDisksFront: this.brakeDisksFront,
            refBrakeDisksFront: this.refBrakeDisksFront,
            brakeDisksRear: this.brakeDisksRear,
            refBrakeDisksRear: this.refBrakeDisksRear,

            oilChange: this.oilChange,
            refOilChange: this.refOilChange,

            oilFilter: this.oilFilter,
            refOilFilter: this.refOilFilter,

            airFilter: this.airFilter,
            refAirFilter: this.refAirFilter,

            fuelFilter: this.fuelFilter,
            refFuelFilter: this.refFuelFilter,

            cabinFilter: this.cabinFilter,
            refCabinFilter: this.refCabinFilter,
          };
          const vehicleId = window.location.pathname.split("/")[2];
          console.log(vehicleId);
          const $error = document.querySelector(".error");
          const vm = this; // Stocker la référence à l'instance Vue
          this.showSuccessMessage = false;
          // Envoyer les données au serveur Flask
          $.ajax({
            url: `/vehicle/${vehicleId}/create_tracking`,
            type: "POST",
            data: formData,
            dataType: "json",
            success: function (resp) {
              vm.successMessage = "Suivi créé avec succès";
              app.showSuccessMessage = true;
              window.location.href = "/dashboard/";
            },
            error: function (xhr) {
              if (xhr.status === 500) {
                vm.errorMessage = "Impossible de créer le suivi";
              }
              $error.textContent = vm.errorMessage;
              $error.classList.remove("error--hidden");
            },
          });
        }
      },
    },
  });
});
