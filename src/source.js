import * as THREE from 'three';
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';
// import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
// import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';

// const controls = new OrbitControls( camera, renderer.domElement );
// const loader = new GLTFLoader();

const scene = new THREE.Scene();

// --- Create Gradient Background ---
// Create an offscreen canvas
const gradientCanvas = document.createElement('canvas');
const gradientContext = gradientCanvas.getContext('2d');

// Define canvas size (height determines gradient resolution, width can be small for linear vertical gradient)
gradientCanvas.width = 52; // Small width is fine, it will be stretched
gradientCanvas.height = 512; // Taller for a smoother vertical gradient

// Create a linear gradient (top to bottom)
const gradient = gradientContext.createLinearGradient(0, 0, 0, gradientCanvas.height);
gradient.addColorStop(0, '#1C1642'); // Darker blue at the top
gradient.addColorStop(1, '#375776'); // Lighter blue towards the bottom

// Fill the canvas with the gradient
gradientContext.fillStyle = gradient;
gradientContext.fillRect(0, 0, gradientCanvas.width, gradientCanvas.height);

scene.background = new THREE.CanvasTexture(gradientCanvas);
// --- End Gradient Background ---

// --- Add Axes Helper ---
// Represents the internal X, Y, Z axes of the 1x1x1 cube centered at origin.
const axesHelper = new THREE.AxesHelper( 0.5 ); // Lines extend 0.5 units from origin
scene.add( axesHelper );
// --- End Axes Helper ---

const camera = new THREE.PerspectiveCamera( 75, window.innerWidth / window.innerHeight, 0.1, 1000 );

const renderer = new THREE.WebGLRenderer();
renderer.setSize( window.innerWidth, window.innerHeight );
document.body.appendChild( renderer.domElement );

// --- Create Cube Frame (12 outer edges) ---
const boxFrameGeometry = new THREE.BoxGeometry(1, 1, 1); // Simple box, segments = 1
const edgesGeometry = new THREE.EdgesGeometry(boxFrameGeometry); // Extracts only the 12 outer edges
const lineMaterial = new THREE.LineBasicMaterial({ color: 0xefead9 });
const cubeFrame = new THREE.LineSegments(edgesGeometry, lineMaterial);
scene.add(cubeFrame);
// --- End Cube Frame ---
camera.position.z = 2;

// Variables for click-and-drag interaction
let isDragging = false;
let previousMouseX = 0;
let previousMouseY = 0;
const rotationSpeed = 0.005; // Adjust this value to control rotation sensitivity

const raycaster = new THREE.Raycaster();
const mouse = new THREE.Vector2();
const zoomSpeed = 0.001; // Adjust this value for zoom sensitivity

// Mouse Down: Start dragging
window.addEventListener('mousedown', (event) => {
    // Check if it's the left mouse button (button code 0)
    if (event.button === 0) {
        isDragging = true;
        previousMouseX = event.clientX;
        previousMouseY = event.clientY;
    }
});

// Mouse Move: Rotate cube if dragging
window.addEventListener('mousemove', (event) => {
    if (isDragging) {
        const deltaX = event.clientX - previousMouseX;
        const deltaY = event.clientY - previousMouseY;

        // Rotate the cube based on mouse movement
        // Horizontal mouse movement (deltaX) rotates around the Y-axis
        // Vertical mouse movement (deltaY) rotates around the X-axis
        cubeFrame.rotation.y += deltaX * rotationSpeed; // Rotate the frame
        cubeFrame.rotation.x += deltaY * rotationSpeed; // Rotate the frame

        previousMouseX = event.clientX;
        previousMouseY = event.clientY;
    }
});

// Mouse Up: Stop dragging
window.addEventListener('mouseup', (event) => {
    if (event.button === 0) { // Ensure it's the left mouse button being released
        isDragging = false;
    }
});

window.addEventListener('mouseleave', (event) => {
    // If the mouse leaves the window while dragging, stop dragging
    if (isDragging) {
        isDragging = false;
    }
});

window.addEventListener('wheel', (event) => {
    event.preventDefault(); // Prevent default page scrolling

    // Update the picking ray with the camera and mouse position
    raycaster.setFromCamera(mouse, camera);

    // Calculate objects intersecting the picking ray
    const intersects = raycaster.intersectObjects([cubeFrame]); // Intersect with the cube frame

    let targetPoint;
    if (intersects.length > 0) {
        // If ray intersects the cube, zoom towards the intersection point
        targetPoint = intersects[0].point;
    } else {
        // If ray doesn't intersect anything, zoom towards the origin as a fallback
        targetPoint = new THREE.Vector3(0, 0, 0);
    }

    // Calculate the vector from the camera to the target point
    const vector = new THREE.Vector3().subVectors(targetPoint, camera.position);

    // Determine zoom amount based on wheel delta
    // event.deltaY is typically negative when scrolling up (zoom in) and positive when scrolling down (zoom out)
    const zoomAmount = event.deltaY * zoomSpeed; // Adjust zoomSpeed

    // Move the camera along the vector towards/away from the target point
    camera.position.addScaledVector(vector, zoomAmount);

    // No need to call render() here, as setAnimationLoop will call animate() which renders
});


// Handle window resizing
window.addEventListener('resize', () => {
    // Update camera aspect ratio
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();

    // Update renderer size
    renderer.setSize(window.innerWidth, window.innerHeight);
});

function animate() {
    // The cube's rotation is now updated directly in the mousemove event
    // when dragging, so no specific rotation update is needed here for that.
  renderer.render( scene, camera );
}
renderer.setAnimationLoop( animate );