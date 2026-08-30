const tabButtons = document.querySelectorAll('.tablinks');
tabButtons.forEach(button => {
    button.addEventListener('click', function () {
        let tabName = this.dataset.tab;
        let tabContent = document.getElementById(tabName);

        let allTabContent = document.querySelectorAll('.tabcontent');
        let allTabButtons = document.querySelectorAll('.tablinks');

        allTabContent.forEach(content => {
            content.style.display = 'none';
        });

        allTabButtons.forEach(button => {
            button.classList.remove('active');
        });

        tabContent.style.display = 'block';
        this.classList.add('active');
    });
});

document.querySelector('.tablinks').click(); // Automatically click the first tab to display its content