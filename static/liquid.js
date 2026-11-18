/**
 * Interactive Liquid Light Trail Simulation
 * Replaces surface ripples with an ethereal, smooth, non-distracting cursor light trail.
 * Palette: Deep obsidian backdrop with glowing lavender-green luminous ribbons.
 * Engineered for 100% UI readability and 60fps performance.
 */

(function () {
    const canvas = document.getElementById("liquid-canvas");
    if (!canvas) return;
    const ctx = canvas.getContext("2d");

    let width = (canvas.width = window.innerWidth);
    let height = (canvas.height = window.innerHeight);

    // Trail points history
    const MAX_POINTS = 32;
    const points = [];

    // Floating ambient liquid embers
    const EMBER_COUNT = 18;
    const embers = [];

    let mouse = {
        x: width / 2,
        y: height / 2,
        px: width / 2,
        py: height / 2,
        speed: 0,
        active: false
    };

    function resize() {
        width = canvas.width = window.innerWidth;
        height = canvas.height = window.innerHeight;
    }
    window.addEventListener("resize", resize);

    // Initialize floating ambient embers
    for (let i = 0; i < EMBER_COUNT; i++) {
        embers.push({
            x: Math.random() * width,
            y: Math.random() * height,
            vx: (Math.random() - 0.5) * 0.4,
            vy: (Math.random() - 0.5) * 0.4,
            radius: Math.random() * 80 + 40,
            hue: Math.random() > 0.5 ? "lavender" : "green",
            alpha: Math.random() * 0.04 + 0.015,
            phase: Math.random() * Math.PI * 2
        });
    }

    // Pointer tracking
    window.addEventListener("pointermove", (e) => {
        const dx = e.clientX - mouse.x;
        const dy = e.clientY - mouse.y;
        mouse.speed = Math.sqrt(dx * dx + dy * dy);

        mouse.px = mouse.x;
        mouse.py = mouse.y;
        mouse.x = e.clientX;
        mouse.y = e.clientY;
        mouse.active = true;

        // Push new point into trail
        points.unshift({
            x: mouse.x,
            y: mouse.y,
            age: 0,
            maxAge: 32,
            speed: Math.min(45, mouse.speed)
        });

        if (points.length > MAX_POINTS) {
            points.pop();
        }
    });

    window.addEventListener("pointerleave", () => {
        mouse.active = false;
    });

    function drawAmbientEmbers() {
        for (let i = 0; i < embers.length; i++) {
            const em = embers[i];
            em.x += em.vx;
            em.y += em.vy;
            em.phase += 0.01;

            // Screen wrap
            if (em.x < -100) em.x = width + 100;
            if (em.x > width + 100) em.x = -100;
            if (em.y < -100) em.y = height + 100;
            if (em.y > height + 100) em.y = -100;

            const pulseAlpha = em.alpha * (0.8 + 0.2 * Math.sin(em.phase));
            const grad = ctx.createRadialGradient(em.x, em.y, 0, em.x, em.y, em.radius);

            if (em.hue === "lavender") {
                grad.addColorStop(0, `rgba(168, 85, 247, ${pulseAlpha})`);
                grad.addColorStop(0.6, `rgba(147, 51, 234, ${pulseAlpha * 0.4})`);
                grad.addColorStop(1, "rgba(0, 0, 0, 0)");
            } else {
                grad.addColorStop(0, `rgba(16, 185, 129, ${pulseAlpha})`);
                grad.addColorStop(0.6, `rgba(5, 150, 105, ${pulseAlpha * 0.4})`);
                grad.addColorStop(1, "rgba(0, 0, 0, 0)");
            }

            ctx.fillStyle = grad;
            ctx.beginPath();
            ctx.arc(em.x, em.y, em.radius, 0, Math.PI * 2);
            ctx.fill();
        }
    }

    function drawLightTrail() {
        if (points.length < 2) return;

        // Age points
        for (let i = 0; i < points.length; i++) {
            points[i].age++;
        }

        // Remove dead points
        while (points.length > 0 && points[points.length - 1].age >= points[points.length - 1].maxAge) {
            points.pop();
        }

        if (points.length < 2) return;

        ctx.save();
        ctx.globalCompositeOperation = "screen";

        // 1. Draw soft diffused fluid ribbon
        for (let i = 0; i < points.length - 1; i++) {
            const p1 = points[i];
            const p2 = points[i + 1];

            const lifeRatio = 1 - p1.age / p1.maxAge;
            const widthScale = (14 + p1.speed * 0.6) * lifeRatio;
            const alpha = 0.16 * lifeRatio;

            // Alternate chromatic glow between lavender and green
            const isLavender = i % 2 === 0;
            const colorCore = isLavender
                ? `rgba(192, 132, 252, ${alpha * 1.2})`
                : `rgba(52, 211, 153, ${alpha * 1.2})`;
            const colorEdge = isLavender
                ? `rgba(147, 51, 234, 0)`
                : `rgba(16, 185, 129, 0)`;

            const midX = (p1.x + p2.x) * 0.5;
            const midY = (p1.y + p2.y) * 0.5;

            const radialGrad = ctx.createRadialGradient(midX, midY, 0, midX, midY, Math.max(20, widthScale * 2.5));
            radialGrad.addColorStop(0, colorCore);
            radialGrad.addColorStop(1, colorEdge);

            ctx.fillStyle = radialGrad;
            ctx.beginPath();
            ctx.arc(midX, midY, Math.max(20, widthScale * 2.5), 0, Math.PI * 2);
            ctx.fill();
        }

        // 2. Draw sharp, flowing luminous core spine
        ctx.lineWidth = 3;
        ctx.lineCap = "round";
        ctx.lineJoin = "round";

        for (let i = 0; i < points.length - 1; i++) {
            const p1 = points[i];
            const p2 = points[i + 1];
            const lifeRatio = 1 - p1.age / p1.maxAge;

            const lineGrad = ctx.createLinearGradient(p1.x, p1.y, p2.x, p2.y);
            const coreAlpha = 0.35 * lifeRatio;

            lineGrad.addColorStop(0, `rgba(233, 213, 255, ${coreAlpha})`);
            lineGrad.addColorStop(0.5, `rgba(168, 85, 247, ${coreAlpha * 0.9})`);
            lineGrad.addColorStop(1, `rgba(52, 211, 153, ${coreAlpha * 0.7})`);

            ctx.strokeStyle = lineGrad;
            ctx.lineWidth = Math.max(1.5, 4.5 * lifeRatio);

            ctx.beginPath();
            ctx.moveTo(p1.x, p1.y);
            ctx.lineTo(p2.x, p2.y);
            ctx.stroke();
        }

        ctx.restore();
    }

    function drawCursorAura() {
        if (!mouse.active) return;

        ctx.save();
        ctx.globalCompositeOperation = "screen";

        // Gentle, non-intrusive cursor spotlight that backlights glass cards
        const radGrad = ctx.createRadialGradient(mouse.x, mouse.y, 0, mouse.x, mouse.y, 140);
        radGrad.addColorStop(0, "rgba(192, 132, 252, 0.12)");
        radGrad.addColorStop(0.4, "rgba(16, 185, 129, 0.06)");
        radGrad.addColorStop(0.8, "rgba(239, 68, 68, 0.02)");
        radGrad.addColorStop(1, "rgba(0, 0, 0, 0)");

        ctx.fillStyle = radGrad;
        ctx.beginPath();
        ctx.arc(mouse.x, mouse.y, 140, 0, Math.PI * 2);
        ctx.fill();

        ctx.restore();
    }

    function animate() {
        // Deep obsidian solid clear ensuring crystal-clear text readability
        ctx.fillStyle = "#07070a";
        ctx.fillRect(0, 0, width, height);

        drawAmbientEmbers();
        drawLightTrail();
        drawCursorAura();

        requestAnimationFrame(animate);
    }

    animate();
})();
