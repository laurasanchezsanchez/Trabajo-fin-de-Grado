
// Get Stripe publishable key
fetch("/tienda/config/")
  .then((result) => { return result.json(); })
  .then((data) => {
    const stripe = Stripe(data.publicKey);

    document.querySelector("#submitBtn").addEventListener("click", () => {
      fetch("/tienda/create-checkout-session/")
        .then((result) => { return result.json(); })
        .then((data) => {
          console.log(data);
          return stripe.redirectToCheckout({ sessionId: data.sessionId })
        })
        .then((res) => {
          console.log(res);
        });
    });
  });