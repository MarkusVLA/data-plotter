#version 120

attribute vec3 position;
varying vec3 vertex_color;

uniform mat4 modelview;
uniform mat4 projection;

vec3 colorGradient(float t) {
    vec3 dark_purple = vec3(0.2, 0.0, 0.4);
    vec3 blue = vec3(0.0, 0.1, 0.6);
    vec3 green = vec3(0.1, 0.8, 0.2);
    vec3 bright_yellow = vec3(1.0, 1.0, 0.5);

    if (t < 0.33) {
        return mix(dark_purple, blue, t / 0.33);
    } else if (t < 0.66) {
        return mix(blue, green, (t - 0.33) / 0.33);
    } else {
        return mix(green, bright_yellow, (t - 0.66) / 0.34);
    }
}

void main() {
    gl_Position = projection * modelview * vec4(position, 1.0);
    float t = (position.y + 3.0) / 6.0;
    vertex_color = colorGradient(t);
}



