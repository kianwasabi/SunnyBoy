<h2>SunnyBoy </h2>
<p>This project consists of two repositories:</br>
Project "SunnyBoy" a Web Server Application AND Project "MoonY" a ioT Client Application </p>
<p>The idea behind the "SunnyBoy" project is, that the Sunnyboy-Server manages and stores (weather-)information and administers the control of several "MoonY" clients. First, a "MoonY" requests its to-do list from the server. It works through all the received process steps in its to-do list and sends back data to the server whenever a process step is required. The from the Moony collected data are stored in the server's database. All stored to-do lists are editable through a web interface to maximize the system's flexibility. Furthermore, the server and client communication is established by Rest API endpoints. </p>
<h2>Table of Contents</h2>
<ul>
  <li><a href="#getting-started">Getting Started</a></li>
  <li><a href="#how-it-is-done">Frontend</a></li>
  <li><a href="#how-it-is-done">Backend</a></li>
  <li><a href="#version">Version</a></li>
  <li><a href="#built-with">Built With</a></li>
  <li><a href="#license">License</a></li>
</ul>
<h2>Getting Started</h2>
<p>The "Sunnyboy" Server Application runs on every server instance as long as python3 is installed. Therefore, it can be used on a hosted server or a raspberry pi running in your local network. </p>
<a href="url"><img src="https://user-images.githubusercontent.com/55065075/216689412-49002b2a-782c-494d-abff-c253f597cb40.png" height="auto" width="500" ></a>
<h2>Frontend</h2>
<p>The frontend consists of four routes.<br>
<h3>/home</h3>
<p>Here, the last in the servers database stored weatherinformations are displayed. The user can edit the requested location by editing the entry in the textfield. By pushing the Update-button, the weatherinformation are updated. </p>
<a href="url"><img src="https://user-images.githubusercontent.com/55065075/234973144-7887be5f-5e5a-40b3-bfe8-94379d13c3f3.png" height="auto" width="500" ></a>
<h3>/client process control</h3>
<h3>/api & /about</h3>
<h2>Backend</h2>
<h3>System Architecture</h3>
<p>The server side consits of the three segments as shown in the picture below. </p>
<a href="url"><img src="https://user-images.githubusercontent.com/55065075/216689615-d3a9c125-5d25-4986-9b0b-50e710d2f788.png" height="auto" width="500" ></a>
<h4>app</h4>
<p>insert routes/API endpoints here</p>
<h4>buisnessfunctions</h4>
<p>...</p>
<h4>database</h4>
<p>insert Database ER-Modell here</p>
<h2>Version</h2>
<p>...</p>
<h2>Built-with</h2>
<p>...</p>
<h2>license</h2>
<p>...</p>
