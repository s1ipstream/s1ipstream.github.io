<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<title>Fuzzy Membership Cockpit</title>
<script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
<style>
  body { font-family: Arial, sans-serif; margin: 20px; }
  #plot { width: 90vw; height: 60vh; }
  #barChart { width: 90vw; height: 300px; margin-top: 1em; }
  label, button { font-size: 1.1em; margin-right: 10px; }
  #info { font-family: monospace; margin-top: 1em; }
</style>
</head>
<body>

<h1>Fuzzy Membership Cockpit</h1>

<div>
  <label for="alphaSlider">Alpha (sharpness): <span id="alphaVal">5</span></label>
  <input type="range" id="alphaSlider" min="1" max="20" step="0.5" value="5" style="width:300px" />
</div>

<div id="plot"></div>

<div>
  <button id="animateBtn">Start Animation</button>
</div>

<h2>Solution Membership Comparison</h2>
<div id="barChart"></div>

<div id="info">Click on the plot or start animation to select identity position.</div>

<script>
  // Solutions to compare
  const solutions = [
    { name: 'Solution A', x: 0.5, y: 0.5 },
    { name: 'Solution B', x: 0.2, y: 0.7 },
    { name: 'Solution C', x: 0.8, y: 0.3 }
  ];

  // Globals
  let alpha = 5;
  let identity = { x: 0.5, y: 0.5 };
  let animating = false;
  let animationStep = 0;
  const animationSteps = 100;
  let animId;

  // Generate surface data for fuzzy field centered on first solution (can adjust)
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
        const dx = x[i] - solutions[0].x;
        const dy = y[j] - solutions[0].y;
        const d = Math.sqrt(dx*dx + dy*dy);
        z[i][j] = Math.exp(-alpha * d);
      }
    }
    return { x, y, z };
  }

  // Plot fuzzy surface
  function plotSurface(alpha) {
    const data = generateSurface(alpha);
    const surface = {
      x: data.x,
      y: data.y,
      z: data.z,
      type: 'surface',
      colorscale: 'Viridis',
      contours: {
        z: { show:true, usecolormap:true, highlightcolor:"#42f462", project:{ z:true } }
      }
    };

    const layout = {
      title: `Fuzzy Membership Field (α = ${alpha}) - Centered on Solution A`,
      scene: {
        xaxis: { title: 'Identity Dim 1', range: [0,1] },
        yaxis: { title: 'Identity Dim 2', range: [0,1] },
        zaxis: { title: 'Membership μ', range: [0,1] }
      },
      dragmode: 'turntable',
      margin: {l:0, r:0, b:0, t:30}
    };

    Plotly.newPlot('plot', [surface], layout);
  }

  // Compute membership for single solution
  function computeMembership(x, y, sol, alpha) {
    const dx = x - sol.x;
    const dy = y - sol.y;
    const d = Math.sqrt(dx*dx + dy*dy);
    return Math.exp(-alpha * d);
  }

  // Compute membership for all solutions
  function computeAllMemberships(x, y, alpha) {
    return solutions.map(sol => ({
      name: sol.name,
      membership: computeMembership(x, y, sol, alpha)
    }));
  }

  // Plot bar chart of memberships
  function plotBarChart(memberships) {
    const data = [{
      x: memberships.map(m => m.name),
      y: memberships.map(m => m.membership),
      type: 'bar',
      marker: { color: 'rgba(55,128,191,0.7)' }
    }];
    const layout = {
      title: 'Membership Comparison',
      yaxis: { range: [0, 1], title: 'Membership μ' }
    };
    Plotly.newPlot('barChart', data, layout);
  }

  // Update info text
  function updateInfoText(x, y, memberships) {
    const membershipsText = memberships
      .map(m => `${m.name}: μ = ${m.membership.toFixed(4)}`)
      .join(' | ');
    document.getElementById('info').textContent =
      `Identity position: (x=${x.toFixed(3)}, y=${y.toFixed(3)}) — ${membershipsText}`;
  }

  // Initial render
  plotSurface(alpha);
  let initialMemberships = computeAllMemberships(identity.x, identity.y, alpha);
  plotBarChart(initialMemberships);
  updateInfoText(identity.x, identity.y, initialMemberships);

  // Slider control
  document.getElementById('alphaSlider').addEventListener('input', (e) => {
    alpha = parseFloat(e.target.value);
    document.getElementById('alphaVal').textContent = alpha;
    plotSurface(alpha);
    const memberships = computeAllMemberships(identity.x, identity.y, alpha);
    plotBarChart(memberships);
    updateInfoText(identity.x, identity.y, memberships);
  });

  // Handle clicks on the surface plot to pick identity
  document.getElementById('plot').on('plotly_click', (data) => {
    const pt = data.points[0];
    identity.x = pt.x;
    identity.y = pt.y;
    const memberships = computeAllMemberships(identity.x, identity.y, alpha);
    plotBarChart(memberships);
    updateInfoText(identity.x, identity.y, memberships);
  });

  // Animation control
  document.getElementById('animateBtn').addEventListener('click', () => {
    if (!animating) {
      animating = true;
      animationStep = 0;
      document.getElementById('animateBtn').textContent = 'Stop Animation';
      animate();
    } else {
      animating = false;
      document.getElementById('animateBtn').textContent = 'Start Animation';
      cancelAnimationFrame(animId);
    }
  });

  function animate() {
    if (!animating) return;
    // Move identity across x axis, y fixed
    identity.x = animationStep / animationSteps;
    identity.y = 0.5;
    const memberships = computeAllMemberships(identity.x, identity.y, alpha);
    plotBarChart(memberships);
    updateInfoText(identity.x, identity.y, memberships);
    animationStep = (animationStep + 1) % (animationSteps + 1);
    animId = requestAnimationFrame(animate);
  }
</script>

</body>
</html>
