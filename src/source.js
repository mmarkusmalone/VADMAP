import * as THREE from 'three';
// GLTFLoader is not used, so its import can be removed if not planned for future use.
// import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';
// import { OrbitControls } from 'three/addons/controls/OrbitControls.js';

const scene = new THREE.Scene();
const journalProcessedData = {'2025-10-31': {'Woke but a bit mad still. Spanish. Work. English. ': [0.08829526850207566, 0.09972470554687381, 0.11754263009953912], 'Met with Lauren to eat, she was feeling the effects of the night before because she was krunk, being out of pocket, and behind the dj. I tried to calm.': [0.044916417311880195, 0.001966609244635976, 0.02630111922254778], 'She also saw Carlos, which she texted before and definitely affected my tummy. It made me want to be there even more, but I knew that wasn’t best for me.': [-0.3798993299817233, 0.036704206154682534, -0.13718336373353662], 'Got over it. I was in a good mood on the way back. Last class, had a project with Evan. Super chill.': [0.8211339001962333, 0.3588097758188453, 0.5212261225393997], 'Then I had my first date! Was feeling nervous because I was scared it would be meaningless and mid. I also didn’t know what he looked like really and I didn’t love my WhatsApp pic of him. Got ready for a while though, felt good. Hot.': [-0.2697908890812549, 0.4824318621767047, -0.16654190572059252], 'Met him at Jarucha which was cool and authentic. Felt awkward at first but the conversation flowed easily. One beer felt good, a buzz. Really enjoyed my time with him, getting to know him. It was good chats.': [0.8215248369585268, 0.39458354181045924, 0.4936143928497997], 'I think he was not that attractive to me sadly. Also didn’t have any edge which I think I need— didn’t provoke me to say anything out of pocket, new, or interesting. Just a nice, normal dude. Not for me. And I got too drunk and out of pocket by the end. Saying goodbye really cemented the lack of attraction to me.': [-0.7398126126549234, -0.22482511910685196, -0.4677471531756463], 'Went back to dorm, was going out with Marshall and Quimper but Marshall went to Club Malasaña and Quimper wanted to go with the AdPhi guys. I also wanted to go with the AdPhi guys for the rush of seeing Carlos.': [0.18938030026563943, 0.10872913886152859, 0.08144417003620498], 'Napped. Tried getting Marshall and sister invited, went out. Completely forgot about Marshall in the rush of it all which I still feel bad about. All I can do is not do it again and feel this feeling of guilt.': [-0.7095839584796684, 0.07122072652790662, -0.33314891508036726], 'Anyways, met Quimper at Espit Chupitos. Carlos in doorway. Ignore his fucking ass! Say hi to others.': [-0.5326555766973184, 0.49916477426947875, 0.056773191643685716], "Blake says 'male model' to me and then said Campbell showed him Phratmail. I made a joke about them talking shit and he took it really personally.": [0.21071211102983792, 0.21932293281200801, 0.16874364026643676], 'Teddy was telling Quimp & I we were his fav girl friend group, he hates the other group. Quimp and I felt super uncomfortable and out of place. It was funny even in the moment though.': [0.5784129642895987, 0.5447331620123338, 0.4260637756605568], 'People left and we get in a car with Teddy. Lit vibes. In line with the SNu guys, also good chats.': [0.7872140523619191, 0.12671467579762385, 0.44735090286238693], 'Also at Chupitos the tension between Carlos and I was suffocating I think for us both. In line I saw him flirting with a random bitch, take out cigs (degen) and he had a mustache… 3/3.': [-0.03258513506338692, 0.030999351282698664, -0.0012746751807714827], 'Got in, took shots and Red Bull. Carlos was lurky when we were around the table then Quimp and I propelled ourselves into our own choreographed dance world. It was so much motherfucking fun. Time flow. Carlos validation was pulsing. He was staring no joke. On way back from the bathroom, I said ‘awkward’ to him and he laughed and lit up a bit.': [0.8015422254863632, 0.5852628947218786, 0.5362365166720712], 'Went back around 4. Good night. Rubicon.': [0.7081792491294533, 0.1499371207890677, 0.47693372872937184], "Wrote this when going to bed: 'Emotional night so I want to edit. I am confused missing Carlos with us meant to be (which he probably makes every girl think). I feel bad for all the attention I didn’t give him (only said one word) but I’m seriously strong for that shit. I will wake up and be happy. Good night. Quimper funny.'": [-0.19574343715916834, 0.1677788332364189, -0.08807744206200305], 'Ha—my take now is that there is a tension/connection from what is wrapped up in our history between us. It will always be there. Means nothing about us now or our future. He made me miserable!': [-0.4380615357974904, -0.006724198180745462, -0.21614233149848697]}};

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
const lineMaterial = new THREE.LineBasicMaterial({ 
    color: 0xefead9,
    // Note: 'linewidth' on LineBasicMaterial is limited to 1 on most systems.
    // 'resolution' is not a property of LineBasicMaterial.
 });
const cubeFrame = new THREE.LineSegments(edgesGeometry, lineMaterial);
scene.add(cubeFrame);

