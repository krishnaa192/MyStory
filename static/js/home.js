let currentIndex = 0;
        const cardWidth = 340; // Width of card including margin
        const numVisibleCards = 4; // Number of visible cards

        const cards = document.querySelectorAll('.card');

        function showCards(startIndex) {
            cards.forEach((card, index) => {
                if (index >= startIndex && index < startIndex + numVisibleCards) {
                    card.classList.add('active');
                } else {
                    card.classList.remove('active');
                }
            });
        }

        function slideCards(direction) {
            const numCards = cards.length;
            const maxIndex = numCards - numVisibleCards;

            if (direction === 'next') {
                currentIndex = Math.min(currentIndex + 1, maxIndex);
            } else if (direction === 'prev') {
                currentIndex = Math.max(currentIndex - 1, 0);
            }

            const offset = -currentIndex * cardWidth;
            const cardsWrapper = document.querySelector('.main-card');
            cardsWrapper.style.transform = `translateX(${offset}px)`;

            showCards(currentIndex);
        }

        // Show initial set of cards
        showCards(currentIndex);

        // Add event listeners for button clicks
        document.getElementById('prevButton').addEventListener('click', () => slideCards('prev'));
        document.getElementById('nextButton').addEventListener('click', () => slideCards('next'));
        document.getElementById('prevButton1').addEventListener('click', () => slideCards('prev'));
        document.getElementById('nextButton1').addEventListener('click', () => slideCards('next'));