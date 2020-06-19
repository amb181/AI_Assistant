<?php
// We need to use sessions, so you should always start sessions using the below code.
session_start();
// If the user is not logged in redirect to the login page...
if (!isset($_SESSION['loggedin'])) {
	header('Location: index.html');
	exit;
}
?>

<html>
   <head>
      <title>Sourcing AI Assistant</title>
      <link href="./assets/css/style.css" rel="stylesheet" type="text/css">
	  <link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.7.1/css/all.css">
      <!--Let browser know website is optimized for mobile-->
      <meta name="viewport" content="width=device-width, initial-scale=1.0" />

      <!--Import Google Icon Font-->
      <link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
      <link href="https://fonts.googleapis.com/css?family=Raleway:500&display=swap" rel="stylesheet">

      <!--Import Font Awesome Icon Font-->
      <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css"
         integrity="sha256-eZrrJcwDc/3uDhsdt61sL2oOBY362qM3lon1gyExkL0=" crossorigin="anonymous" />  

      <!--Import materialize.css-->
      <link rel="stylesheet" type="text/css" href="static/css/materialize.min.css">

      <!--Main css-->
      <link rel="stylesheet" type="text/css" href="static/css/style.css">
      <meta name="viewport" content="width=device-width, initial-scale=1">
            
   </head>
   <body class="loggedin">

        <nav class="navtop">
			<div>
				<h1>Sourcing AI Assistant</h1>
				<a href="profile.php"><i class="fas fa-user-circle"></i>Profile</a>
				<a href="logout.php"><i class="fas fa-sign-out-alt"></i>Logout</a>
			</div>
        </nav>
        <!-- Pass the user session to the srcipt.js in order to create multiple sessions -->
        <input type="hidden" id="myPhpValue" value="<?php echo $myPhpValue = $_SESSION['name'] ?>" />
        
		<div class="content">
			<h2>Home Page</h2>
			<p>Welcome back, <?=$_SESSION['name']?>!</p>
		</div>
    
      <div class="container">
         <!-- Modal for rendering the charts, declare this if you want to render charts, 
         else you remove the modal -->
         <div id="modal1" class="modal">
            <canvas id="modal-chart"></canvas>
         </div>

        <!--chatbot widget -->
         <div class="widget">
            <div class="chat_header">

               <!--Add the name of the bot here -->
               <span class="chat_header_title">Sourcing AI Assistant </span>
               <span class="dropdown-trigger" href='#' data-target='dropdown1'>
                  <i class="material-icons">
                  more_vert
                  </i>
               </span>

               <!-- Dropdown menu-->
               <ul id='dropdown1' class='dropdown-content'>
                  <li><a href="#" id="clear">Clear</a></li>
                  <li><a href="#" id="restart">Restart</a></li>
                  <li><a href="#" id="close" >Close</a></li>
               </ul>
            </div>

            <!--Chatbot contents goes here -->
            <div class="chats" id="chats">
               <div class="clearfix"></div>
            </div>
            
            <!--keypad for user to type the message -->
            <div class="keypad">
               <textarea id="userInput" placeholder="Type a message..." class="usrInput"></textarea>
               <div id="sendButton"><i class="fa fa-paper-plane" aria-hidden="true"></i></div>
            </div>
         </div>

         <!--bot profile-->
         <div class="profile_div" id="profile_div">
            <img class="imgProfile" src="static/img/botAvatar.png" />
         </div>
      </div>

      <!--JavaScript at end of body for optimized loading-->
      <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js"></script>
      <script type="text/javascript" src="static/js/materialize.min.js"></script>

      <!--Main Script -->
      <script type="text/javascript" src="static/js/script.js"></script>

      <!--Chart.js Script -->
      <script type="text/javascript" src="static/js/chart.min.js"></script>

   </body>
</html>
