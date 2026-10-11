(() => {
  const choices = {"games": ["/random_images/games/celeste.jpg", "/random_images/games/hanabi.jpg", "/random_images/games/link.png"], "cooking": ["/random_images/cooking/carbonara.jpg", "/random_images/cooking/pizza.jpg"]};

  document.querySelectorAll("a[data-random-image]").forEach((link) => {
    const images = choices[link.dataset.randomImage];
    if (!images?.length) return;

    const choose = () => {
      link.href = images[Math.floor(Math.random() * images.length)];
      const preview = new Image();
      preview.src = link.href;
    };

    choose();
    // Keep the preloaded URL for native navigation, then prepare the next click.
    link.addEventListener("click", () => setTimeout(choose, 0));
    link.addEventListener("auxclick", (event) => {
      if (event.button === 1) setTimeout(choose, 0);
    });
  });
})();
