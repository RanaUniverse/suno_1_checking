const resendButton = document.getElementById("resend-otp-btn");
const countdownElement = document.getElementById("otp-countdown");

if (resendButton && countdownElement) {
    const initialValue = countdownElement.textContent.trim();
    const secondsValue = Number.parseInt(initialValue, 10);
    if (Number.isNaN(secondsValue)) {
        console.error("Invalid otp resend countdown value, it need int.");
    }
    else if (secondsValue <= 0) {
        console.error("OTP resend countedown must be greate than 0");
    }
    else {
        let seconds = secondsValue;
        const countdown = setInterval(() => {
            seconds--;
            countdownElement.textContent = seconds;

            if (seconds <= 0) {
                clearInterval(countdown);

                resendButton.disabled = false;
                resendButton.textContent = "Resend OTP Now";
            }
        }, 1000);
    }

}