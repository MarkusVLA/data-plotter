#version 120

attribute vec3 position;
varying vec3 vertex_color;

uniform mat4 modelview;
uniform mat4 projection;

void main() {
    gl_Position = projection * modelview * vec4(position, 1.0);
    vertex_color = vec3((position.y + 1.0) / 2.0, (position.y + 3.0) / 6.0, (position.y + 3.0) / 6.0);
    //vertex_color = vec3((position.y + 1.0) / 2.0 * 0.1, (position.z + 3.0) / 6.0, (position.y + 3.0) / 6.0);
}