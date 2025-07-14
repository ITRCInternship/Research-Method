var path = document.querySelector("path");
      path.setAttribute("stroke-dasharray", "240 1386");
      path.setAttribute("stroke-dashoffset", "0");

      var current = null;

      document
        .querySelector("#username")
        .addEventListener("focus", function (e) {
          if (current) current.pause();
          current = anime({
            targets: "path",
            strokeDashoffset: {
              value: 0,
              duration: 700,
              easing: "easeOutQuart",
            },
            strokeDasharray: {
              value: "240 1386",
              duration: 700,
              easing: "easeOutQuart",
            },
          });
        });

 
      document
        .querySelector("#password")
        .addEventListener("focus", function (e) {
          if (current) current.pause();
          current = anime({
            targets: "path",
            strokeDashoffset: {
              value: -336,
              duration: 700,
              easing: "easeOutQuart",
            },
            strokeDasharray: {
              value: "240 1386",
              duration: 700,
              easing: "easeOutQuart",
            },
          });
        });


      document.querySelector("#submit").addEventListener("focus", function (e) {
        if (current) current.pause();
        current = anime({
          targets: "path",
          strokeDashoffset: {
            value: -730,
            duration: 700,
            easing: "easeOutQuart",
          },
          strokeDasharray: {
            value: "530 1386",
            duration: 700,
            easing: "easeOutQuart",
          },
        });
      });


      document.querySelector("#submit").addEventListener("click", function (e) {

        if (current) current.pause();
        current = anime({
          targets: "path",
          strokeDashoffset: {
            value: -730,
            duration: 700,
            easing: "easeOutQuart",
          },
          strokeDasharray: {
            value: "530 1386",
            duration: 700,
            easing: "easeOutQuart",
          },
        });
      });

      
      window.addEventListener("load", function () {
        if (typeof anime === "undefined") {
          console.error(
            "Anime.js لود نشده است. لطفاً اتصال به CDN را بررسی کنید."
          );
        } else {
          console.log("Anime.js با موفقیت لود شد.");
        }
      });