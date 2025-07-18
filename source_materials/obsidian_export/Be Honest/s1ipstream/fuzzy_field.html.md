<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <title>Fuzzy Membership Field</title>
  <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
</head>
<body>
  <h2>Fuzzy Membership Field</h2>
  <label for="alphaSlider">Alpha: <span id="alphaVal">5</span></label><br>
  <input type="range" id="alphaSlider" min="1" max="20" step="0.5" value="5" style="width: 300px;"><br><br>
  <div id="plot" style="width: 90vw; height: 80vh;"></div>

  <script>
    function generateSurface(alpha) {
      const size = 100;
      const x = [], y = [], z = [];
      for (let i = 0; i <= size; i++) {
        x[i] = i / size;
        y[i] = i / size;
      }

      for (let i = 0; i <= size; i++) {
        z[i] = [];
        for (let j = 0; j <= size; j++) {
          const dx = x[i] - 0.5;
          const dy = y[j] - 0.5;
          const d = Math.sqrt(dx * dx + dy * dy);
          z[i][j] = Math.exp(-alpha * d);
        }
      }

      return { x, y, z };
    }

    function plot(alpha) {
      const data = generateSurface(alpha);
      const surface = {
        x: data.x,
        y: data.y,
        z: data.z,
        type: 'surface',
        colorscale: 'Viridis'
      };

      const layout = {
        title: `Fuzzy Membership Field (α = ${alpha})`,
        scene: {
          xaxis: { title: 'Identity Dim 1' },
          yaxis: { title: 'Identity Dim 2' },
          zaxis: { title: 'Membership μ' }
        }
      };

      Plotly.newPlot('plot', [surface], layout);
    }

    // Initial plot
    let alpha = 5;
    plot(alpha);

    // Hook up slider
    const slider = document.getElementById('alphaSlider');
    const alphaVal = document.getElementById('alphaVal');
    slider.addEventListener('input', function () {
      alpha = parseFloat(this.value);
      alphaVal.textContent = alpha;
      plot(alpha);
    });
  </script>
</body>
</html>