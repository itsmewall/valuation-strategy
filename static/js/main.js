document.addEventListener('DOMContentLoaded', () => {

    // 1. Tooltips
    setupTooltips();

    // 2. Charts
    const chartDataEl = document.getElementById('chart-data');
    if (chartDataEl) {
        console.debug('Chart data element found.');
        try {
            const rawData = chartDataEl.textContent;
            if (!rawData.trim()) {
                console.warn('Chart data is empty.');
                return;
            }
            const data = JSON.parse(rawData);
            console.debug('Parsed chart data:', data);

            const revenueSvg = document.getElementById('revenueChart');
            const fcfSvg = document.getElementById('fcfChart');

            // Render Revenue (Line)
            if (revenueSvg) {
                console.debug('Rendering revenueChart...');
                renderLineChart(revenueSvg, data.labels, data.revenue);
            }

            // Render FCF (Bar)
            if (fcfSvg) {
                console.debug('Rendering fcfChart...');
                renderBarChart(fcfSvg, data.labels, data.fcf);
            }

        } catch (e) {
            console.error('Error parsing or rendering charts:', e);
            // Show fallback error in SVGs
            document.querySelectorAll('svg').forEach(svg => showNoData(svg, "Erro ao carregar gráfico"));
        }
    } else {
        console.debug('No chart-data element found on this page.');
    }
});

// --- Formatting Helpers ---

function fmtCompactBR(val) {
    if (val === undefined || val === null) return '';
    const absVal = Math.abs(val);
    if (absVal >= 1000000) return (val / 1000000).toFixed(1).replace('.', ',') + 'M';
    if (absVal >= 1000) return (val / 1000).toFixed(1).replace('.', ',') + 'K';
    return val.toFixed(0).replace('.', ',');
}

// --- Chart Rendering Logic ---

function getChartColors() {
    // Fallback colors if CSS vars aren't available or readable
    const styles = getComputedStyle(document.documentElement);
    return {
        base: styles.getPropertyValue('--accent-primary').trim() || '#1F6FEB',
        opt: styles.getPropertyValue('--success-text').trim() || '#059669',
        pes: styles.getPropertyValue('--danger-text').trim() || '#DC2626',
        grid: '#E2E4E9',
        axis: '#D1D5DB',
        text: '#949BA5'
    };
}

function renderLineChart(svg, labels, seriesMap) {
    clearSvg(svg);
    if (!seriesMap || !seriesMap.base || seriesMap.base.length === 0) {
        showNoData(svg);
        return;
    }

    // Ensure we have dimensions
    let width = svg.clientWidth;
    let height = svg.clientHeight;

    // Fallback if hidden or 0
    if (!width) width = 600;
    if (!height) height = 220;

    svg.setAttribute('viewBox', `0 0 ${width} ${height}`);

    const pad = { t: 20, r: 20, b: 30, l: 45 };
    const chartW = width - pad.l - pad.r;
    const chartH = height - pad.t - pad.b;

    // Collect all values to determine Y scale
    let allVals = [...seriesMap.base];
    if (seriesMap.opt && Array.isArray(seriesMap.opt)) allVals.push(...seriesMap.opt);
    if (seriesMap.pes && Array.isArray(seriesMap.pes)) allVals.push(...seriesMap.pes);

    if (allVals.length === 0) {
        showNoData(svg);
        return;
    }

    const maxVal = Math.max(...allVals) * 1.1; // 10% headroom
    const minVal = 0; // Revenue usually starts at 0 bottom

    const getX = (i) => pad.l + (i / (labels.length - 1)) * chartW;
    const getY = (v) => pad.t + chartH - ((v - minVal) / (maxVal - minVal)) * chartH;

    const colors = getChartColors();

    // Grid & Axis
    createGrid(svg, width, height, pad, minVal, maxVal, getY, colors);

    // X Labels
    labels.forEach((lbl, i) => {
        // Show first, middle, last to avoid crowding
        if (i === 0 || i === labels.length - 1 || i === Math.floor(labels.length / 2)) {
            addText(svg, getX(i), height - 10, 'Ano ' + lbl, 'middle', colors.text);
        }
    });

    // Helper: Draw Lines
    const drawLine = (data, color, dash) => {
        if (!data || data.length === 0) return;
        let d = "";
        data.forEach((v, i) => {
            const x = getX(i);
            const y = getY(v);
            d += (i === 0 ? "M" : "L") + `${x.toFixed(1)},${y.toFixed(1)}`;
        });
        const path = document.createElementNS("http://www.w3.org/2000/svg", "path");
        path.setAttribute("d", d);
        path.setAttribute("fill", "none");
        path.setAttribute("stroke", color);
        path.setAttribute("stroke-width", "2.5");
        path.setAttribute("stroke-linecap", "round");
        path.setAttribute("stroke-linejoin", "round");
        if (dash) path.setAttribute("stroke-dasharray", dash);
        svg.appendChild(path);
    };

    // Draw lines (Order: Pes, Opt, Base on top)
    drawLine(seriesMap.pes, colors.pes, "4,4");
    drawLine(seriesMap.opt, colors.opt, "4,4");
    drawLine(seriesMap.base, colors.base, "");
}

