document.addEventListener("DOMContentLoaded", function () {
  const app = new Vue({
    el: "#app",
    data: {
      editMode: false,

      name: userData.name,
      email: userData.email,
      password: "",
      passwordPlaceholder: "••••••••",

      isNameValid: true,
      isEmailValid: true,
      isPasswordValid: true,

      isLoading: false,

      errorMessage: "",
      successMessage: "",

      showSuccessMessage: false,
    },
    watch: {
      name(value) {
        this.isNameValid = value.length > 0;
      },
      email(value) {
        const regex = new RegExp(
          /(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)/
        );
        this.isEmailValid = regex.test(value);
      },
      password(value) {
        this.isPasswordValid = value.length >= 8;
      },
    },
    methods: {
      handlePasswordFocus() {
        if (!this.password) {
          this.passwordPlaceholder = ""; // Effacez le placeholder quand l'utilisateur se concentre sur le champ
        }
      },
      handlePasswordBlur() {
        if (!this.password) {
          this.passwordPlaceholder = "••••••••"; // Remettez le placeholder quand l'utilisateur clique en dehors du champ
        }
      },
      enterEditMode() {
        this.editMode = true; // Activez le mode d'édition
      },
      validateForm() {
        // Retourne true si tous les champs sont valides, sinon false
        return this.isNameValid && this.isEmailValid && this.isPasswordValid;
      },
      updateInfo() {
        if (this.validateForm()) {
          this.isLoading = true;
          const formData = {
            name: this.name,
            email: this.email,
          };

          // N'incluez le mot de passe que si l'utilisateur a entré un nouveau mot de passe
          if (this.password !== "") {
            formData.password = this.password;
          }

          // Enregistrez l'instance de Vue dans une variable pour y accéder dans les callbacks
          const vm = this;

          $.ajax({
            url: "/user/update",
            type: "POST",
            data: formData,
            dataType: "json",
            success: (resp) => {
              // Supposons que la réponse du serveur contient une clé "message" avec le message de succès
              vm.successMessage = resp.message || "Mise à jour réussie !";
              vm.editMode = false; // Sortir du mode d'édition si la mise à jour est un succès

              vm.$nextTick(() => {
                const $success = document.querySelector(".success");
                if ($success) {
                  $success.textContent = vm.successMessage;
                  $success.classList.remove("error--hidden"); // Assurez-vous que cette classe montre l'élément

                  // Optionnel: cachez le message après un délai
                  setTimeout(() => {
                    $success.classList.add("error--hidden");
                  }, 5000); // Cachez le message après 5 secondes, par exemple
                }
              });
            },
            error: function (xhr) {
              // Parsez la réponse et mettez à jour errorMessage
              let errorMsg = "Erreur inattendue. Veuillez réessayer.";
              if (xhr.responseText) {
                try {
                  const response = JSON.parse(xhr.responseText);
                  errorMsg = response.error || errorMsg;
                } catch (e) {
                  // Erreur lors du parse du JSON, conservez errorMsg par défaut
                }
              }

              // Utilisez vm qui réfère à l'instance Vue ici
              vm.errorMessage = errorMsg;

              vm.$nextTick(() => {
                const $error = document.querySelector(".error");
                if ($error) {
                  $error.textContent = vm.errorMessage;
                  $error.classList.remove("error--hidden");
                }
              });
            },
            complete: () => {
              vm.isLoading = false;
              vm.editMode = false;
              errorMessage = "";
              successMessage = "";
            },
          });
        }
      },
      confirmDelete() {
        if (
          confirm(
            "Êtes-vous sûr de vouloir supprimer votre compte ? Cette action est irréversible."
          )
        ) {
          this.deleteAccount();
        }
      },
      deleteAccount() {
        const vm = this;
        this.isLoading = true;

        $.ajax({
          url: "/user/delete",
          type: "POST",
          dataType: "json",
          success(resp) {
            alert(resp.message || "Compte supprimé avec succès.");
            window.location.href = "/"; // Rediriger l'utilisateur après la suppression du compte
          },
          error(xhr) {
            vm.errorMessage =
              "Impossible de supprimer le compte. Veuillez réessayer.";
            if (xhr.responseText) {
              try {
                const response = JSON.parse(xhr.responseText);
                vm.errorMessage = response.error || vm.errorMessage;
              } catch (e) {
                // Erreur lors du parse du JSON
              }
            }

            vm.$nextTick(() => {
              const $error = document.querySelector(".error");
              if ($error) {
                $error.textContent = vm.errorMessage;
                $error.classList.remove("error--hidden");
              }
            });
          },
          complete() {
            vm.isLoading = false;
          },
        });
      },
    },
  });
});
