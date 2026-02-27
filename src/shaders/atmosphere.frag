precision mediump float;

uniform float uTime;
uniform vec2 uResolution;
uniform float uFever;


void main() {
    vec2 uv = gl_FragCoord.xy / uResolution.xy;

    // Deep Space Gradient
    vec3 baseColor = vec3(0.05, 0.02, 0.1);
    vec3 midColor = vec3(0.1, 0.05, 0.2) + (uFever * vec3(0.3, 0.1, 0.4));
    vec3 topColor = vec3(0.02, 0.01, 0.05);

    vec3 color = mix(baseColor, midColor, uv.y);
    color = mix(color, topColor, pow(uv.y, 2.0));

    // Pulse effect
    float pulse = sin(uTime * 2.0 + uv.y * 10.0) * 0.02 * (1.0 + uFever);
    color += pulse;

    // Vignette
    float vignette = distance(uv, vec2(0.5));
    color *= 1.0 - vignette * 0.8;

    gl_FragColor = vec4(color, 1.0);
}