// --- Group for Data Points ---
const dataPointsGroup = new THREE.Group();
cubeFrame.add(dataPointsGroup); // Add data points as children of the cube frame

// --- End Cube Frame ---

// --- Tooltip Element ---
const tooltip = document.createElement('div');
tooltip.style.position = 'absolute';
tooltip.style.visibility = 'hidden'; // Start hidden
tooltip.style.padding = '8px';
tooltip.style.background = 'rgba(0, 0, 0, 0.75)';
tooltip.style.color = 'white';
tooltip.style.borderRadius = '4px';
tooltip.style.pointerEvents = 'none'; // So it doesn't interfere with mouse events on the canvas
document.body.appendChild(tooltip);

camera.position.z = 2;

// Variables for click-and-drag interaction
let isDragging = false;
let previousMouseX = 0;
let previousMouseY = 0;
const rotationSpeed = 0.005; // Adjust this value to control rotation sensitivity

const raycaster = new THREE.Raycaster();
const mouse = new THREE.Vector2();
const zoomSpeed = 0.001; // Adjust this value for zoom sensitivity

// --- Function to Display Journal Data Points ---
function displayJournalDataPoints(data) {
    // Clear existing points if any (e.g., if data is updated)
    while(dataPointsGroup.children.length > 0){
        dataPointsGroup.remove(dataPointsGroup.children[0]);
    }

    const pointGeometry = new THREE.SphereGeometry(0.02, 16, 16); // Small sphere for each point

    for (const date in data) {
        const dayEntries = data[date];
        for (const text in dayEntries) {
            const vad = dayEntries[text]; // [Valence, Arousal, Dominance]
            if (vad && vad.length === 3) {
                const pointMaterial = new THREE.MeshBasicMaterial({ color: Math.random() * 0xffffff }); // Random color for now
                const pointMesh = new THREE.Mesh(pointGeometry, pointMaterial);

                // Map VAD to X, Y, Z, scaling to fit within the -0.5 to 0.5 range of the 1x1x1 cube
                pointMesh.position.set(
                    vad[0] * 0.5, // Valence to X
                    vad[1] * 0.5, // Arousal to Y
                    vad[2] * 0.5  // Dominance to Z
                );
                pointMesh.userData = { text: text, isDataPoint: true }; // Store text and a flag
                dataPointsGroup.add(pointMesh);
            }
        }
    }
}

function createAxisLabel(text, position) {
    const canvas = document.createElement('canvas');
    canvas.width = 256;
    canvas.height = 64;
    const ctx = canvas.getContext('2d');
    ctx.font = '32px Arial';
    ctx.fillStyle = '#efead9';
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    ctx.fillText(text, canvas.width / 2, canvas.height / 2);

    const texture = new THREE.CanvasTexture(canvas);
    const material = new THREE.SpriteMaterial({ map: texture, transparent: true });
    const sprite = new THREE.Sprite(material);
    sprite.scale.set(0.4, 0.1, 1); // Adjust size as needed
    sprite.position.copy(position);
    return sprite;
}

// Add axis labels
const xLabel = createAxisLabel('Valence', new THREE.Vector3(0.55, 0, 0));
const yLabel = createAxisLabel('Arousal', new THREE.Vector3(0, 0.55, 0));
const zLabel = createAxisLabel('Dominance', new THREE.Vector3(0, 0, 0.55));

cubeFrame.add(xLabel);
cubeFrame.add(yLabel);
cubeFrame.add(zLabel);


const dirLight = new THREE.DirectionalLight( 0xffffff, 0.4 );
dirLight.position.set( 0, 0, 1 ).normalize();
scene.add( dirLight );

const pointLight = new THREE.PointLight( 0xffffff, 4.5, 0, 0 );
pointLight.color.setHSL( Math.random(), 1, 0.5 );
pointLight.position.set( 0, 100, 90 );
scene.add( pointLight );

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
    // Update mouse coordinates for raycasting (normalized -1 to +1)
    mouse.x = (event.clientX / window.innerWidth) * 2 - 1;
    mouse.y = - (event.clientY / window.innerHeight) * 2 + 1;

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

    // Hover detection for data points
    raycaster.setFromCamera(mouse, camera);
    const intersects = raycaster.intersectObjects(dataPointsGroup.children);

    if (intersects.length > 0 && intersects[0].object.userData.isDataPoint) {
        const intersectedObject = intersects[0].object;
        tooltip.innerHTML = intersectedObject.userData.text;
        tooltip.style.visibility = 'visible';

        // Convert 3D position to 2D screen position for tooltip
        const vector = new THREE.Vector3();
        intersectedObject.getWorldPosition(vector); // Get world position of the data point
        vector.project(camera); // Project to normalized device coordinates

        const x = (vector.x * 0.5 + 0.5) * window.innerWidth;
        const y = (vector.y * -0.5 + 0.5) * window.innerHeight;

        tooltip.style.left = `${x + 10}px`; // Offset slightly from cursor
        tooltip.style.top = `${y + 10}px`;

    } else {
        tooltip.style.visibility = 'hidden';
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

// Initial display of data points
displayJournalDataPoints(journalProcessedData);

renderer.setAnimationLoop( animate );