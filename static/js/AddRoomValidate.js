        document.getElementById('hotelRoomForm').addEventListener('submit', function(event) {
            event.preventDefault(); 

            const price = document.getElementById('price').value;
            const type = document.getElementById('type').value;
            const capacity = document.getElementById('capacity').value;
            const description = document.getElementById('description').value;
            const image = document.getElementById('image').files[0];

            const validation = validateHotelRoomForm(price, type, capacity, description, image);

            if (validation.isValid) {
                alert('Room details Successfully Added.');
            } else {
                alert(validation.message);
            }
        });

        function validateHotelRoomForm(price, type, capacity, description, image) {
            if (price === "" || isNaN(price) || price <= 0) {
                return { isValid: false, message: "Room price must be a positive number." };
            }

            if (type.trim() === "") {
                return { isValid: false, message: "Room type is required." };
            }

            if (capacity === "" || isNaN(capacity) || capacity <= 0) {
                return { isValid: false, message: "Room capacity must be a positive number." };
            }

            if (description.trim() === "") {
                return { isValid: false, message: "Description is required." };
            }

            if (!image) {
                return { isValid: false, message: "Room image is required." };
            }
            const validImageTypes = ['image/jpeg', 'image/png', 'image/gif'];
            if (!validImageTypes.includes(image.type)) {
                return { isValid: false, message: "Room image must be a JPEG, PNG, or GIF file." };
            }

            return { isValid: true, message: "Room details are valid." };
        }
        