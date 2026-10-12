<?php
$ini = <<<INI
[\${zz:-x

INI;
var_dump(parse_ini_string($ini));
?>