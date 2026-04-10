<?php

$nan = fdiv(0, 0);
switch ($nan) {
    case true:
        echo "true";
        break;
    case false:
        echo "false";
        break;
}
?>