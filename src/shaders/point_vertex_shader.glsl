#version 120
    attribute vec3 position;
    varying vec3 vertex_color;
    uniform mat4 modelview;
    uniform mat4 projection;
    void main() {
        gl_Position = projection * modelview * vec4(position, 1.0);
        vertex_color = vec3((position.x + 3) / 6.0 * 0.4, (position.y + 3) / 6.0, (position.z + 3) / 6.0 * 0.4); // Normalize z coordinate to [0, 1] range for color
    }