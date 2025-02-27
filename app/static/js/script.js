document.addEventListener("DOMContentLoaded", function () {
    console.log("Flask Blog Loaded!");

    // Confirm before deleting a post
    const deleteForms = document.querySelectorAll(".delete-form");
    deleteForms.forEach(form => {
        form.addEventListener("submit", function (event) {
            if (!confirm("Are you sure you want to delete this post?")) {
                event.preventDefault();
            }
        });
    });
});
