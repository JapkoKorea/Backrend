document.addEventListener("DOMContentLoaded", () => {
    const images = document.querySelectorAll("img");

    images.forEach(image => {
        image.addEventListener("click", async (event) => {
            const imageId = event.target.getAttribute("data-id");
            const imageName = event.target.getAttribute("data-name");
            const timestamp = Date.now();

            const payload = {
                image_id: imageId,
                image_name: imageName,
                timestamp: timestamp,
            };

            try {
                const response = await fetch("/click/", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                    },
                    body: JSON.stringify(payload),
                });

                const result = await response.json();
                console.log(result);
            } catch (error) {
                console.error("Error logging click:", error);
            }
        });
    });
});
