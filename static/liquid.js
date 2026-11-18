/**
 * Interactive Liquid Canvas Simulation
 * Simulates fluid dynamics with ripples, viscous damping, and cursor interaction.
 * Styled with metallic lavender-green and deep obsidian refraction.
 */

(function () {
    const canvas = document.getElementById("liquid-canvas");
    if (!canvas) return;
    const ctx = canvas.getContext("2d");

    let width = (canvas.width = window.innerWidth);
    let height = (canvas.height = window.innerHeight);

    // Grid resolution for wave simulation
    const CELL_SIZE = 12;
    let cols = Math.ceil(width / CELL_SIZE) + 1;
    let rows = Math.ceil(height / CELL_SIZE) + 1;

    let buffer1 = new Float32Array(cols * rows);
    let buffer2 = new Float32Array(cols * rows);
    let damping = 0.965; // Fluid viscosity damping

    let mouse = { x: width / 2, y: height / 2, px: width / 2, py: height / 2, isDown: false, moving: false };
    let lastMoveTime = Date.now();

    function resize() {
        width = canvas.width = window.innerWidth;
        height = canvas.height = window.innerHeight;
        cols = Math.ceil(width / CELL_SIZE) + 1;
        rows = Math.ceil(height / CELL_SIZE) + 1;
        buffer1 = new Float32Array(cols * rows);
        buffer2 = new Float32Array(cols * rows);
    }
    window.addEventListener("resize", resize);

    function addDisturbance(x, y, radius, force) {
        const cx = Math.floor(x / CELL_SIZE);
        const cy = Math.floor(y / CELL_SIZE);
        const rad = Math.ceil(radius / CELL_SIZE);

        for (let j = -rad; j <= rad; j++) {
            for (let i = -rad; i <= rad; i++) {
                const nx = cx + i;
                const ny = cy + j;
                if (nx > 0 && nx < cols - 1 && ny > 0 && ny < rows - 1) {
                    const distSq = i * i + j * j;
                    if (distSq <= rad * rad) {
                        const falloff = 1 - Math.sqrt(distSq) / rad;
                        buffer1[ny * cols + nx] += force * falloff;
                    }
                }
            }
        }
    }

    // Pointer events
    window.addEventListener("pointermove", (e) => {
        const dx = e.clientX - mouse.px;
        const dy = e.clientY - mouse.py;
        const speed = Math.sqrt(dx * dx + dy * dy);

        mouse.x = e.clientX;
        mouse.y = e.clientY;
        mouse.moving = true;
        lastMoveTime = Date.now();

        // Stronger ripple on faster cursor movement
        const force = Math.min(65, Math.max(15, speed * 1.8));
        const radius = Math.min(45, Math.max(20, speed * 0.8));
        addDisturbance(mouse.x, mouse.y, radius, force);

        mouse.px = mouse.x;
        mouse.py = mouse.y;
    });

    window.addEventListener("pointerdown", (e) => {
        mouse.isDown = true;
        addDisturbance(e.clientX, e.clientY, 50, 90);
    });

    window.addEventListener("pointerup", () => {
        mouse.isDown = false;
    });

    // Ambient floating drops when idle
    let idleCounter = 0;
    function addAmbientRipples() {
        idleCounter++;
        if (idleCounter % 75 === 0) {
            const rx = Math.random() * width;
            const ry = Math.random() * height;
            addDisturbance(rx, ry, 30, 35);
        }
    }

    function stepPhysics() {
        // Wave propagation equation
        for (let y = 1; y < rows - 1; y++) {
            const yCols = y * cols;
            for (let x = 1; x < cols - 1; x++) {
                const idx = yCols + x;
                const wave = (
                    buffer1[idx - 1] +
                    buffer1[idx + 1] +
                    buffer1[idx - cols] +
                    buffer1[idx + cols]
                ) * 0.5 - buffer2[idx];

                buffer2[idx] = wave * damping;
            }
        }

        // Swap buffers
        const temp = buffer1;
        buffer1 = buffer2;
        buffer2 = temp;
    }

    function render() {
        ctx.fillStyle = "#07070a";
        ctx.fillRect(0, 0, width, height);

        // Draw metallic liquid contours
        const imgData = ctx.createImageData(cols, rows);
        const data = imgData.data;

        for (let y = 0; y < rows; y++) {
            const yCols = y * cols;
            for (let x = 0; x < cols; x++) {
                const idx = yCols + x;
                const val = buffer1[idx];

                // Calculate surface normal gradient
                const left = x > 0 ? buffer1[idx - 1] : val;
                const right = x < cols - 1 ? buffer1[idx + 1] : val;
                const up = y > 0 ? buffer1[idx - cols] : val;
                const down = y < rows - 1 ? buffer1[idx + cols] : val;

                const dx = (right - left) * 2.0;
                const dy = (down - up) * 2.0;

                // Specular lighting calculation
                const lightX = 0.55;
                const lightY = -0.7;
                const spec = Math.max(0, (dx * lightX + dy * lightY) / Math.sqrt(dx * dx + dy * dy + 4.0));

                const pIdx = idx * 4;

                // Base obsidian color
                let r = 8;
                let g = 8;
                let b = 12;

                // Lavender component (from depth & curvature)
                const lavender = Math.min(220, Math.max(0, val * 2.8 + spec * 120));
                // Green emerald component (from cross-gradient)
                const green = Math.min(200, Math.max(0, -val * 2.2 + spec * 90 + Math.abs(dx) * 2.0));
                // Red subtle highlight on high disturbance peaks
                const red = Math.min(180, Math.max(0, Math.abs(val) > 40 ? (Math.abs(val) - 40) * 3 : 0));

                r += Math.floor(lavender * 0.65 + red * 0.8);
                g += Math.floor(green * 0.75 + lavender * 0.3);
                b += Math.floor(lavender * 0.95 + 15);

                data[pIdx] = Math.min(255, r);
                data[pIdx + 1] = Math.min(255, g);
                data[pIdx + 2] = Math.min(255, b);
                data[pIdx + 3] = Math.min(255, Math.floor(40 + Math.abs(val) * 3.5 + spec * 140));
            }
        }

        // Draw scaled liquid image with smooth blur
        const offCanvas = document.createElement("canvas");
        offCanvas.width = cols;
        offCanvas.height = rows;
        const offCtx = offCanvas.getContext("2d");
        offCtx.putImageData(imgData, 0, 0);

        ctx.save();
        ctx.imageSmoothingEnabled = true;
        ctx.globalCompositeOperation = "screen";
        ctx.drawImage(offCanvas, 0, 0, width, height);

        // Additional radial glow around cursor
        if (mouse.x > 0 && mouse.y > 0) {
            const radGrad = ctx.createRadialGradient(mouse.x, mouse.y, 0, mouse.x, mouse.y, 240);
            radGrad.addColorStop(0, "rgba(168, 85, 247, 0.15)");
            radGrad.addColorStop(0.5, "rgba(16, 185, 129, 0.08)");
            radGrad.addColorStop(1, "rgba(0, 0, 0, 0)");
            ctx.fillStyle = radGrad;
            ctx.beginPath();
            ctx.arc(mouse.x, mouse.y, 240, 0, Math.PI * 2);
            ctx.fill();
        }

        ctx.restore();
    }

    function animate() {
        stepPhysics();
        addAmbientRipples();
        render();
        requestAnimationFrame(animate);
    }

    animate();
})();