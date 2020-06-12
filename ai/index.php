<?php
session_start();
// If the user is not logged in redirect to the login page...
if (!isset($_SESSION['loggedin'])) {
    header('Location: interface/index.html');
    exit;
}
?>
<html>

</html>
