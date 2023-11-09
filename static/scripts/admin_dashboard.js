document.addEventListener("DOMContentLoaded", function () {
  const app = new Vue({
    el: "#app",
    data: {
      new_password: '',
    },
    methods: {
      confirmDelete(userId) {
        const confirmation = window.confirm(
          "Voulez-vous vraiment supprimer cet utilisateur ? Cela entraînera la perte totale des données de suivi."
        );
        if (confirmation) {
          this.deleteUser(userId);
        }
      },
      deleteUser(userId) {
        const formData = {
          _id: userId,
        };

        $.ajax({
          url: "/admin/delete_user/",
          type: "DELETE",
          data: formData,
          dataType: "json",
          success: (data) => {
            window.location.href = window.location.href;
          },
          error: (error) => {
            console.log(JSON.parse(error.responseText).error);
          },
        });
      },
      newPassword(userId) {
        const formData = {
          user_id: userId,
          new_password: this.new_password,
        };

        $.ajax({
          url: "/admin/reset_password/",
          type: "PATCH",
          data: formData,
          dataType: "json",
          success: (data) => {
            alert(data.message);
            window.location.reload();
          },
          error: (error) => {
            alert(JSON.parse(error.responseText).error);
          },
        });
      },
    },
  });
});
