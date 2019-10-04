$(document).ready(function () {


// Kredi kart işlemleri  || Billing Profile
    var stripeFormModule = $(".stripe-payment-form")
    var stripeToken = stripeFormModule.attr("data-token")
    var stripeNextUrl = stripeFormModule.attr("data-next-url")
    var stripeModuleBtnTitle = stripeFormModule.attr("data-btn-title") || "Add card"
    var stripeTemplate = $.templates("#stripeTemplate")
    var stripeTemplateDataContext = {
        publishKey: stripeToken,
        nextUrl: stripeNextUrl,
        btnTitle: stripeModuleBtnTitle
    }
    var stripeTemplateHtml = stripeTemplate.render(stripeTemplateDataContext)
    stripeFormModule.html(stripeTemplateHtml)


    var paymentForm = $(".payment-form");
    if (paymentForm.length > 1) {
        alert("Only one payment form is allowed per page");
        paymentForm.css("display", "none")
    } else if (paymentForm.length == 1) {

        var pubKey = paymentForm.attr("data-token");
        var nextUrl = paymentForm.attr("data-next-url");

        // Create a Stripe client.
        var stripe = Stripe(pubKey);

        // Create an instance of Elements.
        var elements = stripe.elements();

        // Custom styling can be passed to options when creating an Element.
        // (Note that this demo uses a wider set of styles than the guide below.)
        var style = {
            base: {
                color: '#32325d',
                fontFamily: '"Helvetica Neue", Helvetica, sans-serif',
                fontSmoothing: 'antialiased',
                fontSize: '16px',
                '::placeholder': {
                    color: '#aab7c4'
                }
            },
            invalid: {
                color: '#fa755a',
                iconColor: '#fa755a'
            }
        };

        // Create an instance of the card Element.
        var card = elements.create('card', {style: style});

        // Add an instance of the card Element into the `card-element` <div>.
        card.mount('#card-element');

        // Handle real-time validation errors from the card Element.
        card.addEventListener('change', function (event) {
            var displayError = document.getElementById('card-errors');
            if (event.error) {
                displayError.textContent = event.error.message;
            } else {
                displayError.textContent = '';
            }
        });

        // // Handle form submission.
        // var form = document.getElementById('payment-form');
        // form.addEventListener('submit', function (event) {
        //     event.preventDefault();
        //
        //     // display new button ui
        //     loadtime = 1500
        //     var errorHtml = "<i class='fa fa-warning></i>An error occured"
        //     var errorClasses = "btn btn-danger my-4 disabled"
        //     var loadingHtml = "<i class='fa fa-spin fa-spinner'></i>Loading..."
        //     var loadingClasses = "btn btn-success my-4 disabled"
        //
        //     stripe.createToken(card).then(function (result) {
        //         if (result.error) {
        //             // Inform the user if there was an error.
        //             var errorElement = document.getElementById('card-errors');
        //             errorElement.textContent = result.error.message;
        //         } else {
        //             // Send the token to your server.
        //             stripeTokenHandler(nextUrl, result.token);
        //         }
        //     });
        // });


        function redirectToNext(nextPath, timeoffset) {
            if (nextPath) {
                setTimeout(function () {
                    window.location.href = nextPath
                }, timeoffset)
            }
        }

        // Handle form submission.
        var form = $('#payment-form');
        var btnLoad = form.find(".btn-load");
        var btnLoadDefaultHtml = btnLoad.html();
        var btnLoadDefaultClasses = btnLoad.attr("class");
        form.on('submit', function (event) {
            event.preventDefault();

            // display new button ui
            var $this = $(this)
            btnLoad.blur()
            var loadtime = 1000
            var currentTimeout;
            var errorHtml = "<i class='fa fa-warning'></i> Bir hata oluştu"
            var errorClasses = "btn btn-danger my-4 disabled"
            var loadingHtml = "<i class='fa fa-spin fa-spinner'></i> Loading..."
            var loadingClasses = "btn btn-success my-4 disabled"

            stripe.createToken(card).then(function (result) {
                if (result.error) {
                    // Inform the user if there was an error.
                    var errorElement = $('#card-errors');
                    errorElement.textContent = result.error.message;
                    currentTimeout = displayBtnStatus(btnLoad, errorHtml, errorClasses, loadtime, currentTimeout)
                } else {
                    // Send the token to your server.
                    currentTimeout = displayBtnStatus(btnLoad, loadingHtml, loadingClasses, loadtime, currentTimeout)
                    stripeTokenHandler(nextUrl, result.token);
                }
            });
        });


        // Kart bilgileri ekleme  buton durumu
        function displayBtnStatus(element, newHtml, newClasses, loadTime, timeout) {
            // if (timeout) {
            //     clearTimeout(timeout)
            // }
            if (!loadTime) {
                loadTime = 1500
            }
            element.html(newHtml)
            element.removeClass(btnLoadDefaultClasses)
            element.addClass(newClasses)

            return setTimeout(function () {
                element.html(btnLoadDefaultHtml)
                element.removeClass(newClasses)
                element.addClass(btnLoadDefaultClasses)
            }, loadTime)
        }


        // Submit the form with the token ID.
        function stripeTokenHandler(nextUrl, token) {
            var paymentMethodEndpoint = "/billing/payment-method/create/";
            var data = {
                'token': token.id
            };
            $.ajax({
                data: data,
                url: paymentMethodEndpoint,
                method: "POST",
                success: function (data) {
                    var succesMsg = data.message || "Success! Your card was added.";
                    card.clear(); // input clear
                    if (nextUrl) {
                        succesMsg += "<br/><br/><i class='fa fa-spin fa-spinner'></i> Redirect..."
                    }
                    if ($.alert) {
                        $.alert(succesMsg);
                    } else {
                        alert(succesMsg);
                    }
                    btnLoad.html(btnLoadDefaultHtml)
                    btnLoad.attr("class", btnLoadDefaultClasses)
                    redirectToNext(nextUrl, 1500)
                },
                error: function (error) {
                    $.alert({title: "Bir hata oluştu", content: "Lütfen kart bilgilerinizi girmeyi tekrar deneyiniz."})
                    btnLoad.html(btnLoadDefaultHtml)
                    btnLoad.attr("class", btnLoadDefaultClasses)
                }
            });
            // {#// Insert the token ID into the form so it gets submitted to the server#}
            // {#var form = document.getElementById('payment-form');#}
            // {#var hiddenInput = document.createElement('input');#}
            // {#hiddenInput.setAttribute('type', 'hidden');#}
            // {#hiddenInput.setAttribute('name', 'stripeToken');#}
            // {#hiddenInput.setAttribute('value', token.id);#}
            // {#form.appendChild(hiddenInput);#}
            // {##}
            // {#form.submit();#}
        }

    }
})