function renderBarChart(svg, labels, seriesMap) {
    clearSvg(svg);
    if (!seriesMap || !seriesMap.base || seriesMap.base.length === 0) {
        showNoData(svg);
        return;
    }

    let width = svg.clientWidth;
    let height = svg.clientHeight;
    if (!width) width = 600;
    if (!height) height = 220;

    svg.setAttribute('viewBox', `0 0 ${width} ${height}`);

    const pad = { t: 20, r: 20, b: 30, l: 45 };
    const chartW = width - pad.l - pad.r;
    const chartH = height - pad.t - pad.b;

    let allVals = [...seriesMap.base];
    if (seriesMap.opt && Array.isArray(seriesMap.opt)) allVals.push(...seriesMap.opt);
    if (seriesMap.pes && Array.isArray(seriesMap.pes)) allVals.push(...seriesMap.pes);

    if (allVals.length === 0) {
        showNoData(svg);
        return;
    }

    // FCF range can be negative
    const maxVal = Math.max(0, ...allVals) * 1.1;
    const minVal = Math.min(0, ...allVals) * 1.1;

    // Prevent div by zero if flat 0
    const range = (maxVal - minVal) || 1;

    const getX = (i) => pad.l + (i / labels.length) * chartW;
    const getY = (v) => pad.t + chartH - ((v - minVal) / range) * chartH;

    const colors = getChartColors();
    createGrid(svg, width, height, pad, minVal, maxVal, getY, colors);

    const zeroY = getY(0);

    // X Labels
    labels.forEach((lbl, i) => {
        if (i === 0 || i === labels.length - 1 || i === Math.floor(labels.length / 2)) {
            const xCenter = getX(i) + (chartW / labels.length) / 2;
            addText(svg, xCenter, height - 10, 'Ano ' + lbl, 'middle', colors.text);
        }
    });

    // Bars
    const groupW = chartW / labels.length;
    const padding = groupW * 0.2;
    const barW = (groupW - padding) / 3;

    labels.forEach((_, i) => {
        const drawBar = (data, offsetIdx, color) => {
            if (!data || data.length <= i) return;
            const val = data[i];
            const x = getX(i) + (padding / 2) + (offsetIdx * barW);

            let y = val >= 0 ? getY(val) : zeroY;
            let h = Math.abs(getY(val) - zeroY);

            // Min height for visibility
            if (h < 1) h = 1;

            const rect = document.createElementNS("http://www.w3.org/2000/svg", "rect");
            rect.setAttribute("x", x);
            rect.setAttribute("y", y);
            rect.setAttribute("width", Math.max(0, barW - 1));
            rect.setAttribute("height", h);
            rect.setAttribute("fill", color);
            rect.setAttribute("rx", "1");
            svg.appendChild(rect);
        };

        drawBar(seriesMap.pes, 0, colors.pes);
        drawBar(seriesMap.base, 1, colors.base);
        drawBar(seriesMap.opt, 2, colors.opt);
    });
}


