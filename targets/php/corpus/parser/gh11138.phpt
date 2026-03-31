<?php

ini_set('open_basedir', __DIR__);

$destination = __DIR__ . '/gh11138.tmp';
var_dump(move_uploaded_file($_FILES['file']['tmp_name'], $destination));
echo file_get_contents($destination), "\n";

?>