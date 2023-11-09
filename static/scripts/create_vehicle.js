document.addEventListener("DOMContentLoaded", function () {
  const app = new Vue({
    el: "#app",
    data: {
      registrationNumber: "",
      brand: "",
      model: "",
      description: "",
      firstRegistrationDate: "",
      energy: "",
      gearbox: "",
      typeMine: "",
      vin: "",
      isRegistrationNumberValid: true,
      isBrandValid: true,
      isModelValid: true,
      showResults: false,
      isLoading: false,
      errorMessage: "",
    },
    methods: {
      validateRegistrationNumber() {
        this.registrationNumber = this.registrationNumber.toUpperCase();

        // Supprimer les caractères non autorisés (autres que lettres et chiffres)
        this.registrationNumber = this.registrationNumber.replace(
          /[^A-Za-z0-9]/g,
          ""
        );

        // Vérifiez que le premier caractère est alphabétique
        if (this.registrationNumber.length === 1) {
          if (!/[A-Za-z]/.test(this.registrationNumber[0])) {
            this.registrationNumber = this.registrationNumber.substr(0, 0);
          }
        }

        // Vérifiez que le deuxième caractère est alphabétique
        if (this.registrationNumber.length === 2) {
          if (!/[A-Za-z]/.test(this.registrationNumber[1])) {
            this.registrationNumber = this.registrationNumber.substr(0, 1);
          }
        }

        // Vérifiez que les caractères 3 à 5 sont numériques
        if (this.registrationNumber.length === 3) {
          if (!/^\d{0,3}$/.test(this.registrationNumber[2])) {
            this.registrationNumber = this.registrationNumber.substr(0, 2);
          }
        }

        // Vérifiez que les caractères 3 à 5 sont numériques
        if (this.registrationNumber.length === 4) {
          if (!/^\d{0,3}$/.test(this.registrationNumber[3])) {
            this.registrationNumber = this.registrationNumber.substr(0, 3);
          }
        }

        // Vérifiez que les caractères 3 à 5 sont numériques
        if (this.registrationNumber.length === 5) {
          if (!/^\d{0,3}$/.test(this.registrationNumber[4])) {
            this.registrationNumber = this.registrationNumber.substr(0, 4);
          }
        }

        // Vérifiez que le sixième caractère est alphabétique
        if (this.registrationNumber.length === 6) {
          if (!/[A-Za-z]/.test(this.registrationNumber[5])) {
            this.registrationNumber = this.registrationNumber.substr(0, 5);
          }
        }

        // Vérifiez que le septième caractère est alphabétique
        if (this.registrationNumber.length === 7) {
          if (!/[A-Za-z]/.test(this.registrationNumber[6])) {
            this.registrationNumber = this.registrationNumber.substr(0, 6);
          }
        }

        // Assurez-vous que le champ ne contient pas plus de 7 caractères
        if (this.registrationNumber.length > 7) {
          this.registrationNumber = this.registrationNumber.substr(0, 7);
        }

        // Vérifiez que le champ contient 7 caractères au total
        this.isRegistrationNumberValid = this.registrationNumber.length === 7;
      },
      validateSearchForm() {
        return this.isRegistrationNumberValid;
      },
      searchVehicle() {
        this.showResults = false;
        this.isLoading = true;
        this.errorMessage = "";

        if (this.validateSearchForm()) {
          const formData = {
            registrationNumber: this.registrationNumber,
          };

          const $error = document.querySelector(".error");
          $error.textContent = ""; // Efface le contenu du message d'erreur
          $error.classList.add("error--hidden"); // Ajoute la classe "error--hidden" pour le cacher

          // Envoyer les données au serveur Flask
          $.ajax({
            url: "/search_api_registrationNumber",
            type: "POST",
            data: formData,
            dataType: "json",
            success: (data) => {
              this.brand = data.brand;
              this.model = data.model;
              this.description = data.description;
              this.firstRegistrationDate = data.firstRegistrationDate;
              this.energy = data.energy;
              this.gearbox = data.gearbox;
              this.typeMine = data.typeMine;
              this.vin = data.vin;

              this.showResults = true;
            },
            error: (error) => {
              this.isLoading = false;

              if (error.status === 500) {
                this.errorMessage = JSON.parse(error.responseText).error;
                $error.textContent = this.errorMessage;
                $error.classList.remove("error--hidden");
              }
              console.error("Erreur lors de la création du véhicule", error);
            },
            complete: () => {
              this.isLoading = false; // Réinitialiser isLoading lorsque la recherche est terminée
            },
          });
        }
      },
      validateCreateForm() {
        this.isRegistrationNumberValid = this.registrationNumber.length === 7;
        this.isBrandValid = this.brand.length > 0;
        this.isModelValid = this.model.length > 0;

        return (
          this.isRegistrationNumberValid &&
          this.isBrandValid &&
          this.isModelValid
        );
      },
      createVehicle() {
        if (this.validateCreateForm()) {
          const formData = new FormData();
          formData.append("registrationNumber", this.registrationNumber);
          formData.append("brand", this.brand);
          formData.append("model", this.model);
          formData.append("description", this.description);
          formData.append("firstRegistrationDate", this.firstRegistrationDate);
          formData.append("energy", this.energy);
          formData.append("gearbox", this.gearbox);
          formData.append("typeMine", this.typeMine);
          formData.append("vin", this.vin);

          const $error = document.querySelector(".error");

          $.ajax({
            type: "POST",
            url: "/create_vehicle",
            data: formData,
            processData: false,
            contentType: false,
            success: (data) => {
              window.location.href = "/dashboard/";
            },
            error: (error) => {
              if (error.status === 500  || error.status === 409) {
                app.errorMessage = JSON.parse(error.responseText).error;
              }
              console.error("Erreur lors de la création du véhicule", error);
              $error.textContent = this.errorMessage;
              $error.classList.remove("error--hidden");
            },
          });
        }
      },
    },
  });
  // Gestionnaire d'événements pour le champ immatriculation
  const registrationNumberField = document.querySelector(
    'input[name="registrationNumber"]'
  );
  registrationNumberField.addEventListener("input", function () {
    app.isRegistrationNumberValid = registrationNumberField.value.length >= 7;
  });
});