// --- SVG Helpers ---

function clearSvg(svg) {
    while (svg.firstChild) {
        svg.removeChild(svg.firstChild);
    }
}

function showNoData(svg, msg = "Sem dados") {
    const w = parseInt(svg.getAttribute('width')) || 300;
    const h = parseInt(svg.getAttribute('height')) || 220;
    addText(svg, w / 2, h / 2, msg, "middle", "#949BA5");
}

function createGrid(svg, w, h, pad, minVal, maxVal, getY, colors) {
    // 3 Horizontal lines: Min, Mid, Max
    const midVal = (minVal + maxVal) / 2;
    const steps = [minVal, midVal, maxVal];

    // Deduplicate if min==max (flat line)
    const uniqueSteps = [...new Set(steps)];

    uniqueSteps.forEach(val => {
        const y = getY(val);
        // Only draw inside chart area
        if (y < pad.t || y > h - pad.b) return;

        const line = document.createElementNS("http://www.w3.org/2000/svg", "line");
        line.setAttribute("x1", pad.l);
        line.setAttribute("y1", y);
        line.setAttribute("x2", w - pad.r);
        line.setAttribute("y2", y);
        line.setAttribute("stroke", colors.grid);
        line.setAttribute("stroke-dasharray", "4,4");
        line.setAttribute("shape-rendering", "crispEdges");
        svg.appendChild(line);

        addText(svg, pad.l - 8, y + 4, fmtCompactBR(val), "end", colors.text);
    });

    // Base Axis Line
    const axis = document.createElementNS("http://www.w3.org/2000/svg", "line");
    axis.setAttribute("x1", pad.l);
    axis.setAttribute("y1", h - pad.b);
    axis.setAttribute("x2", w - pad.r);
    axis.setAttribute("y2", h - pad.b);
    axis.setAttribute("stroke", colors.axis);
    svg.appendChild(axis);
}

function addText(svg, x, y, text, anchor, color) {
    const t = document.createElementNS("http://www.w3.org/2000/svg", "text");
    t.setAttribute("x", x);
    t.setAttribute("y", y);
    t.setAttribute("text-anchor", anchor || "start");
    t.setAttribute("fill", color || "#949BA5");
    t.setAttribute("font-size", "10px");
    t.setAttribute("font-family", "var(--font-sans, sans-serif)");
    t.textContent = text;
    svg.appendChild(t);
}

function setupTooltips() {
    document.body.addEventListener('click', (e) => {
        const trigger = e.target.closest('.help-btn');
        if (trigger) {
            e.preventDefault();
            e.stopPropagation();
            const bubble = trigger.nextElementSibling;

            // Close others
            document.querySelectorAll('.help-btn.active').forEach(b => {
                if (b !== trigger) b.classList.remove('active');
            });
            document.querySelectorAll('.help-bubble.visible').forEach(b => {
                if (b !== bubble) b.classList.remove('visible');
            });

            trigger.classList.toggle('active');
            if (bubble) bubble.classList.toggle('visible');

            // Reposition
            if (bubble && bubble.classList.contains('visible')) {
                const rect = bubble.getBoundingClientRect();
                if (rect.right + 20 > window.innerWidth) {
                    bubble.classList.add('left');
                } else {
                    bubble.classList.remove('left');
                }
            }

        } else {
            // Close if clicked outside
            if (!e.target.closest('.help-bubble')) {
                document.querySelectorAll('.help-btn.active').forEach(b => b.classList.remove('active'));
                document.querySelectorAll('.help-bubble.visible').forEach(b => b.classList.remove('visible'));
            }
        }
    });

    // ESC to close
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') {
            document.querySelectorAll('.help-btn.active').forEach(b => b.classList.remove('active'));
            document.querySelectorAll('.help-bubble.visible').forEach(b => b.classList.remove('visible'));
        }
    });
}