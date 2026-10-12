<?php
$tok = strtok("This is\tan example\nstring", " \n\t");
while ($tok !== false) {
    var_dump($tok);
    $tok = strtok(" \n\t");
}
?>