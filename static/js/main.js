document.addEventListener("DOMContentLoaded", function () {
    const guessInput = document.querySelector('input[name="guess"]');
    if (guessInput) {
        guessInput.addEventListener("input", function () {
            this.value = this.value.toUpperCase();
        });

        guessInput.addEventListener("keypress", function (e) {
            const char = String.fromCharCode(e.which);
            if (!/^[A-Z]$/i.test(char)) {
                e.preventDefault();
            }
        });
    }

    if (guessForm) {
        guessForm.addEventListener("submit", function (e) {
            // Wait for flash messages to appear and check for success/error
            setTimeout(() => {
                const flash = document.querySelector('.flash-success');
                const errorFlash = document.querySelector('.flash-error');

                if (flash) {
                    launchConfetti();
                } else if (errorFlash) {
                    shakeInput();
                }
            }, 50);
        });
    }

    // Shake input animation for wrong guess
    function shakeInput() {
        guessInput.classList.add('shake');
        setTimeout(() => {
            guessInput.classList.remove('shake');
        }, 500);
    }

    // Simple confetti effect
    function launchConfetti() {
        const duration = 2000;
        const animationEnd = Date.now() + duration;
        const defaults = { startVelocity: 30, spread: 360, ticks: 60, zIndex: 999 };

        function randomInRange(min, max) {
            return Math.random() * (max - min) + min;
        }

        const interval = setInterval(function () {
            const timeLeft = animationEnd - Date.now();

            if (timeLeft <= 0) {
                return clearInterval(interval);
            }

            confetti(Object.assign({}, defaults, {
                particleCount: 3,
                origin: { x: Math.random(), y: Math.random() - 0.2 }
            }));
        }, 250);
    }
});
