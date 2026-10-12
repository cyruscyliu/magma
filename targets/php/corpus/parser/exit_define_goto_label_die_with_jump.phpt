<?php

echo "Before\n";
goto die;
echo "In between\n";
die:
echo "After\n";

?>