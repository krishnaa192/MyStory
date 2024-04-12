
    // Get references to the buttons
    const btnBack = document.getElementById('btnBack');
    const btnForward = document.getElementById('btnForward');
    const pageNumbers = document.querySelectorAll('.page-number');

    // Current page index
    let currentPageIndex = 0;

    // Total number of pages
    const totalPages = 10; // Change this value to your total number of pages

    // Function to update button states based on current page index
    function updateButtonStates() {
        btnBack.disabled = currentPageIndex === 0;
        btnForward.disabled = currentPageIndex === totalPages - 1;
    }

    // Function to update page numbers
    function updatePageNumbers() {
        pageNumbers.forEach((pageNumber, index) => {
            pageNumber.textContent = index + 1;
            pageNumber.classList.toggle('active', index === currentPageIndex);
        });
    }

    // Event listener for back button
    btnBack.addEventListener('click', function() {
        if (currentPageIndex > 0) {
            currentPageIndex--;
            updateButtonStates();
            updatePageNumbers();
            // Perform action to navigate to previous page
            console.log('Navigating to previous page: ', currentPageIndex);
        }
    });

    // Event listener for forward button
    btnForward.addEventListener('click', function() {
        if (currentPageIndex < totalPages - 1) {
            currentPageIndex++;
            updateButtonStates();
            updatePageNumbers();
            // Perform action to navigate to next page
            console.log('Navigating to next page: ', currentPageIndex);
        }
    });

    // Initial button state update
    updateButtonStates();
    updatePageNumbers();
